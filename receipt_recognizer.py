import re
import en_core_web_md
import nltk
import pytesseract
import spoonacular as sp
from nltk.corpus import brown
from PIL import Image

brown = brown.words(categories=brown.categories())
nlp = en_core_web_md.load()
foogoo = sp.API("18b4d68fbd11492f8ac5fd4c771d2b44")


def preprocess(text):
    text = re.sub(r'[0-9]', '', text)
    text = re.sub(r'[\@\.\!\?\:\,\"\/\\\#\%\[\]\^\_\&\'\(\)\+\-\|\~\;\=\^\*]', '', text)
    tokens_text = nltk.word_tokenize(text)
    new_string = []
    for word in tokens_text:
        if word in brown or len(word) > 2:
            new_string.append(word)
    return " ".join(new_string)


def get_ingredient_receipt(img_path):
    image_file = Image.open(img_path)
    tess = pytesseract.image_to_string(image_file)
    new_list = []
    final_list = []
    for item in list(set(tess.split("\n"))):
        new_list.append(preprocess(item))
    for word in new_list:
        if 'TARE' not in word and 'ITEM' not in word and len(word) > 2:
            final_list.append(word)
    text = "\n".join(list(set(final_list)))
    print(text)
    response = foogoo.parse_ingredients(text)
    data = response.json()
    list_ing = [data[i]["name"] for i in range(len(data))]
    return list_ing
