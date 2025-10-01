# Survey Schema

This schema documents the **clean**, enforced types for `clean_survey_data.csv`.

| Column Name     | Required Data Type | Brief Description                                  |
| :---            | :---               | :---                                               |
| `student_id`    | `INT`              | Unique identifier for the student.                 |
| `major`         | `VARCHAR(50)`      | Student’s declared major or program.               |
| `GPA`           | `FLOAT`            | Grade point average on a 4.0 scale.                |
| `is_cs_major`   | `BOOL`             | True if the student is in Computer Science.        |
| `credits_taken` | `FLOAT`            | Total credits the student has completed/taken.     |
