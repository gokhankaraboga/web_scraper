import csv

gundem_links = []
yorum_links = []
with open('/Users/gokhankaraboga/Desktop/socrates_gundem.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        gundem_links.append(row[3])

with open('/Users/gokhankaraboga/Desktop/socrates_yorum.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        yorum_links.append(row[3])

print set(yorum_links) - set(gundem_links)
