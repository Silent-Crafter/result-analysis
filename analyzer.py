from typing import Tuple

from pandas import DataFrame
from parser import parse


def subjectTopper(df: DataFrame, subject: str, exam: str) -> DataFrame:
    sem = 1 if exam == "INSEM" else 2
    subject: DataFrame = df.loc[(df['SUBJECT'] == subject) & (df["SEM"] == sem)]
    return df.loc[subject['TOT'].idxmax()]


def top10(df: DataFrame, gpa) -> DataFrame:
    return df[gpa].sort_values(ascending=False).head(10)


def pass_fail(df: DataFrame, gpa) -> tuple[int, int]:
    passed = len(df.loc[df[gpa] > 0])
    failed = len(df.loc[df[gpa] < 0])
    return passed, failed


def analyze(data: dict):
    t10 = top10(DataFrame(data["STUDENT_INFO"]).T, "CGPA" if data["EXAM"] == "ENDSEM" else "SGPA")
    # print("TOP 10:")
    # print(t10)
    subject_toppers = []
    for subject in set(data['SUBJECTS'].keys()):
        topper = subjectTopper(DataFrame(data["RESULT"]), subject, data["EXAM"])
        # print("\nSUBJECT TOPPERS:")
        # print(subject, data["SUBJECTS"][subject], topper['SEAT NO'], topper['TOT'])
        subject_toppers.append((subject, data["SUBJECTS"][subject], topper['SEAT NO'], topper['TOT']))

    return {
        "TOP 10": t10.to_dict(),
        "SUBJECT TOPPERS": subject_toppers,
        "PASS FAIL": pass_fail(DataFrame(data["STUDENT_INFO"]).T, "CGPA" if data["EXAM"] == "ENDSEM" else "SGPA")
    }


if __name__ == '__main__':
    data = parse('endsem gazette.pdf')
    print(analyze(data))
