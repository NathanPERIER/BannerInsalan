#!/usr/bin/python3
# -*- coding: utf-8 -*-
# file: bannerInsalan.py
# author: Nathan PERIER
# created: 2021/05/28
# last modified: 2021/05/29
# github page: https://github.com/NathanPERIER/BannerInsalan

import sys
import re


def properCentre(s, lenght, char=' ') : 
	s = str(s)
	char = char[0]
	residual_len = lenght - len(s)
	if residual_len > 0 : 
		return char * (residual_len // 2) + s + char * (residual_len - residual_len // 2)
	return None


# https://www.geeksforgeeks.org/converting-decimal-number-lying-between-1-to-3999-to-roman-numerals/
def numberToRoman(number) :
	res = ''
	if number > 3999 or number < 1 : 
		return None
	num = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
	sym = ["I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M"]
	i = 12
	while number :
		div = number // num[i]
		number %= num[i]
		while div :
			res += sym[i]
			div -= 1
		i -= 1
	return res



if len(sys.argv) > 1 :
	if sys.argv[1] in ['-h', '--help'] :
		# print(f"usage : {sys.argv[0]} [--mini] [-t text] [--center | --left | --right] [-n num] [-c colour] [--fill] [--bar]")
		print(f"usage : {sys.argv[0]} [--mini] [-n num] [-c colour] [--fill] [--bar]")
		exit(0)

i = 1


prefix = ['', '', '', '', '']
maxlen = 54
if i < len(sys.argv) and sys.argv[i] == '--mini' :
	prefix[0] = ' ███▖  ▗███ ██ ███▖   ██'
	prefix[1] = ' ████▖▗████ ██ ████▖  ██'
	prefix[2] = ' ██▝████▘██ ██ ██▝██▖ ██'
	prefix[3] = ' ██ ▝██▘ ██ ██ ██ ▝██▖██'
	prefix[4] = ' ██      ██ ██ ██  ▝████'
	i += 1
	maxlen += 24

if i+1 < len(sys.argv) and sys.argv[i] == '-t' : 
	text = sys.argv[i+1]
	i += 2
else : 
	text = ''


align = 'c'
if i < len(sys.argv) : 
	if sys.argv[i] in ['--center', '--left', '--right'] :
		align = sys.argv[i][2]
		i += 1


num = None
if i+1 < len(sys.argv) and sys.argv[i] == '-n' :
	num = sys.argv[i+1]
	if re.match(r'[0-9]+', num) is not None : 
		num = numberToRoman(int(num))
	elif re.match(r'[IVXLCDM]+', num) is None :
		num = None
	i += 2


colour_codes = {
	'black': 0, 
	'red': 1, 
	'green': 2, 
	'yellow': 3, 
	'blue': 4, 
	'magenta': 5, 
	'cyan': 6, 
	'white': 7
}
palette = 2
if i+1 < len(sys.argv) and sys.argv[i] == '-c' :
	if sys.argv[i+1] in colour_codes : 
		col_code = colour_codes[sys.argv[i+1]]
	else : 
		res = re.fullmatch(r'8bit-(\d{1,3})', sys.argv[i+1])
		temp_col = int(res.group(1)) if res != None else 0
		if temp_col > 0 and temp_col < 256 :
			col_code = temp_col
			palette = 8
	i += 2
else : 
	col_code = colour_codes['blue']

text_col = f"[1;3{col_code}m" if palette == 2 else f"[38;5;{col_code}m"
reset_col = '[0m'


fill = False
bars_col = ''
if i < len(sys.argv) and sys.argv[i] == '--fill' :
	fill = True
	if palette == 2 : 
		bars_col = f"[0;3{col_code}m"
		text_col = f"[1;4{col_code}m"
		if col_code == 7 :
			text_col += '[1;30m'
	else : 
		bars_col = text_col
		text_col = f"[48;5;{col_code}m"
	i += 1


for j in range(len(prefix)) :
	prefix[j] = text_col + prefix[j]


bar = (i < len(sys.argv) and sys.argv[i] == '--bar')
if bar :
	i += 1




# https://patorjk.com/software/taag/#p=display&f=ANSI%20Regular&t=INSALAN
if fill :
	bar_up = '▄' * (maxlen+2)
	print(f" {bars_col}{bar_up}{reset_col}")
else : 
	print('')
print(f" {prefix[0]} ██ ███▖   ██ ███████ ▗█████▖ ██      ▗█████▖ ███▖   ██ {reset_col}")
print(f" {prefix[1]} ██ ████▖  ██ ██      ██   ██ ██      ██   ██ ████▖  ██ {reset_col}")
print(f" {prefix[2]} ██ ██▝██▖ ██ ███████ ███████ ██      ███████ ██▝██▖ ██ {reset_col}")
print(f" {prefix[3]} ██ ██ ▝██▖██      ██ ██   ██ ██      ██   ██ ██ ▝██▖██ {reset_col}")
print(f" {prefix[4]} ██ ██  ▝████ ███████ ██   ██ ███████ ██   ██ ██  ▝████ {reset_col}")
if bar : 
	if num is not None :
		bar_middle = "╶" + properCentre(num, maxlen-2, '─') + "╴"
	else : 
		bar_middle = "╶" + "─" * (maxlen-2) + "╴"
	print(f" {text_col} {bar_middle} {reset_col}")
elif num is not None : 
	bar_middle = properCentre(num, maxlen)
	print(f" {text_col} {bar_middle} {reset_col}")
if text != '' : 
	pass
if fill and not ((bar or num is not None) and text == '') :
	bar_up = '▀' * (maxlen+2)
	print(f" {bars_col}{bar_up}{reset_col}")
else : 
	print('')


