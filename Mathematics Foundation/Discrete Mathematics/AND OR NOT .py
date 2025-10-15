# 1. Create a list of all possible combinations for P and Q
combinations = [(True, True), (True, False), (False, True), (False, False)]

print("--- Truth Table for (P AND Q) OR (NOT P) ---")
print("|   P   |   Q   | (P AND Q) OR (NOT P) |")
print("|-------|-------|----------------------|")

# 2. Iterate through each combination
for p, q in combinations:
    # 3. Calculate the value of the statement
    # In Python, 'and', 'or', and 'not' are the logical operators
    result = (p and q) or (not p)
    
    # 4. Print the formatted row
    # Use f-strings for easy formatting
    print(f"| {str(p):<5} | {str(q):<5} | {str(result):<20} |")
