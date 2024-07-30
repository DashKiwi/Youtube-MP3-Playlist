data = [['panel'], ['panel2']]
file = ".\Music\output.txt"

with open(file, "w") as txt_file:
    for line in data:
        txt_file.write(" ".join(line) + "\n")

data = []
with open(file, "r") as txt_file:
    file_lines = txt_file.readlines()
    for line in range(len(file_lines)):
        data.append(file_lines[line])

print(data)