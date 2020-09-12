# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:23:30 2020

@author: Sathya
"""
##Import Libraries
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

##Constant Terms and Parameters
VOCAB_SIZE = 10000
EMBEDDING_DIM = 16
MAX_LENGTH = 200
TRUNC_TYPE='post'
PADDING_TYPE='post'
OOV_TOK = "<OOV>" #Out Of Vocabulary Handling
TRAIN_SIZE = 17000

##Load the json file
wget --no-check-certificate \
    "https://raw.githubusercontent.com/Coypirus/PoliticalDashboard/master/fake_news_json.json"
    -O /tmp/fake_news_json.json
    
    
##Load the JSON File Content and Store
with open("/tmp/fake_news_json.json", 'r') as filename:
    data_store = json.load(filename)

sentences = []
labels = []

for item in data_store:
    sentences.append(item['field_0'])##insert json keys here
    labels.append(item['field_1'])
    
train_sentences = sentences[0:TRAIN_SIZE]
test_sentences = sentences[TRAIN_SIZE:]
train_labels = labels[0:TRAIN_SIZE]
test_labels = labels[TRAIN_SIZE:]

##Assign Tokens for the words, and convert the sentences to token sequences.
tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token=OOV_TOK)
tokenizer.fit_on_texts(train_sentences)

wordIndex = tokenizer.word_index

train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = pad_sequences(train_sequences, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNC_TYPE)

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNC_TYPE)


#Convert to ndarrays
train_padded = np.array(train_padded)
train_labels = np.array(train_labels)
 
test_padded = np.array(test_padded)
test_labels = np.array(test_labels)

##The Neural Net Architechture
quacker = tf.keras.Sequential([
    tf.keras.layers.Embedding(VOCAB_SIZE, EMBEDDING_DIM, input_length=MAX_LENGTH),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid') #Activation test needed: Softmax vs Sigmoid
])
quacker.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])


NUM_EPOCHS = 30##Possibly change this

history = quacker.fit(train_padded, train_labels, epochs=NUM_EPOCHS, validation_data=(test_padded, test_labels), verbose=2 )

##The Actual Thing.
sentence = []
sentence = np.array(sentence, dtype = str)
sequences = tokenizer.texts_to_sequences(sentence)
padded = pad_sequences(sequences, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNC_TYPE)
print(quacker.predict(padded))