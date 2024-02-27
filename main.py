from poppler import load_from_file
import re
import xlsxwriter

patterns = {
    "seat_no": r"Seat no:.*?(\d+)",
    "name": r"Name:.*?([\w\W]+) mother",
    "mother_name": r"mother name:.*?(\w+)",
    "marks": r"\d{7}.*",
}

data = {}

pdf = load_from_file("gadget.pdf")
page = pdf.create_page(0)

txt = page.text()

data["Seat No"] = re.findall(patterns["seat_no"], txt)[0].strip()
data["Name"] = re.findall(patterns["name"], txt)[0].strip()
data["Mother's Name"] = re.findall(patterns["mother_name"], txt)[0].strip()

marks_data = list(map(lambda x: x.split(), re.findall(patterns["marks"], txt)))

print(data)
print("\n".join(map(str, marks_data)))

