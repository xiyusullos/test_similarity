#!usr/bin/env python
# -*- coding:utf-8 -*-
from nltk.corpus import wordnet as wn
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import MinMaxScaler, Imputer

wordsList = [u'comment', u'version', u'give', u'yeah', u'result', u'fail', u'differ', u'end', u'make']#,
                 # u'upgrad', u'binari', u'enough', u'much', u'master', u'build', u'sens', u'save', u'worth', u'minor',
                 # u'given', u'specifi', u'js', u'repo', u'link', u'commit', u'releas', u'affect', u'exact', u'cach',
                 # u'pull', u'github', u'request', u'push', u'x', u'effect', u'latest']
#simScore = np.array(data.iloc[:, [2]])     #[2]表示第2列

predScoreList = np.zeros((36, 1))  #生成相应大小的零矩阵,len(simScore)代表行，1代表列
# for i in range(1,len(wordsList)):
#     if len(wn.synsets(wordsList[i])) == 0:
#         wordsList.remove(wordsList[i])
synsets=[]
for i in range(len(wordsList)):
    synsets.append(wn.synsets(wordsList[i]))
#print synsets
for i in range(len(wordsList)-1):  #列表中相互两个词之间的同义词相似度
    for j in range(len(wordsList)):
        count = 0
        for synset1 in synsets[i]:
            for synset2 in synsets[j]:
                score = synset1.path_similarity(synset2)
                if score is not None:
                    predScoreList[i, 0] += score
                    count += 1
        if predScoreList[i, 0] != 0:
            predScoreList[i, 0] = predScoreList[i, 0] * 1.0 / count
        else:
            predScoreList[i, 0] = 0
print predScoreList  #结果如下
#[[ 0.1087822 ]
 # [        inf]
 # [ 0.15136734]
 # [        inf]
 # [ 0.16405374]
 # [ 0.19658152]
 # [ 0.22401664]
 # [ 0.17379964]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]
 # [ 0.        ]]

#下面可能有错
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
e=(pd.DataFrame(submitData)).to_csv("C:\Users\zw\Desktop\net.csv", index=False,  #将DataFrame写入逗号分隔值（csv）文件
                                  header=["Word1", "Word2", "OriginSimilarity", "PredSimilarity"])


