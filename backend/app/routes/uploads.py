import os
from flask import Blueprint, current_app, request, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "mov", "avi", "csv"}
ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/gif",
    "video/mp4",
    "video/quicktime",
    "video/x-msvideo",
    "text/csv",
}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


uploads_bp = Blueprint("uploads", __name__, url_prefix="/uploads")


@uploads_bp.post("")
def upload_file():
    if "file" not in request.files:
        return {"error": "No file provided"}, 400
    file: FileStorage = request.files["file"]
    if file.filename == "":
        return {"error": "Empty filename"}, 400
    if not allowed_file(file.filename):
        return {"error": "Unsupported file type"}, 400
    # MIME type validation (best-effort based on client-provided mimetype)
    if file.mimetype not in ALLOWED_MIME_TYPES:
        return {"error": "Invalid MIME type"}, 400
    # Enforce size limit using configured MAX_CONTENT_LENGTH
    max_len = int(current_app.config.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))
    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)
    if size > max_len:
        return {"error": "File too large"}, 413

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    filename = secure_filename(file.filename)
    file.save(os.path.join(upload_folder, filename))
    return {"filename": filename, "url": f"/uploads/{filename}"}, 201


@uploads_bp.get("/<path:filename>")
def serve_file(filename: str):
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, filename, as_attachment=False)
