from flask import Flask, request, make_response, render_template, jsonify
import sys
import json
import time
import random
import numpy as np
from wordcloud import WordCloud
from datetime import datetime, timedelta

import popular
import group_color

sample_word_frequencies = {'beautiful': 10, 'explicit':8, 'simple':30, 'sparse':9,
                'readability':2, 'rules':17, 'practicality':20,
                'explicitly':22, 'one':3, 'now':29, 'easy':38, 'obvious':46, 'better':35}

COLORS = ["#f94144", "#f3722c", "#f8961e", "#f9c74f", "#90be6d", "#43aa8b", "#577590"]

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/get_board', methods=['POST', 'GET'])
def get_board():
	board = popular.get_popular_board()
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
	return_data['image_num'] = random.randint(3, 8)

	# 產生的 image file names
	# index 0 是時間最靠近現在的圖片
	return_data['image_names'] = []

	# button 要顯示的文字
	# 固定 8 個
	# index 0 是時間最靠近現在的圖片
	return_data['button_texts'] = []
	today = datetime.now()
	for i in range(8):
		return_data['button_texts'].append(today.strftime("%m")+"/"+today.strftime("%d"))
		today = today - timedelta(days=1)

	# print(return_data['button_texts'], file=sys.stdout)

	# 在 sample_text_frequencies 中加入看板的文字
	sample_word_frequencies[board] = 100

	'''
		!!!!!!! 統計好的 word frequency !!!!!!! 
	'''
	word_frequencies = sample_word_frequencies

	grouped_color_func = get_group_color_func(word_frequencies)

	wc = WordCloud(background_color="white", repeat=False, color_func=grouped_color_func, width=image_width, height=image_height)

	# 產生 word cloud 的 image
	for i in range(return_data['image_num']):
		return_data['image_names'].append(filename+str(i)+".png")
		generate_wordcloud(wc, return_data['image_names'][i], word_frequencies)

	return jsonify(return_data)

def generate_wordcloud(wc, filename, text_frequencies):
	# x, y = np.ogrid[:300, :300]

	# mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
	# mask = 255 * mask.astype(int)
	wc.generate_from_frequencies(text_frequencies).to_file(filename)

def get_group_color_func(text_frequencies):

	# 把 word 按出現次數由大到小排好
	texts = sorted(list(text_frequencies.keys()), key = lambda k: sample_text_frequencies[k], reverse=True)
	
	# 計算每一個顏色要 assign 給幾個 word
	text_num_per_color = len(texts)/len(COLORS)

	# 記錄每一個顏色對應的 words
	color_to_words = {}
	for i in range(0, len(COLORS)):
		color_to_words[COLORS[i]] = texts[int(i*text_num_per_color):int((i+1)*text_num_per_color)]

	# 給定 default color
	default_color = COLORS[-1]

	return group_color.SimpleGroupedColorFunc(color_to_words, default_color)


	


