from pythainlp.word_vector import WordVector
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import ttc
from KmuttSearchEngine.Query import *
from app.models import questionanswer
from django.db import models
from pythainlp.spell import NorvigSpellChecker
from pythainlp.augment import *
import numpy as np
import oskut
import re
import math
from scipy import spatial

class return_Result:
  Retry = 0
  Correct = None
  query = ''
  percentage = ''
  ans = ''


def searchengine (search, query):

    Query=[]
    Position = []
    Answer = []
    location=[]
    percentage = []
    temp1=[]
    retry = 0
    aug = WordNetAug()

    Query = query.question
    dictionary = getDictionary()
    correct = spellCheck(search, dictionary)
    augments = augment(search)
    answer = word2vector (Query,augments)

    pos = sorted(answer,reverse = True)
    location = np.argsort(answer)[::-1]
    print ("\nQuestion: "+ search+ "\n")
    print ("Result:")
    for j in range(len(location)):
        temp = int(location[j])
        Position.append(temp+1)
        temp2 = str("{:.2f}".format(pos[j]*100))
        percentage.append(temp2)

    temp1 = questionanswer.objects.filter(id__in=Position)

    temp1 = dict([(obj.id, obj) for obj in temp1])
    sorted_temp1 = [temp1[id] for id in Position]

    return_Result.query =  sorted_temp1

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

#========================= Spell Check Part ===========================#
def spellCheck(Input,train):

    correct = ""
    oskut.load_model(engine='scads')
    token = oskut.OSKut(Input)
    print(token)

    checker_dataset = NorvigSpellChecker(custom_dict=train) #Using dict from dataset train
    checker_ttc = NorvigSpellChecker(custom_dict=ttc.word_freqs()) #Using dict from pre data train

    for x in range(len(token)):
        temp  = ""
        temp = checker_dataset.correct(token[x])
        correct += temp

    return correct

#========================= Create Synonyms Sentence ===========================#
def augment(Input):

    aug = WordNetAug()
    final = []

    Output = aug.augment(Input, postag = True, max_syn_sent = 10 , postag_corpus='lst20', tokenize = 'Default')
    for x in range(len(Output)):
        temp = "".join(Output[x])
        final.append(temp)

    return final

#========================= Word 2 Vector computation part ===========================#
def word2vector(Query,final):

    wv = WordVector()
    answer = []

    for x in range(len(Query)):
        test1 = wv.sentence_vectorizer(Query[x], use_mean=False)
        value = 0
        for i in range(len(final)):
            test2 = wv.sentence_vectorizer(final[i], use_mean=False)
            temp = 1 - spatial.distance.cosine(test2,test1)
            value += temp
        if (value == len(final)):
            value = 0
        avg = value/len(final)
        answer.append(avg)

    return answer



def train_dictionary(Query):

   for x in range(len(Query)):  
       Question = re.sub('[!#$()“”]','', Query[x])
       print(Question)
       Output = aug.augment(Question, postag = False, max_syn_sent = 5 , postag_corpus='lst20')
       for x in range(len(Output)):
           temp = "".join(Output[x])
           augmented.append(temp)
       print(augmented)

   oskut.load_model(engine='scads')
   for x in augmented:
        token = oskut.OSKut(x)
        for x in token:
            train.append(x)
   train = list(dict.fromkeys(train))
   print (train)
   check_train = 1

   with open('train.txt', 'w' , encoding="utf-8") as f:
        for item in train:
            f.write(item+"\n")
    