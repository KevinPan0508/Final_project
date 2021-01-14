import new_define as nd
import threading
from bs4 import BeautifulSoup
import re

def multi_get_first_page_url(board):
    current_page_url = "http://ptt.cc/bbs/" + board + "/index.html"
    request = nd.modified_requests(current_page_url)
    html = request.text
    bs_class = BeautifulSoup(html,'html.parser')
    previous_page_link = 'http://ptt.cc' + bs_class.find_all('a',class_='btn wide')[1]['href']
    return previous_page_link

def multi_get_seg(board):
    first_page_url = multi_get_first_page_url(board)
    pattern = re.compile(r'\d+')
    url_digit = pattern.findall(first_page_url)
    worker1_start_url = first_page_url
    worker2_start_url = 'http://ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-3) + '.html'
    worker3_start_url = 'http://ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-6) + '.html'
    worker4_start_url = 'http://ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-9) + '.html'
    worker5_start_url = 'http://ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-12) + '.html'
    worker6_start_url = 'http://ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-15) + '.html'
    worker7_start_url = 'http://ptt.cc/bbs/' + board +'/index' + str(int(url_digit[0])-18) + '.html'
    return first_page_url ,worker1_start_url,worker2_start_url,worker3_start_url,worker4_start_url,worker5_start_url,worker6_start_url,worker7_start_url

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
    return text_list

threads = []
start,first,second,third,fourth,fifth,sixth,seventh = multi_get_seg('gossiping')
threads.append(threading.Thread(target = multi_get_text, args = (start,first)))
threads.append(threading.Thread(target = multi_get_text, args = (first,second)))
threads.append(threading.Thread(target = multi_get_text, args = (second,third)))
threads.append(threading.Thread(target = multi_get_text, args = (third,fourth)))
threads.append(threading.Thread(target = multi_get_text, args = (fourth,fifth)))
threads.append(threading.Thread(target = multi_get_text, args = (fifth,sixth)))
threads.append(threading.Thread(target = multi_get_text, args = (sixth,seventh)))

text1 = threads[0].start()
text2 = threads[1].start()
text3 = threads[2].start()
text4 = threads[3].start()
text5 = threads[4].start()
text6 = threads[5].start()
text7 = threads[6].start()
print('')