class Calculator:
    def add(self, x, y):
        output = x + y
        return output

    def subtract(self, x, y):
        output = x - y
        return output

    def multiply(self, x, y):
        output = x * y
        return output

    def divide(self, x, y):
        output = x / y if y != 0 else "Cannot divide by zero"
        return output