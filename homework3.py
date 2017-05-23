###naive bayes classifier
#import training data
import re, codecs
import pandas as pd

with open("TrainingData.txt") as t:
    raw_article = t.readlines() 
#print(raw_article)

training_data = []
for i in raw_article:
    i = i[:-1] #remove \n
    i = i.split(" ")[:-1] #remove space
    i[0] = i[0].split("\t")[1] #remove no. and \t
    training_data.append(i)
    #remove \u3000
    for i in training_data:
        for j in i:
            if j == "\u3000":
                i.remove(j)            
#print(training_data[0]) 

#import testing data
##no. from 3501
with open("TestData.txt") as e:
    raw_articl = e.readlines() 
#print(raw_article)

test_data = []
for i in raw_articl:
    i = i[:-1] #remove \n
    i = i.split(" ")[:-1] #remove space
    i[0] = i[0].split("\t")[1] #remove no. and \t
    test_data.append(i)
    #remove \u3000
    for i in test_data:
        for j in i:
            if j == "\u3000":
                i.remove(j)
#print(test_data[0])  

with open("punctuation.txt") as p:
    raw_pun = p.readlines()
#print(raw_pun)

#remove \n
pun = []
for i in raw_pun:
    i = i[0]
    pun.append(i)

with open("stopword_chinese.txt") as s:
    raw_stopword = s.readlines()
#print(raw_stopword)

#remove \n
stopword = []
for i in raw_stopword:
    i = i[:-1]
    stopword.append(i)
    
#filt pun & stopword
final_train = []
final_test = []
for i in training_data:
    article_1 = list(filter(lambda x: x not in pun, i))
    article_2 = list(filter(lambda y: y not in stopword, article_1))
    final_train.append(article_2)
    
for i in test_data:
    article_3 = list(filter(lambda x: x not in pun, i))
    article_4 = list(filter(lambda y: y not in stopword, article_3))
    final_test.append(article_4)
    
print(final_train[0])
print(final_test[0])

##build lable list & vocabulary
#save lable into lable_list
lable_list = []
for line in final_train:
    lable_list.append(line[0])
    
#print(len(lable_list)) 3500
#politics: 0-1999
#sports: 2000-3499

#remove label
raw_train = []
for line in final_train:
    raw_train.append(line[1:])

#print(len(raw_train)) 3500

#build vocabulary
train_v = []
for line in raw_train:
    train_v.append(list(set(line)))    
#print(len(train_v)) 3500

count_v = 0
for i in range (0, 3500):
    count_v += len(train_v[i])    
#print(count_v) 472283

##dealing with training data
#split raw_train to sports_train and politics_train
sports_train = raw_train[:2000]
politics_train = raw_train[2000:]
#len(sports_train) 1500
#len(politics_train) 1000

#build politics_train TF data
def get_token_TF(cat_train, cat_dict):
    for line in cat_train:
        for token in line:
            if token not in list(cat_dict.keys()):
                cat_dict[token] = 1
            else:
                cat_dict[token] += 1
    return cat_dict
    
sports_dict = {}
get_token_TF(sports_train, sports_dict)
politics_dict = {}
get_token_TF(politics_train, politics_dict)

#transform politics_dict & sports_dict into dataframe
df_sports = pd.DataFrame(sports_dict, index = ['sports_TF']).T #30603 rows
df_politics = pd.DataFrame(politics_dict, index = ['politics_TF']).T #26509 rows

#caculate Probability
df_sports['sports_p'] = (df_sports['sports_TF'] + 1) / (30603 + count_v)
df_politics['politics_p'] = (df_politics[ㄎ'politics_TF'] + 1) / (26509 + count_v)

#combine two df
df_join = df_sports.combine_first(df_politics)
df_join.fillna(0, inplace = True)

#caculate P of token whose TF = 0
for i in range(0, len(df_join.index)):
    if df_join['politics_TF'][i] == 0:
        df_join['politics_p'][i] = (df_join['politics_TF'][i] + 1) / (26509 + count_v)

    if df_join['sports_TF'][i] == 0:
        df_join['sports_p'][i] = (df_join['sports_TF'][i] + 1) / (30603 + count_v)
        
#dealing with testing data
#calculate TF of each document in final_test
test_TF = {}
doc_id = 3500
for line in final_test:
    doc_id += 1
    test_dict = {}
    for token in line:
        if token not in list(test_dict.keys()):
            test_dict[token] = 1
        else:
            test_dict[token] += 1
    test_TF[doc_id] = test_dict
    
#transform test_TF into DataFrame
df_test = pd.DataFrame(test_TF)
df_test.fillna(0, inplace = True)

#join sports_p & politics_p with df_test
df_test = df_test.join(df_join['sports_p'])
df_test = df_test.join(df_join['politics_p'])
df_test.fillna(0, inplace = True)
df_test

#calculate
import math
sports_ratio = 2000 / 3500
politics_ratio = 1500 / 3500

final_result = []
for col in list(test_TF.keys()):
    sports_prob = sports_ratio 
    politics_prob = politics_ratio 
    for row in df_test.index:
        if df_test[col][row] > 0 and df_test['sports_p'][row] > 0:
            sports_prob *= df_test[col][row] * math.log10(df_test['sports_p'][row])
            
        if df_test[col][row] > 0 and df_test['politics_p'][row] > 0:
            politics_prob *= df_test[col][row] * math.log10(df_test['politics_p'][row])
            
        result = [int(col)]
        if sports_prob > politics_prob:
            result.append('sports')
            
        elif sports_prob < politics_prob:
            result.append('politics')
        else:
            result.append('sports & politics')
            
    final_result.append(result)
