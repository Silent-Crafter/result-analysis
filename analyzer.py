from pandas import DataFrame
from parser import parse


def subjectTopper(df: DataFrame, subject: str, exam: str) -> DataFrame:
    sem = 1 if exam == "SEM1" else 2
    subject: DataFrame = df.loc[(df['SUBJECT'] == subject) & (df["SEM"] == sem)]
    return subject.sort_values(by=['TOT'], ascending=False).head(10)


def top10(df: DataFrame, gpa) -> DataFrame:
    return df[gpa].sort_values(ascending=False).head(10)


def pass_fail(df: DataFrame, gpa):
    passed = len(df.loc[df[gpa] > 0])
    failed = len(df.loc[df[gpa] < 0])
    return {"PASS": passed, "FAIL": failed}


def analyze(data: dict):
    t10 = top10(DataFrame(data["STUDENT_INFO"]).T, "CGPA" if data["EXAM"] == "SEM2" else "SGPA")
    # print("TOP 10:")
    # print(t10)
    sub_tops = {}
    for subject in set(data['SUBJECTS'].keys()):
        subject_toppers = []
        toppers = subjectTopper(DataFrame(data["RESULT"]), subject, data["EXAM"])
        for topper in zip(toppers['SEAT NO'], toppers['TOT']):
            subject_toppers.append((topper[0], topper[1]))
        sub_tops[subject] = subject_toppers

    return {
        "TOP 10": t10.to_dict(),
        "SUBJECT TOPPERS": sub_tops,
        "PASS FAIL": pass_fail(DataFrame(data["STUDENT_INFO"]).T, "CGPA" if data["EXAM"] == "SEM2" else "SGPA")
    }


if __name__ == '__main__':
    data = parse('endsem gazette.pdf')
    print(analyze(data))
