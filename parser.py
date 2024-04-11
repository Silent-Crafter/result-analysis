from poppler import load_from_file
import re


def parse(pdffile):
    patterns = {
        "seat_no": r"Seat No:.*?(\w+)",
        "name": r"Name:\s+?([\w]+?)\s+",
        "mother_name": r" Mother’s Name:[\s]*?([\w]+?)\s+[\w]",
        "marks": r"\w{6}\s*\w*[\W\w]*",
    }

    data: list[dict] = []

    pdf = load_from_file(pdffile)
    for count in range(pdf.pages):
        dat = {}
        page = pdf.create_page(count)
        txt = page.text()

        dat["Seat No"] = re.findall(patterns["seat_no"], txt)[0].strip()
        dat["Name"] = re.findall(patterns["name"], txt)[0].strip()
        dat["Mother's Name"] = re.findall(patterns["mother_name"], txt)[0].strip()

        marks_dat: list[tuple] = []
        for line in txt.splitlines():
            stuff = re.findall(r"^(\d{6})\s*\w*\s*[\w\-]*\s*\s*[\w\-]*\s*\s*[\w\-]*\s*\s*[\w\-/]*\s*\s*[\w\-]*\s*\s*[\w\-]*\s*\s*[\w\-]*\s*\s*([\w\-]*)\s*\s*[\w\-]*\s*\s*([\w\-]*)\s*\s*[\w\-]*\s*\s*[\w\-]*\s*\s*[\w\-]*\s*\s*[\w\-]*", line.strip())
            if stuff:
                marks_dat.append(stuff[0])

        dat["result"] = {}

        for mark in marks_dat:
            subject, tot, grade = mark
            dat["result"][subject] = {}
            dat["result"][subject]["Total%"] = tot
            dat["result"][subject]["Grade"] = grade

        data.append(dat)

    return data


if __name__ == "__main__":
    data = parse("gadget.pdf")
    print(data)
