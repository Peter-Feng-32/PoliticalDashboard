from flask import render_template, request, jsonify, Flask
from app import app
from app import textscraper
import nltk.data

#ML Imports
import os
import tensorflow as tf
import numpy as np
import pandas as pd
import json
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


@app.route('/')
@app.route('/index')
@app.route('/home')
@app.route('/home.html')
def home():
    return render_template('home.html')


#Fake news detection with ML model
@app.route("/bd", methods=['GET', 'POST'])
def bd():

    def list_sequencer(str_list):
        sequences = tokenizer.texts_to_sequences(str_list)
        padded = pad_sequences(sequences, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNC_TYPE)
        return padded

    #ML Model constants
    VOCAB_SIZE = 10000
    EMBEDDING_DIM = 16
    MAX_LENGTH = 200
    TRUNC_TYPE='post'
    PADDING_TYPE='post'
    OOV_TOK = "<OOV>" #Out Of Vocabulary Handling
    TRAIN_SIZE = 17000

    text_df = pd.read_json("https://raw.githubusercontent.com/Coypirus/PoliticalDashboard/master/fake_news_json.json")
    text_df = text_df.drop(['field_1'], axis = 1)

    numpy_texts = text_df.to_numpy()
    text_list = numpy_texts.tolist()
    text_list = text_list[0:TRAIN_SIZE]
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token=OOV_TOK)
    tokenizer.fit_on_texts(text_list)

    wordIndex = tokenizer.word_index

    if request.method == 'POST':
        nltk.download('punkt')
        try:
            #Turn string into list
            myText = textscraper.text_from_html(request.form.get('url'))
            myList = nltk.tokenize.sent_tokenize(myText)

            my_model = tf.keras.models.load_model('FakeDetection.h5')
            vals = []
            vals.append(my_model.predict(list_sequencer(myList)))

            #Add cumulative scores here.
            ## Full Page Evaluation

            sentence_predictions = []

            for i in range(0, len(vals[0])):
 
                if(vals[0][i] >= 0.9):
                    sentence_predictions.append(1)
                else:
                    sentence_predictions.append(0)
            
            
            final_preds = np.array(sentence_predictions)

            good = 0
            bad = 0

            for val in final_preds:

                if (val==1):
                    bad+=1
                else:
                    good+=1

            print(good)
            print(bad)
            if (good>bad):
                output = "Real News"
            else:
                output = "Fake News"

            return render_template("bd.html", hasData=True, output=output)

        except Exception as e:
            message = "Please enter a correct value!"
            print(e)
            return render_template("bd.html", hasData = True, output=message)
 
    
    return render_template("bd.html", hasData=False)


@app.route('/tips')
def tips():
    return render_template("tips.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/impdates')
def impdates():
    return render_template("impdates.html")

@app.route('/tweets')
def tweets():
    return render_template("tweets.html")

@app.route('/pn')
def pn():
    return render_template("pn.html")

#Sidebar is loaded in on each page
@app.route('/sidebar')
def sidebar():
    return render_template("sidebar.html")

@app.route('/footer')
def footer():
    return render_template("footer.html")
