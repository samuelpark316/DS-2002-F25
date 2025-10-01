#!/usr/bin/env python3
import os, csv, json, textwrap
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent

RAW_CSV            = BASE / "raw_survey_data.csv"
RAW_JSON           = BASE / "raw_course_catalog.json"
CLEAN_CSV          = BASE / "clean_survey_data.csv"
CLEAN_CATALOG_CSV  = BASE / "clean_course_catalog.csv"
SURVEY_SCHEMA_MD   = BASE / "survey_schema.md"
CATALOG_SCHEMA_MD  = BASE / "catalog_schema.md"


# Part 1
def make_raw_csv():
    rows = [
        [1001, "Computer Science", 3,       "Yes", "10.5"],
        [1002, "Statistics",       3.7,     "No",  "15.0"],
        [1003, "Data Science",     3,       "Yes", "12.0"],
        [1004, "Economics",        3.25,    "No",  "9.5"],
        [1005, "Mechanical Eng",   4,       "Yes", "18.0"],
    ]
    with RAW_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["student_id", "major", "GPA", "is_cs_major", "credits_taken"])
        w.writerows(rows)
    print(f"✅ Wrote {RAW_CSV}")

#Part 2
def make_raw_json():
    data = [
        {
            "course_id": "DS2002",
            "section": "001",
            "title": "Data Science Systems",
            "level": 200,
            "instructors": [
                {"name": "Austin Rivera", "role": "Primary"},
                {"name": "Heywood Williams-Tracy", "role": "TA"}
            ]
        },
        {
            "course_id": "CS3240",
            "section": "001",
            "title": "Software Engineering",
            "level": 300,
            "instructors": [
                {"name": "Derrick Stone", "role": "Primary"},
                {"name": "Brandon Istafan", "role": "TA"}
            ]
        }
    ]
    with RAW_JSON.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {RAW_JSON}")

#Part 3
def clean_csv():
    df = pd.read_csv(RAW_CSV)

    df["is_cs_major"] = (
        df["is_cs_major"]
        .astype(str).str.strip().str.lower()
        .map({"yes": True, "no": False})
    )

    df = df.astype({"GPA": "float64", "credits_taken": "float64"})

    df["major"] = df["major"].astype("string")

    print("\nDtypes after cleaning:")
    print(df.dtypes)

    df.to_csv(CLEAN_CSV, index=False)
    print(f"\nWrote {CLEAN_CSV}")

#Part 4
def normalize_json():
    """Task 4: Flatten instructors → rows using pd.json_normalize."""
    with RAW_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    norm = pd.json_normalize(
        data,
        record_path=["instructors"],
        meta=["course_id", "section", "title", "level"],
        errors="ignore"
    )

    print("\nPreview of normalized catalog:")
    print(norm.head())

    norm.to_csv(CLEAN_CATALOG_CSV, index=False)
    print(f"\nWrote {CLEAN_CATALOG_CSV}")

def write_survey_schema_md():
    md = textwrap.dedent("""
    # Survey Schema

    This schema documents the **clean**, enforced types for `clean_survey_data.csv`.

    | Column Name     | Required Data Type | Brief Description                                  |
    | :---            | :---               | :---                                               |
    | `student_id`    | `INT`              | Unique identifier for the student.                 |
    | `major`         | `VARCHAR(50)`      | Student’s declared major or program.               |
    | `GPA`           | `FLOAT`            | Grade point average on a 4.0 scale.                |
    | `is_cs_major`   | `BOOL`             | True if the student is in Computer Science.        |
    | `credits_taken` | `FLOAT`            | Total credits the student has completed/taken.     |

    """).strip()

    SURVEY_SCHEMA_MD.write_text(md + "\n", encoding="utf-8")
    print(f"Wrote {SURVEY_SCHEMA_MD}")

def write_catalog_schema_md():
    md = textwrap.dedent("""
    # Course Catalog (Normalized) Schema

    Each row represents a single instructor–course pairing from `clean_course_catalog.csv`.

    | Column Name | Required Data Type | Brief Description        |
    | :---        | :---               | :---                     |
    | `name`      | `VARCHAR(100)`     | Instructor full name.    |
    | `role`      | `VARCHAR(20)`      | Instructor role (Primary/TA). |
    | `course_id` | `VARCHAR(10)`      | Course identifier.       |
    | `section`   | `VARCHAR(10)`      | Section identifier (nullable). |
    | `title`     | `VARCHAR(200)`     | Official course title.   |
    | `level`     | `INT`              | Course level (e.g., 200, 300). |

    """).strip()

    CATALOG_SCHEMA_MD.write_text(md + "\n", encoding="utf-8")
    print(f"Wrote {CATALOG_SCHEMA_MD}")

def main():
    # Part 1
    make_raw_csv()
    make_raw_json()

    # Part 2
    clean_csv()
    normalize_json()

    # Part 3
    write_survey_schema_md()
    write_catalog_schema_md()

    print("\nAll done. Expected files created:")
    for p in [
        RAW_CSV, RAW_JSON, CLEAN_CSV, CLEAN_CATALOG_CSV, SURVEY_SCHEMA_MD, CATALOG_SCHEMA_MD
    ]:
        print(" -", p)

if __name__ == "__main__":
    main()
