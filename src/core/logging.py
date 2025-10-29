import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    """
    Configure consistent logging across the entire app, including Uvicorn.

    Args:
        level: Logging level (default: "INFO")
    """
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    formatter = logging.Formatter(log_format)

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    while root.handlers:
        root.handlers.pop()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    for name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        for h in logger.handlers:
            h.setFormatter(formatter)
