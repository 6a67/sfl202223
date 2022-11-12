import sys
import io

# supress print statements for the import
old_stdout = sys.stdout
sys.stdout = io.StringIO()
from hash import hash
# restore print statements
sys.stdout = old_stdout



input = input("Enter the base64 given hash:\n")

decoded = hash(input)
print(f"The flag is:\n{decoded}")