from pandas import DataFrame
from parser import parse


def subjectTopper(df: DataFrame, subject: str) -> DataFrame:
    subject: DataFrame = df.loc[df['SUBJECT'] == subject]
    return df.loc[subject['TOT'].idxmax()]


def top10(df: DataFrame) -> DataFrame:
    return df.loc[df["CGPA"].idxmax()]


def analyze(data: dict):
    df = DataFrame(data["RESULT"])
    for subject in set(df['SUBJECT']):
        topper = subjectTopper(df, subject)
        print(subject, data["SUBJECTS"][subject], topper['SEAT NO'], topper['TOT'])


if __name__ == '__main__':
    data = parse('gadget.pdf')
    analyze(data)
