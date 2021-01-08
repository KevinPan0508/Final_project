from flask import Flask, request, make_response, render_template, jsonify
import sys
import json
import time
import random
import numpy as np
from wordcloud import WordCloud
from datetime import datetime, timedelta

import popular


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
	board = request.get_json()['board']
	filename = "static/images/" + board + "_" + str(int(round(time.time() * 1000))) + "_"
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

	# 產生 word cloud 的 image
	for i in range(return_data['image_num']):
		return_data['image_names'].append(filename+str(i)+".png")
		generate_wordcloud(return_data['image_names'][i], board)
		print("generate image " + str(i) + "/" + str(return_data['image_num']), file=sys.stdout)

	return jsonify(return_data)

def generate_wordcloud(filename, text):
	x, y = np.ogrid[:300, :300]

	mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
	mask = 255 * mask.astype(int)

	wc = WordCloud(background_color="white", repeat=True, color_func=my_color_func)
	wc.generate(text).to_file(filename)

COLORS = ["249, 65, 68", "243, 114, 44", "248, 150, 30", "249, 132, 74", "249, 199, 79", "144, 190, 109", "67, 170, 139", "77, 144, 142", "87, 117, 144", "39, 125, 161"]
def my_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
	
    return "rgb(%s)" % COLORS[random.randint(0, len(COLORS)-1)]

