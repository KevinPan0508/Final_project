import multidict as multidict
import numpy as np
import os
import random
from PIL import Image
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

font =  'SourceHanSansTW-Regular.otf'
COLORS = ["249, 65, 68", "243, 114, 44", "248, 150, 30", "249, 132, 74", "249, 199, 79", "144, 190, 109", "67, 170, 139", "77, 144, 142", "87, 117, 144", "39, 125, 161"]

def getFrequencyDictForText(list):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
    for text in list:
        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict

def my_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
	return "rgb(%s)" % COLORS[random.randint(0, len(COLORS)-1)]

def generate_wordcloud(filename, text):
	x, y = np.ogrid[:300, :300]

	mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
	mask = 255 * mask.astype(int)
	wc = WordCloud(background_color="white", repeat=True, color_func=my_color_func, font_path=font)
	wc.generate_from_frequencies(text).to_file(filename)
