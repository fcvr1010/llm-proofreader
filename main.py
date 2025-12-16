#!/usr/bin/env python3

import logging
import sys
import threading

from src import config
from src.modern_gui import ModernProofreaderApp
from src.proofreader import ProofreaderApp

# Configure logging from config
logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
    handlers=[logging.FileHandler(config.LOG_FILE), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the application."""
    logger.info("LLM Proofreader starting")

    proofreader_app = ProofreaderApp()
    gui_app = ModernProofreaderApp(proofreader_app)

    # Start keyboard listener in background thread
    def run_keyboard_listener():
        try:
            proofreader_app.run()
        except Exception as e:
            logger.error(f"Error in keyboard listener: {e}")

    threading.Thread(target=run_keyboard_listener, daemon=True).start()

    # Run GUI main loop
    try:
        return gui_app.run()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
