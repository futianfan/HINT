import os 
from tqdm import tqdm 
from time import time 
import requests, json
# from lxml import html
from bs4 import BeautifulSoup
from html2json import html2json 

# output_folder = 'nctid_publication_abstract'
# input_file = 'nctid_publication_abstract/nctid2puburl.txt'
# with open(input_file, 'r') as fin:
# 	lines = fin.readlines() 
# nctid_puburl = [(line.split()[0],line.strip().split()[1]) for line in lines]	


# def xml_to_dict(xml_data):
#     """
#     xml转换为字典
#     :param xml_data:
#     :return:
#     """
#     # soup = BeautifulSoup(xml_data, features='xml') ##
#     soup = BeautifulSoup(xml_data.text, features='xml') ##
#     xml = soup.find('xml')
#     if not xml:
#         return {}
#     # 将 XML 数据转化为 Dict
#     data = dict([(item.name, item.text) for item in xml.find_all()])
#     return data

url = 'https://clinicaltrials.gov/ct2/show/study/NCT03469336'
text = 'We investigated changes in anisometropia and aniso-axial length with myopia progression in the Correction of Myopia Evaluation Trial (COMET) cohort.'
text2 = 'ired anisometropia (interocular difference in spherical equivalent refraction) '
nctid = 'NCT00000113'
url = 'https://clinicaltrials.gov/ct2/bye/rQoPWwoRrXS9-i-wudNgpQDxudhWudNzlXNiZip9Ei7ym67VZR0VLgFBOK4jA6h9Ei4L3BUgWwNG0it.'
url = 'https://clinicaltrials.gov/ct2/bye/rQoPWwoRrXS9-i-wudNgpQDxudhWudNzlXNiZip9Ei7ym67VZRFjWR0jagCwA6h9Ei4L3BUgWwNG0it.'
# headers = {'accept': 'application/json', 'content-type':'application/json'}
# page = requests.get(url)
# # soup = BeautifulSoup(page.text)
# html_file = BeautifulSoup(page.text, "html.parser")
# soup = BeautifulSoup(page.text, 'lxml')
# idxlst = [idx for idx,i in enumerate(list(soup.html.body.children)) if i.name is None]
# [list(soup.html.body.children)[i] for i in idxlst]


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




# dic = xml_to_dict(page)

# texts = page.text.split('\n')
# for idx, sentence in enumerate(texts):
# 	if 'abstract' in sentence.lower():
# 		abs_idx = idx
# 		print(idx, sentence)
cnt = 0 
def top_down_traverse(node, dic):
	global cnt 
	for i in node.children:
		if i is None or len(str(i).strip()) == 0:
			continue
		if i.name is not None:
			newdict = {}
			top_down_traverse(i, newdict)
			dic[i.name] = newdict
			if 'abstract' in i.name.lower():
				# print("AAAAA ", cnt, i.name)
				pass 
		else:
			dic["leaf_node__"+i] = {}
			if 'abstract' in i.lower():
				# print("BBBBB ", cnt, i)
				pass
			if text.lower() in i.lower():
				# print("CCCCC ",cnt, i)
				pass
			if text2.lower() in i.lower():
				# print("CCCCC ",cnt, i)	
				pass 			
		cnt += 1

		# if 2128 <= cnt <= 2154:
		# 	print(cnt, '>>>>', i.name, '>>>>', i)

		# if i.name == 'p' and 'id="abstract"' in str(i):
		# 	print(cnt, '>>>>', i.name, '>>>>', i)

		result = search_node(i)
		if len(result)==2:
			print(result[0], '\t\t\t', result[1], '\n\n')
		# if i.name == 'strong' and ":" in i.text: #and str(i.content).strip() == 'Conclusions:': 
		# 	print(cnt, i.text.strip())
'''
2129 Purpose:
2133 Methods:
2137 Results:
2141 Conclusions:
2149 Keywords:
'''



def url2tree(url):
	global cnt
	cnt = 0  
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'lxml')
	dic = {}
	top_down_traverse(soup, dic)
	return dic 



dic = url2tree(url)
# print(dic)















