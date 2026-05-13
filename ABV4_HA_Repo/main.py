from app.utils import calculate_average_points, load_students, print_report


def run() -> None:
	students = load_students()
	average = calculate_average_points(students, min_students=5)
	print_report(students, average)


run()
