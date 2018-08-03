import csv

f = open('cols.txt', 'r')
lines = [l.strip() for l in f.readlines()]
f.close()


cols = []
cols.append(lines[0])
for i in range(1,len(lines)-1):
    cols.append(lines[i])

ignore = [0,2,18,26]
with open('OrdersDataFrame.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        csv_cols = row
        break

for i in range(len(csv_cols)):
    if i not in ignore:
        cols.append(csv_cols[i])

cols.append(lines[-1])
print(len(cols))
for i in range(len(cols)):
    print("%i %s" % (i, cols[i]))
