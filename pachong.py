import requests
from bs4 import BeautifulSoup
import csv
import time
import re
#url='https://bugzilla.mozilla.org/buglist.cgi?product=Core&component=Audio%2FVideo%3A%20cubeb&resolution=---'
url='https://bugzilla.mozilla.org/buglist.cgi?product=Release%20Engineering&query_format=advanced&resolution=FIXED&order=changeddate%20DESC%2Cbug_status%2Cpriority%2Cassigned_to%2Cbug_id&limit=0'
#def getHTMLText(url):
r = requests.get(url, timeout=30)
r.raise_for_status()
r.encoding = r.apparent_encoding
demo = r.text
soup = BeautifulSoup(demo,'html.parser')
#labela1 = soup.find("tbody",attrs={"class":"sorttable_body"}).findAll("td",attrs={"class":"bz_changeddate_column"})
labela1 = soup.find("tbody",attrs={"class":"sorttable_body"}).findAll("td",attrs={"class":"first-child bz_id_column"})
res=r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
m = re.findall(res,demo)
# print(labela1[1].getText())
# print (m[1])
def Checktime(starttime,endtime,weibotime):
    Flag=False
    starttime=time.strptime(starttime,'%Y-%m-%d %H:%M:%S')
    endtime=time.strptime(endtime,'%Y-%m-%d %H:%M:%S')
    weibotime=time.strptime(str(weibotime),'%Y-%m-%d %H:%M:%S')
    if int(time.mktime(starttime))<= int(time.mktime(weibotime)) and int(time.mktime(endtime))>=int(time.mktime(weibotime)):
        Flag=True
    else:
        Flag=False
    return Flag
def main():
    datas=[]
    D=[]
    starttime='2016-05-31 07:34:00'
    endtime='2017-06-14 07:34:00'
    for i in range(len(m)):
        weibotime=m[i]
        a=Checktime(starttime, endtime, weibotime)
        if (a):
            D.append(labela1[i].getText())
            datas.append(D)
            datas.append(weibotime)
            # print (D)
            # print (weibotime)
    # with open('D:\\1372918 id.csv', "w", newline="") as csvfile:
    with open('./1372918 id.csv', "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['bug_id', 'bug_msg'])
        writer.writerows(datas)
        csvfile.close()

    print (D)
if __name__=='__main__':
    main()
#print (labela1)
# datas = []
# #labela1 = soup.find("tbody",attrs={"class":"sorttable_body"}).findAll("td",attrs={"class":"first-child bz_id_column"})
# labela2 = soup.find("tbody",attrs={"class":"sorttable_body"}).findAll("td",attrs={"class":"bz_short_desc_column"})
# for i in range(len(labela1)):
#     data = []
#     a = labela1[i].getText()
#     b = labela2[i].getText()
#     a = re.sub('\n', '', a)
#     b = re.sub('\n', '', b)
#     b = re.sub('\t', '', b)
#     data.append(a)
#     data.append(b)
#     print(data)
#     datas.append(data)
#
# with open('F:\\IdandMag51.csv', "w",newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['bug_id', 'bug_msg'])
#     writer.writerows(datas)
#     csvfile.close()

