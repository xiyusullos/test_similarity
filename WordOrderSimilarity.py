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
# import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import csv
import pandas as pd
from string import punctuation
from WordsSimilarityCalculationModel import wordsimilarity

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

    # stopwords
    english_stopwords =stopwords.words('english')  # 得到停词
    texts_filtered_stopwords = [document for document in texts_filtered if not document in english_stopwords]  # 过滤掉停词

    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '\n', '||',
                            '<', '>', '/', '\"', '\'', '{', '}', '!', '~', '`', '0', '$', '^', '/*', '*/', '/**', '**/',
                            '**', '-', '_', '__', '|', '+', '=', r'-?-', r'@?']  # 得到标点

    texts_filtered = [document for document in texts_filtered_stopwords if
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

    #print all_reports_tokens[0]

    pos=['NN','NNS','NNP','NNPS','VB','VBD','VBN','VBP','VBZ','VBG']
    all_reports_tokens = []
    for j in range(0,2):
        for i in range(0,1):
            texts0=[]
            texts0.append(sheet1.cell(j,i).value.encode('utf-8'))
            #print(texts0)
            all_reports_tokens.append(tokenize_stopwords_stemmer(texts0))
    #print  all_reports_tokens[0]
    l1 = []
    for i in range(len(all_reports_tokens[0])):
        words = nltk.word_tokenize(all_reports_tokens[0][i])
        word_tag = nltk.pos_tag(words)
        for j in range(len(pos)):
            if word_tag[0][1]==pos[j]:
                l1.append(all_reports_tokens[0][i])


    l2 = []
    for i in range(len(all_reports_tokens[1])):
        words = nltk.word_tokenize(all_reports_tokens[1][i])
        word_tag = nltk.pos_tag(words)
        for j in range(len(pos)):
            if word_tag[0][1] == pos[j]:
                l2.append(all_reports_tokens[1][i])
    # print l1
    # print l2

    L=set(l1)&set(l2)
    ham12=len(l1)
    print L
    t2 = 0
    for i in range(len(l1)):
        if l1[i] in L:
            ham12=ham12-1
            #print ham12
            #print l1[i]
            for j in range(len(l2)):
                if l2[j]==l1[i]:
                    t2=j
            for i in range(0,t2):
                if l2[i] in L:
                    L.remove(l2[i])
        else:
            if l1[i] not in L:
                #print t2
                s = []
                for j in range(t2,len(l2)):
                    s.append(wordsimilarity(l1[i], l2[j]))
                if s != []:
                    if max(s) > 0.2:
                        ham12 = ham12 - 1
                        for j in range(t2, len(l2)):
                            if wordsimilarity(l1[i], l2[j]) == max(s):
                                t2 = j
                                for i in range(0, t2):
                                    if l2[i] in L:
                                        L.remove(l2[i])
                else:
                    ham12=min(len(l1),len(l2))


    #print ham12

    ham21 = len(l2)
    # print L
    t1 = 0
    for i in range(len(l2)):
        if l2[i] in L:
            ham21 = ham21 - 1
            # print ham12
            # print l1[i]
            for j in range(len(l1)):
                if l1[j] == l2[i]:
                    t1 = j
            for i in range(0, t1):
                if l1[i] in L:
                    L.remove(l1[i])
        else:
            if l2[i] not in L:
                # print t2
                s1 = []
                for j in range(t1, len(l1)):
                    s1.append(wordsimilarity(l2[i], l1[j]))
                if s1!=[]:
                    if max(s1) > 0.2:
                        ham21 = ham21 - 1
                        for j in range(t1, len(l1)):
                            if wordsimilarity(l2[i], l1[j]) == max(s1):
                                t1 = j
                                for i in range(0, t1):
                                    if l1[i] in L:
                                        L.remove(l1[i])
                else:
                    ham21 = min(len(l1), len(l2))






    #print ham21

    m=min(ham12,ham21)
    n=min(len(l1),len(l2))
    sim=1-m/n
    return sim
    # print n
    #print L

    #return sim




    # words = nltk.word_tokenize(all_reports_tokens[0][1])  求一个单词的词性
    # print(words)
    # word_tag = nltk.pos_tag(words)
    # print(word_tag[0][1])

if __name__ == '__main__':
    main()