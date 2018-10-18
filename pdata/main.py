import requests
from bs4 import BeautifulSoup
import sqlite3
from patchModel import PatchModel
import re

s = requests.Session()


def download(name, model):
    # with open(name + ".patch", 'w') as f:
    #     text = s.get('https://github.com/elastic/elasticsearch/commit/' + name + '.patch').text
    #     f.write(text)
    model.patch = s.get('https://github.com/elastic/elasticsearch/commit/' + name + '.patch').text
    # print(model.bugReportURL, model.commitSHA1)
    curs.execute("insert into patchtable values(?,?,?,?)", (model.bugReportURL, model.info, model.commitSHA1, model.patch))
    conn.commit()


def crawler_in_one_issue(partOfUrl):
    url = "https://github.com" + partOfUrl
    htmlAccept = s.get(url)
    soup = BeautifulSoup(htmlAccept.text, 'html.parser')
    i = soup.select('svg.octicon.octicon-check.v-align-middle')
    if i == []:
        # print('meizhaodaogou')
        return
    else:
        # print(len(i))
        patchModel = PatchModel()
        patchModel.bugReportURL = url
        patchModel.info =  soup.select('span.js-issue-title')[0].text.replace("\n", '')[8:-6]
        ineed = i[0].parent.parent.parent.parent
        commiturl = ineed.select('.commit-id')[0]["href"]
        sha1 = commiturl.split('/')[4]
        patchModel.commitSHA1 = sha1
        # print(commiturl.split('/')[4])
        # print(commiturl)
        download(sha1, patchModel)


conn = sqlite3.connect('./elasticsearchDiff.db')
curs = conn.cursor()
for page in range(50, 55):
    url = 'https://github.com/elastic/elasticsearch/issues?q=is%3Aissue+label%3A>bug+is%3Aclosed&page=' + str(page)
    print(url)
    try:
        htmlAccept = s.get(url)
    except:
        continue
    soup = BeautifulSoup(htmlAccept.text, 'html.parser')
    soup = soup.select('.link-gray-dark.v-align-middle.no-underline.h4.js-navigation-open')
    for i in soup:
        print(i["href"])
        crawler_in_one_issue(i["href"])



curs.close()
conn.close()
