
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 03:47:29 2020
@author: sathya
"""

##Imports
import pandas as pd
import numpy as np
from sklearn import model_selection
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

##Constants
VOCAB_SIZE = 100000
EMBEDDING_DIM = 16
MAX_LENGTH = 200
TRUNC_TYPE='post'
PADDING_TYPE='post'
OOV_TOK = "<OOV>" #Out Of Vocabulary Handling
TRAIN_SIZE = 15542

##Data Loading and Preprocessing
Train = pd.read_csv("train.csv")

Train = Train.dropna()
Train = Train.copy()
Train.reset_index(inplace = True)
x = Train['title']
y = Train['label']
x = np.array(x)
y = np.array(y)
train_sentences, test_sentences, train_labels, test_labels = model_selection.train_test_split(x, y, test_size = 0.15, random_state=101)
    
train_sentences = np.array(train_sentences)
test_sentences = np.array(test_sentences)
train_labels = np.array(train_labels)
test_labels = np.array(test_labels)

tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token=OOV_TOK)
tokenizer.fit_on_texts(train_sentences)
wordIndex = tokenizer.word_index

train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = pad_sequences(train_sequences, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNC_TYPE)

test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNC_TYPE)

