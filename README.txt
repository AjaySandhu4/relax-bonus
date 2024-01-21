Run code using:
    python3 main.py

Relations are parsed from the test file with the name held in the constant RELATION_FILE.
The relations in the text file can be replaced (in the correct format).

The system supports the following operations:
    Select (σ)
    Projection (π)
    Cross Product (×)
    Intersection (∩)
    Union (∪)
    Minus (-)
    Inner Join (⨝)
    Left Outer Join (⟕)
    Right Outer Join (⟖)
    Full Outer Join (⟗)

Note: Inner Join (⨝) supports natural, equi, and theta join

Examples of possible queries:
    (Course) × (takes)
    π name, email (Student)
    (takes) ⨝ cname=name (Course)
    σ name='John' (Student)
    σ id=2 (Student)
    (Student) ⨝ (CourseTwo)
    (takes) ∩ (takesTwo)
    (takes) ∪ (takesTwo)
    (takesTwo) - (takes)
    (Student) ⟗ name=name (CourseTwo)
    σ name='John' ((Student) ⟗ name=name (CourseTwo))
    (Student) ⟕ name=name (CourseTwo)
    (Course) ⟖ name=name (π name, email (Student))
    (Student) ⨝ id<sid (takes)
