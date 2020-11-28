import os 
from tqdm import tqdm 
from time import time 
import requests, json
from lxml import html
from bs4 import BeautifulSoup


'''
1. nctid -> paper's url 

2. paper's url -> abstract 

'''

nctid = 'NCT03469336'

tag = "Publications automatically indexed to this study by ClinicalTrials.gov Identifier (NCT Number):"
url_prefix = 'https://clinicaltrials.gov/ct2/show/study/'
url_prefix2 = 'https://clinicaltrials.gov'
start_idx, end_idx = 25590, 60000 
nctid_file = 'ctgov_data/nctid_with_publication.txt' ### 59977 
nctid2publication_url_file = './nctid_publication_abstract/nctid2puburl_' + str(start_idx) + '_' + str(end_idx) + '.txt'

with open(nctid_file, 'r') as fin:
	lines = fin.readlines()
nctid_lst = [line.strip() for line in lines]

# headers = {'Content-Type': 'application/json'}
# url = 'https://clinicaltrials.gov/ct2/show/study/NCT03469336'
'''
https://clinicaltrials.gov/ct2/show/study/NCT03469336

https://clinicaltrials.gov/ct2/bye/rQoPWwoRrXS9-i-wudNgpQDxudhWudNzlXNiZip9Ei7ym67VZRFn-g0wcgF5A6h9Ei4L3BUgWwNG0it.
'''

# page = requests.get(url, headers=headers)
# texts = requests.get(url).text.split('\n')
# json.loads(page.text)

def page2url(page):
	texts = page.text.split('\n')
	for idx, sentence in enumerate(texts):
		if tag.lower() in sentence.lower():
			break 
	for sentence in texts[idx+1:]: 
		if '<a href=' in sentence:
			break 
	index_1 = sentence.index('"')
	sentence = sentence[index_1+1:]
	index_1 = sentence.index('"')
	sentence = sentence[:index_1]
	url = url_prefix2 + sentence 
	return url

for nctid in tqdm(nctid_lst[start_idx:end_idx]):
	url = url_prefix + nctid
	page = requests.get(url)
	try:
		puburl = page2url(page)
		with open(nctid2publication_url_file, 'a') as fout:
			fout.write(nctid + '\t' + puburl + '\n')
	except:
		pass 



# # page=requests.Session().get(url) 
# page=requests.get(url)
# ##  <class 'requests.models.Response'>

# tree=html.fromstring(page.text) 
# result=tree.xpath('//td[@class="title"]//a/text()') 

# text = page.text

# for idx, i in enumerate(text.split('\n')):
# 	if "publications automatically" in i.lower():
# 		idx_o = idx 
# 		break 

# for i in range(idx_o, idx_o + 5):
# 	print(text.split('\n')[i])








