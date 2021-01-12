import threading
import define as d
import cut as c
import cloud as wordc



#text_list = d.get_text_by_day('gossiping',1)
#cut_list1 = c.cut(text_list)
#cut_list2 = c.cut_paddle(text_list)
#test1 = wordc.getFrequencyDictForText(cut_list1)
#test2 = wordc.getFrequencyDictForText(cut_list2)
#wordc.generate_wordcloud('test2.png',test1)



def test_multi(board):
    text_list = d.get_text_regular(board,type='text+date')
    day1,day2,day3,day4,day5,day6,day7=d.split_text_by_days(text_list)
    threads = []
    threads.append(threading.Thread(target = c.cut, args=day1))
    threads.append(threading.Thread(target = c.cut, args=day2))
    threads.append(threading.Thread(target = c.cut, args=day3))
    threads.append(threading.Thread(target = c.cut, args=day4))
    threads.append(threading.Thread(target = c.cut, args=day5))
    threads.append(threading.Thread(target = c.cut, args=day6))
    threads.append(threading.Thread(target = c.cut, args=day7))
    for i in range(len(threads)):
        threads[i].start()



def normal(board):
    text_list = d.get_text_regular(board,type='text+date')
    day1,day2,day3,day4,day5,day6,day7=d.split_text_by_days(text_list)
    day1_cut = c.cut(day1)
    day2_cut = c.cut(day2)
    day3_cut = c.cut(day3)
    day4_cut = c.cut(day4)
    day5_cut = c.cut(day5)
    day6_cut = c.cut(day6)
    day7_cut = c.cut(day7)
    wordc.generate_wordcloud('0.png',wordc.getFrequencyDictForText(day1_cut))
    wordc.generate_wordcloud('1.png',wordc.getFrequencyDictForText(day1_cut+day2_cut))
    wordc.generate_wordcloud('2.png',wordc.getFrequencyDictForText(day1_cut+day2_cut+day3_cut))
    wordc.generate_wordcloud('3.png',wordc.getFrequencyDictForText(day1_cut+day2_cut+day3_cut+day4_cut))
    wordc.generate_wordcloud('4.png',wordc.getFrequencyDictForText(day1_cut+day2_cut+day3_cut+day4_cut+day5_cut))
    wordc.generate_wordcloud('5.png',wordc.getFrequencyDictForText(day1_cut+day2_cut+day3_cut+day4_cut+day5_cut+day6_cut))
    wordc.generate_wordcloud('6.png',wordc.getFrequencyDictForText(day1_cut+day2_cut+day3_cut+day4_cut+day5_cut+day6_cut+day7_cut))

normal('ntu')