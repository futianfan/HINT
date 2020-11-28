# -*- coding: utf-8 -*- 

'''

input: 	9k data ?  
	1. ctgov_data/raw_data.csv 

nctid,status,why_stop,label,phase,diseases,icdcodes,drugs,smiless,criteria

processing:  
	1. phase I
	2. phase II
	3. phase III
	4. indication 
	5. train/test split 


output:
	1. ctgov_data/phase_I.csv 
	2. ctgov_data/phase_II.csv 
	3. ctgov_data/phase_III.csv 
	4. ctgov_data/trial.csv 

requires ~10 minutes. 

'''

import csv 
# from random import shuffle 
## no shuffle 
from functools import reduce


from ccs_utils import file2_icd2ccs_and_ccs2description, file2_icd2ccsr
# icd2ccs, ccscode2description = file2_icd2ccs_and_ccs2description() 
icd2ccsr = file2_icd2ccsr()


def csvfile2rows(input_file):
	with open(input_file, 'r') as csvfile:
		rows = list(csv.reader(csvfile, delimiter = ','))[1:]
	return rows 

def filter_phase_I(row):
	if "phase 1" in row[4]:
		return True	
	## enhance 
	if int(row[3])==1 and row[4]=='phase 4':
		return True 

	return False 

def filter_phase_II(row):
	phase = row[4] 
	label = int(row[3])

	if "phase 2" in row[4]:
		return True
	## enhance
	if int(row[3])==1 and 'phase 4' in row[4]:
		return True

	return False

def filter_phase_III(row):
	if "phase 3" in row[4]:
		return True
	### enhance 
	if "phase 4" in row[4] and int(row[3])==1:
		return True
	if int(row[3])==0 and row[4] =='phase 2':
		return True 
	return False 

def filter_trial(row):
	label = int(row[3])
	if label == 0 and ('phase 1' in row[4] or 'phase 2' in row[4]):
		return True 
	if ('phase 3' in row[4] or 'phase 4' in row[4]) and label==1:  ### label == 1
		return True 
	return False 

# def filter_chronic(row):
# 	if 'chronic' in row[5]:
# 		return True 
# 	return False 

# def filter_cardio(row):
# 	if 'cardio' in row[5]:
# 		return True 
# 	return False 

# def filter_cancer(row):
# 	if 'cancer' in row[5] or 'neoplasm' in row[5] or 'tumor' in row[5]:
# 		return True 
# 	return False 

# def filter_pain(row):
# 	if 'pain' in row[5]:
# 		return True 
# 	return False 

def icdcode_text_2_lst_of_lst(text):
	text = text[2:-2]
	lst_lst = []
	for i in text.split('", "'):
		i = i[1:-1]
		lst_lst.append([j.strip()[1:-1] for j in i.split(',')])
	return lst_lst 

def row2icdcodelst(row):
	icdcode_text = row[6]
	icdcode_lst2 = icdcode_text_2_lst_of_lst(icdcode_text)
	icdcode_lst = reduce(lambda x,y:x+y, icdcode_lst2)
	icdcode_lst = [i.replace('.', '') for i in icdcode_lst]
	return icdcode_lst 

# def filter_cancer(row):
# 	icdcode_text = row[6]
# 	icdcode_lst2 = icdcode_text_2_lst_of_lst(icdcode_text)
# 	icdcode_lst = reduce(lambda x,y:x+y, icdcode_lst2)
# 	icdcode_lst = [i.replace('.', '') for i in icdcode_lst]
# 	for icdcode in icdcode_lst:
# 		try:
# 			ccs = icd2ccs[icdcode]
# 			description = ccscode2description[ccs].lower() 	
# 			if 'cancer' in description or 'neoplasm' in description:
# 				return True 
# 		except:
# 			pass 
# 	return False 


# def filter_heart(row):
# 	icdcode_text = row[6]
# 	icdcode_lst2 = icdcode_text_2_lst_of_lst(icdcode_text)
# 	icdcode_lst = reduce(lambda x,y:x+y, icdcode_lst2)
# 	icdcode_lst = [i.replace('.', '') for i in icdcode_lst]
# 	for icdcode in icdcode_lst:
# 		try:
# 			ccs = icd2ccs[icdcode]
# 			description = ccscode2description[ccs].lower() 	
# 			if 'heart' in description:
# 				return True 
# 		except:
# 			pass 
# 	return False 

# def filter_infection(row):
# 	icdcode_text = row[6]
# 	icdcode_lst2 = icdcode_text_2_lst_of_lst(icdcode_text)
# 	icdcode_lst = reduce(lambda x,y:x+y, icdcode_lst2)
# 	icdcode_lst = [i.replace('.', '') for i in icdcode_lst]
# 	for icdcode in icdcode_lst:
# 		try:
# 			ccs = icd2ccs[icdcode]
# 			description = ccscode2description[ccs].lower() 	
# 			if 'infect' in description:
# 				return True 
# 		except:
# 			pass
# 	return False 



# def filter_disorder(row):
# 	icdcode_text = row[6]
# 	icdcode_lst2 = icdcode_text_2_lst_of_lst(icdcode_text)
# 	icdcode_lst = reduce(lambda x,y:x+y, icdcode_lst2)
# 	icdcode_lst = [i.replace('.', '') for i in icdcode_lst]
# 	for icdcode in icdcode_lst:
# 		try:
# 			ccs = icd2ccs[icdcode]
# 			description = ccscode2description[ccs].lower() 	
# 			if 'disorder' in description:
# 				return True 
# 		except:
# 			pass 
# 	return False 

def filter_nervous(row):
	icdcode_lst = row2icdcodelst(row)
	for icdcode in icdcode_lst:
		try:
			ccsr = icd2ccsr[icdcode]
			if ccsr == 'NVS':
				return True 
		except:
			pass 
	return False 


def filter_infect(row):
	icdcode_lst = row2icdcodelst(row)
	for icdcode in icdcode_lst:
		try:
			ccsr = icd2ccsr[icdcode]
			if ccsr == 'INF':
				return True 
		except:
			pass 
	return False 


def filter_respiratory(row):
	icdcode_lst = row2icdcodelst(row)
	for icdcode in icdcode_lst:
		try:
			ccsr = icd2ccsr[icdcode]
			if ccsr == 'RSP':
				return True 
		except:
			pass 
	return False 

def filter_digest(row):
	icdcode_lst = row2icdcodelst(row)
	for icdcode in icdcode_lst:
		try:
			ccsr = icd2ccsr[icdcode]
			if ccsr == 'DIG':
				return True 
		except:
			pass 
	return False 




def write_row_to_csvfile(rows, fieldname, output_file):
	with open(output_file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldname)
		writer.writeheader()	
		for row in rows:
			dic = {k:row[i] for i,k in enumerate(fieldname)}
			writer.writerow(dic)
	return	



def split_data(rows, train_valid_test_ratio):
	n = len(rows)
	train_num = int(n*train_valid_test_ratio[0])
	valid_num = int(n*train_valid_test_ratio[1])	
	train_row = rows[:train_num]
	valid_row = rows[train_num:train_num + valid_num]
	test_row = rows[train_num + valid_num:]
	return train_row, valid_row, test_row


def check_pos_and_neg(rows):
	pos_cnt, neg_cnt = 0, 0
	for row in rows:
		if int(row[3])==1:
			pos_cnt += 1
		elif int(row[3])==0:
			neg_cnt += 1
	print("pos: ", pos_cnt, " neg:", neg_cnt)

def select_and_split_data(input_file, filter_func, output_file_name, train_valid_test_ratio = [0.7,0.1,0.2]):
	rows = csvfile2rows(input_file)
	rows = list(filter(filter_func, rows))
	# shuffle(rows)
	positive_num = len(list(filter(lambda x:int(x[3])==1, rows)))
	negative_num = len(rows) - positive_num 
	print("\t\tpos =", str(positive_num), "  neg =", str(negative_num))
	train_row, valid_row, test_row = split_data(rows, train_valid_test_ratio)
	fieldname = ['nctid', 'status', 'why_stop', 'label', 'phase', 
				 'diseases', 'icdcodes', 'drugs', 'smiless', 'criteria']

	print("train")
	check_pos_and_neg(train_row)
	print("valid")
	check_pos_and_neg(valid_row)
	print("test")
	check_pos_and_neg(test_row)
	output_file = output_file_name.replace('.csv', '_train.csv')
	write_row_to_csvfile(train_row, fieldname, output_file)
	output_file = output_file_name.replace('.csv', '_valid.csv')
	write_row_to_csvfile(valid_row, fieldname, output_file)
	output_file = output_file_name.replace('.csv', '_test.csv')
	write_row_to_csvfile(test_row, fieldname, output_file)

	# subset_test_row = list(filter(filter_chronic, test_row))
	# output_file = output_file_name.replace('.csv', '_chronic_test.csv')
	# write_row_to_csvfile(subset_test_row, fieldname, output_file)

	# subset_test_row = list(filter(filter_cardio, test_row))
	# output_file = output_file_name.replace('.csv', '_cardio_test.csv')
	# write_row_to_csvfile(subset_test_row, fieldname, output_file)

	# subset_test_row = list(filter(filter_cancer, test_row))
	# output_file = output_file_name.replace('.csv', '_cancer_test.csv')
	# write_row_to_csvfile(subset_test_row, fieldname, output_file)

	# subset_test_row = list(filter(filter_pain, test_row))
	# output_file = output_file_name.replace('.csv', '_pain_test.csv')
	# write_row_to_csvfile(subset_test_row, fieldname, output_file)

	# subset_test_row = list(filter(filter_cancer, test_row))
	# output_file = output_file_name.replace('.csv', '_cancer_test.csv')
	# write_row_to_csvfile(subset_test_row, fieldname, output_file)

	# subset_test_row = list(filter(filter_infection, test_row))
	# output_file = output_file_name.replace('.csv', '_infection_test.csv')
	# write_row_to_csvfile(subset_test_row, fieldname, output_file)

	# subset_test_row = list(filter(filter_disorder, test_row))
	# output_file = output_file_name.replace('.csv', '_disorder_test.csv')
	# write_row_to_csvfile(subset_test_row, fieldname, output_file)

	# subset_test_row = list(filter(filter_heart, test_row))
	# output_file = output_file_name.replace('.csv', '_heart_test.csv')
	# write_row_to_csvfile(subset_test_row, fieldname, output_file)



	subset_test_row = list(filter(filter_respiratory, test_row))
	output_file = output_file_name.replace('.csv', '_respiratory_test.csv')
	write_row_to_csvfile(subset_test_row, fieldname, output_file)

	subset_test_row = list(filter(filter_infect, test_row))
	output_file = output_file_name.replace('.csv', '_infection_test.csv')
	write_row_to_csvfile(subset_test_row, fieldname, output_file)

	subset_test_row = list(filter(filter_nervous, test_row))
	output_file = output_file_name.replace('.csv', '_nervous_test.csv')
	write_row_to_csvfile(subset_test_row, fieldname, output_file)

	subset_test_row = list(filter(filter_digest, test_row))
	output_file = output_file_name.replace('.csv', '_digest_test.csv')
	write_row_to_csvfile(subset_test_row, fieldname, output_file)



	return



if __name__ == "__main__":
	input_file = 'ctgov_data/raw_data.csv'

	print("\tphase I")
	select_and_split_data(input_file, filter_phase_I, 'ctgov_data/phase_I.csv')
	print("\tphase II")
	select_and_split_data(input_file, filter_phase_II, 'ctgov_data/phase_II.csv')
	print("\tphase III")
	select_and_split_data(input_file, filter_phase_III, 'ctgov_data/phase_III.csv')
	print("\tindication")
	select_and_split_data(input_file, filter_trial, 'ctgov_data/trial.csv')




'''
origin 
	phase I
		pos = 997   neg = 558
	phase II
		pos = 1069   neg = 2377
	phase III
		pos = 2399   neg = 1458
	indication
		pos = 3146   neg = 2146





'''








