from splinter import Browser
from bs4 import BeautifulSoup as BS 
import re
import pickle
import time
import logging

'''
------------------------------------------------------------------------
Step2：해당 영화에 대한 리뷰와 별을 획득하다.
------------------------------------------------------------------------
'''

logging.basicConfig(filename='myProgramLog.txt', level=logging.INFO, format='%(asctime)s, %(levelname)s - &(message)s')

# Step1에서 얻은 데이터fmf 읽다.
with open('movie_data.txt') as f:
	lines = f.readlines()
lines = list(set(lines))
data = [[], [], []]
for line in lines:
        data[0].append(line.split()[0])
        data[1].append(line.split()[1])
        data[2].append(float(line.split()[2]))

# 다운로드 받은 리뷰와 평점은 pickle로 저장하여 나중에 호출할 수 있다.
# 영화마다 COMMENTS_NUM 개씩 리뷰를 받다.
COMMENTS_NUM = 20
f = open('comments.p', 'wb')
comments = {}
for i in range(len(data[0])):
	bser = Browser('chrome', headless=True)
	url = 'https://movie.douban.com/subject/%s/comments?status=P' % data[0][i]
	comments[data[1][i]] = [[], []]
	bser.visit(url)
	bs = BS(bser.html, 'lxml')
	bs_com = bs.find('div', attrs={'id': 'comments'})
	try:
		score_lists = bs_com.find_all('span', attrs={'class': 'comment-info'})
		comment_lists = bs_com.find_all('p')
		for j in range(COMMENTS_NUM):
			score_data = score_lists[j]
			score = re.findall('allstar(\d\d).*?', str(score_data))[0]
			comment_data = comment_lists[j]
			comment = comment_data.text
			comments[data[1][i]][0].append(score)
			comments[data[1][i]][1].append(comment)
		logging.info('movie <%s> have [%d]comments' % (data[1][i], len(comments[data[1][i]][1])))
		time.sleep(2)
	except:
		# print('ERROR', i)
		pass
	bser.quit()
pickle.dump(comments, f)
f.close()
