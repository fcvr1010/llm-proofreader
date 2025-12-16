"""
Modern customtkinter-based GUI for LLM Proofreader.
Features a results window triggered by F9 key press.
"""

import contextlib
import logging

import customtkinter as ctk

from src.utils import get_random_processing_message

logger = logging.getLogger(__name__)

# Set appearance mode and default color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class ModernResultsWindow(ctk.CTkToplevel):
    """
    Window for displaying proofreading results.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.withdraw()  # Hide initially

    def setup_ui(self):
        """Set up the results window UI."""
        self.title("")
        self.attributes("-topmost", True)

        # Intercept window close button to hide instead of destroy
        self.protocol("WM_DELETE_WINDOW", self.hide_window)

        # Calculate window size - up to 1/3 of screen height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        max_height = int(screen_height / 3)
        window_height = min(max_height, 700)  # Cap at 700px for very large screens

        self.geometry(f"550x{window_height}")

        # Position in top-right corner
        self.geometry(f"+{screen_width - 570}+20")

        # Create header
        self.header_frame = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="#667eea")
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        # Title in header
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="✨ Here are the LLM suggestions",
            font=("Segoe UI", 18, "bold"),
            text_color="white",
        )
        self.title_label.pack(side="left", padx=20, pady=15)

        # Close button in header
        self.close_btn = ctk.CTkButton(
            self.header_frame,
            text="✕",
            width=32,
            height=32,
            corner_radius=16,
            fg_color="#8899ff",
            hover_color="#aabbff",
            font=("Segoe UI", 18, "bold"),
            command=self.hide_window,
        )
        self.close_btn.pack(side="right", padx=20, pady=15)

        # Content area
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.content_frame.pack(fill="both", expand=True)

        # Scrollable text display with larger font
        self.text_display = ctk.CTkTextbox(
            self.content_frame,
            font=("Segoe UI", 12),
            fg_color="white",
            text_color="#2c3e50",
            wrap="word",
            activate_scrollbars=True,
        )
        self.text_display.pack(fill="both", expand=True, padx=20, pady=20)

        # Force font configuration on the underlying Text widget
        with contextlib.suppress(AttributeError):
            self.text_display._textbox.configure(font=("Segoe UI", 12))

        # Bind ESC key to close window
        self.bind("<Escape>", lambda _: self.hide_window())

    def hide_window(self):
        """Hide the results window."""
        self.withdraw()

    def show_processing(self, token_count=None):
        """Show processing message."""
        # Check if window still exists
        if not self.winfo_exists():
            logger.warning("Results window was destroyed, skipping show_processing")
            return

        self.title_label.configure(text="✨ Processing...")

        # Enable editing first
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", "end")

        # Center-aligned processing message
        message = get_random_processing_message()
        self.text_display.insert("1.0", "\n\n")
        self.text_display.insert("end", message, "processing")

        if token_count is not None:
            self.text_display.insert("end", f"\n\n~{token_count} tokens", "token_info")

        # Configure tags (font not supported in CTkTextbox tag_config)
        self.text_display.tag_config("processing", foreground="#667eea", justify="center")
        self.text_display.tag_config("token_info", foreground="#95a5a6", justify="center")

        self.text_display.configure(state="disabled")
        self.deiconify()
        self.lift()
        self.focus_force()  # Ensure window has focus for ESC key binding

    def show_result(self, result_text):
        """Display proofreading results."""
        # Check if window still exists
        if not self.winfo_exists():
            logger.warning("Results window was destroyed, skipping show_result")
            return

        self.title_label.configure(text="✨ Proofreading Results")
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", "end")

        # Parse result to extract fixes and suggestions. Printing
        # the LLM output directly is a bit ugly.
        lines = result_text.split("\n")
        fixes = []
        suggestions = []
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line == "FIXES:":
                current_section = "fixes"
            elif line == "SUGGESTIONS:":
                current_section = "suggestions"
            elif line.startswith("•"):
                if current_section == "fixes":
                    fixes.append(line)
                elif current_section == "suggestions":
                    suggestions.append(line)

        # Display fixes
        if fixes:
            self.text_display.insert("end", "Fixes Required:\n", "header_error")
            for fix in fixes:
                self.text_display.insert("end", f"{fix}\n\n", "bullet")
        else:
            self.text_display.insert("end", "✓ No fixes required\n\n", "status_good")

        # Display suggestions
        if suggestions:
            self.text_display.insert("end", "Suggestions:\n", "header_suggestion")
            for suggestion in suggestions:
                self.text_display.insert("end", f"{suggestion}\n\n", "bullet")
        else:
            self.text_display.insert("end", "✓ No suggestions\n\n", "status_good")

        # Configure text tags
        self.text_display.tag_config("status_good", foreground="#27ae60")
        self.text_display.tag_config("header_error", foreground="#e74c3c")
        self.text_display.tag_config("header_suggestion", foreground="#f39c12")
        self.text_display.tag_config("bullet", foreground="#2c3e50")

        self.text_display.configure(state="disabled")
        self.deiconify()
        self.lift()
        self.focus_force()  # Ensure window has focus for ESC key binding

    def show_error(self, error_message):
        """Display an error message."""
        # Check if window still exists
        if not self.winfo_exists():
            logger.warning("Results window was destroyed, skipping show_error")
            return

        self.title_label.configure(text="❌ Error")
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", "end")

        self.text_display.insert("1.0", "Error:\n\n", "error_header")
        self.text_display.insert("end", error_message, "error_text")

        # Configure tags (font not supported in CTkTextbox tag_config)
        self.text_display.tag_config("error_header", foreground="#e74c3c")
        self.text_display.tag_config("error_text", foreground="#721c24")

        self.text_display.configure(state="disabled")
        self.deiconify()
        self.lift()
        self.focus_force()  # Ensure window has focus for ESC key binding


class ModernProofreaderApp:
    """
    Main application class that manages the customtkinter GUI.
    """

    def __init__(self, proofreader_app):
        """
        Initialize the modern GUI app.

        Args:
            proofreader_app: ProofreaderApp instance
        """
        self.proofreader_app = proofreader_app

        # Create main window (hidden)
        self.root = ctk.CTk()
        self.root.withdraw()
        self.root.title("LLM Proofreader")

        # Create results window
        self.results_window = ModernResultsWindow(self.root)

        # Set up callbacks
        self.setup_callbacks()

        logger.info("GUI initialized")

    def setup_callbacks(self):
        """Set up the callback interface for proofreader."""
        self.proofreader_app.gui_callbacks = self

    def show_processing(self, token_count=None):
        """Show processing window."""
        self.root.after(0, lambda: self.results_window.show_processing(token_count))

    def show_result(self, result_text):
        """Show results window."""
        self.root.after(0, lambda: self.results_window.show_result(result_text))

    def show_error(self, error_message):
        """Show error window."""
        self.root.after(0, lambda: self.results_window.show_error(error_message))

    def run(self):
        """Run the application."""
        logger.info("Application ready - press F9 to proofread")

        # Start the event loop
        self.root.mainloop()
