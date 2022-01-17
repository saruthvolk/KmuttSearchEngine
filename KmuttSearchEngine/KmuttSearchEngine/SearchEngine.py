from pythainlp.word_vector import WordVector
from KmuttSearchEngine.Query import *
from app.models import questionanswer
from pythainlp.spell import NorvigSpellChecker
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
    Position = []
    location=[]
    percentage = []
    temp1=[]

    print(search);

    Query = query.question
    dictionary = getDictionary()

    result = spellCheck(search, dictionary)
    correct = result.correct
    tokenized = result.tokenized

    print(tokenized)

    augments = augment(tokenized)

    print("Input:" + search)
    print ("Augmentation: ")
    for x in range(len(augments)):
        print(str((x+1))+".) " + augments[x])

    answer = word2vector (Query,augments)

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

    start = time.time()

    with open("train.txt", 'r', encoding='UTF-8') as f:
        train = f.read().splitlines()

    end = time.time()
    print ("Dictionary: "+ str((end - start)))

    return train

#========================= Spell Check Part ===========================#
def spellCheck(Input,train):

    #start = time.time()

    class return_result:
        tokenized = []
        correct = []

    correct = ""
    oskut.load_model(engine='scads')
    tokenized = oskut.OSKut(Input)

    checker_dataset = NorvigSpellChecker(custom_dict=train) #Using dict from dataset train
    #checker_ttc = NorvigSpellChecker(custom_dict=ttc.word_freqs()) #Using dict from pre data train

    for x in range(len(tokenized)):
        temp  = ""
        temp = checker_dataset.correct(tokenized[x])
        return_result.correct.append(temp)

    return_result.correct = ''.join(return_result.correct)

    return_result.tokenized = tokenized

    #end = time.time()
    #print ("Spell check: "+ str((end - start)))

    return return_result

#========================= Create Synonyms Sentence ===========================#
def augment(Input):

    #start = time.time()

    aug = WordNetAug()
    final = []

    Output = aug.augment(Input, postag = True, max_syn_sent = 3 , postag_corpus='orchid', tokenize = 'Tokenized')
    for x in range(len(Output)):
        temp = "".join(Output[x])
        final.append(temp)
    
    Input = ''.join(Input)
    final.append(Input)

    #end = time.time()
    #print ("Augment: "+ str((end - start)))

    return final

#========================= Word 2 Vector computation part ===========================#
def word2vector(Query,final):

    wv = WordVector()
    answer = []

    start = time.time()

    wv.load_wordvector("thai2fit_wv")

    v1 = [wv.sentence_vectorizer(i, use_mean=False) for i in Query]
    v2 = [wv.sentence_vectorizer(i, use_mean=False) for i in final]

   # for x in range(len(v2)):
   #     print ("Vector augment")
   #     print(str(x+1)+"):"+ str(v2[x]))

    temp = [(1 - spatial.distance.cosine(test1,test2)) for test1 in v1 for test2 in v2]
    

    def list_split(listA, n):
        for x in range(0, len(listA), n):
            every_chunk = listA[x: n+x]

            if len(every_chunk) < n:
                every_chunk = every_chunk + \
                    [None for y in range(n-len(every_chunk))]
            yield every_chunk

    temp = list(list_split(temp, len(final)))

    #answer = [(max(x)) if (max(x)) > 0.55 else 0.0 for x in temp]

    
    #  get the max value from the list of the answer #
    for x in temp:
        max_value = max(x)
        if max_value < 0.55:    
            max_value = 0.0
        answer.append(max_value)


    # use to dect if result found is 0 #
    if answer.count(answer[0]) == len(answer):   
        answer = [0,0]

    end = time.time()
    print ("w2v: "+ str((end - start)))

    return answer


def train_dictionary(Query):

   aug = WordNetAug()

   augmented = []
   train = []

   for x in range(len(Query)):  
       Question = re.sub('[a-zA-Z!#$()“”?/\0-9!@#$%^&*<>:;=]','',Query[x])
       augmented.append(Question)
      
   oskut.load_model(engine='scads')
   for x in augmented:

        if x is '':
             x = 'Null';
        else:
            token = oskut.OSKut(x)
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

   return_Result.code = 300

   return (return_Result)