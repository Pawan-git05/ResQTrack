import requests
import json

BASE_URL = "http://localhost:5000/api"

# --- Test Data ---
NGO_DATA = {
    "name": "Test NGO",
    "email": "test@ngo.com",
    "phone": "1234567890",
    "password": "testpassword"
}

CASE_DATA = {
    "description": "This is a test case.",
    "location": "Test Location"
}


def run_verification():
    """Runs a series of tests to verify the MySQL migration."""
    print("--- Starting MySQL Migration Verification ---")

    # 1. Register a new NGO
    try:
        response = requests.post(f"{BASE_URL}/register/ngo", json=NGO_DATA)
        response.raise_for_status()
        print("✅ NGO Registration: PASSED")
    except requests.exceptions.RequestException as e:
        print(f"❌ NGO Registration: FAILED - {e}")
        return

    # 2. Log in as the new NGO
    try:
        login_data = {"email": NGO_DATA["email"], "password": NGO_DATA["password"], "role": "NGO"}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        response.raise_for_status()
        token = response.json().get("access_token")
        if not token:
            print("❌ NGO Login: FAILED - No access token returned")
            return
        print("✅ NGO Login: PASSED")
    except requests.exceptions.RequestException as e:
        print(f"❌ NGO Login: FAILED - {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create a new case
    try:
        response = requests.post(f"{BASE_URL}/cases", json=CASE_DATA, headers=headers)
        response.raise_for_status()
        print("✅ Case Creation: PASSED")
    except requests.exceptions.RequestException as e:
        print(f"❌ Case Creation: FAILED - {e}")
        return

    # 4. Fetch cases
    try:
        response = requests.get(f"{BASE_URL}/cases", headers=headers)
        response.raise_for_status()
        cases = response.json()
        if not cases:
            print("❌ Case Fetching: FAILED - No cases returned")
            return
        print("✅ Case Fetching: PASSED")
    except requests.exceptions.RequestException as e:
        print(f"❌ Case Fetching: FAILED - {e}")
        return

    print("\n--- MySQL Migration Verification Complete ---")

if __name__ == "__main__":
    run_verification()
