import enum
from pythainlp.word_vector import WordVector
from pythainlp.tokenize import THAI2FIT_TOKENIZER
from KmuttSearchEngine.Query import *
from itertools import zip_longest, chain, repeat
from KmuttSearchEngine.tfidf import *
from app.models import questionanswer
from pythainlp.spell import NorvigSpellChecker
from collections import Iterable
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


def searchengine(search, query):
    try:
        Query = []
        Query_Tokenized = []
        Position = []
        location = []
        percentage = []
        temp1 = []

        #print(search)

        start = time.time()

        Query = query.question
        Query_ID = query.id

        dictionary = getDictionary()

        #======= spell check ========#
        result = spellCheck(search, dictionary)
        correct = result.correct
        tokenized = result.tokenized
        #print(tokenized)

        #======= augment ========#
        augments = augment(search)

        #======= remove stop words ========#
        removed_stopwords_Query, removed_stopwords_Final = stopwords(
            Query, augments)

        check = removed_stopwords_Final
        if check.count(check[0]) == len(check):
            print("All the samee")
            removed_stopwords_Final = [check[0]]

        #============ TF-IDF ==============#

        tfid, index_question, user_tfidf, removed_stopwords_Query = tfidf(
            removed_stopwords_Query, removed_stopwords_Final)  # TF-IDF

        #======= W2V process ========#

        answer = word2vector(removed_stopwords_Query, removed_stopwords_Final, tfid, index_question, user_tfidf,Query_ID)

        pos = {ans: answer[ans] for ans in sorted(answer,reverse=True)}
        Position = list(pos.values())
        del Position[-1]
        percentage = list(pos.keys())

        query = questionanswer.objects.filter(id__in=Position)
        query = dict([(obj.id, obj) for obj in query])
        sorted_query = [query[id] for id in Position]

        return_Result.query = sorted_query

        end = time.time()
        print("Total Search: " + str((end - start)))

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

    except:
        return_Result.query = None
        return(return_Result)

#========================= Read Dictionary from file ===========================#


def getDictionary():
    
    word_dictionary = {}
    
    file = open("KmuttSearchEngine/train.txt", 'r', encoding='UTF-8')
    file.readlines()

    for line in file:
        print ("Data: " + line)
        key, value = line.split()
        word_dictionary[key] = int(value)

    print(word_dictionary)

    return word_dictionary

#=========================== Spell Check Part ================================#

def spellCheck(Input, train):

    start = time.time()

    class return_result:
        tokenized = []
        correct = []

    #tl-deepcut-tnhc
    oskut.load_model(engine='tl-deepcut-tnhc')
    tokenized = oskut.OSKut(Input, k=100)

    checker_dataset = NorvigSpellChecker(custom_dict=train)  # Using dict from dataset train
    # checker_ttc = NorvigSpellChecker(custom_dict=ttc.word_freqs()) #Using dict from pre data train
    #tokenized = [re.sub('\W+','', word)  for word in tokenized]
    return_result.correct = [checker_dataset.correct(word) if not(re.search('[a-zA-Z\s]', word)) else word for word in tokenized ]
    print(return_result.correct)

    if len(return_result.correct) != 0:
        return_result.correct = ''.join(return_result.correct)
    else:
        return_result.correct = None

    return_result.tokenized = tokenized

    end = time.time()
    print("Spell check deepcut: " + str((end - start)))
    return return_result

#========================= Create Synonyms Sentence ==========================#

def augment(Input):

    start = time.time()

    aug = WordNetAug()
    final = []
    
    Output = aug.augment(Input, postag=True, max_syn_sent=3 ,postag_corpus='orchid_ud', tokenize='Default')
    print(Output)

    for x in Output:
        temp = "".join(x)
        final.append(temp)

    #final = ["".join(x) for x in Output]

    Input = ''.join(Input)
    final.append(Input)

    if final.count(final[0]) == len(final):
        #print("All the samee")
        final = [Input]

    end = time.time()
    print("Augment: " + str((end - start)))

    return final

#========================= Word 2 Vector computation part ===========================#


def word2vector(Query, final, tfidf_value, index_question, user_tfidf,Query_ID):

    wv = WordVector()
    wv1, wv2, user_eng = [], [],[]
    answer = defaultdict()
    i, j, value = 0, 0, 0

    start = time.time()

    wv.load_wordvector("thai2fit_wv")

    length_question = {}

    for count, question in enumerate(Query):
        length = len(question)-1
        length_question[count+1] = str(length)

    word_list = list(chain.from_iterable(Query))
    word_list = map(str.lower,word_list)

    user_question_index = next(iter(user_tfidf))
    index_user = user_question_index

    
    for question in final:
        value, i = 0, 0
        if len(question) < 4:
            for word in question:
                if (word.lower() in word_list):
                    user_eng.append(word.lower())
                    temp = np.full((1, 300), 1.0)
                    #print(user_eng)
                else:
                    temp = wv.word_vectorizer(word, use_mean=False)
                #print ("tfidf: "+ str(word)+" "+"["+ str(user_tfidf.get(index_user)[i])+ "]")
                value += (user_tfidf.get(index_user)[i]) * temp
                i += 1
            wv2.append(value)
            #print ("tfidf: "+ str(question)+" "+"["+ str(value) + "]")
            index_user += 1
        else:
            for word in question:
                if (re.search('[a-zA-Z]', word.lower()) and (word.lower() in word_list)):
                    user_eng.append(word.lower())
                    temp = np.full((1, 300), 1.0)
                else:
                    temp = wv.word_vectorizer(word, use_mean=False)
                #print ("tfidf: "+ str(word)+" "+"["+ str(user_tfidf.get(index_user)[i])+ "]")
                value += (user_tfidf.get(index_user)[i]) * temp
                i += 1
            wv2.append(value)
            #print ("tfidf: "+ str(question)+" "+"["+ str(value) + "]")
            index_user += 1
    
    for count, question in enumerate(Query):
        length = len(question)-1
        length_question[count+1] = str(length)

    word_list = list(chain.from_iterable(Query))

    value, i = 0, 0
    count = 1

    for _ in repeat(None, len(word_list)):
        if (word_list[0].lower() in user_eng):
            temp = np.full((1, 300), 1.0)
        else:
            temp = wv.word_vectorizer(word_list[0], use_mean=False)
        value += (tfidf_value.get(count)[i])*temp
        i += 1
        del(word_list[0])
        if str(i-1) == length_question[count]:
            i = 0
            count += 1
            wv1.append(value)
            value = 0
        else:
            continue

    wv_answer = [(1 - spatial.distance.cosine(v1, v2))
            for v1 in wv1 for v2 in wv2]
    wv_answer = list(list_split(wv_answer, len(final)))

    for id,wv_set in enumerate(wv_answer):
        max_value = max(wv_set)
        if max_value < 0.55:
            max_value = 0.0
        answer[float(round(max_value*100,3))] = Query_ID[id]

    # use to dect if result found is 0 #
    if all(value == 0 for value in answer.values()):
        answer[1] = 0

    end = time.time()
    print("w2v: " + str((end - start)))

    return answer


def list_split(listA, n):

    for x in range(0, len(listA), n):
        every_chunk = listA[x: n+x]

        if len(every_chunk) < n:
            every_chunk = every_chunk + \
                [None for y in range(n-len(every_chunk))]
        yield every_chunk


def train_dictionary(Query_data):

    print("Creating Dict")
    aug = WordNetAug()

    print(Query_data)
    Question = None
    quest = None
    augmented = []
    token_question = []
    train = []

    for quest in Query_data:
        Question = re.sub('[a-zA-Z!#$()“”?/\0-9!@#$%^&*<>:;=]', '', quest)
        augmented.append(Question)

    oskut.load_model(engine='ws-augment-60p')
    #oskut.load_model(engine='tl-deepcut-tnhc')

    for question in augmented:

        if not question:
            continue
        else:
            token = oskut.OSKut(question, k=100)
            token_question.append(token)
    
    flatten_token_question = list(flatten(token_question))

    for word in flatten_token_question:
        synnonyms_word = aug.find_synonyms(word)
        train.append(synnonyms_word)
        train.append(word)

    train = list(flatten(train))

    converter = lambda x: x.replace('_', '')
    train = list(map(converter, train))
    train_word_count = Counter(train)

    with open('train.txt', 'w', encoding="utf-8") as f:
        for word,counter in train_word_count.items():
            f.write(str(word)+" "+str(counter)+"\n")
    f.close()

    return_Result.code = 300

    return (return_Result)


def stopwords(Query, final):

    start = time.time()

    removed_stopwords_Query = []
    removed_stopwords_Final = []

    f = open('KmuttSearchEngine/stopwords_th.txt', 'r', encoding="utf-8")
    words_list = f.read().splitlines()
    f.close()

    tokenized_Query = tokenized(Query)
    tokenized_Final = tokenized(final)

    for word_query, word_final in zip_longest(tokenized_Query, tokenized_Final, fillvalue=None):

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
    print("stopwords: " + str((end - start)))

    return removed_stopwords_Query, removed_stopwords_Final


def stopwords1(Query):

    removed_stopwords_Query = []

    f = open('KmuttSearchEngine/stopwords_th.txt', 'r', encoding="utf-8")
    words_list = f.read().splitlines()
    f.close()

    oskut.load_model(engine='scads')

    for x in Query:
        temp = []
        if x is '':
            x = 'Null'
        else:
            token = oskut.OSKut(x)
            temp = [word for word in token if not word in words_list]
            removed_stopwords_Query.append(''.join(temp))

    return removed_stopwords_Query


def tokenized(Query):

    tokenized_Query = []

    for x in Query:
        temp = []
        if x is '':
            x = 'Null'
        else:
            token = THAI2FIT_TOKENIZER.word_tokenize(x)

            token = [x.strip(" ") for x in token if x.strip(" ")]

            tokenized_Query.append(token)

    return tokenized_Query


def tfidf(remove_sw_query, remove_sw_final):

    start = time.time()

    removed_stopwords_Query_tfid = []
    removed_stopwords_Final_tfid = []

    for x in remove_sw_final:
        remove_sw_query.append(x)

    get_tfidf, get_index, user_tfidf = get_tf_idf(
        remove_sw_query, remove_sw_final)

    del remove_sw_query[-(len(remove_sw_final)):]

    end = time.time()
    print("TFIDF: " + str((end - start)))

    return (get_tfidf, get_index, user_tfidf, remove_sw_query)

def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item