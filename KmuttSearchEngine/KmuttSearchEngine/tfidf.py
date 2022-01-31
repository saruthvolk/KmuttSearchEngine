import numpy as np
import string
import operator
import math
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from collections import defaultdict
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_tf_idf (sentences,final):

    vectors = []
    i = 0

    tfidf = defaultdict(dict)
    user_tfidf = defaultdict(dict)

    word_set = [word for question in sentences for word in question]
    total_documents = len(sentences)
    index_sentence = {}
   
    word_count = count_dict(sentences,word_set)
    
    index_sentence = {}
    for sent in sentences:
        i += 1
        index_sentence[i] = tuple(sent)
        tf_idf_sentence_value = []
        for word in sent:
            tf = termfreq(sent,word)
            idf = inverse_doc_freq(word,total_documents,word_count)

            value = tf*idf

            tf_idf_sentence_value.append(value)

        if (i >= (len(sentences)-len(final))+1):
            user_tfidf[i] = tf_idf_sentence_value
        else:
            tfidf[i] = tf_idf_sentence_value
        
 
    return (tfidf, index_sentence, user_tfidf) 

def count_dict(sentences,word_set):

    word_count = Counter(word_set)

    return word_count

def termfreq(document, word):

    N = len(document)

    occurance = len([token for token in document if token == word])

    tf = occurance/N

    return tf

def inverse_doc_freq(word,total_documents,word_count):

    try:
        word_occurance = word_count[word] + 1
    except:
        word_occurance = 1
    
    idf = np.log(total_documents/word_occurance)

    return idf
