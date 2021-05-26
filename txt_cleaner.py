import langdetect
from langdetect import detect
import os
import demoji
from demoji import replace_with_desc
from demoji import replace


cleanfile = "filename_clean.txt"
noemojis = "filename_noemojis.txt"

def detect_lang(string):
    language = detect(string)
    return language


for filename in os.listdir(os.getcwd()):
    with open(os.path.join(os.getcwd(), filename), 'r', encoding="utf-8") as input:
    #only appends posts if they match the correct format provided by instascraper
        if "UTC" in filename:
            text = input.read()
    if len(text) == 0:
        continue
    try:
        lang = detect_lang(text)
    except:
        print("error")
    if lang == "en":
        demojified = replace_with_desc(text, sep='§')
        textonly = demoji.replace(text, repl = "")

    with open(cleanfile, "a", encoding="utf-8") as output_a:
        output_a.write(demojified)
        output_a.write("\n ;;; \n")
    with open(noemojis, "a", encoding= "utf-8") as output_b:
        output_b.write(textonly)
        output_b.write("\n ;;; \n")
