import os 
from tqdm import tqdm 
from time import time 
import requests, json
# from lxml import html
from bs4 import BeautifulSoup

output_folder = 'nctid_publication_abstract'
input_file = 'nctid_publication_abstract/nctid2puburl.txt'
with open(input_file, 'r') as fin:
	lines = fin.readlines() 
nctid_puburl = [(line.split()[0],line.strip().split()[1]) for line in lines]	

url = 'https://clinicaltrials.gov/ct2/bye/rQoPWwoRrXS9-i-wudNgpQDxudhWudNzlXNiZip9Ei7ym67VZR0VLgFBOK4jA6h9Ei4L3BUgWwNG0it.'


def search_node(node):
	if node.name != 'p':
		return False, 
	flag = False
	for i in node.children:
		if i.name == 'strong' and ":" in i.text.strip():
			flag = True
			tag = i.text.strip() 
	if not flag:
		return False, 
	for i in node.children:
		if i.name is None and len(i.strip()) > 30:
			return tag, i.strip() 
	return False,


def top_down_traverse(node, text_lst):
	for i in node.children:
		if i is None or len(str(i).strip()) == 0:
			continue
		if i.name is not None:
			new_text_lst = []
			top_down_traverse(i, new_text_lst)
			text_lst.extend(new_text_lst)

		result = search_node(i)
		if len(result)==1:
			continue 
		assert len(result)==2
		text = result[0] + '\t\t' + result[1] + '\n\n'
		text_lst.append(text)




def url2text(url):
	global cnt
	cnt = 0  
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'lxml')
	text_lst = []
	top_down_traverse(soup, text_lst)

	return text_lst



# text_lst = url2tree(url)
# for i in text_lst:
# 	print(i)

start_idx, end_idx = 50000, 60000
for nctid, url in tqdm(nctid_puburl[start_idx:end_idx]):
	print(nctid)
	text_lst = url2text(url)
	output_file = os.path.join(output_folder, nctid + '.txt')
	with open(output_file, 'w') as fout:
		for text in text_lst:
			fout.write(text)











