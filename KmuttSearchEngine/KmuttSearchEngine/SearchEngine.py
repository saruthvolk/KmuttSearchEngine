from pythainlp.word_vector import WordVector
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import ttc
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
  res = ''

def searchengine (search):

    print(search)
    train = []
    augmented = []
    aug = WordNetAug()
    Query = ['อยากดูโปรเจกต์เก่าต้องทำไง','คืนหนังสือที่ยืมมาอย่างไร','บัตรนักศึกษาหายทำยังไง','ข้อสอบเก่าสามารถดูได้ที่ไหนครับ','SSO คืออะไร','ทำไมต้องเปลี่ยนไปใช้ SSO ตัวใหม่','จะเปลี่ยนไปใช้ SSO ตัวใหม่ต้องเตรียมตัวอย่างไร',
         'เมื่อเปลี่ยนมาใช้ SSO ใหม่แล้ว เมล (@mail.kmutt.ac.th ) จะยังสามารถใช้งานได้อยู่หรือไม่ ต้องทำอย่างไรบ้าง','เมื่อเปลี่ยนไปใช้ SSO ใหม่ นักศึกษาต้องเปลี่ยน User Account ตามหรือไม่',
         'ระบบแจ้งว่า “Your account is not SSO ready” หมายความว่าอะไร','ระบบแจ้งว่า “Your account is not SSO ready” ต้องดำเนินการอย่างไร','เปิดใช้งานของ KMUTT Google Account ต้องทำอย่างไร',
         'ต้องการนำเข้า E-mail จาก KMUTT E-mail ไปใน KMUTT Google Apps ต้องทำอย่างไร','การตั้งค่าการซิงค์ KMUTT Google Apps Account ไปยังระบบปฏิบัติการ Android','การตั้งค่าการซิงค์ KMUTT Google Apps Account ไปยังระบบปฏิบัติการ iOS',
         'การตั้งค่าการซิงค์ KMUTT Google Apps Account ไปยัง Microsoft Outlook',' ']

#========================= Train Dictionary to file ===========================#
#   for x in range(len(Query)):  
#       Question = re.sub('[!#$()“”]','', Query[x])
#       print(Question)
#       Output = aug.augment(Question, postag = False, max_syn_sent = 5 , postag_corpus='lst20')
#       for x in range(len(Output)):
#           temp = "".join(Output[x])
#           augmented.append(temp)
#       print(augmented)

#    oskut.load_model(engine='scads')
#    for x in augmented:
#        token = oskut.OSKut(x)
#        for x in token:
#            train.append(x)
#    train = list(dict.fromkeys(train))
#    print (train)
#    check_train = 1

#    with open('train.txt', 'w' , encoding="utf-8") as f:
#        for item in train:
#            f.write(item+"\n")

#========================= Read Dictionary from file ===========================#
    with open("train.txt", 'r', encoding='UTF-8') as f:
        train = f.read().splitlines()
    
    Input = search #ต้องคืยหนงสือที่ยมมาที่ไหขครัช
    correct = ""
    retry = 1
#========================= Spell Check Part ===========================#
    oskut.load_model(engine='scads')
    token = oskut.OSKut(Input)
    print(token)

#=============== Custom dict from data set =======================#
    checker_dataset = NorvigSpellChecker(custom_dict=train) #Using dict from dataset train
    checker_ttc = NorvigSpellChecker(custom_dict=ttc.word_freqs()) #Using dict from pre data train

    for x in range(len(token)):
        temp  = ""
        temp = checker_dataset.correct(token[x])
        correct += temp

    retry = 0
    final = []
    Result = []
    final.append(Input)
    aug = WordNetAug()
    wv = WordVector()
  #========================= Create Synonyms Sentence ===========================#
    Output = aug.augment(Input, postag = True, max_syn_sent = 10 , postag_corpus='lst20', tokenize = 'Default')
    for x in range(len(Output)):
        temp = "".join(Output[x])
        final.append(temp)
    answer = []
    location=[]
    max = 0
    Query = ['อยากดูโปรเจกต์เก่าต้องทำไง','คืนหนังสือที่ยืมมาอย่างไร','บัตรนักศึกษาหายทำยังไง','ข้อสอบเก่าสามารถดูได้ที่ไหนครับ','SSO คืออะไร','ทำไมต้องเปลี่ยนไปใช้ SSO ตัวใหม่','จะเปลี่ยนไปใช้ SSO ตัวใหม่ต้องเตรียมตัวอย่างไร',
         'เมื่อเปลี่ยนมาใช้ SSO ใหม่แล้ว เมล (@mail.kmutt.ac.th ) จะยังสามารถใช้งานได้อยู่หรือไม่ ต้องทำอย่างไรบ้าง','เมื่อเปลี่ยนไปใช้ SSO ใหม่ นักศึกษาต้องเปลี่ยน User Account ตามหรือไม่',
         'ระบบแจ้งว่า “Your account is not SSO ready” หมายความว่าอะไร','ระบบแจ้งว่า “Your account is not SSO ready” ต้องดำเนินการอย่างไร','เปิดใช้งานของ KMUTT Google Account ต้องทำอย่างไร',
         'ต้องการนำเข้า E-mail จาก KMUTT E-mail ไปใน KMUTT Google Apps ต้องทำอย่างไร','การตั้งค่าการซิงค์ KMUTT Google Apps Account ไปยังระบบปฏิบัติการ Android','การตั้งค่าการซิงค์ KMUTT Google Apps Account ไปยังระบบปฏิบัติการ iOS',
         'การตั้งค่าการซิงค์ KMUTT Google Apps Account ไปยัง Microsoft Outlook']

  #========================= Word 2 Vector computation part ===========================#
    for x in range(len(Query)):
        test1 = wv.sentence_vectorizer(Query[x], use_mean=False)
        value = 0
        for i in range(len(final)):
            test2 = wv.sentence_vectorizer(final[i], use_mean=False)
            temp = 1 - spatial.distance.cosine(test1, test2)
            value += temp
        avg = value/len(final)
        answer.append(avg)

    if math.isnan(avg):
       print("No Result Found")

    else:
        pos = sorted(answer,reverse = True)
        location = np.argsort(answer)[::-1]
        print ("\nQuestion: "+ Input+ "\n")
        print ("Result:")
        for j in range(len(location)):
            position = location[j]
            temp = (str(j+1)+".) "+ Query[position] + ' [ '+ str("{:.2f}".format(pos[j]*100))+ '% ]')
            Result.append(temp)

        if Input != correct:
           return_Result.res = Result
           return_Result.Correct = correct
           return (return_Result)
               
        else:
           retry = 0
           return_Result.Correct = None
           return_Result.res = Result
           return_Result.Retry = 0
           return(return_Result)