import magic

from tkinter import Tk, filedialog, messagebox, Label
from tkinter import ttk


class App:
    def __init__(self):
        self.root = None
        self.window_width = 480
        self.window_height = 240

        self.infile = None
        self.outfile = None

    def __setup(self):
        # Create main window
        self.root = Tk()
        self.root.title("Result Analysis")

        # Set window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (self.window_width / 2))
        y_coordinate = int((screen_height / 2) - (self.window_height / 2))
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")

        # Create label
        self.upload_label = Label(self.root, text="Upload a PDF file:", font=("Serif Sans", 14))
        self.upload_label.pack(pady=10)

        # Create upload button
        self.upload_button = ttk.Button(
            self.root,
            text="Upload PDF",
            command=self.__upload_handler,
        )
        self.upload_button.pack()

        # Create analyse button (initially disabled)
        self.analyse_button = ttk.Button(
            self.root, text="Analyse PDF",
            command=lambda: messagebox.showinfo("Analysis Complete", "PDF analysis complete"),
            state="disabled"
        )
        self.analyse_button.pack()

    def __upload_handler(self):
        self.infile = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

        if self.infile and magic.from_file(self.infile, mime=True) == 'application/pdf':
            self.analyse_button["state"] = "Normal"

    def run(self):
        self.__setup()
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
