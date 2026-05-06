"""Agent that calculates the sum of two numbers."""

import argparse


def run(a: float, b: float) -> float:
    result = a + b
    print(f"{a} + {b} = {result}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sum two numbers")
    parser.add_argument("a", type=float, help="First number")
    parser.add_argument("b", type=float, help="Second number")
    args = parser.parse_args()
    run(args.a, args.b)
