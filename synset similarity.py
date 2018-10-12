#!usr/bin/env python
# -*- coding:utf-8 -*-


from nltk.corpus import wordnet as wn

import pandas as pd
import numpy as np
from scipy import stats

from sklearn.preprocessing import MinMaxScaler, Imputer

data = pd.read_csv("C:\Users\zw\Desktop\info.csv")
wordsList = np.array(data.iloc[:, [0, 1]])  # : 表示所有的行，[0, 1]表示第0列，第一列
print wordsList
simScore = np.array(data.iloc[:, [2]])     #[2]表示第2列

predScoreList = np.zeros((len(simScore), 1))  #生成相应大小的零矩阵,len(simScore)代表行，1代表列
print predScoreList
for i, (word1, word2) in enumerate(wordsList):  #对于一个可迭代的（iterable）/可遍历的对象（如列表、字符串），enumerate将其组成一个索引序列，利用它可以同时获得索引和值
    print "process #%d words pair [%s,%s]" % (i, word1, word2)
    count = 0
    synsets1 = wn.synsets(word1)  #获得word1的所有同义词
    synsets2 = wn.synsets(word2)
    for synset1 in synsets1:
        for synset2 in synsets2:
            score = synset1.path_similarity(synset2)  #比较synset1与synset2的同义词分数
            if score is not None:
                predScoreList[i, 0] += score
                count += 1
            # else:
            #      print synset1, "path_similarity", synset2, "is None", "==" * 10
    if  predScoreList[i, 0]!=0:
        predScoreList[i, 0] = predScoreList[i, 0] * 1.0 / count
    else:
        predScoreList[i, 0] = 0
    print(predScoreList[i, 0])
# max(predScoreList)=array([ 1.])    min(predScoreList)=array([ 0.04166667])


imp = Imputer(missing_values='NaN', strategy='mean', axis=0)  #Imputer类提供了一些基本的方法来处理缺失值，如使用均值、中位值或者缺失值所在列中频繁出现的值来替换。
impList = imp.fit_transform(predScoreList)
mms = MinMaxScaler(feature_range=(0.0, 1.0))  #MinMaxScaler类是将属性缩放到一个指定的最大和最小值之间（对数据进行标准化），使用这种方法的目的包括：1、对于方差非常小的属性可以增强其稳定性。2、维持稀疏矩阵中为0的条目。
impMmsList = mms.fit_transform(impList)
# max(impMmsList)=array([ 10.])    min(impMmsList)=array([ 0.])  最大值是10，最小值是0
# impMmsList.mean()=0.74249450173161169
# print(simScore)
# print(impMmsList)
(coef1, pvalue) = stats.spearmanr(simScore, impMmsList)  #计算Spearman排序相关系数和p值以测试非相关性。
# (correlation=0.3136469783526708, pvalue=1.6943792485183932e-09)
# print((coef1, pvalue))

submitData = np.hstack((wordsList, simScore, impMmsList))  #np.hstack按顺序堆叠数组（按列方式）。
e=(pd.DataFrame(submitData)).to_csv("C:\Users\zw\Desktop\wordnet.csv", index=False,  #将DataFrame写入逗号分隔值（csv）文件
                                  header=["Word1", "Word2", "OriginSimilarity", "PredSimilarity"])
