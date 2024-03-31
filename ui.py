import magic
import parser

from tkinter import Tk, filedialog, messagebox
from tkinter.ttk import Label, Button
from spreadsheet import Spreadsheet


class App(Tk):
    def __init__(self):
        super().__init__()
        self.window_width = 480
        self.window_height = 240

        self.infile = None
        self.outfile = None

    def __setup(self):
        # Create main window
        self.title("Result Analysis")

        # Set window size and position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (self.window_width // 2)
        y_coordinate = (screen_height // 2) - (self.window_height // 2)
        self.geometry(f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")

        # Create label
        self.upload_label = Label(self, text="Upload a PDF file:", font=("Sans Serif", 14))
        self.upload_label.pack(pady=10)

        # Create upload button
        self.upload_button = Button(
            self,
            text="Upload PDF",
            command=self.__upload_button_handler,
        )
        self.upload_button.pack()

        # Create analyse button (initially disabled)
        self.analyze_button = Button(
            self, text="Analyse PDF",
            command=self.__analyze_button_handler,
            state="disabled"
        )
        self.analyze_button.pack()

    def __upload_button_handler(self):
        self.infile = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

        if self.infile and magic.from_file(self.infile, mime=True) == 'application/pdf':
            self.analyze_button["state"] = "Normal"

    def __analyze_button_handler(self):
        data = parser.parse(self.infile)
        sheet = Spreadsheet(f"{self.infile}.xlsx")
        worksheet = sheet.add_worksheet()
        worksheet.write("B2", "Name")
        worksheet.write("C2", data["Name"])
        sheet.close()

        messagebox.showinfo("Analysis Complete", "PDF analysis complete")

    def run(self):
        self.__setup()
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
