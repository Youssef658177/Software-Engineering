 # Define the two sets
Admins = {'Ahmed', 'Sara', 'Omar'}
Developers = {'Omar', 'Laila', 'Ahmed', 'Khaled'}

print("--- User Permissions Analysis ---")

# 1. Union: All users in both teams
all_users = Admins.union(Developers)
print(f"1. All Users (Union): {all_users}")

# 2. Intersection: Users who are both Admins AND Developers
admin_devs = Admins.intersection(Developers)
print(f"2. Admin & Devs (Intersection): {admin_devs}")

# 3. Difference: Users who are Admins ONLY
only_admins = Admins.difference(Developers)
print(f"3. Admins ONLY (Difference): {only_admins}")
