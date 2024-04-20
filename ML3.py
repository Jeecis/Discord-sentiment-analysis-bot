""""I TESTED MY OWN TRAINED ML ALGORITHM HERE"""
#Due to high amount of bugs and only 25% accuracy it wasn't implemented



# import os
#
# import keras.src.legacy.preprocessing.text
# import pandas as pd
# import nltk
# from nltk.corpus import stopwords
# import random
# import matplotlib.pyplot as plt
# import seaborn as sns
# from collections import Counter
# from wordcloud import WordCloud
# from nltk.stem import PorterStemmer
# import numpy as np
# from keras.utils import to_categorical
# from sklearn.metrics import confusion_matrix
#
# import tensorflow as tf
# from keras.src.legacy.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from keras.layers import Embedding, LSTM, Dense, Bidirectional
# from keras.models import Sequential
# from keras.optimizers import Adam
# from keras.regularizers import l2
#
# val_data=pd.read_csv("EmotionRecognition/validation.csv")
# train_data=pd.read_csv("EmotionRecognition/training.csv")
#
# vocab_size = 16000
# embedding_dim = 16
# max_length = 66
# trunc_type='post'
# padding_type='post'
# oov_tok = "<OOV>"
# training_size = 16000
#
# test_data=pd.read_csv("EmotionRecognition/test.csv")
#
# print("Val data: ",val_data.shape)
# print("train data: ",train_data.shape)
# print("test data: ",test_data.shape)
#
# # print(train_data.head(10))
#
# # labels={0: "sadness", 1:"joy", 2:"love", 3:"anger", 4:"fear", 5:"surprise"}
# training_labels=train_data["label"].tolist()
# val_labels=val_data["label"].tolist()
# test_labels=test_data["label"].tolist()
#
#
# # print(train_data.groupby(["label","label_name"]).size())
#
# ## visualisation
#
# # plt.figure()
# # train_data["label_name"].value_counts().plot(kind='bar', color=['yellow', 'blue','red','green','orange','cyan'])
# # plt.show()
#
# ## Data cleaning
# # print(train_data.isnull().sum())
# # print(test_data.isnull().sum())
# # print(val_data.isnull().sum())
#
# ## TODO if data isnt clean fix it
#
# ## Tokenization and stemming
# sentences=train_data["text"].tolist()
# tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
# tokenizer.fit_on_texts(sentences)
# word_index=tokenizer.word_index
#
# sequences=tokenizer.texts_to_sequences(sentences)
# training_padded=pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)
#
# val_sentences=val_data["text"].tolist()
# sequences2=tokenizer.texts_to_sequences(val_sentences)
# val_padded=pad_sequences(sequences2, maxlen=max_length, padding=padding_type, truncating=trunc_type)
#
# test_sentences=val_data["text"].tolist()
# sequences3=tokenizer.texts_to_sequences(test_sentences)
# test_padded=pad_sequences(sequences3, maxlen=max_length, padding=padding_type, truncating=trunc_type)
#
#
# training_padded = np.array(training_padded)
# training_labels = np.array(training_labels)
# val_padded = np.array(val_padded)
# val_labels = np.array(val_labels)
# test_padded = np.array(test_padded)
# test_labels = np.array(test_labels)
#
# print(training_padded[3])
# print(training_labels[3])
# print(val_padded[3])
# print(val_labels[3])
#
# from keras.layers import Flatten
#
# model = Sequential()
# model.add(Embedding(16000, 100))
# model.add(Bidirectional(LSTM(150)))
# model.add(Dense(6, activation='softmax'))
# adam = Adam(learning_rate=0.01)
# model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
# # model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
#
# from keras.utils import to_categorical
#
# # Assuming num_classes is the number of unique classes in your dataset
# num_classes = 6
#
# # Convert target labels to one-hot encoded format
# training_labels_one_hot = to_categorical(training_labels, num_classes=num_classes)
# val_labels_one_hot = to_categorical(val_labels, num_classes=num_classes)
# test_labels_one_hot = to_categorical(test_labels, num_classes=num_classes)
#
# nepochs=1
# history = model.fit(training_padded, training_labels_one_hot, epochs=nepochs, validation_data=(val_padded, val_labels_one_hot), verbose=2)
# # keras.saving.save_model("newModel.keras","C:\\Users\\jekab\\PycharmProjects", overwrite=True)
# # tf.saved_model.save(model,"C:\\Users\\jekab\\PycharmProjects")
#
# # tf.saved_model.save(model, "newModel.h5")
#
# # new_model = keras.layers.TFSMLayer("newModel.h5", call_endpoint='serving_default')
# # new_model=model
# sentence = ["im feeling rather rotten so im not very ambitious right now", "im updating my blog because i feel shitty","i cant walk into a shop anywhere where i do not feel uncomfortable","i find myself in the odd position of feeling supportive of"]
# sequences = tokenizer.texts_to_sequences(sentence)
# padded = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)
# np.set_printoptions(suppress=True)
# # predictions=new_model.predict(padded)
# # predicted_labels = np.argmax(predictions, axis=1)
# # print(predicted_labels)
# # correct_predictions = (predicted_labels == [0,0,4,2])
# # accuracy = np.mean(correct_predictions)
#
# predictions=model.predict(test_padded)
# print(predictions)
# predicted_labels = np.argmax(predictions, axis=1)
# print(predicted_labels)
# correct_predictions = (predicted_labels == test_labels)
# accuracy = np.mean(correct_predictions)
#
# print("Accuracy:", accuracy)