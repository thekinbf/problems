import check50
import csv
import re


@check50.check()
def exists():
    """big5.R exists"""
    check50.exists("big5.R")
    check50.include("tests.tsv")


@check50.check(exists)
def error():
    """big5.R runs without error"""
    status = check50.run("Rscript big5.R").exit()
    if status != 0:
        out = check50.run("Rscript big5.R").stdout()
        if match := re.search(r"cannot open file '(?P<filename>[^']+)'", out):
            filename = match.group("filename")
            raise check50.Failure(f"big5.R could not open \"{filename}\"", help="Be sure to provide a relative path, such as \"tests.tsv\"")
        raise check50.Failure("big5.R encountered an error")


@check50.check(error)
def format():
    """big5.R produces a properly formatted analysis.csv"""
    check50.exists("analysis.csv")
    with open("analysis.csv", "r") as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        if dialect.delimiter != ',':
            raise check50.Failure("analysis.csv does not use a comma as a separator")


@check50.check(format)
def rows():
    """analysis.csv contains all rows from tests.tsv"""
    row_count = 0
    with open("analysis.csv", "r") as f:
        reader = csv.DictReader(f)
        for _ in reader:
            row_count += 1

    if row_count < 19719:
        raise check50.Failure("analysis.csv has fewer rows than tests.tsv")

    if row_count > 19719:
        raise check50.Failure("analysis.csv has more rows than tests.tsv")


@check50.check(rows)
def columns():
    """analysis.csv adds columns for each personality trait"""
    with open("analysis.csv", "r") as f:
        reader = csv.DictReader(f)
        fieldnames = [fieldname.lower() for fieldname in reader.fieldnames]

    for trait in [
        "extroversion",
        "neuroticism",
        "agreeableness",
        "conscientiousness",
        "openness",
    ]:
        if trait not in fieldnames:
            raise check50.Failure(f'Could not find "{trait}" in column names')


@check50.check(columns)
def gender_column_test():
    """big5.R converts gender column to text"""
    expected_counts = {"unanswered": 24, "male": 7608, "female": 11985, "other": 102}
    counts = {"unanswered": 0, "male": 0, "female": 0, "other": 0}

    with open("analysis.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            gender = row["gender"].lower()
            if gender == "unanswered" or gender == "na":
                counts["unanswered"] += 1
            elif gender == "male":
                counts["male"] += 1
            elif gender == "female":
                counts["female"] += 1
            elif gender == "other":
                counts["other"] += 1
            else:
                raise check50.Failure(
                    f"\"{row['gender']}\" is not included in codebook.txt"
                )

    for gender in counts.keys():
        if counts[gender] != expected_counts[gender]:
            raise check50.Failure(
                f"Expected {expected_counts[gender]} {gender} values in gender column. Found {counts[gender]}."
            )


@check50.check(columns)
def results():
    """big5.R computes correct personality test results"""
    expected_results = {
        "extroversion": 0.93,
        "neuroticism": 0.27,
        "agreeableness": 1,
        "conscientiousness": 0.87,
        "openness": 0.8,
    }
    with open("analysis.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = {k.lower(): v for k, v in row.items()}

            for trait in expected_results.keys():
                try:
                    row[trait] = float(row[trait])
                except ValueError:
                    raise check50.Failure(f"{row[trait]} is not a number")

                if row[trait] != expected_results[trait]:
                    raise check50.Failure(
                        f"Expected to find {expected_results[trait]} in first row's {trait} column. Found {row[trait]}."
                    )

            break
