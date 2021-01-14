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

# sample_word_frequencies = {'beautiful': 10, 'explicit':8, 'simple':30, 'sparse':9,
#                 'readability':2, 'rules':17, 'practicality':20,
#                 'explicitly':22, 'one':3, 'now':29, 'easy':38, 'obvious':46, 'better':35}

sample_word_frequencies = {'ntu': 1, '返回': 15, 'oooeee77': 2, 'tue': 1, 'jan': 1, 'i': 9, 'imgur': 31, 'com': 31, 'b0ehq4': 1, 'jpg': 6, '拍照': 1, '問': 2, '翻拍': 1, '大家': 9, '分享': 1, '站': 18, 'ptt': 28, 'cc': 31, 'www': 15, 'bbs': 15, 'm': 1, 'a': 1, 'd06': 1, 'html': 16, 'cpl812': 1, 'http': 1, 'e0zh4g5': 1, '心情': 2, '路': 5, 'cwh0105': 2, 'ex': 1, '咖哩': 2, '如題': 2, '入口': 2, '最近': 1, '走': 2, '窄窄': 1, '小路': 1, '就算': 1, '路超': 1, '超': 2, '平整': 1, 'vrgovm4': 1, 'y0acudbhttps': 1, 'nq5cofn': 1, 'goau9fhttps': 1, 'y2ho3ic': 1, 'vdfwwwkhttps': 1, 'vots1f': 1, 'gdj20pwhttps': 1, 'd2ammnq': 1, 'mc0yaef': 1, 'b7e': 1, 'jason90814': 2, '小': 2, 'loserfeizie': 1, '地板': 1, '高': 2, '根本': 2, '使': 2, '人': 4, 'yongxchen': 2, '走破路': 1, '柏油': 1, '知道': 1, 'kurtzouma': 1, '殺': 1, '奉行': 1, 'jerryh612': 2, '靠': 1, '角落': 1, '人行道': 1, '突起': 1, 'dosoleil': 1, '攔': 1, 'thejackys': 1, 'nirejoy': 1, '敢': 1, '想像': 1, '新': 1, '宿舍': 1, '會': 4, '台大': 6, '中心': 7, '兼任': 4, '助理': 4, 'linru24': 3, '駝鈴': 2, 'part': 3, 'time': 3, 'v': 1, 'jt4dg': 1, '台北': 1, '一般': 1, '法律': 2, '使用': 1, '本板': 1, '保': 1, '願受': 1, '於': 2, '不得': 1, '得視': 1, '提出': 1, '工期': 1, '休息': 4, '工作': 9, '交件': 1, '期': 1, '上班': 2, '排班': 4, '方式': 5, '固定': 1, '內': 1, '可': 5, '特殊': 2, '降': 1, '計薪': 1, '供餐': 1, '無': 2, '以上': 2, '依法': 1, '投保': 1, '政策': 2, '研究': 10, '行政': 1, '公文': 1, '支援': 1, '校稿': 1, '周邊': 1, '跑腿': 1, '以下': 1, '擇': 1, '上架': 1, '管理': 1, '版面': 1, '含': 1, 'css': 1, '影片': 1, '提供': 1, 'b': 1, '中英': 1, '蒐集': 1, '整理': 1, '分析': 1, '地址': 1, '台北市': 1, '社科院': 1, '頤賢館': 1, '室': 1, '官方': 1, 'rsprc': 2, 'edu': 2, 'tw': 3, '小姐': 1, '先生': 1, 'email': 1, 'protected': 1, '回覆': 2, '收到': 1, '通知': 3, '不合': 1, '另行': 1, '不限': 1, '科系': 1, '能': 1, '配合': 1, '尤佳': 3, '需對': 1, '熟悉': 2, 'premiere': 1, 'ps': 1, 'ai': 1, 'adobe': 1, '請': 3, '背景': 1, '社群': 1, '能源': 1, '前瞻': 1, '描述': 2, '能力': 2, 'excel': 1, '圖': 1, '表': 1, '身心': 1, '之': 1, 'pdf': 1, '檔': 1, '姓名': 2, '信箱': 1, '信件': 1, '主旨': 1, '寫': 1, '需求': 1, '值班': 1, '教育': 1, '即': 1, '截止': 1, 'zh': 1, 'join': 1, 'us': 1, '期末考': 4, 'wcnoname5': 2, '勇者': 1, '要': 7, '完': 1, '做': 4, '看': 5, '去': 4, '睡': 1, '加油': 7, 'fun5566': 1, 'shibasun': 1, 'jerejesse': 2, '淡': 1, '嵐': 1, '科': 3, '教授': 1, '佛心': 1, '看到': 1, '快': 1, '剩下': 1, 'e': 1, 'lyu7': 1, 'zxcv200298': 5, '三科': 1, '佛': 1, '菸酒': 1, '生': 2, 'xd': 1, '瑜': 3, '希望': 2, '阿': 1, '火海': 1, '默哀': 1, 'youtu': 1, 'be': 1, 'elgihtgt9vi': 1, 'sent': 1, 'from': 2, 'jptt': 1, 'on': 2, 'my': 2, 'asus': 1, 'i01wd': 1, 'sion1993': 2, '孩子': 1, 'tw15': 2, '腦': 1, 'deep77092': 1, '教': 1, 'mightymouse': 1, '解': 1, 'eunhailoveu': 2, '哀矜': 1, '物喜': 1, '痛失': 2, '人才': 1, 'jzoethai': 1, '因界': 1, '素材': 1, 'zxcvbnm9426': 1, '蹲': 1, '低': 1, '跳': 1, 'qq': 1, 'juice': 1, '掉': 1, '考': 1, '哭': 2, '祝': 1, 'chrizeroxtwo': 1, 'u': 1, 'jun059': 5, 'u01': 1, 'ysae9': 1, '感穴': 1, 'zouelephant': 1, '痛苦': 1, '死': 1, '田': 2, 'mmm87963': 3, 'tongue561651511': 1, 'f91': 1, 'chung0817': 2, 'z5582143': 1, 'peko': 16, '滑倒': 2, 'saturday5566': 2, '推推': 1, 'karta2032150': 1, 'syanift': 1, 'cmrafsts': 1, 'pekora': 1, '祝福': 1, 'kenefreet': 1, '老婆': 1, 'isonaei': 1, '專板': 2, 'j0socute': 1, '版': 1, '變': 1, 'eusebius': 1, '樓': 4, 'gtyuse': 3, '麻枝': 2, '歌': 2, 'shiburin': 1, '編': 1, 'et847sw': 1, 'e5': 1, 'mv': 1, 'daye87': 1, '放': 3, '寒假': 4, 'jsstarlight': 1, 'ina': 1, '破': 3, 'mayolane': 2, '前': 1, 'nrerk4w': 1, 'jpgina': 1, '直播': 1, '日程表': 1, 'c2cvcup': 1, 'jpghttps': 1, 'uumwocy': 1, '可能': 1, 'a58524andy': 1, '婆': 2, '板': 1, '抽': 2, '發': 3, 'p': 2, '心力': 1, '停好': 1, '改善': 1, '交通': 1, '做起': 1, '選': 1, 'fc': 1, 'cw3a5hl': 1, 'png': 1, '搶': 1, '改': 1, '爆': 2, 'howard0113': 1, 'mark0204': 3, 'mpedros': 1, '熊': 2, '道歉': 3, '好': 3, '想': 1, '乳提': 1, '台害': 1, '沒': 1, 'nlnloeo': 1, 'sony': 1, 'g8342': 1, 'bf2': 1, '屁眼': 1, '失物': 4, 'airpods': 1, 'pro': 1, 'laijacky': 3, 'jacky': 1, 'mon': 1, '打': 1, '方便': 1, '物品': 2, '信': 1, '直接': 1, '放回': 1, '處': 1, '小心': 1, '調': 1, '搞': 1, '感恩': 1, 'cc7': 1, 'cal28802672': 2, '人士': 1, '拿走': 1, '說': 1, '冷': 4, '專發': 1, 'id': 1, '女口': 1, '太冷': 1, '人家': 1, 'whfcalt': 1, 'corkin': 1, 'ashi0127': 1, 'ijjkimv': 1, '考前': 1, 'nctujumpegg': 1, 'toto0306': 1, 'koybtj3': 1, 'bun': 2, 'cha': 1}

COLORS = ["#EB8384", "#F7AA4C", "#F8A57C", "#EDC360", "#96BB79", "#43aa8b", "#577590"]
# COLORS = ["#faae7b", "#cc8b79", "#9f6976", "#714674", "#432371"]
HOT_BOARD = ['gossiping','stock','c_chat','nba','baseball','lifeismoney', 'car','hatepolitics','koreastar','sex','mobilecomm','boy-girl','lol','e-shopping','marriage','beauty','tech_job','babymother','womentalk','pc_shopping']
MAX_WORD = 100

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

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
		
	word_frequencies0, word_frequencies1, word_frequencies2, word_frequencies3, word_frequencies4, word_frequencies5, word_frequencies6, length= main.popular_frequency(board)
	for i in range(8):
		return_data['button_texts'].append(str(topic_num))
		topic_num += length
	
	grouped_color_func = get_group_color_func(word_frequencies0)
	wc = WordCloud(background_color="white", repeat=False, color_func=grouped_color_func, width=image_width, height=image_height, font_path="font/SourceHanSansTW-Regular.otf", max_words=MAX_WORD)
	return_data['image_names'].append(filename+str(0)+".png")
	generate_wordcloud(wc, return_data['image_names'][0], word_frequencies0)
	return_data['image_names'].append(filename+str(1)+".png")
	generate_wordcloud(wc, return_data['image_names'][1], word_frequencies1)
	return_data['image_names'].append(filename+str(2)+".png")
	generate_wordcloud(wc, return_data['image_names'][2], word_frequencies2)
	return_data['image_names'].append(filename+str(3)+".png")
	generate_wordcloud(wc, return_data['image_names'][3], word_frequencies3)
	return_data['image_names'].append(filename+str(4)+".png")
	generate_wordcloud(wc, return_data['image_names'][4], word_frequencies4)
	return_data['image_names'].append(filename+str(5)+".png")
	generate_wordcloud(wc, return_data['image_names'][5], word_frequencies5)
	return_data['image_names'].append(filename+str(6)+".png")
	generate_wordcloud(wc, return_data['image_names'][6], word_frequencies6)
	return jsonify(return_data)

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


	


