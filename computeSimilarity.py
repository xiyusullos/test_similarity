#coding=utf-8
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import io
import math
import nltk
from nltk.tokenize.stanford import StanfordTokenizer
from nltk.corpus import stopwords#停词
from nltk.tokenize import word_tokenize#分词
import xlrd
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import csv
import numpy as np
from string import punctuation

# wb = xlwt.Workbook()
# ws = wb.add_sheet('A Test Sheet')
#
# ws.write(0, 0, 1234.56,)

#
# wb.save(r'C:\Users\Lenovo\Desktop\bugresult.xls')

def tokenize_stopwords_stemmer(texts):
    
    #用斯坦福的分词采用这一段，用普通分词时不用这个
    #tokenize
    Str_texts=texts[0]
    #tokenizer = StanfordTokenizer(path_to_jar=r"/Users/apple/Documents/tools/stanford-parser-full-2015-04-20/stanford-parser.jar")
    tokenizer = StanfordTokenizer(path_to_jar=r"stanford-parser.jar") #path_to_jar: 用来定位jar包，r是防止字符转义的，如果路径中出现'\t'的话 不加r的话\t就会被转义 而加了'r'之后'\t'就能保留原有的样子
    java_path = 'C:/Program Files/Java/jdk1.8.0_121/bin/java.exe'
    os.environ['JAVAHOME'] = java_path
    texts_tokenized=tokenizer.tokenize(Str_texts)#输入必须是字符串,进行分词
    #print(texts_tokenized)

    p1=r'[-@<#$%^&*].+'
    pa1=re.compile(p1)  #re.compile()函数，将正则表达式的字符串形式编译为Pattern实例，然后使用Pattern实例处理文本并获得匹配结果（一个Match实例）
    texts_filtered0 = [ document for document in  texts_tokenized  if not document in pa1.findall(document) ]
    
    p2=r'.+[-_\/].+'  #将r'.+[-_\./].+'改为r'.+[-_\/].+'，可以保留数字间的句号，比如保留3.1.2这样的格式
    pa2=re.compile(p2)
    texts_filtered=[]
    for document in  texts_filtered0:
        if document in pa2.findall(document):
            if document.find('_')>-1 : #split()：拆分字符串。通过指定分隔符对字符串进行切片，并返回分割后的字符串列表（list）
                texts_filtered = texts_filtered + document.split('_')
            elif document.find('-')>-1:
                texts_filtered = texts_filtered + document.split('-')
            elif document.find('.')>-1:
                texts_filtered = texts_filtered + document.split('.')
            elif document.find('/')>-1:
                texts_filtered = texts_filtered + document.split('/')
        else:
            texts_filtered.append(document)
    
    texts_filtered = [ document for document in  texts_filtered  if  document != '' and document != "''" and document != "``" ]#过滤掉空格，单引号和--
  
    #stopwords
    english_stopwords = stopwords.words('english')#得到停词
    texts_filtered_stopwords = [ document for document in texts_filtered if not document in english_stopwords]#过滤掉停词
    
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','\n'
                            ,'<','>','/','\"','\'','{','}','!','~','`'
                            ,'$','^','/*','*/','/**','**/','**','-','_','+','=',r'-?-',r'@?']#得到标点

    texts_filtered = [ document for document in  texts_filtered_stopwords if not document in english_punctuations]#过滤掉标点
    #print texts_filtered
    temp = texts_filtered[:]  #实现去除带'comment'元素的代码
    for i in temp:
        if 'comment' in i:
            texts_filtered.remove(i)
    #print(texts_filtered)
    #texts_filtered=[re.sub(r'^[1-9]\d*$'.format(punctuation), '', x) for x in texts_filtered]  # ^[1-9]\d*$过滤掉整数

    porter = nltk.PorterStemmer() #词干提取算法
    texts_Stemmered=[porter.stem(t) for t in texts_filtered] #列表类型，提取词干
    return texts_Stemmered #返回一个列表

    


#统计关键词及个数
def CountKey(text_words):
    try:
        #统计格式 格式<Key:Value> <属性:出现个数>
        i = 0
        table = {}
        
        #字典插入与赋值
        for word in text_words:
            if word!="" and word in table:      #如果存在次数加1  table.has_key(word)在Python3中被删除
                num = table[word]
                table[word] = num + 1
            elif word!="":                            #否则初值为1
                table[word] = 1
        i += 1

        #键值从大到小排序 函数原型：sorted(dic,value,reverse)
        dic = sorted(table.items(), key = lambda asd:asd[1], reverse = True) #items函数，将一个字典以列表的形式返回，因为字典是无序的，所以返回的列表也是无序的
        return dic

        
    except Exception as e:
        print('Error:',e)
    finally:
        pass
        #print 'END\n\n'


''' ------------------------------------------------------- '''
#统计关键词及个数 并计算相似度
def MergeKeys(dic1,dic2,all_reports_tokens):
    #合并关键词 采用三个数组实现
    arrayKey = []
    for i in range(len(dic1)):
        arrayKey.append(dic1[i][0])       #向数组中添加关键字元素
    for i in range(len(dic2)):       
        if dic2[i][0] in arrayKey:
            pass
            #print 'has_key',dic2[i][0]
        else:                             #合并
            arrayKey.append(dic2[i][0])
    else:
        pass
        #print '\n\n'
    #print arrayKey
    #test = str(arrayKey).decode('string_escape')  #字符转换
    #print testS

    #计算词频 infobox可忽略TF-IDF
    arrayNum1 = [0]*len(arrayKey)
    arrayNum2 = [0]*len(arrayKey)
    #print arrayNum1

    #赋值arrayNum1
    for i in range(len(dic1)):     
        key = dic1[i][0]
        value = dic1[i][1]#词频TF
        j = 0
        while j < len(arrayKey):
            if key == arrayKey[j]:
                
                #计算DF
                k=0
                for t in range(len(all_reports_tokens)):
                    if key in all_reports_tokens[t]:
                        k = k + 1
                        
                arrayNum1[j] = float(value) / float(k)
                #arrayNum1[j]=value
                break
            else:
                j = j + 1

    #赋值arrayNum2
    for i in range(len(dic2)):     
        key = dic2[i][0]
        value = dic2[i][1]
        j = 0
        while j < len(arrayKey):
            if key == arrayKey[j]:
                
                #计算DF
                k=0
                for t in range(len(all_reports_tokens)):
                    if key in all_reports_tokens[t]:
                        k = k + 1
                        
                arrayNum2[j] = float(value) / float(k)
                #arrayNum1[j]=value
                break
            else:
                j = j + 1
    
    #print arrayNum1
    #print arrayNum2
    #print len(arrayNum1),len(arrayNum2),len(arrayKey)

    #计算两个向量的点积
    x = 0
    i = 0
    while i < len(arrayKey):
        x = x + arrayNum1[i] * arrayNum2[i]
        i = i + 1

    #计算两个向量的模
    i = 0
    sq1 = 0
    while i < len(arrayKey):
        sq1 = sq1 + arrayNum1[i] * arrayNum1[i]   #pow(a,2)
        i = i + 1
    
    i = 0
    sq2 = 0
    while i < len(arrayKey):
        sq2 = sq2 + arrayNum2[i] * arrayNum2[i]
        i = i + 1
    
    try:
        result = float(x) / ( math.sqrt(sq1) * math.sqrt(sq2) )
    except ZeroDivisionError:
        result=0.0
        
    return result


def all_compute2Similarity(text1,text2,basic_texts):#计算两个文本间的相似度
    #text1:[“。。。”]   text2: [“。。。”]   basic_texts:【 [ “。。。”] , [“。。。” ] , [ ] , [ ] 】
    
    #检查text1，或text2  是否在数据集中
    if text1 in basic_texts:
        pass
    else:
        basic_texts.append(text1)
    if text2 in basic_texts:
        pass
    else:
        basic_texts.append(text2)
        
    
    dic1 = CountKey(tokenize_stopwords_stemmer(text1))
    dic2 = CountKey(tokenize_stopwords_stemmer(text2))
    
    all_reports_tokens=[]
    for i in range(len(basic_texts)):
        text0=basic_texts[i]
        all_reports_tokens.append(tokenize_stopwords_stemmer(text0))
    
    result= MergeKeys(dic1, dic2,all_reports_tokens) 
    
    return result
    
def all_computeSimilarity(text1, basic_texts):#计算数据集中所有文本相似度
    #text1:[“。。。”]  basic_texts:【 [“。。。” ] , [ ] , [ ] , [ ] 】
    
    #检查text1，是否在数据集中
    if text1 in basic_texts:
        pass
    else:
        basic_texts.append(text1)      
    
    dic1 = CountKey(tokenize_stopwords_stemmer(text1))
    
    
    all_reports_tokens=[]
    for i in range(len(basic_texts)):
        text0=basic_texts[i]
        all_reports_tokens.append(tokenize_stopwords_stemmer(text0))
    
    
    result=[]
    for i in range(len(basic_texts)):
    #计算文档2-互动的关键词及个数
        dic2 = CountKey(all_reports_tokens[i])
    #合并两篇文章的关键词及相似度计算
        result.append( MergeKeys(dic1, dic2,all_reports_tokens) )
            
    return result


#其中  text1以及 basic_texts都是经过tokenize_stopwords_stemmer(texts)处理的
#此输入为tokenize_stopwords_stemmer(texts):的输出
def half_computeSimilarity(text1, basic_texts):#计算数据集中所有文本相似度
    #text1:[“。。。”]  basic_texts:【 [“  ” , "  " , "  " ] , 
    #                                 ......
    #                                [ "  ","  ","  " ] 】

    #检查text1，是否在数据集中
    if text1 in basic_texts:
        pass
    else:
        basic_texts.append(text1)      
    
    
    dic1 = CountKey(text1)

    result=[]
    for i in range(len(basic_texts)):
    #计算文档2-互动的关键词及个数
        dic2 = CountKey(basic_texts[i])
    #合并两篇文章的关键词及相似度计算
        result.append( MergeKeys(dic1, dic2,basic_texts) )

    return result


# 计算相似度函数
def Similarity(all_reports_tokens, all_reports_tokens2):
    all_reports_tokens1 = []
    all_reports_tokens3 = []
    dic1 = CountKey(all_reports_tokens[0])
    all_reports_tokens1.append(all_reports_tokens[0])#添加前一行的分词结果
    all_reports_tokens3.append(all_reports_tokens1[0])

    dic2 = CountKey(all_reports_tokens2[0])
    all_reports_tokens3.append(all_reports_tokens2[0])#添加后一行的分词结果
    result = []
    result.append(MergeKeys(dic1, dic2, all_reports_tokens3))

    return result


def main():
    keys = []
    results = []
    index = 500  # 如果要比较1-10行 index=9
    workbook = xlrd.open_workbook('data/bug.xlsx')  # 打开文件
    sheet1 = workbook.sheet_by_index(0)
    for i in range(1, index - 1):
        print i, index - 1
        all_reports_tokens = []
        texts0 = []
        texts0.append(sheet1.cell(i, 4).value.encode('utf-8'))
        all_reports_tokens.append(tokenize_stopwords_stemmer(texts0))
        # print(all_reports_tokens)
        for j in range(i + 1, index+1):
            print j, index + 1
            all_reports_tokens2 = []
            texts1 = []
            texts1.append(sheet1.cell(j, 4).value.encode('utf-8'))
            # print(texts1)
            all_reports_tokens2.append(tokenize_stopwords_stemmer(texts1))
            # print(all_reports_tokens2)

            # 计算相似度的函数
            #print("第" + str(i) + "行和第" + str(j) + "行")
            keys.append(('L'+str(i)+','+'L'+str(j)))
            #print keys
            results.append(Similarity(all_reports_tokens, all_reports_tokens2))
            #print(results)
    data = []
    for key, result in zip(keys, results):
        # row = {
        #     'key': key,
        #     'result': result
        #     }
        data.append([str(key), str(result)])

    # execel = r'C:\Users\Lenovo\Desktop\similarresult.csv'
    # #with open('com.csv', "a+", newline="", encoding='utf-8') as csvfile:
    # with open(execel, "a+") as csvfile:
    #     fieldnames = ['key', 'result']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     writer.writerows([])
    # data = [
    #     ['key', 'result'],
    #     [
    #         1,2
    #     ]
    # ]

    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')

    for (i, row) in enumerate(data):
        for (j, item) in enumerate(row):
            ws.write(i, j, item)

    wb.save('example.xls')

# def main():
#     all_reports_tokens = []
#     all_reports_tokens2 = []
#     workbook = xlrd.open_workbook(r'C:\Users\Lenovo\Desktop\bug.xlsx')  # 打开文件
#     #sheet1_name= workbook.sheet_names()[0] # 获取所有sheet
#     #('sheet1')# 根据sheet索引或者名称获取sheet内容
#     #print(sheet1.cell(2,0).value.encode('utf-8'))#获取单元格内容
#     sheet1 = workbook.sheet_by_index(0)
#     for i in range(1,10):
#         texts0 = []
#         texts0.append(sheet1.cell(i, 4).value.encode('utf-8'))
#         print(texts0)
#         all_reports_tokens.append(tokenize_stopwords_stemmer(texts0))
#         print(all_reports_tokens)
#         for j in range(i+1, i+2):
#           texts1 = []
#           texts1.append(sheet1.cell(j, 4).value.encode('utf-8'))
#           print(texts1)
#           all_reports_tokens2.append(tokenize_stopwords_stemmer(texts1))
#           print(all_reports_tokens2)
# #上述两个数组进行比较
#         for m in range(i-1,i):
#             all_reports_tokens1 = []
#             dic1 = CountKey(all_reports_tokens[m])
#             all_reports_tokens1.append(all_reports_tokens[m])
#             # print(all_reports_tokens1)
#             result = []
#             for n in range(i-1,i):
#                 all_reports_tokens3 = []
#                 all_reports_tokens3.append(all_reports_tokens1[0])
#                 #append(all_reports_tokens1[0]是随着i的值变化的
#                 #计算文档2-互动的关键词及个数
#                 dic2 = CountKey(all_reports_tokens2[n])
#                 all_reports_tokens3.append(all_reports_tokens2[n])
#                 #print(all_reports_tokens3)
#                 #合并两篇文章的关键词及相似度计算
#                 result.append(MergeKeys(dic1, dic2,all_reports_tokens3))
#                 #return all_reports_tokens3
#         # print(all_reports_tokens)
#         # print(all_reports_tokens2)
#             print result


             # rr.append(result[j])
             # print(rr[j])
        # for n in range(0,43):
        #     rr[n]=rr
        # print rr[n]
        # dataframe = pd.DataFrame(
        #
        # with open("F:\\test.csv", "w", encoding="utf-8") as f:
        #     dataframe.to_csv(f, index=False, sep='')

    #print len(result)



if __name__ == '__main__':
    main()
    



        