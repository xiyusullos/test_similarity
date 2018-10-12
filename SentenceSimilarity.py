#coding=utf-8
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import division
import re
import math
import nltk
from nltk.tokenize import StanfordTokenizer
from nltk.corpus import stopwords  # 停词
from nltk.tokenize import word_tokenize  # 分词
import xlrd
# import xlwt  WordsSimilarityCalculationModel1
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import csv
import pandas as pd
from string import punctuation
from WordsSimilarityCalculationModel1 import wordsimilarity

def tokenize_stopwords_stemmer(texts):
    Str_texts = texts[0]
    # tokenizer = StanfordTokenizer(path_to_jar=r"/Users/apple/Documents/tools/stanford-parser-full-2015-04-20/stanford-parser.jar")
    tokenizer = StanfordTokenizer(
        path_to_jar=r"C:\Users\zw\Desktop\stanford-parser.jar")  # path_to_jar: 用来定位jar包，r是防止字符转义的，如果路径中出现'\t'的话 不加r的话\t就会被转义 而加了'r'之后'\t'就能保留原有的样子
    java_path = 'E:soft/Java/jdk1.8.0_121/bin/java.exe'
    os.environ['JAVAHOME'] = java_path
    texts_tokenized = tokenizer.tokenize(Str_texts)  # 输入必须是字符串,进行分词
    # print(texts_tokenized)

    p1 = r'[-@<#$%^&*].+'
    pa1 = re.compile(p1)  # re.compile()函数，将正则表达式的字符串形式编译为Pattern实例，然后使用Pattern实例处理文本并获得匹配结果（一个Match实例）
    texts_filtered0 = [document for document in texts_tokenized if not document in pa1.findall(document)]

    p2 = r'.+[-_\/].+'  # 将r'.+[-_\./].+'改为r'.+[-_\/].+'，可以保留数字间的句号，比如保留3.1.2这样的格式
    pa2 = re.compile(p2)
    texts_filtered = []
    for document in texts_filtered0:
        if document in pa2.findall(document):
            if document.find('_') > -1:  # split()：拆分字符串。通过指定分隔符对字符串进行切片，并返回分割后的字符串列表（list）
                texts_filtered = texts_filtered + document.split('_')
            elif document.find('-') > -1:
                texts_filtered = texts_filtered + document.split('-')
            elif document.find('.') > -1:
                texts_filtered = texts_filtered + document.split('.')
            elif document.find('/') > -1:
                texts_filtered = texts_filtered + document.split('/')
        else:
            texts_filtered.append(document)

    texts_filtered = [document for document in texts_filtered if
                      document != '' and document != "''" and document != "``"]  # 过滤掉空格，单引号和--

    # # stopwords
    # english_stopwords =stopwords.words('english')  # 得到停词
    # texts_filtered_stopwords = [document for document in texts_filtered if not document in english_stopwords]  # 过滤掉停词

    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '\n', '||',
                            '<', '>', '/', '\"', '\'', '{', '}', '!', '~', '`', '0', '$', '^', '/*', '*/', '/**', '**/',
                            '**', '-', '_', '__', '|', '+', '=', r'-?-', r'@?']  # 得到标点

    texts_filtered = [document for document in texts_filtered if
                      not document in english_punctuations]  # 过滤掉标点
    return texts_filtered
    #print texts_filtered
def main():
    #!!!!!!!!!!!!!!!!!!!
    #数据集！！！！！以[ [..。] , [...] , ... , [...] , [...]]形式存放数据集
    all_reports_tokens2 = []
    workbook = xlrd.open_workbook(r'C:\Users\zw\Desktop\com-msg.xlsx') # 打开文件
    #sheet1_name= workbook.sheet_names()[0] # 获取所有sheet
    sheet1 = workbook.sheet_by_index(6)#('sheet1')# 根据sheet索引或者名称获取sheet内容
    #print(sheet1.cell(2,0).value.encode('utf-8'))#获取单元格内容
    sheet2 = workbook.sheet_by_index(1)
    keys1 = []
    #得到所有文档的分词结果
    all_reports_tokens = []
    for j in range(0,2):
        for i in range(0,1):
            texts0=[]
            texts0.append(sheet1.cell(j,i).value.encode('utf-8'))
            #print(texts0)
            all_reports_tokens.append(tokenize_stopwords_stemmer(texts0))
            #print tokenize_stopwords_stemmer(texts0)
    unionwords=list(set(all_reports_tokens[0]).union(set(all_reports_tokens[1])))
    # print unionwords    #[u'being', u'memory', u'as', u'uses', u'worked', u'with', u'The', u'a', u'term', u'short', u'things', u'RAM', u'CPU', u'keeps', u'store']
    # print all_reports_tokens[0]
    # print all_reports_tokens[1]
    # print unionwords
    s1 = [0] * len(unionwords)
    s2 = [0] * len(unionwords)

    #得到第一句英文的两个向量
    for i in range(len(unionwords)):
        for j in range(len(all_reports_tokens[0])):
            if unionwords[i]==all_reports_tokens[0][j]:
                s1[i]=1
                #print unionwords[i]
    #print s1

    diff1=list(set(unionwords)-set(all_reports_tokens[0]))
    #print diff
    s11 = []
    for i in range(len(diff1)):
        for j in range(len(unionwords)):
            if diff1[i]==unionwords[j]:
                for n in range(len(all_reports_tokens[0])):
                    # print unionwords[j]
                    # print all_reports_tokens[0][n]
                    s11.append(wordsimilarity(str(unionwords[j]), str(all_reports_tokens[0][n])))
                    #print s
                    if max(s11) < 0.2:
                        s1[j] = 0
                    else:
                        s1[j] = max(s11)
    #print s1

    # 得到第二句英文的两个向量
    for i in range(len(unionwords)):
        for j in range(len(all_reports_tokens[1])):
            if unionwords[i]==all_reports_tokens[1][j]:
                s2[i]=1
                #print unionwords[i]
    #print s2

    diff2=list(set(unionwords)-set(all_reports_tokens[1]))
    #print diff2
    s22 = []
    for i in range(len(diff2)):
        for j in range(len(unionwords)):
            if diff2[i]==unionwords[j]:
                for n in range(len(all_reports_tokens[1])):
                    # print unionwords[j]
                    # print all_reports_tokens[0][n]
                    s22.append(wordsimilarity(str(unionwords[j]), str(all_reports_tokens[1][n])))
                    #print s
                    if max(s22) < 0.2:
                        s2[j] = 0
                    else:
                        s2[j] = max(s22)
    #print s2

    # 计算两个向量的点积
    x = 0
    a = 0
    while a < len(unionwords):
        x = x + s1[a] * s2[a]
        a = a + 1

    # 计算两个向量的模
    b = 0
    sq1 = 0
    while b < len(unionwords):
        sq1 = sq1 + s1[b] * s1[b]  # pow(a,2)
        b = b + 1

    c = 0
    sq2 = 0
    while c < len(unionwords):
        sq2 = sq2 + s2[c] * s2[c]
        c = c + 1

    try:
        result = float(x) / (math.sqrt(sq1) * math.sqrt(sq2))
    except ZeroDivisionError:
        result = 0.0

    return result
    # print result
    # print x
    # print math.sqrt(sq1)
    # print math.sqrt(sq2)

if __name__ == '__main__':
    main()
