from ckiptagger import data_utils, construct_dictionary, WS,POS,NER



ws = WS('./data')
pos= POS('./data')
ner = NER('./data')


sentence_list = '操貼不進去，操你媽的期末，快中風了，OOOOOOOOOoooooooooooooOOOOOOOOOOOOOOO這到底他媽的什麼閃現'

word_sentence_list = ws(sentence_list)

pos_sentence_list = pos(word_sentence_list)

entity_sentenct_list = ner(word_sentence_list, pos_sentence_list)
print(',')