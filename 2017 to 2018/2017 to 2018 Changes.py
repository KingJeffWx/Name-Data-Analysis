names_2017 = dict()
names_2018 = dict()

all_names = set()

with open("yob2017.txt") as f:
    for line in f:
        line = line.split(",")
        names_2017[(line[0], line[1])] = int(line[2].rstrip())
        all_names.add((line[0], line[1]))
with open("yob2018.txt") as f:
    for line in f:
        line = line.split(",")
        names_2018[(line[0], line[1])] = int(line[2].rstrip())
        all_names.add((line[0], line[1]))

diff = dict()
for name in all_names:
    if name not in names_2017:
        diff[name] = names_2018[name]
    elif name not in names_2018:
        diff[name] = names_2017[name] * -1
    else:
        diff[name] = names_2018[name] - names_2017[name]

f = open("2017vs2018.txt", "w")
for name in diff:
    if name not in names_2017:
        f.write(name[0] + ',' + name[1] + ',' + '0' + ',' + str(names_2018[name]) + ',' + str(diff[name]) + '\n')
    elif name not in names_2018:
        f.write(name[0] + ',' + name[1] + ',' + str(names_2017[name])  + ',' + '0' + ',' + str(diff[name]) + '\n')
    else:
        f.write(name[0] + ',' + name[1] + ',' + str(names_2017[name])  + ',' + str(names_2018[name]) + ',' + str(diff[name]) + '\n')
f.close()
