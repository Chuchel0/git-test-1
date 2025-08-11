import math
import sys

def is_perfect_square(n):
    """Checks if a number is a perfect square."""
    if n < 0:
        return False
    sqrt_n = int(math.sqrt(n))
    return sqrt_n * sqrt_n == n

def is_fibonacci(n):
    """
    Checks if a number is a Fibonacci number using the property:
    A number n is a Fibonacci number if and only if one or both of
    5*n^2 + 4 or 5*n^2 - 4 is a perfect square.
    """
    if n < 0:
        return False, -1
    if n == 0:
        return True, 0

    if is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4):
        # If it's a Fibonacci number, find its position
        a, b = 0, 1
        position = 0
        while a < n:
            a, b = b, a + b
            position += 1
        if a == n:
            return True, position

    return False, -1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fibonacci.py <integer>")
        sys.exit(1)

    try:
        num = int(sys.argv[1])
        is_fib, pos = is_fibonacci(num)
        if is_fib:
            print(f"{num} is a Fibonacci number at position {pos}.")
        else:
            print(f"{num} is not a Fibonacci number.")
    except ValueError:
        print("Invalid input. Please provide an integer.")
        sys.exit(1)
