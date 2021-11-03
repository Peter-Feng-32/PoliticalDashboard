
##Imports
from newspaper import Article
import nltk
nltk.download('punkt')
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

##Constants
MAX_LENGTH = 100 ##Specify
PADDING_TYPE = 'post'
TRUNC_TYPE = 'post'

##Loading the tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

def content_sequencer(content_list):
    content_sequences = tokenizer.texts_to_sequences(str_list)
    content_padded = pad_sequences(content_sequences, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNC_TYPE)
    return content_padded
def deep_search(URL):
    article = Article(URL, 'en')
    article.download()
    article.parse()
    article.nlp()
    content = article.summary.replace("\n","").replace('"',"").replace("?","").replace(",","").split(".")
    for string in content:
        if(len(string)<10):
            content.remove(string)
    print(content)

def basic_search(URL):
    article = Article(URL, 'en')
    article.download()
    article.parse()
    article.nlp()
    content = article.text.replace("\n","").replace('"',"").replace("?","").replace(",","").split(".")
    for string in content:
        if(len(string)<10):
            content.remove(string)
    print(content)

def main():
    URL = input("Enter news source URL: ")
    print("Choose Between Deep Search and Basic Search")
    print("     1. Deep Search")
    print("     2. Basic Search")
    choice = input("Enter Choice: ")
    if (choice==1):
        deep_search(URL)
    else:
        basic_search(URL)
if __name__ == "__main__":
    main()
    