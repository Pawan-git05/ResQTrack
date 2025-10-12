import os
from flask import Blueprint, current_app, request, send_from_directory
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "mov", "avi"}


def allowed_file(filename: str) -> bool:
	return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


uploads_bp = Blueprint("uploads", __name__, url_prefix="/uploads")


@uploads_bp.post("")
def upload_file():
	if "file" not in request.files:
		return {"error": "No file provided"}, 400
	file = request.files["file"]
	if file.filename == "":
		return {"error": "Empty filename"}, 400
	if not allowed_file(file.filename):
		return {"error": "Unsupported file type"}, 400

	upload_folder = current_app.config["UPLOAD_FOLDER"]
	os.makedirs(upload_folder, exist_ok=True)
	filename = secure_filename(file.filename)
	file.save(os.path.join(upload_folder, filename))
	return {"filename": filename, "url": f"/uploads/{filename}"}, 201


@uploads_bp.get("/<path:filename>")
def serve_file(filename: str):
	upload_folder = current_app.config["UPLOAD_FOLDER"]
	return send_from_directory(upload_folder, filename, as_attachment=False)
