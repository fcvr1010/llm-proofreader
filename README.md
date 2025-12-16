# LLM Proofreader

Simple Python application to proofread content using a local Large Language Model (LLM) via [ollama](https://ollama.com/).

All your content stays local... Privacy!

Currently tested on Ubuntu 24.04 and, in general, expected to work only on Linux systems. It could be
extended to other systems by replacing the keyboard event listeners.

> **DISCLAIMER**: this is intended as a Proof-of-Concept and as such it's not professional-grade software.
If you want to build on it, it's recommended to add unit tests and a CI pipeline.

## Tech Stack

- [ollama](https://ollama.com/) to run the LLM.
- [tiktoken](https://github.com/openai/tiktoken) to estimate the text size in LLM tokens.
- [requests](https://pypi.org/project/requests/) to interact with ollama using REST APIs.
- [evdev](https://python-evdev.readthedocs.io/en/latest/) to capture keyboard events.
- [customtkinter](https://customtkinter.tomschimansky.com/) for the GUI.
- [wl-clipboard](https://github.com/bugaevc/wl-clipboard): Wayland clipboard utilities for reading text selection.

## Installation

### 1. Install System Dependencies

```bash
# Install wl-clipboard (Wayland clipboard utilities)
sudo apt-get install wl-clipboard

# Add your user to the input group (required for keyboard monitoring with evdev)
sudo usermod -a -G input $USER

# IMPORTANT: Log out and log back in for group changes to take effect
```

### 2. Set Up Python Environment with Poetry

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install Python dependencies
poetry install

# Alternatively, to run without activating the virtual environment
poetry run python main.py
```

### 3. Setting Up Development Environment

```bash
# Install dependencies including dev dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install
```

### 3. Configuration

Edit [src/config.py](src/config.py) to set at least:

- `OLLAMA_HOST`: Where ollama is running
- `OLLAMA_PORT`: Which port ollama uses
- `OLLAMA_MODEL`: Which model should be used

More configuration options, such as LLM temperature, prompt, and context length
can be set as well.

## Usage

### Running the Application

```bash
poetry run python main.py
```

### How it works

Select any text on the screen and then press F9. The text will be
captured and sent to your local LLM. Proofreading results will be
displayed in a pop-up window that you can close by clicking ESC.

## Troubleshooting

### No Text Captured

- **Issue**: Notification says "No text selected"
- **Solution**: Make sure text is selected before pressing F9
- **Check logs**: Look for "No text was selected or clipboard is empty"

### Cannot Connect to Ollama

- **Issue**: Error notification about connection failure
- **Solution**:
  - Verify Ollama is running: `curl http://<ollama host>:<ollama port>/api/tags`
  - Check hostname is correct in configuration
  - Check firewall settings
- **Check logs**: Look for "Failed to connect to Ollama server"

### F9 Not Working

- **Issue**: F9 key doesn't trigger proofreading
- **Solution**:
  - Check if another app is capturing F9
  - Verify application is running (check console)
- **Check logs**: Should see "F9 key detected by listener" when pressed

### Keyboard Input Permissions

- **Issue**: Cannot detect F9 key presses
- **Solution**:
  - Add your user to input group: `sudo usermod -a -G input $USER`
  - Log out and log back in
  - Verify keyboard device access

## Running as a Background Service

To run the application automatically on startup, create a systemd service.

**Important**: adapt the values in the following snippet to reflect your local setup.

### 1. Create Service File

Create `/etc/systemd/system/llm-proofreader.service`:

```ini
[Unit]
Description=LLM Proofreader Service
After=network.target

[Service]
Type=simple
User=francesco
WorkingDirectory=/home/francesco/workspace/llm-proofreader
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/francesco/.Xauthority"
ExecStart=/home/francesco/.local/bin/poetry -C /home/francesco/workspace/llm-proofreader run python main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

### 2. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable llm-proofreader.service
sudo systemctl start llm-proofreader.service

# Check status
sudo systemctl status llm-proofreader.service

# View logs
journalctl -u llm-proofreader.service -f
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to modify and adapt this application to your needs! Contributions are welcome too.
