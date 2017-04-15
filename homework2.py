#import article
import re, codecs
with open("/Users/yichiehchen/python file/text mining/PA-2/TMBD_news_files_2000.txt") as f:
    raw_article = f.readlines() 

#print(raw_article)

article = []
for i in raw_article:
    i = i[:-1] #remove \n
    i = i.split(" ")[:-1] #remove space
    i[0] = i[0].split("\t")[1] #remove no. and \t
    article.append(i)
    #remove \u3000
    for i in article:
        for j in i:
            if j == "\u3000":
                i.remove(j)
            
#print(article[0:3])  

#import stopword & punctuation
with open("/Users/yichiehchen/python file/text mining/PA-2/punctuation.txt") as p:
    raw_pun = p.readlines()
#print(raw_pun)

#remove \n
pun = []
for i in raw_pun:
    i = i[0]
    pun.append(i)

with open("/Users/yichiehchen/python file/text mining/PA-2/stopword_chinese.txt") as s:
    raw_stopword = s.readlines()
#print(raw_stopword)

#remove \n
stopword = []
for i in raw_stopword:
    i = i[:-1]
    stopword.append(i)
    
#remove stopword & punctuation
final_article = []
for i in article:
    article_1 = list(filter(lambda x: x not in pun, i))
    article_2 = list(filter(lambda y: y not in stopword, article_1))
    final_article.append(article_2)
    
print(final_article[0]) 
#print(final_article[1])
#print(len(final_article))

#caculate TF in each document {no.: {term:TF...}}
each_doc = {}

for i in range(1, 2001):
    each_doc[i] = {}
    for j in final_article[i-1]:
        if j not in list(each_doc[i].keys()):
            each_doc[i][j] = 1
        else:
            each_doc[i][j] += 1
print(each_doc[1])

#build term dictionary {term:[TF,DF]...}
term_dict = {}

for i in list(each_doc.keys()):
    for j in list(each_doc[i].keys()):
        if j not in list(term_dict.keys()):
            term_dict[j] = [0, 1]
            term_dict[j][0] += each_doc[i][j]
        else:
            term_dict[j][0] += each_doc[i][j]
            term_dict[j][1] += 1
            
print(term_dict)  

#transform term_dict into dataframe & calculate IDF, WEIGHT
import pandas as pd
import numpy as np
term_frame = pd.DataFrame(term_dict).T
term_frame.columns = ['TF', 'DF']
term_frame['IDF'] = np.log10(2000/term_frame['DF'])
term_frame['Weighting'] = term_frame['TF'] * term_frame['IDF']
print(term_frame)
print(term_frame.T['風格'])

#transform each_doc into dataframe & combine two dataframe
doc_frame = pd.DataFrame(each_doc)
#replace NA with 0
doc_frame.fillna(0, inplace = True)
#1 代表有出現該term
doc_frame[doc_frame > 0] = 1
final_frame = term_frame.join(doc_frame)
final_frame
print(final_frame.T['風格'])

#add vector columns
for i in range(1, 2001):
    vector = 'vector_doc{}'.format(i)
    final_frame[vector] = final_frame[i] * final_frame['Weighting']
    
#calculate similarity
sim = {}
for i in range(1, 2001):
    comparison = 'vector_doc{}'.format(i)
    a = sum(final_frame['vector_doc56'] * final_frame[comparison])
    b = (sum((final_frame['vector_doc56'] ** 2)) ** 0.5) * (sum((final_frame[comparison] ** 2)) ** 0.5)
    sim[i] = a/b
print(sim)
import operator
sorted_sim = sorted(sim.items(), key=operator.itemgetter(1), reverse=True)

print(sorted_sim[1:12])
result_sim = sorted_sim[1:12]

#export sorted_sim into txt file
final_sim = ["Result Format\n" + "ID Similarity\n"]

for i in result_sim:
    i = str(i[0]) + " " + str(i[1]) + "\n"
    final_sim.append(i)
    
print(final_sim)

file = open("result_sim.txt", "w", encoding = "UTF-8")

for i in final_sim:
    file.write(str(i))   
file.close()      
