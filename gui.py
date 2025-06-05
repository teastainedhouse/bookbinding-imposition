import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, Toplevel, messagebox
from PIL import Image, ImageTk, ImageSequence
import threading


class ImpositionGUI:
    def __init__(self, root, on_run_callback):
        self.root = root
        self.root.title("Bookbinding Imposition")
        self.root.minsize(500, 300)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.signature_size = tk.IntVar(value=16)

        self.on_run_callback = on_run_callback
        self.setup_widgets()

    def setup_widgets(self):
        # create widgets
        input_lbl = ttk.Label(self.root, text="PDF to convert: ")
        input_entry = ttk.Entry(self.root, textvariable=self.input_path, width=50)
        input_btn = ttk.Button(self.root, text="Select", command=self.pick_input)
        output_lbl = ttk.Label(self.root, text="Output location: ")
        output_entry = ttk.Entry(self.root, textvariable=self.output_path, width=50)
        output_btn = ttk.Button(self.root, text="Select", command=self.pick_output)
        sig_lbl = ttk.LabelFrame(self.root, text="Signature size:", padding=(10,5))
        for idx, size in enumerate([8, 12, 16, 32]):
            tk.Radiobutton(
                sig_lbl,
                text=f"{size} pages",
                variable=self.signature_size,
                value=size
            ).grid(row=0, column=idx, padx=10, pady=5)
        run_btn = ttk.Button(self.root, text="Run", width=25, command=self.run)

        # grid widgets
        input_lbl.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        input_entry.grid(row=0, column=1, padx=5, pady=5)
        input_btn.grid(row=0, column=2, padx=5, pady=5)
        sig_lbl.grid(row=1, column=0, columnspan=3, padx=(5, 5), pady=(10, 10))
        output_lbl.grid(row=7, column=0, padx=5, pady=(20, 20))
        output_entry.grid(row=7, column=1)
        output_btn.grid(row=7, column=2, padx=(5, 15))
        run_btn.grid(row=8, column=1)

    def pick_input(self):
        path = filedialog.askopenfilename(
            title="Choose the file you want to convert",
            initialdir=os.getcwd(),
            filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.input_path.set(path)

    def pick_output(self):
        path = filedialog.asksaveasfilename(
            title="Choose where to save output",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="imposed_output.pdf"
        )
        if path:
            self.output_path.set(path)

    def run(self):
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        sig_size = self.signature_size.get()

        if input_path and output_path:
            # Start the processing in a thread
            threading.Thread(
                target=self.run_with_spinner,
                args=(input_path, output_path, sig_size),
                daemon=True
            ).start()
        else:
            messagebox.showerror(
                title="Missing File Path",
                message="Please select both a PDF to be converted and a location where you want the output to be saved."
            )

    def run_with_spinner(self, input_path, output_path, sig_size):
        # Show loading popup
        self.show_spinner()

        # Run the actual processing (this runs in a separate thread)
        try:
            self.on_run_callback(input_path, output_path, sig_size)
        finally:
            # Ensure spinner closes even if there's an error
            self.spinner.destroy()
            ImpositionGUI.play_done_sound()
            ImpositionGUI.open_output_folder(output_path)

    @staticmethod
    def play_done_sound():
        system = platform.system()
        if system == "Windows":
            import winsound
            winsound.MessageBeep(winsound.MB_OK)
        elif system == "Darwin":  # macOS
            subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])
        elif system == "Linux":
            subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"])
        else:
            print("No sound support for this OS.")

    @staticmethod
    def open_output_folder(path):
        folder = os.path.dirname(path)
        system = platform.system()
        if system == "Windows":
            os.startfile(folder)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", folder])
        elif system == "Linux":
            subprocess.run(["xdg-open", folder])
        else:
            print("Don't know how to open folders on this OS.")

    def show_spinner(self):
        self.spinner = Toplevel(self.root)
        self.spinner.title("Processing...")
        self.spinner.geometry("200x200")
        self.spinner.resizable(False, False)
        self.spinner.attributes("-topmost", True)

        # Load the animated GIF
        gif = Image.open(resource_path("hourglass.gif"))
        self.frames: list = [ImageTk.PhotoImage(f.copy().convert("RGBA")) for f in ImageSequence.Iterator(gif)]
        self.spinner_label = tk.Label(self.spinner)
        self.spinner_label.pack(expand=True)

        def update_frame(frame_idx=0):
            if hasattr(self, "spinner_label"):
                self.spinner_label.config(image=self.frames[frame_idx])
                next_idx = (frame_idx + 1) % len(self.frames)
                self.spinner_label.after(100, update_frame, next_idx)

        update_frame()
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
