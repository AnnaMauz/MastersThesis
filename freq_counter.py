import string
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import word_tokenize
import re, nltk, csv, json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize as tokenize
from nltk.stem import WordNetLemmatizer as lemmatize
from collections import Counter
from nltk.util import ngrams
from nltk.corpus import stopwords
import gensim
import spacy


stop_words = set(stopwords.words('english'))

#adding frequent contractions to stopwords, including different types of apostrophes
stop_words.update(("it's","it’s", "i'm", "i’m", "i've","i’ve","you're", "you’re", "that's","that’s", "don't","don’t", "can’t", "would"))


# inputfile1 = "MLMclean.txt"
# inputfile2 = "MLMnoemojis.txt"
#
# emoji_output = "Emoji_CountMLM.json"
# hashtag_output = "Hashtag_CountMLM.json"
# token_output = "Cleantokens_MLM.json"
# nohashtags_output = "Nohashtags_MLM.json"
# nostopwords_output = "Nostopwords_MLM.json"
# unigrams_output = "UnigramsMLM.json"
# bigrams_output = "BigramsMLM.json"
# trigrams_output = "TrigramsMLM.json"
# tetragrams_output = "TetragramsMLM.json"
# misc_frequencies = "TermFreqMLM.json"

# inputfile1 = "nonMLMclean.txt"
# inputfile2 = "nonMLMnoemojis.txt"
#
# emoji_output = "Emoji_CountNonMLM.json"
# hashtag_output = "Hashtag_CountNonMLM.json"
# token_output = "Cleantokens_nonMLM.json"
# nohashtags_output = "Nohashtags_nonMLM.json"
# nostopwords_output = "Nostopwords_nonMLM.json"
# unigrams_output = "UnigramsNonMLM.json"
# bigrams_output = "BigramsNonMLM.json"
# trigrams_output = "TrigramsNonMLM.json"
# tetragrams_output = "TetragramsNonMLM.json"
# misc_frequencies = "TermFreqNonMLM.json"

inputfile1 = "BeautyBrandsClean.txt"
inputfile2 = "BeautyBrandsnoemojis.txt"

emoji_output = "Emoji_CountBB.json"
hashtag_output = "Hashtag_CountBB.json"
token_output = "Cleantokens_BB.json"
nohashtags_output = "Nohashtags_BB.json"
nostopwords_output = "Nostopwords_BB.json"
unigrams_output = "UnigramsBB.json"
bigrams_output = "BigramsBB.json"
trigrams_output = "TrigramsBB.json"
tetragrams_output = "TetragramsBB.json"
misc_frequencies = "TermFreqBB.json"



#removes punctuation from tokens
def clean(rawtokens):
    cleantokens = []
    punctuation = r'[!?.,•;…:-_~*"()%&=+\/-]'
    for token in rawtokens:
        #deletes specific punctuation
        newstring = re.sub(punctuation, "", token)
        #checks for presence of any alphanumeric character
        chkalphanum = re.search("\w", newstring)
        #if string contains at least one alphanumeric character, it is appended to cleantokens
        #this is to avoid empty strings and stray punctuation
        if chkalphanum != None:
            cleantokens.append(newstring)
    return cleantokens


#count emojis only
with open(inputfile1, encoding='utf-8') as input:
    text = input.read()
text = re.sub("§§", "§ §", text)
posts = text.split(";;;")
itemamount = len(posts)
print("Amount of analyzed posts: "+ str(itemamount))
wssplit = text.split()
emojis = []
#counts the amount of times a price is mentioned by counting tokens that include a dollar sign
price = 0
for string in wssplit:
    if "§" in string:
        emojis.append(string)
    if "$" in string:
        price +=1
    elif "€" in string:
        price += 1
    elif "£" in string:
        price += 1

print("Amount of tokens that contain a currency sign: " + str(price))

emojicount = Counter(emojis)

print("Token frequency of all emojis: " + str(len(emojis)))


with open(emoji_output, "w", encoding='utf-8') as output:
    #output.write(str(emojicount.most_common(100)))
    emojis_top = emojicount.most_common(100)
    i = 0
    for item in emojis_top:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #json.dump(emojicount.most_common(100), output, indent=1)

#count hashtags only
hashtags = []
for string in wssplit:
    if "#" in string:
        hashtags.append(string)
hashtagcount = Counter(hashtags)
with open(hashtag_output, "w", encoding='utf-8') as output:
    #output.write(str(hashtagcount.most_common(200)))
    json.dump(hashtagcount.most_common(200), output, indent=1)



#tokenize (text without emojis)
with open(inputfile2, encoding = "utf-8") as textonly:
    text = textonly.read()
    text = text.lower()
    rawtokens = text.split()
    cleantokens = clean(rawtokens)

# with open(token_output, "w", encoding = "utf-8") as output:
#     #output.write(str(cleantokens))
#     json.dump(cleantokens, output)

#filter hashtags from tokens
tokens_nohashtags = []
for token in cleantokens:
    if "#" not in token:
        tokens_nohashtags.append(token)
token_numbers = len(tokens_nohashtags)
unique_tokens = set(tokens_nohashtags)
print("Total number of tokens without hashtags and emojis: "+str(token_numbers))
print("Total number of unique tokens without hashtags and emojis: " + str(len(unique_tokens)))
# with open(nohashtags_output, "w", encoding = "utf-8") as output:
#     #output.write(str(tokens_nohashtags))
#     json.dump(tokens_nohashtags, output)
#filter stopwords from tokens
tokens_nostopwords = []
for token in tokens_nohashtags:
    if token not in stop_words:
        tokens_nostopwords.append(token)
#with open(nostopwords_output, "w", encoding = "utf-8") as output:
#    #output.write(str(tokens_nostopwords))
#    json.dump(tokens_nostopwords, output)

#count frequencies of certain terms:
freq_list = ["boss babe", "bossbabe", "momboss", "bossmom", "ladyboss", "bosslady", "mompreneur", "goal digger", "goaldigger", "gogetter", "go-getter", "girlpower", "empower", "empowering", "feminism"]

with open (misc_frequencies, "w", encoding = "utf-8")as output:
    for word in freq_list:
        word_freq = text.count(word)
        print("Frequency for word " + word + " : " + str(word_freq))
        print("Frequency for word " + word + " : " + str(word_freq), file =output)




#count n-grams
#unigrams / Bag-of-Words
unigrams = Counter(tokens_nostopwords)
with open (unigrams_output, "w", encoding = "utf-8") as output:
    unigrams_top = unigrams.most_common(150)
    i = 0
    for item in unigrams_top:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #output.write(str(unigrams.most_common(150)))
    #json.dump(unigrams.most_common(150), output)

#bigrams
bigrams = ngrams(tokens_nostopwords, 2)
bigrams_freq = Counter(bigrams)

with open (bigrams_output, "w", encoding = "utf-8") as output:
    bigrams_top = bigrams_freq.most_common(150)
    i = 0
    for item in bigrams_top:
        i +=1
        print(str(i) + ". " + str(item), file = output)

    #output.write(str(bigrams_freq.most_common(150)))
    #json.dump(bigrams_freq.most_common(150), output)



trigrams = ngrams(tokens_nostopwords, 3)
trigrams_freq = Counter(trigrams)

with open (trigrams_output, "w", encoding = "utf-8") as output:
    trigrams_top = trigrams_freq.most_common(125)
    i = 0
    for item in trigrams_top:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #output.write(str(trigrams_freq.most_common(100)))
    #json.dump(trigrams_freq.most_common(125), output)

#tetragrams
tetragrams = ngrams(tokens_nostopwords, 4)
tetragrams_freq = Counter(tetragrams)

with open (tetragrams_output, "w", encoding = "utf-8") as output:
    tetragrams_top = tetragrams_freq.most_common(100)
    i = 0
    for item in tetragrams_top:
        i +=1
        print(str(i) + ". " + str(item), file = output)
    #output.write(str(tetragrams_freq.most_common(100)))
    #json.dump(tetragrams_freq.most_common(100), output)
