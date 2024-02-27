import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        # Enable analyse button
        analyse_button.config(state="normal")


def analyse_pdf():
    # Perform analysis on the PDF (in this example, simply print a message)
    print("PDF analysis complete.")
    result = messagebox.askquestion("Analysis Complete", "PDF analysis complete. Do you want to save changes?")
    if result == "yes":
        save_changes()
    else:
        discard_changes()


def save_changes():
    # Your saving logic here
    # Assuming the spreadsheet is generated here
    messagebox.showinfo("Success", "Changes saved successfully. Spreadsheet generated successfully.")


def discard_changes():
    # Your discard logic here
    messagebox.showinfo("Discarded", "Changes discarded successfully. Spreadsheet generated successfully.")


# Create main window
root = tk.Tk()
root.title("PDF Analysis")

# Set window size and position
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width/2) - (window_width/2))
y_coordinate = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Create label
label = tk.Label(root, text="Upload a PDF file:", font=("Arial", 14))
label.pack(pady=10)

# Create upload button
upload_button = ttk.Button(root, text="Upload PDF", command=upload_pdf)
upload_button.pack()

# Create analyse button (initially disabled)
analyse_button = ttk.Button(root, text="Analyse PDF", command=analyse_pdf, state="disabled")
analyse_button.pack()

root.mainloop()