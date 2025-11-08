import os
from functions.get_files_info import run_python_file


print(run_python_file("calculator", "main.py")) # (should print the calculator's usage instructions)
print("----------------------------------------")
print(run_python_file("calculator", "main.py", ["3 + 5"])) # (should run the calculator... which gives a kinda nasty rendered result)
print("----------------------------------------")
print(run_python_file("calculator", "tests.py"))
print("----------------------------------------")
print(run_python_file("calculator", "../main.py")) # (this should return an error)
print("----------------------------------------")
print(run_python_file("calculator", "nonexistent.py")) # (this should return an error)
print("----------------------------------------")
print(run_python_file("calculator", "lorem.txt")) # (this should return an error)