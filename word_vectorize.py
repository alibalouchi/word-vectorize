from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors
import numpy as np
import csv
from nltk.stem import PorterStemmer
import sys
import gensim.downloader as api
import pickle
import enchant

enchant_dict = enchant.Dict("en_US") 

model = api.load("glove-wiki-gigaword-50")

# glove_input_file = '../model/glove.6B.100d.txt'
# word2vec_output_file = 'glove.6B.100d.txt.word2vec'
# glove2word2vec(glove_input_file, word2vec_output_file)
# filename = 'glove.6B.100d.txt.word2vec'
# model = KeyedVectors.load_word2vec_format(filename)

keywords = open("./keywords", mode='rb')
keywords_dict = pickle.load(keywords)

# print(keywords_dict)
ps = PorterStemmer()

movies_vector_dict = {}
for movie in keywords_dict.keys():
    vectors = []
    for word in keywords_dict[movie]:
        if type(word) is tuple:
            lower_word = word[0].lower()
            if enchant_dict.check(lower_word) == True:
                try:
                    word_vector = model.word_vec(lower_word)
                    vectors.append(word_vector)
                except KeyError:
                    try:
                        new_words = lower_word.split("-")
                        for item in new_words:
                            vectors.append(model.word_vec(item))
                    except:
                        print("not in vocab", lower_word)
                        continue
            else:
                try:
                    word_vector = model.word_vec((enchant_dict.suggest(lower_word)[0]).lower())
                    vectors.append(word_vector)
                except KeyError:
                    continue
                except IndexError:
                    continue
        else:
            lower_word = word.lower()
            if enchant_dict.check(lower_word) == True:
                word_vector = model.word_vec(lower_word)
                vectors.append(word_vector)
            else:
                word_vector = model.word_vec((enchant_dict.suggest(lower_word)[0]).lower())
                vectors.append(word_vector)
    if len(vectors) > 1:
        movies_vector_dict[movie] = list(np.mean(vectors, axis=0))
    elif len(vectors) == 1:
        movies_vector_dict[movie] = vectors[0]
    else:
        print("vectors",vectors)
        continue

new_csv = csv.writer(open("new_csv.csv", mode="a"))
new_csv.writerow(["imdb_id","movie_vector"])
for movie in movies_vector_dict.keys():
  new_csv.writerow([movie, movies_vector_dict[movie]])