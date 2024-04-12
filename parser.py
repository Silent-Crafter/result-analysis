from poppler import load_from_file
import re


def parse(pdffile):
    patterns = {
        "seat_no": r"Seat No:.*?(\w+)",
        "prn": r"PRN:\s*([\d\w]*)",
        "name": r"Name:\s+?([\w]+?)\s+",
        "mother_name": r"Mother’s Name:[\s]*?([\w]+?)\s+[\w]",
        "cgpa": r"cgpa\s*([\d\-\.]*)",
        "sgpa": r"sgpa\s*([\d\-\.]*)",
        "college": r"College:\s*([\w\d\s]*)",
        "marks": r"^(\d{6})" + r"\s*(\w*)" + r"\s*[\d\-/]*" * 7 + r"\s*(\d*)" + r"\s*(\d*)" + r"\s*(\w*)" + r"\s*(\d*)" + r"[\d\s]*"
    }

    data = {"SUBJECTS": {}, "STUDENT_INFO": {}, "RESULT": []}

    pdf = load_from_file(pdffile)
    marks_data = []
    for count in range(pdf.pages):
        page = pdf.create_page(count)
        txt = page.text()

        seat_no = re.findall(patterns["seat_no"], txt)[0].strip()
        name = re.findall(patterns["name"], txt)[0].strip()
        mother_name = re.findall(patterns["mother_name"], txt)[0].strip()
        prn = re.findall(patterns["prn"], txt)[0].strip()

        data["STUDENT_INFO"][seat_no] = {"NAME": name, "MOTHER": mother_name, "PRN": prn}

        cgpa = re.findall(patterns["cgpa"], txt)
        sgpa = re.findall(patterns["sgpa"], txt)

        if not cgpa:
            pass
        elif cgpa[0] == '-':
            data["STUDENT_INFO"][seat_no]["CGPA"] = -1
        else:
            data["STUDENT_INFO"][seat_no]["CGPA"] = float(cgpa[0])

        if not sgpa:
            pass
        elif sgpa[0] == '-':
            data["STUDENT_INFO"][seat_no]["SGPA"] = -1
        else:
            data["STUDENT_INFO"][seat_no]["SGPA"] = float(sgpa[0])


        sem = 1
        college = None
        for line in txt.splitlines():
            if not college:
                college = re.findall(patterns["college"], line.strip())
                if college:
                    data["STUDENT_INFO"][seat_no]["COLLEGE"] = college[0]
            _sem = re.findall(r"sem(\d)", line.strip())
            if _sem:
                sem = int(_sem[0])

            stuff = re.findall(patterns["marks"], line.strip())
            if stuff:
                subject, subname, tot, cr, grade, gp = stuff[0]
                data["SUBJECTS"][subject] = subname

                marks_data.append({
                    "SEAT NO": seat_no,
                    "NAME": name,
                    "SEM": sem,
                    "SUBJECT": subject,
                    "TOT": int(tot),
                    "GRADE": grade,
                    "GP": gp,
                    "CR": cr
                })

    data["RESULT"] = marks_data
    return data


if __name__ == "__main__":
    data = parse("insem gazette.pdf")
    for key, value in data["STUDENT_INFO"].items():
        print(f"{key}: {value}")
