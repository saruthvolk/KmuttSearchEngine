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

def get_tf_idf (sentences):

    vectors = []
    i = 0
    start = time.time()

    tfidf = defaultdict(dict)

    word_set = [word for question in sentences for word in question]
    total_documents = len(sentences)

    #index_dict = {} #Dictionary to store index for each word
    #i = 0
    #for word in word_set:
    #    index_dict[word] = i
    #    i += 1
    #print (index_dict)
    
    word_count = count_dict(sentences,word_set)

    tf_idf_vec = np.zeros((len(word_set),))
    tf_idf_sentence_value = []
    
    index_sentence = {}
    for sent in sentences:
        i += 1
        index_sentence[tuple(sent)] = i
        tf_idf_sentence_value = []
        for word in sent:
            tf = termfreq(sent,word)
            idf = inverse_doc_freq(word,total_documents,word_count)

            value = tf*idf
            #tf_idf_sentence_value.append(value)
            #if (tfidf.get(word,value) != value):
            #    temp = tfidf[word]
            #    temp2 = value + temp
            #    tfidf[word] = temp2
            #tfidf[i][word] = value
            #else:
            tf_idf_sentence_value.append(value)

        tfidf[i] = tf_idf_sentence_value
        
    #sorted_tfidf = dict(sorted(tfidf.items(), key=operator.itemgetter(1),reverse=True))
       
    #print (sorted_tfidf)

    #for word in tfidf:
    #    tfidf_value = tfidf[word]
    #    occurance = word_count[word]
    #    value = tfidf_value/occurance
    #    tfidf[word] = value
            #print ("word:"+ str(word) + "value:"+ str(value))

            #tf_idf_vec[index_dict[word]] = value 

        #vectors.append(tf_idf_vec)

    #sorted_tfidf = dict(sorted(tfidf.items(), key=operator.itemgetter(1),reverse=True))
    #print (sorted_tfidf )
 
    end = time.time()
    print ("TFIDF: "+ str((end - start)))

    return (tfidf, index_sentence) 

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



























'''
def identity_fun(text):

        print (text)

        return text

def identity_fun1(text):
    
    text1 = []
    for x in text:
        temp = x.split(", ")
        text1.append(temp)
    print ("tfidf"+str(text))

    return text

def get_tf_idf (sentences, query):


        tfidf_vectorizer = TfidfVectorizer(analyzer = 'word', #this is default
                                   tokenizer= identity_fun1, #does no extra tokenizing
                                   preprocessor=identity_fun, #no extra preprocessor
                                   token_pattern=None)
        #สุ่มช่วงของ 5 เอกสารที่ติดกันมาทดลองใช้งาน
        tfidf_vector= tfidf_vectorizer.fit_transform(sentences)
        tfidf_query_vector = tfidf_vectorizer.transform(query[len(query)-1])

        tfidf_query_array = np.array(tfidf_query_vector.todense())
        tfidf_array = np.array(tfidf_vector.todense())

        result = [(cosine_similarity(test2,test1)).flatten() for test1 in tfidf_query_vector for test2 in tfidf_vector]

        print(result)
'''

'''
    vectors = []
    start = time.time()

    tfidf = {}
    word_set = [word for question in sentences for word in question]
    total_documents = len(sentences)

    #index_dict = {} #Dictionary to store index for each word
    #i = 0
    #for word in word_set:
       # index_dict[word] = i
       # i += 1
    
    word_count = count_dict(sentences,word_set)

    #tf_idf_vec = np.zeros((len(word_set),))

    for sent in sentences:
        for word in sent:

            tf = termfreq(sent,word)
            idf = inverse_doc_freq(word,total_documents,word_count)
         
            value = tf*idf
            
            #if (tfidf.get(word,value) != value):
            #    temp = tfidf[word]
            #    temp2 = value + temp
            #    tfidf[word] = temp2

            #else:
            tfidf[word] = value
        print ("["+ str(sent)+"]")
        sorted_tfidf = dict(sorted(tfidf.items(), key=operator.itemgetter(1),reverse=True))
       
        print (sorted_tfidf)
    #for word in tfidf:
    #    tfidf_value = tfidf[word]
    #    occurance = word_count[word]
    #    value = tfidf_value/occurance
    #    tfidf[word] = value
            #print ("word:"+ str(word) + "value:"+ str(value))

            #tf_idf_vec[index_dict[word]] = value 

        #vectors.append(tf_idf_vec)

    #sorted_tfidf = dict(sorted(tfidf.items(), key=operator.itemgetter(1),reverse=True))
    #print (sorted_tfidf )
    #print (vectors )

    end = time.time()
    print ("TFIDF: "+ str((end - start)))

    return vectors 

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
'''