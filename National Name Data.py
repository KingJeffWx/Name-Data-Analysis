import csv
import collections
import numpy as np

def read_data():
    nf = open('usnames.txt', 'w')
    for year in range(1880, 2016):
        filename = 'yob' + str(year) + '.txt'
        with open(filename) as f:
            for line in f:
                nf.write(str(year) + ',' + line)
    nf.close()

def get_namedata(name, gender): # get births per year for a name and expected amount of people with name alive
    filename = name + '(' + gender + ')' + '.txt'
    nf = open(filename, 'w')
    l = len(name)
    total_alive = 0
    alive_peryear = collections.OrderedDict()
    with open('usnames.txt') as f:
        for line in f:
            if line[5:5+l] == name and line[5+l+1] == gender:
                comma_count = 0
                birth_index = 0 # where in the line the birth count starts
                for i in range(len(line)):
                    if line[i] == ',':
                        comma_count += 1
                    if comma_count == 3:
                        birth_index = i + 1
                        break
                year = int(line[0:4])
                births = int(line[birth_index:])
                life_ratio = get_expectedlife(name, gender, year)
                alive = int(births * life_ratio)
                total_alive += alive
                alive_peryear[year] = alive
                #print(str(year) + ',' + str(births) + ',' + str(alive))
                nf.write(str(year) + ',' + str(births) + ',' + str(alive) + '\n')   # year, number of births
    median_age = get_medianage(name, gender, alive_peryear)
    p25th = get_agepercentile(name, gender, alive_peryear, 25)
    p75th = get_agepercentile(name, gender, alive_peryear, 75)
    #print('Expected number alive today: ' + str(total_alive) + '\n')
    print(name + ', 25th percentile: ' + str(p25th))
    print(name + ', 50th percentile: ' + str(median_age))
    print(name + ', 75th percentile: ' + str(p75th))
    #nf.write('Median age: ' + str(median_age))

def get_medianage(name, gender, alive_peryear):
    cum_alive = {}  # how many are alive, cumulative
    i = 0
    cumalive_list = np.cumsum(list(alive_peryear.values()))
    for key, value in alive_peryear.items():
        cum_alive[key] = cumalive_list[i]
        i += 1
    median_amount = cumalive_list[-1] / 2
    for key, value in cum_alive.items():
        if cum_alive[key] >= median_amount:
            return 2017 - key

def get_agepercentile(name, gender, alive_peryear, percentile):
    cum_alive = {}  # how many are alive, cumulative
    i = 0
    cumalive_list = np.cumsum(list(alive_peryear.values()))
    for key, value in alive_peryear.items():
        cum_alive[key] = cumalive_list[i]
        i += 1
    percentile_amount = cumalive_list[-1] * .01 * (100 - percentile)
    for key, value in cum_alive.items():
        if cum_alive[key] >= percentile_amount:
            return 2017 - key

def get_expectedlife(name, gender, year): # get the expected percent of people alive with name given birth year
    fileyear = get_fileyear(year)
    filename = str(fileyear) + ' Life Table.csv'
    age = 2017 - year
    if age > 119:   # handle age over 119 exception
        return 0
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if int(row[0]) == age:
                if gender == 'M':
                    return int(row[1]) / 100000
                if gender == 'F':
                    return int(row[2]) / 100000

def get_fileyear(year): # given year, shows which life table to lookup
    if year < 1886: # handle years before 1886
        return 1900
    if year >= 1886 and year <= 1905:
        return 1900
    if year >= 1906 and year <= 1915:
        return 1910
    if year >= 1916 and year <= 1925:
        return 1920
    if year >= 1926 and year <= 1935:
        return 1930
    if year >= 1936 and year <= 1945:
        return 1940
    if year >= 1946 and year <= 1955:
        return 1950
    if year >= 1956 and year <= 1965:
        return 1960
    if year >= 1966 and year <= 1975:
        return 1970
    if year >= 1976 and year <= 1985:
        return 1980
    if year >= 1986 and year <= 1995:
        return 1990
    if year >= 1996 and year <= 2005:
        return 2000
    if year >= 2006 and year <= 2015:
        return 2010

def get_malenames(): # return all male names
    nf = open('malenames.txt', 'w')
    male_names = set()
    female_names = set()
    with open('usnames.txt') as f:
        for line in f:
            comma_indicies = []
            for i in range(len(line)):
                if line[i] == ',':
                    comma_indicies.append(i)
            name = line[comma_indicies[0]+1:comma_indicies[1]]
            gender = line[comma_indicies[1]+1:comma_indicies[2]]
            if gender == 'M':
                male_names.add(name)
            if gender == 'F':
                female_names.add(name)
    for name in male_names:
        nf.write(name + '\n')
    nf.close()
    return male_names

def get_femalenames(): # return all female names
    nf = open('femalenames.txt', 'w')
    male_names = set()
    female_names = set()
    with open('usnames.txt') as f:
        for line in f:
            comma_indicies = []
            for i in range(len(line)):
                if line[i] == ',':
                    comma_indicies.append(i)
            name = line[comma_indicies[0]+1:comma_indicies[1]]
            gender = line[comma_indicies[1]+1:comma_indicies[2]]
            if gender == 'M':
                male_names.add(name)
            if gender == 'F':
                female_names.add(name)
    for name in female_names:
        nf.write(name + '\n')
    nf.close()
    return female_names

def get_topmalenames(targetyear, number): # return top x male names from a given year
    filename = str(targetyear) + ' Top ' + str(number) + ' Male Names.txt'
    nf = open(filename, 'w')
    male_names = []
    entrynumber = 0
    with open('usnames.txt') as f:
        for line in f:
            comma_indicies = []
            for i in range(len(line)):
                if line[i] == ',':
                    comma_indicies.append(i)
            year = int(line[:comma_indicies[0]])
            name = line[comma_indicies[0]+1:comma_indicies[1]]
            gender = line[comma_indicies[1]+1:comma_indicies[2]]
            if year == targetyear and entrynumber < number:
                if gender == 'M':
                    male_names.append(name)
                    entrynumber += 1
    for name in male_names:
        nf.write(name + '\n')
    nf.close()
    return male_names

def get_topfemalenames(targetyear, number): # return top x female names from a given year
    filename = str(targetyear) + ' Top ' + str(number) + ' Female Names.txt'
    nf = open(filename, 'w')
    female_names = []
    entrynumber = 0
    with open('usnames.txt') as f:
        for line in f:
            comma_indicies = []
            for i in range(len(line)):
                if line[i] == ',':
                    comma_indicies.append(i)
            year = int(line[:comma_indicies[0]])
            name = line[comma_indicies[0]+1:comma_indicies[1]]
            gender = line[comma_indicies[1]+1:comma_indicies[2]]
            if year == targetyear and entrynumber < number:
                if gender == 'F':
                    female_names.append(name)
                    entrynumber += 1
    for name in female_names:
        nf.write(name + '\n')
    nf.close()
    return female_names
#get_namedata('Olivia', 'F')
#male_names = get_malenames()
#female_names = get_femalenames()
#test_m = get_topmalenames(2015, 1000)
#test_f = get_topfemalenames(2015, 1000)
get_namedata('Sydney', 'F')
#for m in test_m:
#    get_namedata(m, 'M')
#for f in test_f:
#    get_namedata(f, 'F')
