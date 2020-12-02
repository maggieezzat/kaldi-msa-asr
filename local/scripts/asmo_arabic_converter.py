# -*- coding: utf-8 -*-
from __future__ import division
import sys
from multiprocessing import Pool, cpu_count
from os import listdir, makedirs
import os

def conv_arab(line):
	words = line.strip().split(' ')
	temp_line=''
	for word in words:
		if word == 'L191':
			arab_word = '0'
		elif word == 'L192':
			arab_word = '1'
		elif word == 'L193':
			arab_word = '2'
		elif word == 'L194':
			arab_word = '3'
		elif word == 'L195':
			arab_word = '4'
		elif word == 'L196':
			arab_word = '5'
		elif word == 'L197':
			arab_word = '6'
		elif word == 'L198':
			arab_word = '7'
		elif word == 'L199':
			arab_word = '8'
		elif word == 'L200':
			arab_word = '9'
		elif word == 'L201':
			arab_word = '،'
		elif word == 'L202':
			arab_word = ':'
		elif word == 'L203':
			arab_word = '؛'
		elif word == 'L204':
			arab_word = '-'
		elif word == 'L205':
			arab_word = '+'
		elif word == 'L206':
			arab_word = '*'
		elif word == 'L207':
			arab_word = '('
		elif word == 'L208':
			arab_word = ''
		elif word == 'L209':
			arab_word = '='
		elif word == 'L210':
			arab_word = '%'
		elif word == 'L211':
			arab_word = '!'
		elif word == 'L212':
			arab_word = '/'
		elif word == 'L213':
			arab_word = '"'
		elif word == 'L214':
			arab_word = '؟'
		elif word == 'L215':
			arab_word = '.'
		elif word == ' ':
			arab_word = ' '
		elif word == 'L342':
			pass
		else:
			arab_word = word
		temp_line += (arab_word + ' ') 
		
		out_line = ''
		for letter in temp_line:
			if letter == 'A':
				out_line += 'ء'
			elif letter == 'B':
				out_line += 'آ'
			elif letter == 'C':
				out_line += 'أ'
			elif letter == 'D':
				out_line += 'ؤ'
			elif letter == 'E':
				out_line += 'إ'
			elif letter == 'F':
				out_line += 'ئ'
			elif letter == 'G':
				out_line += 'ا'
			elif letter == 'H':
				out_line += 'ب'
			elif letter == 'I':
				out_line += 'ة'
			elif letter == 'J':
				out_line += 'ت'
			elif letter == 'K':
				out_line += 'ث'
			elif letter == 'L':
				out_line += 'ج'
			elif letter == 'M':
				out_line += 'ح'
			elif letter == 'N':
				out_line += 'خ'
			elif letter == 'O':
				out_line += 'د'
			elif letter == 'P':
				out_line += 'ذ'
			elif letter == 'Q':
				out_line += 'ر'
			elif letter == 'R':
				out_line += 'ز'
			elif letter == 'S':
				out_line += 'س'
			elif letter == 'T':
				out_line += 'ش'
			elif letter == 'U':
				out_line += 'ص'
			elif letter == 'V':
				out_line += 'ض'
			elif letter == 'W':
				out_line += 'ط'
			elif letter == 'X':
				out_line += 'ظ'
			elif letter == 'Y':
				out_line += 'ع'
			elif letter == 'Z':
				out_line += 'غ'
			elif letter == 'a':
				out_line += 'ف'
			elif letter == 'b':
				out_line += 'ق'
			elif letter == 'c':
				out_line += 'ك'
			elif letter == 'd':
				out_line += 'ل'
			elif letter == 'e':
				out_line += 'م'
			elif letter == 'f':
				out_line += 'ن'
			elif letter == 'g':
				out_line += 'ه'
			elif letter == 'h':
				out_line += 'و'
			elif letter == 'i':
				out_line += 'ى'
			elif letter == 'j':
				out_line += 'ي'
			elif letter == ' ':
				out_line += ' '
			else:
				out_line += letter
	return out_line


def convert_file(in_file):
	'''
	Inputs: 
	in_file: Path to ASMO file to be converted
	'''
	head, tail = os.path.split(in_file)
	'''
	

	root_dir = head.split('/')[0]
	data_set_type = head.split('/')[1]
	file_number = tail.split('.')[0].split('_')[-1]
	dir = root_dir + '/' + data_set_type+'/'+data_set_type+'_corpus_ar'
	if not os.path.exists(dir):
		os.makedirs(dir)
	file_path = dir+'/'+data_set_type+'_corpus_'+str(file_number)+'.txt'
	'''
	file_path = "data/ar_lexicon.txt"

	#check if the converted file has been created before or not
	num_written_lines = 0
	if os.path.exists(file_path):
		print(f'***{tail} is resuming***')
		with open(file_path, 'r') as f:
			for line in f:
				num_written_lines += 1
		
		with open(file_path, 'a') as f:
			with open(in_file, 'r') as data:
				count = 0
				for line in data:
					count += 1
					if count > num_written_lines:
						f.write("%s\n" % conv_arab(line))
	else:
		print(f'***{tail} is starting***')
		with open(file_path, 'w') as f:
			with open(in_file, 'r') as data:
				for line in data:
					f.write("%s\n" % conv_arab(line))
	print(tail+' has been finished')

			

def main():
	#files_names = ['data/msa_coll/msa_coll_corpus_split'+'/'+f for f in listdir('data/msa_coll/msa_coll_corpus_split')]
	#files_names = ['data/msa/msa_corpus_uniq_split'+'/'+f for f in listdir('data/msa/msa_corpus_uniq_split')]

	#p = Pool(processes=cpu_count())
	#p.map(convert_file,files_names)
	#convert_file('/home/maggie/arabic-asr/utilities/ASMO Convertion/data/data_asmo/data_clean.txt')
	convert_file('/home/maggie/kaldi/egs/msa_asr/data/local/dict/lexicon.txt')

if __name__ == "__main__":
	main()
