age_list = [21,22,23,24,28,28,28,28]
def display_age_list(age_list):
    for i in age_list:
        print(i)

display_age_list(age_list)

n = len(age_list)
for i in range(n):
    for j in range(i+1,n):
        if age_list[i] != age_list[j]:
         print(f"{age_list[i]} vs {age_list[j]}")
        else:
           print(f"Age {i} and age {j} are the same")

