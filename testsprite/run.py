import sys
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List
import requests
import yaml


@dataclass
class StepResult:
	name: str
	success: bool
	message: str


def load_suite(path: str) -> Dict[str, Any]:
	with open(path, 'r', encoding='utf-8') as f:
		return yaml.safe_load(f)


def build_url(base_url: str, path: str) -> str:
	if path.startswith('http://') or path.startswith('https://'):
		return path
	return f"{base_url}{path}"


def perform_request(base_url: str, req: Dict[str, Any]) -> requests.Response:
	method = req.get('method', 'GET').upper()
	path = req.get('path', '/')
	url = build_url(base_url, path)
	headers = req.get('headers') or {}
	json_body = req.get('json')
	data = req.get('data')
	files = None
	return requests.request(method, url, headers=headers, json=json_body, data=data, files=files, timeout=10, allow_redirects=True)


def validate_response(resp: requests.Response, expect: Dict[str, Any]) -> str | None:
	if 'status_in' in expect:
		allowed = set(expect['status_in'] or [])
		if resp.status_code not in allowed:
			return f"Expected status in {sorted(allowed)} got {resp.status_code}"
	elif 'status' in expect and resp.status_code != expect['status']:
		return f"Expected status {expect['status']} got {resp.status_code}"
	if 'json_contains' in expect or 'json_has_keys' in expect:
		try:
			payload = resp.json()
		except Exception:
			return "Response is not valid JSON"
		if 'json_contains' in expect:
			for k, v in (expect['json_contains'] or {}).items():
				if payload.get(k) != v:
					return f"JSON key {k} expected {v} got {payload.get(k)}"
		if 'json_has_keys' in expect:
			for k in (expect['json_has_keys'] or []):
				if k not in payload:
					return f"JSON missing key: {k}"
	return None


def run_steps(base_url: str, steps: List[Dict[str, Any]]) -> List[StepResult]:
	results: List[StepResult] = []
	for step in steps:
		name = step.get('name', 'unnamed')
		try:
			resp = perform_request(base_url, step.get('request') or {})
			err = validate_response(resp, step.get('expect') or {})
			if err:
				results.append(StepResult(name, False, err))
			else:
				results.append(StepResult(name, True, f"ok ({resp.status_code})"))
		except Exception as e:
			results.append(StepResult(name, False, str(e)))
		time.sleep(0.05)
	return results


def main() -> int:
	path = sys.argv[1] if len(sys.argv) > 1 else 'testsprite/tests.yml'
	suite = load_suite(path)
	base_url = suite.get('base_url', 'http://localhost:5000')
	steps = suite.get('steps', [])
	results = run_steps(base_url, steps)
	failed = [r for r in results if not r.success]
	for r in results:
		status = 'PASS' if r.success else 'FAIL'
		print(f"[{status}] {r.name}: {r.message}")
	return 1 if failed else 0


if __name__ == '__main__':
	sys.exit(main())
