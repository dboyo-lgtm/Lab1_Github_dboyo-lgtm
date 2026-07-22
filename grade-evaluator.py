#!/usr/bin/env python3
"""Grade evaluator program validates a grades CSV and reports and displays them on an
academic table containing assignment, Category,  Grade (%),  Weight,  Final weight,"""

import csv
import sys

GRADES_FILE = "grades.csv"

REQUIRED_TOTAL_WEIGHT = 100
REQUIRED_SUMMATIVE_WEIGHT = 40
REQUIRED_FORMATIVE_WEIGHT = 60
PASS_MARK = 50
GPA_SCALE = 5.0

# Transcript has both FA and SA; spelling in full is also accepted
FORMATIVE_ALIASES = ("fa", "formative")
SUMMATIVE_ALIASES = ("sa", "summative")


def normalise_category(raw_category):
    """Map FA/Formative to 'Formative' and SA/Summative to 'Summative'."""
    cleaned = raw_category.strip().lower()
    if cleaned in FORMATIVE_ALIASES:
        return "Formative"
    if cleaned in SUMMATIVE_ALIASES:
        return "Summative"
    return ""


def load_assignments(file_path):
    """Read the CSV into a list of assignment dictionaries.

    Tolerates several header spellings (assignment/name, group/category/type,
    score/grade) and skips blank lines.
    """
    assignments = []
    with open(file_path, newline="") as grades_file:
        reader = csv.DictReader(grades_file)
        if reader.fieldnames is None:
            return assignments

        for line_number, row in enumerate(reader, start=2):
            row = {
                (column or "").strip().lower(): (value or "").strip()
                for column, value in row.items()
            }
            if not any(row.values()):
                continue

            assignment_name = (
                row.get("assignment name")
                or row.get("assignment")
                or row.get("name")
                or ""
            ).strip()

            category = normalise_category(
                row.get("group")
                or row.get("category")
                or row.get("type")
                or ""
            )

            try:
                weight = float(row.get("weight") or 0)
                score = float(row.get("score") or row.get("grade") or 0)
            except ValueError:
                raise ValueError(
                    f"Line {line_number}: score and weight must be numbers "
                    f"(got score={row.get('score')!r}, weight={row.get('weight')!r})"
                )

            if not assignment_name:
                raise ValueError(f"Line {line_number}: missing assignment name")

            if not category:
                raise ValueError(
                    f"Line {line_number}: '{assignment_name}' has an unrecognised "
                    "category; expected FA, SA, Formative or Summative"
                )

            assignments.append({
                "name": assignment_name,
                "category": category,
                "weight": weight,
                "score": score,
                "final_weight": score / 100 * weight,
            })

    return assignments


def validate_assignments(assignments):
    """It collects all problems in a list rather than stopping the entire code  (errors, summative_weight, formative_weight)."""
    errors = []

    for assignment in assignments:
        if not 0 <= assignment["score"] <= 100:
            errors.append(
                f"Invalid score for {assignment['name']}: "
                f"{assignment['score']} (must be 0-100)"
            )
        if assignment["weight"] < 0:
            errors.append(
                f"Invalid weight for {assignment['name']}: "
                f"{assignment['weight']} (must not be negative)"
            )

    total_weight = sum(assignment["weight"] for assignment in assignments)

    summative_weight = sum(
        assignment["weight"]
        for assignment in assignments
        if assignment["category"] == "Summative"
    )

    formative_weight = sum(
        assignment["weight"]
        for assignment in assignments
        if assignment["category"] == "Formative"
    )

    if total_weight != REQUIRED_TOTAL_WEIGHT:
        errors.append(
            f"Total weight is {total_weight:g}, must be {REQUIRED_TOTAL_WEIGHT}"
        )
    if summative_weight != REQUIRED_SUMMATIVE_WEIGHT:
        errors.append(
            f"Summative weight is {summative_weight:g}, "
            f"must be {REQUIRED_SUMMATIVE_WEIGHT}"
        )
    if formative_weight != REQUIRED_FORMATIVE_WEIGHT:
        errors.append(
            f"Formative weight is {formative_weight:g}, "
            f"must be {REQUIRED_FORMATIVE_WEIGHT}"
        )

    return errors, summative_weight, formative_weight


def calculate_weighted_score(assignments, category):
    """it adds up the final weight of one category."""
    return sum(
        assignment["final_weight"]
        for assignment in assignments
        if assignment["category"] == category
    )


def find_resubmission_candidates(assignments):
    """It builds a list of FA below 50 because both conditions have to be made which is above 50 in SA and FA"""
    failed_assignments = [
        assignment
        for assignment in assignments
        if assignment["category"] == "Formative" and assignment["score"] < PASS_MARK
    ]

    if not failed_assignments:
        return []

    highest_weight = max(assignment["weight"] for assignment in failed_assignments)

    return [
        assignment
        for assignment in failed_assignments
        if assignment["weight"] == highest_weight
    ]


def print_assignment_table(assignments):
    """It measures the length of the assignment name andmjoins two list together"""
    name_width = max(
        [len("Assignment")] + [len(a["name"]) for a in assignments]
    )

    header = (
        f"{'Assignment':<{name_width}}  {'Category':>8}  "
        f"{'Grade (%)':>9}  {'Weight':>6}  {'Final weight':>12}"
    )
    print(header)
    print("-" * len(header))

    for assignment in assignments:
        category_code = "FA" if assignment["category"] == "Formative" else "SA"
        print(
            f"{assignment['name']:<{name_width}}  {category_code:>8}  "
            f"{assignment['score']:>9g}  {assignment['weight']:>6g}  "
            f"{assignment['final_weight']:>12g}"
        )

    print("-" * len(header))


def main():
    try:
        assignments = load_assignments(GRADES_FILE)
    except FileNotFoundError:
        sys.exit(f"Error: {GRADES_FILE} not found in the current directory.")
    except PermissionError:
        sys.exit(f"Error: no permission to read {GRADES_FILE}.")
    except ValueError as error:
        sys.exit(f"Error reading {GRADES_FILE}: {error}")

    if not assignments:
        sys.exit(
            f"Error: {GRADES_FILE} contains no assignment records. "
            "Add grade data before running the evaluator."
        )

    errors, summative_weight, formative_weight = validate_assignments(assignments)
    if errors:
        print("Validation failed:")
        for error in errors:
            print("  -", error)
        sys.exit(1)

    formative_score = calculate_weighted_score(assignments, "Formative")
    summative_score = calculate_weighted_score(assignments, "Summative")
    total_grade = formative_score + summative_score
    gpa = total_grade / 100 * GPA_SCALE

    formative_percentage = formative_score / formative_weight * 100
    summative_percentage = summative_score / summative_weight * 100
    has_passed = (
        formative_percentage >= PASS_MARK and summative_percentage >= PASS_MARK
    )

    resubmission_candidates = find_resubmission_candidates(assignments)
    if resubmission_candidates:
        resubmission_text = ", ".join(
            assignment["name"] for assignment in resubmission_candidates
        )
    else:
        resubmission_text = "None"

    print_assignment_table(assignments)

    label_width = 28
    print(f"{f'Formatives ({formative_weight:g})':<{label_width}}{formative_score:g}")
    print(f"{f'Summatives ({summative_weight:g})':<{label_width}}{summative_score:g}")
    print(f"{'Total Grade':<{label_width}}{total_grade:g}/100")
    print(f"{'GPA':<{label_width}}{gpa:g}/{GPA_SCALE:g}")
    print(f"{'Status':<{label_width}}{'PASSED' if has_passed else 'FAILED'}")
    print(f"{'Available for resubmission':<{label_width}}{resubmission_text}")


if __name__ == "__main__":
    main()
