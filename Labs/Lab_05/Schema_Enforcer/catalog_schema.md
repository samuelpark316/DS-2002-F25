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
