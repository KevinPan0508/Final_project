from flask import Flask, request, make_response, render_template, jsonify
import sys
import json
import time
import random
import numpy as np
import new_define as d
from wordcloud import WordCloud
from datetime import datetime, timedelta
import main
import group_color
import threading
import queue


COLORS = ["#EB8384", "#F7AA4C", "#F8A57C", "#EDC360", "#96BB79", "#43aa8b", "#577590"]
MAX_WORD = 50

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/get_board', methods=['POST', 'GET'])
def get_board():
	board = d.get_popular_board()
	return json.dumps(board)

@app.route('/get_images/', methods=['POST'])
def get_images():

	# 取出前端傳過來的 data
	board = request.get_json()['board']
	image_width = request.get_json()['width']
	image_height = request.get_json()['height']
	filename = "static/images/" + board + "_" + str(int(round(time.time() * 1000))) + "_"

	# 要傳回給前端的 data
	return_data = {}

	# 會產生的 image 數量
	return_data['image_num'] = 7

	# 產生的 image file names
	# index 0 是時間最靠近現在的圖片
	return_data['image_names'] = []

	# button 要顯示的文字
	# 固定 7 個
	# index 0 是時間最靠近現在的圖片
	return_data['button_texts'] = []
	sample_word_frequencies[board] = 100
	# 熱門版只爬 490 篇
	# 其他爬 7 天
	topic_num = 0
		
	word_frequencies0, word_frequencies1, word_frequencies2, word_frequencies3, word_frequencies4, word_frequencies5, word_frequencies6, length= main.multi_popular_frequency(board)
	for i in range(8):
		return_data['button_texts'].append(str(topic_num))
		topic_num += length
	
	grouped_color_func = get_group_color_func(word_frequencies0)
	wc = WordCloud(background_color="white", repeat=False, color_func=grouped_color_func, width=image_width, height=image_height, font_path="font/SourceHanSansTW-Regular.otf", max_words=MAX_WORD)
	threads = []
	threads.append(threading.Thread(target=multi_generate_image, args=(word_frequencies0,wc,return_data,0)))
	threads.append(threading.Thread(target=multi_generate_image, args=(word_frequencies1,wc,return_data,1)))
	threads.append(threading.Thread(target=multi_generate_image, args=(word_frequencies2,wc,return_data,2)))
	threads.append(threading.Thread(target=multi_generate_image, args=(word_frequencies3,wc,return_data,3)))
	threads.append(threading.Thread(target=multi_generate_image, args=(word_frequencies4,wc,return_data,4)))
	threads.append(threading.Thread(target=multi_generate_image, args=(word_frequencies5,wc,return_data,5)))
	threads.append(threading.Thread(target=multi_generate_image, args=(word_frequencies6,wc,return_data,6)))
	for i in range(len(threads)):
		return_data['image_names'].append(filename+str(i)+".png")
		threads[i].start()
		print('generate ' + str(i+1) + 'th image')
	return jsonify(return_data)

def multi_generate_image(freq0,wc,dict,i):
	generate_wordcloud(wc, dict['image_names'][i], freq0)




def generate_wordcloud(wc, filename, text_frequencies):
	# x, y = np.ogrid[:300, :300]

	# mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
	# mask = 255 * mask.astype(int)
	wc.generate_from_frequencies(text_frequencies).to_file(filename)

def get_group_color_func(text_frequencies):

	# 把 word 按出現次數由大到小排好
	texts = sorted(list(text_frequencies.keys()), key = lambda k: text_frequencies[k], reverse=True)[:MAX_WORD+1]
	
	# 計算每一個顏色要 assign 給幾個 word
	text_num_per_color = len(texts)/len(COLORS)

	# 記錄每一個顏色對應的 words
	color_to_words = {}
	for i in range(0, len(COLORS)):
		color_to_words[COLORS[i]] = texts[int(i*text_num_per_color):int((i+1)*text_num_per_color)]

	# 給定 default color
	default_color = COLORS[-1]
	print(color_to_words, file=sys.stdout)

	return group_color.SimpleGroupedColorFunc(color_to_words, default_color)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')


