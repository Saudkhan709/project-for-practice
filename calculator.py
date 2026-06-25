# calculator.py
def add(a,b):
    return a+b
def subtract (a,b):
    return a-b
def multiply(a,b):
    return a*b
def divide(a,b):
    if b == 0:
        return "error: division by zero"
    return a/b
# add this below your functions
def run_calculator():
    print("=== simple calculator ===")
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("invalid number, try again")
            continue

        op = input("Enter operator (+, -, *, /): ").strip()
        print(f"you entered {num1} {op} {num2}")

        if op == "+":
            result = add(num1, num2)
        elif op == "-":
            result = subtract(num1, num2)
        elif op == "*":
            result = multiply(num1, num2)
        elif op == "/":
            result = divide(num1, num2)
        else:
            result = "unknown operator"

        print(f"result: {result}")

        choice = input("\ncalculate again? (yes/quit): ").strip().lower()
        if choice in ("quit", "q", "no"):
            print("goodbye!")
            break

if __name__ == "__main__":
    run_calculator()

