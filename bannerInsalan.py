#!/usr/bin/python3
# -*- coding: utf-8 -*-
# file: bannerInsalan.py
# author: Nathan PERIER
# created: 2021/05/28
# last modified: 2021/06/06
# github page: https://github.com/NathanPERIER/BannerInsalan

import sys
import re
import time

from text import textToBanner


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
		print(f"usage : {sys.argv[0]} [--smooth] [--mini] [-n num] [-c colour] [--fill] [--bar] [--wallpaper]")
		exit(0)

i = 1


smooth = (i < len(sys.argv) and sys.argv[i] == '--smooth')
if smooth : 
	i += 1

banner_text = None
if i < len(sys.argv) :
	if sys.argv[i] == '--mini' :
		banner_text = 'mininsalan'
	elif sys.argv[i] == '--salad' :
		banner_text = 'insalade'
	elif sys.argv[i] == '--fog' :
		banner_text = 'fogsalan'
	elif sys.argv[i] == '--flang' :
		banner_text = 'flang'
	elif sys.argv[i] == '--hostname' :
		import socket
		banner_text = socket.gethostname()
	elif sys.argv[i] == '--local-ip' :
		import socket
		try :
			banner_text = socket.gethostbyname(socket.getfqdn())
		except socket.gaierror : 
			banner_text = socket.gethostbyname(socket.gethostname())
		if banner_text.startswith("127.") :
			try :
				s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				s.connect(('1.1.1.1', 1))
				banner_text = s.getsockname()[0]
			except OSError :
				pass
	elif sys.argv[i] == '--global-ip' :
		import requests
		try : 
			response = requests.get('http://canihazip.com')
			if response.ok :
				print(response.text)
				banner_text = response.text
			else :
				i += 1
		except OSError :
			i += 1

if banner_text is not None :
	i += 1
else :
	banner_text = 'insalan'
banner = textToBanner(banner_text)


align = 'c'
if i < len(sys.argv) and sys.argv[i] in ['--center', '--left', '--right'] :
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



bar = (i < len(sys.argv) and sys.argv[i] == '--bar')
if bar :
	i += 1

mode = 'banner'
if i < len(sys.argv) : 
	if sys.argv[i] == '--wallpaper' :
		mode = 'wallpaper'


maxlen = len(banner[0])
for i in range(len(banner)) :
	banner[i] = f" {text_col} {banner[i]} {reset_col}"

if fill :
	bar_up = '▄' * (maxlen+2)
	banner.insert(0, f" {bars_col}{bar_up}{reset_col}")
else : 
	banner.insert(0, ' ' * (maxlen+2))
if bar : 
	if num is not None :
		bar_middle = "╶" + properCentre(num, maxlen-2, '─') + "╴"
	else : 
		bar_middle = "╶" + "─" * (maxlen-2) + "╴"
	banner.append(f" {text_col} {bar_middle} {reset_col}")
elif num is not None : 
	bar_middle = properCentre(num, maxlen)
	banner.append(f" {text_col} {bar_middle} {reset_col}")
if fill and not bar and num is None :
	bar_up = '▀' * (maxlen+2)
	banner.append(f" {bars_col}{bar_up}{reset_col}")
else : 
	banner.append(' ' * (maxlen+2))


if mode == 'wallpaper' : 
	import shutil
	term_size = shutil.get_terminal_size((0,0))
	if term_size.columns > 0 and term_size.lines > 0 :
		x_off = (term_size.lines - len(banner)) // 2
		y_off = (term_size.columns - len(banner[0])) // 2
		fill = ' ' * term_size.columns
		lfill = ' ' * y_off
		rfill = ' ' * (term_size.columns - y_off - len(banner[0]) - 1)
		screenprint = []
		for i in range(x_off) : 
			screenprint.append(fill)
		for line in banner : 
			screenprint.append(lfill + line + rfill)
		for i in range(term_size.lines - x_off - len(banner)) : 
			screenprint.append(fill)
		print('\n'.join(screenprint), end='')
		time.sleep(10)
		exit(0)

for line in banner : 
	print(line)




