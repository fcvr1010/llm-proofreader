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

PROOFREADING_PROMPT = """You are a professional proofreader. Review the following text and provide feedback.

Text to review:
"{text}"

Format your response EXACTLY as follows:

FIXES:
[If there are grammar/spelling errors that MUST be fixed, list them as: "• original → correction (reason)"]
[If no errors, write "None required"]

SUGGESTIONS:
[If there are style improvements or optional enhancements, list them as: "• original → suggestion (reason)"]
[If no suggestions, write "None"]

Rules:
- FIXES are for actual errors (grammar, spelling, punctuation)
- SUGGESTIONS are for style improvements (clarity, conciseness, better word choice)
- Keep concise. Maximum 3-4 items per section."""

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
