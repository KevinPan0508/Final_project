
# -*- coding: utf-8 -*-
from ckiptagger import WS, POS, NER
import new_define

trash_ws = ['站內','內信','網址','坊','實業','實業坊','版規','內文','原文','處罰','水桶''https','imgur','批踢踢','踢踢','看板','文章','刪文','遵守','排版','作者','標題','時間','推','有','是']
wanted_pos = ['Na','Nb','Nc','Nd','Nh','VC','VK','VJ','VG','VHC']
segment_delimiter = {'，',',','。','.','：',':','[',']','「','」','！','!','、','(',')'}


ws = WS("./data")
pos = POS("./data")
ner = NER("./data")


def ckip_cut(list):
    pos_list = []
    ws_list = []
    final_list = []
    word_sentence_list = ws(list)
    pos_sentence_list = pos(word_sentence_list)
    for i in range(len(word_sentence_list)):
        ws_list = ws_list + word_sentence_list[i]
        pos_list = pos_list + pos_sentence_list[i]
    for i in range(len(ws_list)):
        if(ws_list[i] not in trash_ws):
            if(pos_list[i] in wanted_pos):
                final_list.append(ws_list[i])
    return final_list




