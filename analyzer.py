from pandas import DataFrame
from parser import parse


def subjectTopper(df: DataFrame, subject: str) -> DataFrame:
    subject: DataFrame = df.loc[df['SUBJECT'] == subject]
    return df.loc[subject['TOT'].idxmax()]


def top10(df: DataFrame) -> DataFrame:
    sem = "SGPA"
    return df["SGPA"].sort_values(ascending=False).head(10)


def analyze(data: dict):
    print(data)
    t10 = top10(DataFrame(data["STUDENT_INFO"]).T)
    print("TOP 10:\n", t10)
    for subject in set(data['SUBJECTS'].keys()):
        topper = subjectTopper(DataFrame(data["RESULT"]), subject)
        print("\nSUBJECT TOPPERS:")
        print(subject, data["SUBJECTS"][subject], topper['SEAT NO'], topper['TOT'])


if __name__ == '__main__':
    data = parse('insem gazette.pdf')
    analyze(data)
