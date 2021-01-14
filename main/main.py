import new_define as d
import cloud as wordc
import ckip as ck
 
def normal_frequency(board):
    text_list = d.get_text_7days(board,type='text+date')
    day1,day2,day3,day4,day5,day6,day7=d.split_text_by_days(text_list)
    day1_cut = ck.ckip_cut(day1)
    day1_frequency = wordc.getFrequencyDictForText(day1_cut)
    day2_cut = ck.ckip_cut(day2)
    day2_frequency = wordc.getFrequencyDictForText(day1_cut+day2)
    day3_cut = ck.ckip_cut(day3)
    day3_frequency = wordc.getFrequencyDictForText(day1_cut+day2_cut+day3)
    day4_cut = ck.ckip_cut(day4)
    day4_frequency = wordc.getFrequencyDictForText(day1_cut+day2_cut+day3_cut+day4)
    day5_cut = ck.ckip_cut(day5)
    day5_frequency = wordc.getFrequencyDictForText(day1_cut+day2_cut+day3_cut+day4_cut+day5)
    day6_cut = ck.ckip_cut(day6)
    day6_frequency = wordc.getFrequencyDictForText(day1_cut+day2_cut+day3_cut+day4_cut+day5_cut+day6_cut)
    day7_cut = ck.ckip_cut(day7)
    day7_frequency = wordc.getFrequencyDictForText(day1_cut+day2_cut+day3_cut+day4_cut+day5_cut+day6_cut+day7_cut)
    return  day1_frequency, day2_frequency, day3_frequency, day4_frequency, day5_frequency, day6_frequency, day7_frequency

def popular_frequency(board):
    text_list = d.get_text_by_number(board)
    text1,text2,text3,text4,text5,text6,text7,length = d.split_text_by_numbers(text_list)
    text1_cut = ck.ckip_cut(text1)
    text1_frequency = wordc.getFrequencyDictForText(text1_cut)
    text2_cut = ck.ckip_cut(text2)
    text2_frequency = wordc.getFrequencyDictForText(text1_cut+text2_cut)
    text3_cut = ck.ckip_cut(text3)
    text3_frequency = wordc.getFrequencyDictForText(text1_cut+text2_cut+text3_cut)
    text4_cut = ck.ckip_cut(text4)
    text4_frequency = wordc.getFrequencyDictForText(text1_cut+text2_cut+text3_cut+text4_cut)
    text5_cut = ck.ckip_cut(text5)
    text5_frequency = wordc.getFrequencyDictForText(text1_cut+text2_cut+text3_cut+text4_cut+text5_cut)
    text6_cut = ck.ckip_cut(text6)
    text6_frequency = wordc.getFrequencyDictForText(text1_cut+text2_cut+text3_cut+text4_cut+text5_cut+text6_cut)
    text7_cut = ck.ckip_cut(text7)
    text7_frequency = wordc.getFrequencyDictForText(text1_cut+text2_cut+text3_cut+text4_cut+text5_cut+text6_cut+text7_cut)
    return text1_frequency,text2_frequency,text3_frequency,text4_frequency,text5_frequency,text6_frequency,text7_frequency,length

