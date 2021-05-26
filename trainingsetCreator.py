import csv
import re

nonMLMfile1 = "nonMLMclean.txt"
nonMLMfile2 = "BeautyBrandsClean.txt"
MLMfile = "MLMclean.txt"
trainingfile = "trainingset_all.csv"

fields = ["Text", "Tag"]

def removehashtags(data):
    data = re.sub(r'(#discoverunder2k)', "", data)
    data = re.sub(r'(#joinmeorwatchme)', "", data)
    data = re.sub(r'(#arbonne)', "", data)
    data = re.sub(r'(#monathair)', "", data)
    data = re.sub(r'(#younique)', "", data)
    data = re.sub(r'(#herbalifenutrition)', "", data)
    return data

with open(nonMLMfile1, "r", encoding ="utf-8") as input:
    nonMLMtxt = input.read().lower()
    nonMLMtxt = removehashtags(nonMLMtxt)

nonMLMposts = nonMLMtxt.split(";;;")

with open(nonMLMfile2, "r", encoding ="utf-8") as input:
    bbtxt = input.read().lower()
    bbtxt = removehashtags(bbtxt)

bbposts = bbtxt.split(";;;")

nonMLMposts.extend(bbposts)

with open(MLMfile, "r", encoding = "utf-8") as input:
    MLMtxt = input.read().lower()
    MLMtxt = removehashtags(MLMtxt)

MLMposts = MLMtxt.split(";;;")


with open(trainingfile, "w", encoding ="utf-8") as output:
    writer = csv.writer(output)
    writer.writerow(fields)
    for post in nonMLMposts:
        sublist = []
        sublist.append(post)
        #sublist.append("nonMLM")
        sublist.append(0)
        writer.writerow(sublist)
    for post in MLMposts:
        sublist = []
        sublist.append(post)
        #sublist.append("MLM")
        sublist.append(1)
        writer.writerow(sublist)
