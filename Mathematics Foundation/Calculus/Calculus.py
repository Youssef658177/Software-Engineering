import sympy

# 1. Create a symbolic variable 'x'
x = sympy.Symbol('x')

# 2. Define the mathematical function
function = x**2 + 3*x + 5

# 3. Find the derivative of the function with respect to 'x'
# The diff() function calculates the derivative
derivative = sympy.diff(function, x)

# 4. Print the results
print(f"The original function is: {function}")
print(f"The derivative of the function is: {derivative}")

# The expected output should be 2*x + 3
