import logging

# ============================================================================
# Ollama Configuration
# ============================================================================

# Ollama server settings
OLLAMA_HOST = "francesco-desktop.local"
OLLAMA_PORT = 11434
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"

# Ollama request timeout (seconds)
OLLAMA_TIMEOUT = 30

# LLM generation parameters
OLLAMA_MODEL_TEMPERATURE = 0.3
OLLAMA_MODEL_CONTEXT_LENGTH = 4096

# ============================================================================
# Logging Configuration
# ============================================================================

# Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = logging.DEBUG

# Log file path
LOG_FILE = "proofreader.log"

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


# ============================================================================
# Proofreading Prompt
# ============================================================================

PROOFREADING_PROMPT = """Proofread the following [TEXT] and point out any errors.

TEXT: "{text}"

Format your response EXACTLY as follows:

FEEDBACK:
[If there are grammar/spelling errors, style improvements, or enhancements, list them as: "• original → suggestion (reason)"]
[If no feedback, write "None required"]

Rules:
- Errors first, suggestions later.
- Keep concise. Maximum 5-6 items total.
"""

# ============================================================================
# UI Messages
# ============================================================================

# Status messages
MSG_PROCESSING_MESSAGES = [
    "Consulting the stars...",
    "Summoning the grammar spirits...",
    "Awakening the ancient spellchecker...",
    "Communing with the syntax sages...",
    "Channeling linguistic wisdom...",
    "Decoding the prophecy...",
    "Seeking enlightenment...",
    "Meditating on your prose...",
    "Conjuring corrections...",
    "Invoking the muse...",
    "Pondering perfection...",
    "Analyzing the runes...",
    "Consulting the oracle...",
    "Brewing verbal excellence...",
    "Polishing your words...",
    "Divining the details...",
    "Transcribing wisdom...",
    "Harmonizing your sentences...",
    "Reading the tea leaves...",
    "Calibrating the quill...",
    "Aligning the paragraphs...",
    "Summoning clarity...",
    "Weaving word magic...",
    "Distilling perfection...",
    "Unlocking secrets...",
    "Peering into the prose...",
    "Casting judgment...",
    "Refining the essence...",
    "Balancing the clauses...",
    "Illuminating errors...",
    "Crystallizing thoughts...",
    "Probing the depths...",
    "Untangling complexity...",
    "Sculpting sentences...",
    "Sharpening expressions...",
]

MSG_NO_TEXT_SELECTED = "No text selected. Please select some text first."
