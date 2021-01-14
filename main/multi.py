import new_define as nd
import threading
import ckip
import queue
from bs4 import BeautifulSoup
import re   

def multi_get_first_page_url(board):
    current_page_url = "http://www.ptt.cc/bbs/" + board + "/index.html"
    request = nd.modified_requests(current_page_url)
    html = request.text
    bs_class = BeautifulSoup(html,'html.parser')
    previous_page_link = 'http://ptt.cc' + bs_class.find_all('a',class_='btn wide')[1]['href']
    return previous_page_link

def multi_get_seg(board):
    first_page_url = multi_get_first_page_url(board)
    pattern = re.compile(r'\d+')
    url_digit = pattern.findall(first_page_url)
    worker1_start_url = first_page_url.lower()
    worker2_start_url = 'http://www.ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-1) + '.html'
    worker3_start_url = 'http://www.ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-2) + '.html'
    worker4_start_url = 'http://www.ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-3) + '.html'
    worker5_start_url = 'http://www.ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-4) + '.html'
    worker6_start_url = 'http://www.ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-5) + '.html'
    worker7_start_url = 'http://www.ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-6) + '.html'
    end =  'http://www.ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-7) + '.html'
    return worker1_start_url, worker2_start_url, worker3_start_url, worker4_start_url, worker5_start_url, worker6_start_url, worker7_start_url, end

def multi_get_text(start_url,stop_url):
    text_list = []
    pattern = re.compile(r'\d+')
    while(start_url != stop_url):
        temp = nd.get_title_meta_per_page(start_url)
        for i in range(len(temp)):
            print(temp[-1]['link'])
            text = nd.get_text(temp.pop()['link']).replace('\n','')
            text_list.append(text)
        url_digit = pattern.findall(start_url)
        start_url = start_url.replace(url_digit[0],str(int(url_digit[0])-1))
    text_list = ckip.ckip_cut(text_list)
    return text_list

def multi_start(board):
    ret = []
    my_queue = queue.Queue()
    threads = []
    start,first,second,third,fourth,fifth,sixth,seventh = multi_get_seg('board')
    threads.append(threading.Thread(target=lambda q, arg1, arg2: q.put(multi_get_text(arg1,arg2)), args=(my_queue,start,first)))
    threads.append(threading.Thread(target=lambda q, arg1, arg2: q.put(multi_get_text(arg1,arg2)), args=(my_queue,first,second)))
    threads.append(threading.Thread(target=lambda q, arg1, arg2: q.put(multi_get_text(arg1,arg2)), args=(my_queue,second,third)))
    threads.append(threading.Thread(target=lambda q, arg1, arg2: q.put(multi_get_text(arg1,arg2)), args=(my_queue,third,fourth)))
    threads.append(threading.Thread(target=lambda q, arg1, arg2: q.put(multi_get_text(arg1,arg2)), args=(my_queue,fourth,fifth)))
    threads.append(threading.Thread(target=lambda q, arg1, arg2: q.put(multi_get_text(arg1,arg2)), args=(my_queue,fifth,sixth)))    
    threads.append(threading.Thread(target=lambda q, arg1, arg2: q.put(multi_get_text(arg1,arg2)), args=(my_queue,sixth,seventh)))
    for i in range(7):
        threads[i].start()
    for i in range(7):
        threads[i].join()
    while not my_queue.empty():
        ret.append(my_queue.get())
    return ret[0],ret[1],ret[2],ret[3],ret[4],ret[5],ret[6]

def multi_ckip_cut(board):
    text1,text2,text3,text4,text5,text6,text7,length = multi_start(board)
    threads = []
    threads.append(threading.Thread(target = ckip.ckip_cut, args = (text1)))
    threads.append(threading.Thread(target = ckip.ckip_cut, args = (text2)))
    threads.append(threading.Thread(target = ckip.ckip_cut, args = (text3)))
    threads.append(threading.Thread(target = ckip.ckip_cut, args = (text4)))
    threads.append(threading.Thread(target = ckip.ckip_cut, args = (text5)))
    threads.append(threading.Thread(target = ckip.ckip_cut, args = (text6)))
    threads.append(threading.Thread(target = ckip.ckip_cut, args = (text7)))
    text1_cut = threads[0].start()
    text2_cut = threads[1].start()
    text3_cut = threads[2].start()
    text4_cut = threads[3].start()
    text5_cut = threads[4].start()
    text6_cut = threads[5].start()
    text7_cut = threads[6].start()
    return text1_cut, text2_cut, text3_cut, text4_cut, text5_cut, text6_cut, text7_cut, length

