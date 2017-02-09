#!/usr/bin/env python3
from urllib import parse
import sys
import bs4 as bs
import urllib.request
import math
import threading
from queue import Queue

def problemURL(contest):
  sauce = urllib.request.urlopen('http://codeforces.com/contest/'+str(contest)).read()
  soup = bs.BeautifulSoup(sauce, 'lxml')

  l = []
  probs = soup.find("table", class_="problems")
  for links in probs.find_all('a', href=True):
    text = ''.join(links.get_text().split())
    if len(text) == 1:
      l.append((parse.urljoin("http://codeforces.com",links['href'])))
  return l


def extractIO(soup, io):
    data = soup.find_all("div", class_=io+"put")
    problem = soup.title.get_text().split()[2]

    for i,datas in enumerate(data):
      datas = datas.find("pre")
      f = open(problem+str((int)(i))+"."+io, 'w')
      f.write(datas.get_text(separator="\n"))
      f.close()

def extractData(url):
  sauce = urllib.request.urlopen(url).read()
  soup = bs.BeautifulSoup(sauce, 'lxml')
  extractIO(soup, "in")
  extractIO(soup, "out")

NUMBER_OF_THREADS = 4
queue = Queue()

def create_workers():
  for _ in range(NUMBER_OF_THREADS):
    t = threading.Thread(target=work)
    t.daemon = True
    t.start()

def work():
  while True:
    url = queue.get()
    print(url)
    extractData(url)
    queue.task_done()

def create_jobs(num):
  for link in problemURL(num):
    queue.put(link)

create_jobs(sys.argv[1])
create_workers()
while(not queue.empty()):
  pass
