import csv


HEADER = ["x", "y"]

with open("data.csv", "a") as f:
    w = csv.writer(f)
    w.writerow(HEADER)
