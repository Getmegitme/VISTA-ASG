import csv

with open("D:\\My_Python\\VISTA-ASG\\Python learning\\product.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)