#coding=utf-8
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#针对所有词性的词，求同词性之间的相似度

from __future__ import division
from nltk.corpus import wordnet
import math
import os
import nltk
from nltk.stem.porter import PorterStemmer
# x = wordnet.synsets('boy')[0]
# y = wordnet.synsets('person')[0]
# print (x.shortest_path_distance(y))  #两个词的最短路径
# print x.lowest_common_hypernyms(y)   #两个词的最小公共上位词
# print y.min_depth()     #得到一个词的深度
# print y.hypernyms()     #得到一个词的所有上位词
# print  y.root_hypernyms()   #得到一个词的（最一般d）根上位词
def wordsimilarity(str1,str2):
    a = 0.1
    b = 0.5
    L = []
    C = []
    S = []
    pos1=['NN','NNS','NNP','NNPS']
    pos2=['VB','VBD','VBN','VBP','VBZ','VBG']
    pos3=['JJ','JJR','JJS']
    pos4 = ['RB', 'RBR', 'RBS']
    words11 = nltk.word_tokenize(str1)
    word_tag1 = nltk.pos_tag(words11)
    words12 = nltk.word_tokenize(str2)
    word_tag2 = nltk.pos_tag(words12)
    #if ((word_tag1[0][1] in pos1 and word_tag2[0][1] in pos1) or (word_tag1[0][1] in pos2 and word_tag2[0][1] in pos2) or (word_tag1[0][1] in pos3 and word_tag2[0][1] in pos3) or (word_tag1[0][1] in pos4 and word_tag2[0][1] in pos4) or (word_tag1[0][1]==word_tag2[0][1])):
    if (word_tag1[0][1]==word_tag2[0][1]):
        word1 = wordnet.synsets(str1)
        word2 = wordnet.synsets(str2)
        for i in range(len(word1)):
            for j in range(len(word2)):
                if word1[i].shortest_path_distance(word2[j]) != None:
                    L.append(word1[i].shortest_path_distance(word2[j]))
                else:
                    pass
        if L == []:
            s = 0
            # print '1234'
            return s
        else:
            l = min(L)  # 两个词的最短路径距离
            # print l
            e = math.exp(-a * l)
            for i in range(len(word1)):
                for j in range(len(word2)):
                    if (word1[i].shortest_path_distance(word2[j]) == l):
                        # print word1[i]
                        # print word2[j]
                        w = word1[i].lowest_common_hypernyms(word2[j])
                        # print w
                        for n in range(len(w)):
                            w0 = w[0].min_depth()
                            if w[n].min_depth() > w0:
                                w0 = w[n].min_depth()
                                # print w0
                            C.append(w0)

            if C == []:
                s = 0
                return s
            else:
                c = max(C)  # 两个词的最小公共上位词的最大深度
                for i in range(len(word1)):
                    for j in range(len(word2)):
                        if (word1[i].shortest_path_distance(word2[j]) == l):
                            w = word1[i].lowest_common_hypernyms(word2[j])
                            for n in range(len(w)):
                                if w[n].min_depth() == c:
                                    d1 = word1[i].min_depth()
                                    d2 = word2[j].min_depth()
                                    if d1 == 0:
                                        s = 0
                                        return s
                                    if d2 == 0:
                                        s = 0
                                        return s
                                    else:
                                        sim = e * b * (c / d1 + c / d2)
                                        S.append(sim)
        s = max(S)
        return s
    else:
        return 0





def main():
    str1='called'
    str2='evidence'
    s1=wordsimilarity(str1,str2)
    print s1


if __name__ == '__main__':
    main()