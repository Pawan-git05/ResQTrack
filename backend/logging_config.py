import logging
import os
from logging.handlers import RotatingFileHandler


def configure_logging(app):
	level_name = os.getenv("LOG_LEVEL", "INFO").upper()
	level = getattr(logging, level_name, logging.INFO)

	# Clear existing handlers to avoid duplicate logs in reloads/tests
	for handler in list(app.logger.handlers):
		app.logger.removeHandler(handler)

	app.logger.setLevel(level)

	formatter = logging.Formatter(
		"%(asctime)s %(levelname)s [%(name)s] %(message)s",
	)

	# Console handler
	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(level)
	stream_handler.setFormatter(formatter)
	app.logger.addHandler(stream_handler)

	# Optional file handler
	log_dir = os.getenv("LOG_DIR", "logs")
	try:
		os.makedirs(log_dir, exist_ok=True)
		file_handler = RotatingFileHandler(os.path.join(log_dir, "app.log"), maxBytes=1_000_000, backupCount=3)
		file_handler.setLevel(level)
		file_handler.setFormatter(formatter)
		app.logger.addHandler(file_handler)
	except Exception:
		# If filesystem not writable (e.g., some containers), ignore file handler
		pass

	app.logger.info("Logging configured (level=%s)", level_name)
