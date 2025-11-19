import os
import io
from flask import Blueprint, current_app, request, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

# Allowed extensions and MIME types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4", "mov", "avi", "csv"}
ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/gif",
    "video/mp4",
    "video/quicktime",
    "video/x-msvideo",
    "text/csv",
    "application/vnd.ms-excel",
    "application/octet-stream"  # browsers sometimes send this for CSVs
}

def allowed_file(filename: str) -> bool:
    """Check if file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Use /api/uploads so it matches your frontend routes
uploads_bp = Blueprint("uploads", __name__, url_prefix="/api/uploads")


@uploads_bp.post("")
def upload_file():
    """Handle file uploads from frontend."""
    if "file" not in request.files:
        return {"error": "No file provided"}, 400

    file: FileStorage = request.files["file"]

    if not file or file.filename == "":
        return {"error": "Empty filename"}, 400

    if not allowed_file(file.filename):
        return {"error": "Unsupported file type"}, 400

    # Fallback MIME validation (some browsers misreport CSV types)
    if file.mimetype not in ALLOWED_MIME_TYPES:
        return {"error": f"Invalid MIME type: {file.mimetype}"}, 400

    # ✅ SAFEST WAY: read once, save once, and manually check size
    upload_folder = current_app.config.get("UPLOAD_FOLDER", os.path.join(os.getcwd(), "uploads"))
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)

    # Save file directly instead of seeking or reading multiple times
    try:
        file.save(file_path)
    except Exception as e:
        return {"error": f"Failed to save file: {str(e)}"}, 500

    # Check size AFTER saving
    try:
        size = os.path.getsize(file_path)
    except OSError:
        size = 0

    # Enforce max content length if set
    max_len = int(current_app.config.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))
    if size > max_len:
        os.remove(file_path)
        return {"error": "File too large"}, 413

    return {
        "filename": filename,
        "size": size,
        "url": f"/api/uploads/{filename}",
        "message": "File uploaded successfully!"
    }, 201


@uploads_bp.get("/<path:filename>")
def serve_file(filename: str):
    """Serve uploaded files from disk."""
    upload_folder = current_app.config.get("UPLOAD_FOLDER", os.path.join(os.getcwd(), "uploads"))
    return send_from_directory(upload_folder, filename, as_attachment=False)
