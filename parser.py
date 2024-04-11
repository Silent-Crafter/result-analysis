from poppler import load_from_file
import re


def parse(pdffile):
    patterns = {
        "seat_no": r"Seat No:.*?(\w+)",
        "name": r"Name:\s+?([\w]+?)\s+",
        "mother_name": r"Mother’s Name:[\s]*?([\w]+?)\s+[\w]",
        "cgpa": r"cgpa\s*([\d\-])*",
        "sgpa": r"sgpa\s*([\d\-])*",
        "marks": r"^(\d{6})" + r"\s*(\w*)" + r"\s*[\d\-/]*" * 7 + r"\s*(\d*)" + r"\s*(\d*)" + r"\s*(\w*)" + r"\s*(\d*)" + r"[\d\s]*"
    }

    data = {"SUBJECTS": {}, "STUDENT_INFO": {}, "RESULT": []}

    pdf = load_from_file(pdffile)
    marks_data = []
    for count in range(pdf.pages-1):
        page = pdf.create_page(count)
        txt = page.text()

        seat_no = re.findall(patterns["seat_no"], txt)[0].strip()
        name = re.findall(patterns["name"], txt)[0].strip()
        mother_name = re.findall(patterns["mother_name"], txt)[0].strip()

        data["STUDENT_INFO"][seat_no] = {"NAME": name, "MOTHER": mother_name}

        cgpa = re.findall(patterns["cgpa"], txt)
        sgpa = re.findall(patterns["sgpa"], txt)

        if not cgpa:
            cgpa = -1
        elif cgpa[0] == '-':
            cgpa = -1
        else:
            cgpa = int(cgpa[0])

        if not sgpa:
            sgpa = -1
        elif sgpa[0] == '-':
            sgpa = -1
        else:
            sgpa = int(sgpa[0])

        data["STUDENT_INFO"][seat_no]["CGPA"] = cgpa
        data["STUDENT_INFO"][seat_no]["SEM 1 RESULT"] = "FAIL" if cgpa == -1 else "PASS"
        data["STUDENT_INFO"][seat_no]["SGPA"] = sgpa
        data["STUDENT_INFO"][seat_no]["SEM 2 RESULT"] = "FAIL" if sgpa == -1 else "PASS"

        sem = 1
        for line in txt.splitlines():
            _sem = re.findall(r"sem(\d)", line.strip())
            if _sem:
                sem = int(_sem[0])

            stuff = re.findall(patterns["marks"], line.strip())
            if stuff:
                subject, subname, tot, cr, grade, gp = stuff[0]
                data["SUBJECTS"][subject] = subname
                # marks_data[counter]['SEAT NO'] = seat_no
                # marks_data[counter]['NAME'] = name
                # marks_data[counter]['SEM'] = int(sem)
                # marks_data[counter]['SUBJECT'] = subject
                # marks_data[counter]['TOT'] = int(tot)
                # marks_data[counter]['GRADE'] = grade
                # marks_data[counter]['GP'] = gp
                # marks_data[counter]['CR'] = cr

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

                # counter += 1

    data["RESULT"] = marks_data
    return data


if __name__ == "__main__":
    data = parse("gadget.pdf")
    for key, value in data["STUDENT_INFO"].items():
        print(f"{key}: {value}")
