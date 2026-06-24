def simple_calculator():
    print("Simple Calculator")
    print("Enter two numbers and choose an operation.")

    try:
        x = float(input("First number: "))
        y = float(input("Second number: "))
    except ValueError:
        print("Please enter valid numbers.")
        return

    print("Operations: +  -  *  /")
    op = input("Choose operation: ")

    if op == "+":
        result = x + y
    elif op == "-":
        result = x - y
    elif op == "*":
        result = x * y
    elif op == "/":
        if y == 0:
            print("Cannot divide by zero.")
            return
        result = x / y
    else:
        print("Invalid operation.")
        return

    print(f"Result: {x} {op} {y} = {result}")


if __name__ == "__main__":
    simple_calculator()