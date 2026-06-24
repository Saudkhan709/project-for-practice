
"""Student Info Collector

Simple CLI to add, list, search and save student records (JSON + CSV).
"""
import json
import csv
import os
from pathlib import Path

DATA_JSON = Path("students.json")


def load_students():
	if DATA_JSON.exists():
		try:
			return json.loads(DATA_JSON.read_text(encoding="utf-8"))
		except Exception:
			return []
	return []


def save_students(students):
	DATA_JSON.write_text(json.dumps(students, ensure_ascii=False, indent=2), encoding="utf-8")
	# also write CSV
	if students:
		keys = ["id", "name", "age", "grade", "email"]
		with open("students.csv", "w", newline='', encoding="utf-8") as f:
			writer = csv.DictWriter(f, fieldnames=keys)
			writer.writeheader()
			for s in students:
				writer.writerow({k: s.get(k, "") for k in keys})


def prompt_student():
	sid = input("Student ID: ").strip()
	if not sid:
		print("ID required.")
		return None
	name = input("Name: ").strip()
	age = input("Age: ").strip()
	grade = input("Grade: ").strip()
	email = input("Email: ").strip()
	return {"id": sid, "name": name, "age": age, "grade": grade, "email": email}


def list_students(students):
	if not students:
		print("No records.")
		return
	for s in students:
		print(f"{s.get('id')} | {s.get('name')} | Age: {s.get('age')} | Grade: {s.get('grade')} | {s.get('email')}")


def search_students(students, term):
	term = term.lower()
	return [s for s in students if term in s.get('id','').lower() or term in s.get('name','').lower() or term in s.get('email','').lower()]


def main():
	students = load_students()
	while True:
		cmd = input("[A]dd [L]ist [S]earch [Q]uit: ").strip().lower()
		if cmd in ('q', 'quit'):
			save_students(students)
			print("Saved. Bye.")
			break
		if cmd in ('a', 'add'):
			s = prompt_student()
			if s:
				students.append(s)
				print("Added.")
		elif cmd in ('l', 'list'):
			list_students(students)
		elif cmd in ('s', 'search'):
			term = input("Search term: ").strip()
			res = search_students(students, term)
			list_students(res)
		else:
			print("Unknown command.")


if __name__ == '__main__':
	main()
