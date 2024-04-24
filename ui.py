import magic

import analyzer
import parser

from tkinter import filedialog, messagebox
import customtkinter as ctk
from spreadsheet import Spreadsheet
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import os


class App(ctk.CTk):
    class Child(ctk.CTkToplevel):
        def __init__(self, parent, **kwargs):
            super().__init__()

            self.parent: App = parent

            self.title(kwargs.get('title', "Analysis Viewer"))
            self.width = kwargs.get('width', 1280)
            self.height = kwargs.get('height', 720)

            self.button_frame = None
            self.output_frame = None
            self.top10_button = None
            self.subject_topper_button = None
            self.pass_fail = None

            self.curr_frame = None

        def create_output_frame(self) -> ctk.CTkFrame:
            output_frame = ctk.CTkFrame(self)
            output_frame.grid(row=0, column=2, columnspan=6, rowspan=6, sticky="nsew")
            return output_frame

        def setup_ui(self):
            x_coordinate = (self.parent.screen_width // 2) - (self.width // 2)
            y_coordinate = (self.parent.screen_height // 2) - (self.height // 2)
            self.geometry(f"{self.width}x{self.height}+{x_coordinate}+{y_coordinate}")

            self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
            self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

            self.button_frame = ctk.CTkFrame(self)
            self.button_frame.grid(row=0, column=0, columnspan=2, rowspan=6, sticky="nsew")
            self.button_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
            self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)

            self.output_frame = self.create_output_frame()

            self.top10_button = ctk.CTkButton(
                self.button_frame,
                text="Top 10 students",
                command=self.parent.top10_handler,
                font=("sans-serif", 36)
            )
            self.top10_button.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

            self.subject_topper_button = ctk.CTkButton(
                self.button_frame,
                text="Subject topper",
                command=self.parent.subject_topper_handler,
                font=("sans-serif", 36)
            )
            self.subject_topper_button.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

            self.pass_fail = ctk.CTkButton(
                self.button_frame,
                text="Pass fail",
                command=self.parent.pass_fail_handler,
                font=("sans-serif", 36)
            )
            self.pass_fail.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

    def __init__(self):
        super().__init__()
        self.window_width = 800
        self.window_height = 600

        self.infile = None
        self.outfile = None
        ctk.set_appearance_mode("dark")

    def __setup(self):
        # Create main window
        self.title("Result Analysis")

        # Set window size and position
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        x_coordinate = (self.screen_width // 2) - (self.window_width // 2)
        y_coordinate = (self.screen_height // 2) - (self.window_height // 2)
        self.geometry(f"{self.window_width}x{self.window_height}+{x_coordinate}+{y_coordinate}")

        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.heading = ctk.CTkLabel(self, text="Result Gazette Analyzer", font=("Sans Serif", 64, "underline"))
        self.heading.grid(row=0, columnspan=3)

        # Create label
        self.label_text = ctk.StringVar(self, value="Upload a pdf file:")
        self.upload_label = ctk.CTkLabel(self, textvariable=self.label_text, font=("Sans Serif", 48))
        self.upload_label.grid(row=1, column=1)

        # Create upload button
        self.upload_button = ctk.CTkButton(
            self,
            text="Upload PDF",
            command=self.upload_button_handler,
            font=("Sans Serif", 32)
        )
        self.upload_button.grid(ipadx=20, ipady=20, pady=10, row=3, column=1, sticky=ctk.S)

        # Create analyse button (initially disabled)
        self.analyze_button = ctk.CTkButton(
            self, text="Analyse PDF",
            command=self.analyze_button_handler,
            state="disabled",
            text_color_disabled="#1a1a1a",
            font=("Sans Serif", 32)
        )
        self.analyze_button.grid(ipadx=20, ipady=20, pady=10, row=4, column=1, sticky=ctk.N)

        self.filevariable = ctk.StringVar(value="")
        self.filelable = ctk.CTkLabel(
            self,
            textvariable=self.filevariable,
            font=("Sans Serif", 28),
            fg_color="transparent"
        )
        self.filelable.grid(row=2, columnspan=3)

    def upload_button_handler(self):
        self.infile = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

        if self.infile and magic.from_file(self.infile, mime=True) == 'application/pdf':
            self.analyze_button.configure(state="normal")
            filename = os.path.basename(self.infile)
            self.filevariable.set("Selected File: " + filename)
            self.filelable.configure(text_color="red")
            self.label_text.set("Click on Analyze button to start analysis!!")
            self.upload_label.configure(text_color="green")
            self.upload_label.configure(font=("Sans Serif", 36))

    def analyze_button_handler(self):
        self.data = parser.parse(self.infile)
        self.results = analyzer.analyze(self.data)
        print(self.results)
        self.label_text.set("Analysis Complete!!")
        sheet = Spreadsheet('result.xlsx', self.data)
        sheet.create()

        messagebox.showinfo("ANALYSIS STATUS!",
                            "Analysis Completed successfully. Spreadsheet has been generated with name result.xlsx")

        self.child = self.Child(self)
        self.child.setup_ui()
        self.child.mainloop()

    def top10_handler(self):
        if self.child.output_frame:
            self.child.output_frame.destroy()

        top10_frame: ctk.CTkFrame = self.child.create_output_frame()
        self.child.output_frame = top10_frame

        top10_frame.grid_rowconfigure(tuple(range(20)), weight=1)
        top10_frame.grid_columnconfigure(tuple(range(3)), weight=1)

        top10 = self.results["TOP 10"]

        curr_row = 5
        ctk.CTkLabel(
            top10_frame,
            text=f"SEAT NO",
            font=("sans-serif", 24)
        ).grid(row=curr_row - 1, column=0, padx=5, pady=5)
        ctk.CTkLabel(
            top10_frame,
            text=f"STUDENT NAME",
            font=("sans-serif", 24)
        ).grid(row=curr_row - 1, column=1, padx=5, pady=5)
        ctk.CTkLabel(
            top10_frame,
            text=f"GPA",
            font=("sans-serif", 24)
        ).grid(row=curr_row - 1, column=2, padx=5, pady=5)
        curr_row += 1
        for student, gpa in top10.items():
            ctk.CTkLabel(
                top10_frame,
                text=f"{student}",
                font=("sans-serif", 24)
            ).grid(row=curr_row, column=0, padx=5, pady=5)
            ctk.CTkLabel(
                top10_frame,
                text=f"{self.data['STUDENT_INFO'][student]['NAME']}",
                font=("sans-serif", 24)
            ).grid(row=curr_row, column=1, padx=5, pady=5)
            ctk.CTkLabel(
                top10_frame,
                text=f"{gpa}",
                font=("sans-serif", 24)
            ).grid(row=curr_row, column=2, padx=5, pady=5)
            curr_row += 1

    def subject_topper_handler(self):
        if self.child.output_frame:
            self.child.output_frame.destroy()

        self.child.output_frame = self.child.create_output_frame()
        self.child.output_frame.grid_rowconfigure(tuple(range(15)), weight=1)
        self.child.output_frame.grid_columnconfigure(tuple(range(3)), weight=1)

        sub_tops = self.results["SUBJECT TOPPERS"]
        toppers = []

        def display_data():
            topper_frame = ctk.CTkFrame(self.child.output_frame)
            topper_frame.grid_rowconfigure(tuple(range(12)), weight=1)
            topper_frame.grid_columnconfigure(tuple(range(3)), weight=1)
            topper_frame.grid(row=3, column=0, columnspan=3, rowspan=10, sticky=ctk.NSEW)
            self.child.update()

            curr_row = 1
            ctk.CTkLabel(
                topper_frame,
                text=f"SEAT NO",
                font=("sans-serif", 24)
            ).grid(row=curr_row - 1, column=0, padx=5, pady=5)
            ctk.CTkLabel(
                topper_frame,
                text=f"STUDENT NAME",
                font=("sans-serif", 24)
            ).grid(row=curr_row - 1, column=1, padx=5, pady=5)
            ctk.CTkLabel(
                topper_frame,
                text=f"TOT",
                font=("sans-serif", 24)
            ).grid(row=curr_row - 1, column=2, padx=5, pady=5)
            curr_row += 1
            for seat_no, tot in toppers:
                ctk.CTkLabel(
                    topper_frame,
                    text=f"{seat_no}",
                    font=("sans-serif", 24)
                ).grid(row=curr_row, column=0, padx=5, pady=5)
                ctk.CTkLabel(
                    topper_frame,
                    text=f'{self.data["STUDENT_INFO"][seat_no]["NAME"]}',
                    font=("sans-serif", 24)
                ).grid(row=curr_row, column=1, padx=5, pady=5)
                ctk.CTkLabel(
                    topper_frame,
                    text=f"{tot}",
                    font=("sans-serif", 24)
                ).grid(row=curr_row, column=2, padx=5, pady=5)
                curr_row += 1

        def combobox_callback(option: str):
            nonlocal toppers
            for key, value in self.data['SUBJECTS'].items():
                if value == option:
                    toppers = sub_tops[key]
                    break
            display_data()
            self.child.update()

        subjects = list(self.data['SUBJECTS'].values())

        dropdown = ctk.CTkComboBox(
            self.child.output_frame,
            values=subjects,
            font=("sans-serif", 24),
            command=combobox_callback
        )
        dropdown.grid(row=2, column=1, padx=5, pady=5)

    def pass_fail_handler(self):
        if self.child.output_frame:
            self.child.output_frame.destroy()

        self.child.output_frame = self.child.create_output_frame()
        self.child.output_frame.grid_rowconfigure(tuple(range(10)), weight=1)
        self.child.output_frame.grid_columnconfigure(tuple(range(3)), weight=1)

        ctk.CTkLabel(
            self.child.output_frame,
            text="Pass & Fail chart",
            font=("sans-serif", 24, "underline"),
        ).grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(
            self.child.output_frame,
            text=f"PASSED: {self.results['PASS FAIL']['PASS']}    FAILED: {self.results['PASS FAIL']['FAIL']}",
            font=("sans-serif", 24)
        ).grid(row=2, column=1, padx=5, pady=5)

        graphframe = ctk.CTkFrame(self.child.output_frame)
        graphframe.grid(row=3, column=0, rowspan=7, columnspan=3, sticky="nsew")
        graphframe.grid_rowconfigure(tuple(range(7)), weight=1)
        graphframe.grid_columnconfigure(tuple(range(7)), weight=1)

        fig = Figure()
        fig.add_subplot().pie(self.results["PASS FAIL"].values(), labels=self.results["PASS FAIL"].keys(), autopct="%.2f%%")

        canvas = FigureCanvasTkAgg(fig, master=graphframe)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1, padx=5, pady=5, rowspan=5, columnspan=5)

        graphframe.update()
        self.child.output_frame.update()
        self.child.update()

    def run(self):
        self.__setup()
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
