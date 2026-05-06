---
name: sum
description: 'Calculate the sum of two numbers. Use when the user asks to add, sum, or total two numbers together.'
argument-hint: 'Two numbers to add, e.g. 3 5'
---

# Sum Two Numbers

## When to Use
- User asks to add two numbers
- User wants a sum or total calculated

## Procedure
1. Get the two numbers from the user (passed as arguments)
2. Run the sum agent script:
   ```bash
   python agents/sum_numbers.py <number1> <number2>
   ```
3. Return the result to the user
