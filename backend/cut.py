import jieba
import jieba.posseg as pseg

jieba.enable_paddle()
jieba.set_dictionary("./dict.txt")
#jieba.load_userdict("./dict.txt")
#jieba.enable_parallel(8)
'''
flags參考
https://github.com/fxsjy/jieba
'''
wanted_flags = ['n','nr','nz','f','a','ad','an','PER','LOC','ORG','v','vd','vn','ns','nt']
word_filter = ['踢踢','看板','文章','刪文','遵守','排版','作者','標題','時間','推']

def cut_paddle(list):
    cut_list = []
#   f= open('cut_paddle.txt','w+',encoding='UTF-8')
    for str in list:
        words = pseg.cut(str,use_paddle=True)
        for word,flag in words:
            if(word not in word_filter):
                if(flag in wanted_flags):
#                f.write('%s %s' %(word,flag))
#                f.write('\n')
                    cut_list.append(word)
    return cut_list
#    f.close()

def cut(list):
    cut_list = []
#    f= open('cut.txt','w+',encoding='UTF-8')
    for str in list:
        words = pseg.cut(str)
        for word,flag in words:
            if(word not in word_filter):
                if(flag in wanted_flags):
#                f.write('%s %s' %(word,flag))
#                f.write('\n')
                    cut_list.append(word)
    return cut_list
#    f.close()