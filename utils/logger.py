import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "aetherstem", log_level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a structured logger that outputs to both console and a file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevent adding handlers if they already exist (e.g., during re-imports)
    if logger.handlers:
        return logger

    # Formatter for structured logs
    # Format: [Timestamp] [Level] [Module] Message
    log_format = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # File Handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "aetherstem.log"
    
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger

# Default logger instance
logger = setup_logger()
