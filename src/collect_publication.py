import os 
from tqdm import tqdm 
from time import time 
import requests
from lxml import html
from bs4 import BeautifulSoup
from utils import get_path_of_all_xml_file, walkData
input_file_lst = get_path_of_all_xml_file()

nctid_lst = [file.split('/')[-1].split('.')[0] for file in input_file_lst]
nctid = 'NCT03469336'

tag = "Publications automatically indexed to this study by ClinicalTrials.gov Identifier (NCT Number):"
url_prefix = 'https://clinicaltrials.gov/ct2/show/study/'

start_idx, end_idx = 300000, 350000



for nctid in tqdm(nctid_lst[start_idx:end_idx]):
	url = url_prefix + nctid
	suffix = str(start_idx)[:-3] + 'K_' + str(end_idx)[:-3] + 'K'
	t1 = time()
	page=requests.get(url)
	t2 = time() 
	if tag.lower() in page.text.lower():
		with open("ctgov_data/nctid_with_publication" + suffix + ".txt", 'a') as fout:
			fout.write(nctid + '\n')
		print(nctid)	



start_idx, end_idx = 50000, 100000
start_idx, end_idx = 100000, 150000
start_idx, end_idx = 150000, 200000
start_idx, end_idx = 200000, 250000
start_idx, end_idx = 250000, 300000
start_idx, end_idx = 300000, 350000




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








