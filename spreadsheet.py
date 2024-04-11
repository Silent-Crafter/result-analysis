from openpyxl import Workbook
from parser import parse
import csv


class Spreadsheet:
    def __init__(self, file_name):
        super().__init__(file_name)


if __name__ == '__main__':
    workbook = Workbook()

    data = parse('gadget.pdf')
    print(data["RESULT"][-1])
    counter = 0
    for student in data["STUDENT_INFO"].keys():
        workbook.create_sheet(student)
        worksheet = workbook[student]
        student_data = data["STUDENT_INFO"][student]
        marks_data = data["RESULT"]

        worksheet.cell(1, 1, "Seat No:")
        worksheet.cell(1, 2, student)

        worksheet.cell(2, 1, "Student Name:")
        worksheet.cell(2, 2, student_data["NAME"])

        worksheet.cell(2, 4, "Mother Name:")
        worksheet.cell(2, 5, student_data["MOTHER"])

        worksheet.cell(4, 1, "Sem")
        worksheet.cell(4, 2, "SubCode")
        worksheet.cell(4, 3, "Subject Name")
        worksheet.cell(4, 4, "Crd")
        worksheet.cell(4, 5, "Grd")
        worksheet.cell(4, 6, "GP")

        cell_index_row = 5
        cell_index_col = 2
        while True:
            try:
                if marks_data[counter]["SEAT NO"] != student:
                    break

                curr_sem = marks_data[counter]["SEM"]
            except (KeyError, IndexError):
                break
            worksheet.cell(cell_index_row, 1, curr_sem)

            try:
                while marks_data[counter]["SEM"] == curr_sem:
                    cell_index_col = 2
                    worksheet.cell(cell_index_row, cell_index_col, marks_data[counter]["SUBJECT"])
                    worksheet.cell(cell_index_row, cell_index_col+1, data["SUBJECTS"][marks_data[counter]["SUBJECT"]])
                    worksheet.cell(cell_index_row, cell_index_col+2, marks_data[counter]["CR"])
                    worksheet.cell(cell_index_row, cell_index_col+3, marks_data[counter]["GRADE"])
                    worksheet.cell(cell_index_row, cell_index_col+4, marks_data[counter]["GP"])
                    cell_index_row += 1
                    counter += 1
                    print(marks_data[counter])
            except IndexError:
                break

    workbook.save('demo.xlsx')
    workbook.close()
