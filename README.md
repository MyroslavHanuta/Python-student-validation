# Student Grade Calculator

A command-line Python tool that calculates students' overall module marks and grade categories from manual input or a `.txt` file.

## Features

- Standard assessment pattern (4 components weighted 10/20/30/40%) or a custom pattern with your own components and weights
- Batch import from a comma-separated `.txt` file, skipping corrupted lines
- Input validation for IDs, names (regex), dates of birth and marks (0–100)
- Calculates age, weighted overall score and grade category
- Displays results as a table and can save them to `student_grades.txt`

## Usage

```bash
pip install tabulate
python main.py
```

File format (standard pattern), one student per line:

```
ID, Full Name, YYYY-MM-DD, mark1, mark2, mark3, mark4
```
