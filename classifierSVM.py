import csv
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from pprint import pprint


trainingfile = "trainingset_all.csv"


#testfile = "kp_testset_MLM.txt"
#testfile = "dp_testset_nonMLM.txt"
#testfile = "exa_testset_antimlm.txt"
#testfile = "testsetMLMclean.txt"
testfile = "testsetnonMLMclean.txt"
#testfile = "testset.txt"
outputfile = "Results_classifierSVM.txt"


with open (testfile, encoding = "utf-8") as input:
    data = input.read().lower()
data = re.sub(r'(#discoverunder2k)', "", data)
data = re.sub(r'(#joinmeorwatchme)', "", data)
data = re.sub(r'(#arbonne)', "", data)
data = re.sub(r'(#monathair)', "", data)
data = re.sub(r'(#younique)', "", data)
data = re.sub(r'(#herbalifenutrition)', "", data)


testposts = data.split(";;;")

#testpost = """ """


posts = []

labels = []

with open(trainingfile, encoding='utf-8') as input:
    csvread = csv.DictReader(input)
    for row in csvread:
        post = row["Text"]
        posts.append(post)
        #0 is for non-MLM, 1 is for MLM
        label = row["Tag"]
        labels.append(label)




bow_vectorizer = CountVectorizer()

post_vectors = bow_vectorizer.fit_transform(posts)

#Support Vector Machine
classifierSVM = SVC()

classifierSVM.fit(post_vectors, labels)



resultsSVM = []



for testpost in testposts:
    test_vector = bow_vectorizer.transform([testpost])
    predictionSVM = [classifierSVM.predict(test_vector)]
    resultSVM = predictionSVM[0] if predictionSVM[0] else "unclear"
    resultsSVM.append(resultSVM)


#pprint(resultsSVM)

i=0
postid = 1

MLMcount = 0
nonMLMcount = 0
undeterminedcount = 0


postamount = len(testposts)

with open(outputfile, "w", encoding ="utf-8") as output:
    print("Classification results for file: " + testfile, file = output)
    print("Amount of posts analyzed: %d \n" % postamount, file = output)
    #for post in posts:
    while i < postamount:
        print("\n \n Post Nr. %d \n" % postid, file = output)
        print(testposts[i], file = output)
        print("\n Classification result for Post Nr. %d: " % postid, file = output)
        result = resultsSVM[i][0]
        print(result, file = output)
        resultint = int(result)
        if resultint == 0:
            print("non-MLM", file = output)
            nonMLMcount += 1
        elif resultint == 1:
            print("MLM", file = output)
            MLMcount += 1
        else:
            print("undetermined", file = output)
            undeterminedcount += 1
        i+=1
        postid+=1
    print("\n \n Amount of undetermined posts: " + str(undeterminedcount), file = output)
    mlmpercentage = MLMcount / postamount * 100
    nonmlmpercentage = nonMLMcount / postamount * 100
    print("Amount of posts classified as MLM posts: " + str(MLMcount) + " (%d percent)" % mlmpercentage, file =output )
    print("Amount of posts classified as non-MLM posts: " + str(nonMLMcount) + "(%d percent)" % nonmlmpercentage, file = output)

#Brief summary to be printed to the console
print("Classification results for file: " + testfile)
print("Amount of posts analyzed: %d" % postamount)
print("Amount of undetermined posts: " + str(undeterminedcount))
print("Amount of posts classified as MLM posts: " + str(MLMcount) + " (%d percent)" % mlmpercentage)
print("Amount of posts classified as non-MLM posts: " + str(nonMLMcount) + "(%d percent)" % nonmlmpercentage)
