from dataclasses import dataclass
#from app.utils import normalize_name

def normalize_name(name: str) -> str:
    return name.strip().title()

@dataclass
class Student:
    name: str
    points: int
    passed: bool

    @classmethod
    def from_csv_row(cls, row):
        name = normalize_name(row["name"])
        try:
            points = int(row["points"])
        except ValueError:
            raise ValueError(f"Row skipped: {name} --> {row["points"]}")
        passed = bool(row["passed"])
        return cls(name=name, points=points, passed=passed)
