import io


def test_upload_image_happy_path(client):
	png_bytes = b"\x89PNG\r\n\x1a\n" + b"0" * 128
	data = {
		"file": (io.BytesIO(png_bytes), "test.png")
	}
	res = client.post("/uploads", data=data, content_type="multipart/form-data")
	assert res.status_code == 201
	json = res.get_json()
	assert json["filename"] == "test.png"


def test_upload_invalid_mime(client):
	fake_bytes = b"notanimage"
	data = {
		"file": (io.BytesIO(fake_bytes), "test.exe")
	}
	res = client.post("/uploads", data=data, content_type="multipart/form-data")
	assert res.status_code in (400, 413)
