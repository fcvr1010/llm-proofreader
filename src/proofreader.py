"""
LLM Proofreader - Background service that monitors F9 key press
and sends selected text to Ollama for proofreading.
"""

import logging
import subprocess
from threading import Thread

import requests
from evdev import InputDevice, categorize, ecodes, list_devices

from src import config
from src.utils import estimate_tokens

logger = logging.getLogger(__name__)


class ProofreaderApp:
    """Main application class for the LLM proofreader."""

    def __init__(self):
        """Initialize the proofreader application."""
        self.processing = False
        self.gui_callbacks = None
        logger.info(f"Ollama server: {config.OLLAMA_URL}, Model: {config.OLLAMA_MODEL}")

    def get_selected_text(self):
        """Get currently selected text using wl-paste (Wayland primary selection)."""
        try:
            result = subprocess.run(
                ["wl-paste", "--primary"], capture_output=True, text=True, timeout=1
            )

            if result.returncode == 0 and result.stdout.strip():
                logger.info(f"Captured text: '{result.stdout[:50]}...'")
                return result.stdout.strip()

            logger.warning("No text selected")
            return None

        except subprocess.TimeoutExpired:
            logger.error("wl-paste timed out")
            return None
        except FileNotFoundError:
            logger.error("wl-paste not found. Install wl-clipboard package")
            return None
        except Exception as e:
            logger.error(f"Error getting selected text: {e}")
            return None

    def proofread_text(self, text):
        """Send text to Ollama for proofreading."""
        logger.info(f"Proofreading: '{text[:50]}...'")

        payload = {
            "model": config.OLLAMA_MODEL,
            "prompt": config.PROOFREADING_PROMPT.format(text=text),
            "stream": False,
            "options": {
                "temperature": config.OLLAMA_MODEL_TEMPERATURE,
                "num_ctx": config.OLLAMA_MODEL_CONTEXT_LENGTH,
            },
        }

        try:
            response = requests.post(config.OLLAMA_URL, json=payload, timeout=config.OLLAMA_TIMEOUT)

            if response.status_code == 200:
                result = response.json()
                if "response" in result:
                    logger.info(f"Proofreading completed ({len(result['response'])} chars)")
                    return result["response"].strip()
                else:
                    logger.error(f"Unexpected response format: {result}")
                    return "Error: Unexpected response format from Ollama"
            else:
                logger.error(f"Ollama returned status {response.status_code}")
                return f"Error: Ollama API returned status code {response.status_code}"

        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {config.OLLAMA_TIMEOUT}s")
            return "Error: Request timed out"
        except requests.exceptions.ConnectionError:
            logger.error(f"Cannot connect to Ollama at {config.OLLAMA_HOST}")
            return f"Error: Cannot connect to Ollama at {config.OLLAMA_HOST}"
        except Exception as e:
            logger.error(f"Error during proofreading: {e}")
            return f"Error: {str(e)}"

    def show_result_callback(self, result):
        """Callback to show results."""
        if self.gui_callbacks:
            self.gui_callbacks.show_result(result)
        else:
            logger.info(f"Result: {result}")

    def show_processing_callback(self, token_count=None):
        """Callback to show processing state."""
        if self.gui_callbacks:
            self.gui_callbacks.show_processing(token_count)
        else:
            msg = f"Processing (~{token_count} tokens)..." if token_count else "Processing..."
            logger.info(msg)

    def show_error_callback(self, message):
        """Callback to show error messages."""
        if self.gui_callbacks:
            self.gui_callbacks.show_error(message)
        else:
            logger.error(f"Error: {message}")

    def process_proofreading(self):
        """Process the proofreading workflow in a separate thread."""
        try:
            self.processing = True

            # Get selected text
            selected_text = self.get_selected_text()
            if not selected_text:
                self.show_error_callback(config.MSG_NO_TEXT_SELECTED)
                return

            # Estimate and validate token count
            token_count = estimate_tokens(selected_text)
            if token_count > config.OLLAMA_MODEL_CONTEXT_LENGTH:
                error_msg = (
                    f"Text too long: ~{token_count} tokens exceeds "
                    f"context window of {config.OLLAMA_MODEL_CONTEXT_LENGTH} tokens"
                )
                logger.warning(error_msg)
                self.show_error_callback(error_msg)
                return

            # Show processing and proofread
            self.show_processing_callback(token_count)
            result = self.proofread_text(selected_text)

            # Check if result is an error message
            if result.startswith("Error:"):
                self.show_error_callback(result)
            else:
                self.show_result_callback(result)

        except Exception as e:
            logger.error(f"Error in proofreading workflow: {e}")
            self.show_error_callback(f"An error occurred: {str(e)}")
        finally:
            self.processing = False

    def on_f9_press(self):
        """Handle F9 key press event."""
        if self.processing:
            logger.warning("Already processing, ignoring F9 press")
            return

        logger.info("F9 pressed - starting proofreading")
        thread = Thread(target=self.process_proofreading, daemon=True)
        thread.start()

    def find_keyboard_device(self):
        """Find a keyboard input device with F9 key support."""
        devices = [InputDevice(path) for path in list_devices()]

        for device in devices:
            capabilities = device.capabilities(verbose=False)
            if ecodes.EV_KEY in capabilities:
                if ecodes.KEY_F9 in capabilities[ecodes.EV_KEY]:
                    logger.info(f"Using keyboard: {device.name}")
                    return device

        logger.error("No keyboard device with F9 key found")
        return None

    def listen_for_f9(self, device):
        """Listen for F9 key presses on the given device."""
        logger.info("Listening for F9 key events")
        try:
            for event in device.read_loop():
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if key_event.keycode == "KEY_F9" and key_event.keystate == 1:
                        self.on_f9_press()
        except Exception as e:
            logger.error(f"Error in key listener: {e}")

    def run(self):
        """Run the proofreader application."""
        logger.info("Starting LLM Proofreader - Press F9 to proofread selected text")

        # Test Ollama connection
        try:
            test_url = f"http://{config.OLLAMA_HOST}:{config.OLLAMA_PORT}/api/tags"
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                models = [m["name"] for m in response.json().get("models", [])]
                logger.info(f"✓ Connected to Ollama. Available models: {models}")
            else:
                logger.warning(f"Ollama responded with status {response.status_code}")
        except Exception as e:
            logger.error(f"✗ Failed to connect to Ollama: {e}")
            logger.error("Proofreading may not work")

        # Find keyboard device
        keyboard_device = self.find_keyboard_device()
        if not keyboard_device:
            logger.error("No keyboard device found. Add yourself to 'input' group:")
            logger.error("  sudo usermod -a -G input $USER")
            logger.error("Then log out and back in")
            return

        # Start keyboard listener
        logger.info("Keyboard listener active")
        try:
            self.listen_for_f9(keyboard_device)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        except Exception as e:
            logger.error(f"Error in keyboard listener: {e}")
        finally:
            keyboard_device.close()
            logger.info("Stopped")
