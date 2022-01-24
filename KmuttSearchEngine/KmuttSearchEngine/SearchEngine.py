from pythainlp.word_vector import WordVector
from pythainlp.tokenize import THAI2FIT_TOKENIZER
from KmuttSearchEngine.Query import *
from itertools import zip_longest, groupby
from KmuttSearchEngine.tfidf import *
from app.models import questionanswer
from pythainlp.spell import NorvigSpellChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from pythainlp.augment import *
import numpy as np
import oskut
import re
from scipy import spatial
import time

class return_Result:
  Retry = 0
  Correct = None
  code = ''
  query = ''
  percentage = ''
  ans = ''


def searchengine (search, query):

    Query=[]
    Query_Tokenized=[]
    Position = []
    location=[]
    percentage = []
    temp1=[]

    print(search);

    start = time.time()   

    Query = query.question

    dictionary = getDictionary()

    #======= spell check ========#
    result = spellCheck(search, dictionary)
    correct = result.correct
    tokenized = result.tokenized
    print (tokenized)

    #======= augment ========#
    augments = augment(tokenized)

    #======= remove stop words ========#
    removed_stopwords_Query,removed_stopwords_Final = stopwords(Query,augments)

    check = removed_stopwords_Final
    if check.count(check[0]) == len(check):
        print ("All the samee")
        removed_stopwords_Final = [check[0]]

    #============ TF-IDF ==============#

    removed_stopwords_Query_tfid,removed_stopwords_Final_tfid = tfidf(removed_stopwords_Query,removed_stopwords_Final) #TF-IDF

    #======= W2V process ========#

    answer = word2vector (removed_stopwords_Query_tfid , removed_stopwords_Final_tfid)

    pos = sorted(answer,reverse = True)
    pos = list(filter(lambda a: a != 0.0, pos))


    location = np.argsort(answer)[::-1]


    for j in range(len(pos)):
        temp = int(location[j])
        Position.append(temp+1) 
        temp2 = str("{:.2f}".format(pos[j]*100))
        percentage.append(temp2)
 
    
    temp1 = questionanswer.objects.filter(id__in=Position)

    temp1 = dict([(obj.id, obj) for obj in temp1])
    sorted_temp1 = [temp1[id] for id in Position]

    return_Result.query =  sorted_temp1

    end = time.time()   
    print ("Total Search: "+ str((end - start)))

    #======================================#

    if search != correct:
      return_Result.percentage = percentage
      return_Result.Correct = correct
      return (return_Result)
               
    else:
      return_Result.percentage = percentage
      retry = 0
      return_Result.Correct = None
      return_Result.Retry = 0
      return(return_Result)

#========================= Read Dictionary from file ===========================#
def getDictionary():

    with open("train.txt", 'r', encoding='UTF-8') as f:
        train = f.read().splitlines()

    return train

#=========================== Spell Check Part ================================#
def spellCheck(Input,train):

    start = time.time()

    class return_result:
        tokenized = []
        correct = []

    correct = ""

    start = time.time()
    oskut.load_model(engine='tl-deepcut-tnhc')
    tokenized = oskut.OSKut(Input,k=100)
    end = time.time()   
    print ("Spell check deepcut: "+ str((end - start)))

    checker_dataset = NorvigSpellChecker(custom_dict=train) #Using dict from dataset train
    #checker_ttc = NorvigSpellChecker(custom_dict=ttc.word_freqs()) #Using dict from pre data train

    for x in range(len(tokenized)):
        temp  = ""
        temp = checker_dataset.correct(tokenized[x])
        return_result.correct.append(temp)

    return_result.correct = ''.join(return_result.correct)

    return_result.tokenized = tokenized

    return return_result

#========================= Create Synonyms Sentence ===========================#
def augment(Input):

    start = time.time()

    aug = WordNetAug()
    final = []

    Output = aug.augment(Input, postag = True, max_syn_sent = 3 , postag_corpus='orchid', tokenize = 'Tokenized')
    for x in range(len(Output)):
        temp = "".join(Output[x])
        final.append(temp)
    
    Input = ''.join(Input)
    final.append(Input)

    if final.count(final[0]) == len(final):
        print ("All the samee")
        final = [Input]

    end = time.time()
    print ("Augment: "+ str((end - start)))

    return final

#========================= Word 2 Vector computation part ===========================#

def word2vector(Query,final):

    wv = WordVector()
    answer = []

    start = time.time()

    wv.load_wordvector("thai2fit_wv")

    v1 = [wv.sentence_vectorizer(i, use_mean=False) for i in Query]
    v2 = [wv.sentence_vectorizer(i, use_mean=False) for i in final]

    end = time.time()
    print ("w2v: "+ str((end - start)))

    temp = [(1 - spatial.distance.cosine(test1,test2)) for test1 in v1 for test2 in v2]

    def list_split(listA, n):
        for x in range(0, len(listA), n):
            every_chunk = listA[x: n+x]

            if len(every_chunk) < n:
                every_chunk = every_chunk + \
                    [None for y in range(n-len(every_chunk))]
            yield every_chunk

    temp = list(list_split(temp, len(final)))
    
    #  get the max value from the list of the answer #
    for x in temp:
        max_value = max(x)
        if max_value < 0.55:    
            max_value = 0.0
        answer.append(max_value)

    # use to dect if result found is 0 #
    if answer.count(answer[0]) == len(answer):   
        answer = [0,0]

    return answer


def train_dictionary(Query):
   
   print("Creating Dict")
   aug = WordNetAug()

   augmented = []
   train = []

   for x in range(len(Query)):  
       print (x)
       Question = re.sub('[a-zA-Z!#$()“”?/\0-9!@#$%^&*<>:;=]','',Query[x])
       augmented.append(Question)
     
   
   oskut.load_model(engine='ws-augment-60p')
   #oskut.load_model(engine='tl-deepcut-tnhc')

   for x in augmented:

        if x is '':
             x = 'Null';
        else:
            token = oskut.OSKut(x,k=100)
            for x in token:
                train.append(x)
                temp = aug.find_synonyms(x)
                for x in temp:
                  train.append(x)

   train = list(dict.fromkeys(train))
   check_train = 1

   with open('train.txt', 'w' , encoding="utf-8") as f:
        for item in train:
            f.write(item+"\n")
   f.close()

   return_Result.code = 300

   return (return_Result)

def stopwords (Query,final):

    start = time.time()

    removed_stopwords_Query = []
    removed_stopwords_Final = []

    f = open('stopwords_th.txt', 'r' , encoding="utf-8")
    words_list = f.read().splitlines()
    f.close()

    #oskut.load_model(engine='scads')
    tokenized_Query = tokenized(Query)
    tokenized_Final = tokenized(final)
    
    #Query = [x.split("|") for x in Query]
    #final = [x.split("|") for x in final]

    for word_query,word_final in zip_longest(tokenized_Query,tokenized_Final,fillvalue=None):

        temp = []

        if word_final is not None:

            temp = [word for word in word_query if not word in words_list]
            removed_stopwords_Query.append(temp)

            temp1 = [word for word in word_final if not word in words_list]
            removed_stopwords_Final.append(temp1)

        else:

            temp = [word for word in word_query if not word in words_list]
            removed_stopwords_Query.append(temp)


    end = time.time()
    print ("stopwords: "+ str((end - start)))
   
    return removed_stopwords_Query,removed_stopwords_Final

def stopwords1 (Query):

    removed_stopwords_Query = []

    f = open('stopwords_th.txt', 'r' , encoding="utf-8")
    words_list = f.read().splitlines()
    f.close()

    oskut.load_model(engine='scads')

    for x in Query:
        temp = []
        if x is '':
             x = 'Null';
        else:
            token = oskut.OSKut(x)
            temp = [word for word in token if not word in words_list]
            removed_stopwords_Query.append(''.join(temp))

    return removed_stopwords_Query


def tokenized (Query):

    tokenized_Query = []

    #oskut.load_model(engine='scads')

    for x in Query:
        temp = []
        if x is '':
             x = 'Null';
        else:
            token = THAI2FIT_TOKENIZER.word_tokenize(x)
            #tokenized_Query.append('|'.join(token))
            token = [x.strip(" ") for x in token if x.strip(" ")]
            
            tokenized_Query.append(token)
    
    return tokenized_Query

def tfidf (remove_sw_query, remove_sw_final):

    MAX_TFIDF = 0.121

    removed_stopwords_Query_tfid = []
    removed_stopwords_Final_tfid = []

    get_tfidf = get_tf_idf(remove_sw_query)

    for question,input_question in zip_longest(remove_sw_query,remove_sw_final):
    
        if input_question is not None:

            temp = [word for word in question if get_tfidf[word] > MAX_TFIDF]
            print(temp)
            removed_stopwords_Query_tfid.append(temp)

            temp1 = [word for word in input_question if get_tfidf.get(word, float(1)) > MAX_TFIDF]
            print (temp1)
            removed_stopwords_Final_tfid.append(temp1)

        else:
            temp = [word for word in question if get_tfidf[word] > MAX_TFIDF]
            print(temp)
            removed_stopwords_Query_tfid.append(temp)

    return (removed_stopwords_Query_tfid,removed_stopwords_Final_tfid)