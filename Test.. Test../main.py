import base64

input = input("Enter the base64 encoded string:\n")

decoded = base64.b64decode(input)
print(f"The flag is:\n{decoded.decode()}")