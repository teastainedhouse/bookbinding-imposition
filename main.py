import tkinter as tk
from gui import ImpositionGUI
from imposition import create_pdf


def main():
    def run_imposition(input_path, output_path, signature_size):
        create_pdf(input_path, output_path, signature_size)

    root = tk.Tk()
    ImpositionGUI(root, run_imposition)
    root.mainloop()


if __name__ == "__main__":
    main()
