def calculate(x, y, operator):
    if operator == '+':
        return x + y
    if operator == '-':
        return x - y
    if operator == 'x':
        return x * y
    if operator == '/':
        return x // y

    return False
