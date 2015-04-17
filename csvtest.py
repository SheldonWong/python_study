import csv  
  
FIELDS = ['Name', 'Sex', 'E-mail', 'Blog']  
  
# DictWriter  
csv_file = open('d:/test.csv', 'r+')  
writer = csv.DictWriter(csv_file, fieldnames=FIELDS)  
# write header  
writer.writerow(dict(zip(FIELDS, FIELDS)))  
  
d = {}  
d['Name'] = 'Qi'  
d['Sex'] = 'Male'  
d['E-mail'] = 'redice@163.com'  
d['Blog'] = 'http://www.redicecn.com'  
  
writer.writerow(d)
print("success")
csv_file.close()

for d in csv.DictReader(open('test.csv', 'r+')):  
    print(d)

