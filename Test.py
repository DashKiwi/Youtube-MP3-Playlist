data = [['Playlist 1','panel'], ['nameservers','panel']]
file = ".\Music\output.txt"

with open(file, "w") as txt_file:
    for line in data:
        txt_file.write(" ".join(line) + "\n")

data = []
with open(file, "r") as txt_file:
    #lines = file.readlines()
    #line_count = len(lines)
    #word_count = sum(len(line.split()) for line in lines)
    #print("Number of lines:", line_count)
    for line in range(len(txt_file.readlines())):
        data.append(txt_file.read(line))
        print(data)