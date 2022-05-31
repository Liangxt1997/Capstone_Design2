from splinter import Browser
from bs4 import BeautifulSoup as BS 
import re
import time

'''
------------------------------------------------------------------------
Step1：다양한 종류의 영화 페이지에서 필요한 데이터를 가져온다.
------------------------------------------------------------------------
'''

# 7개 종류의 영화를 선택하다. 종류별로 MOVIE_DATA_NUM편씩 영화를 고르다.
MOVIE_DATA_NUM = 20
main_urls = ['https://movie.douban.com/explore#!type=movie&tag=%E5%8A%A8%E4%BD%9C&sort=recommend&page_limit=20&page_start=0',
             'https://movie.douban.com/explore#!type=movie&tag=%E5%96%9C%E5%89%A7&sort=recommend&page_limit=20&page_start=0',
             'https://movie.douban.com/explore#!type=movie&tag=%E7%88%B1%E6%83%85&sort=recommend&page_limit=20&page_start=0',
             'https://movie.douban.com/explore#!type=movie&tag=%E7%A7%91%E5%B9%BB&sort=recommend&page_limit=20&page_start=0',
             'https://movie.douban.com/explore#!type=movie&tag=%E6%82%AC%E7%96%91&sort=recommend&page_limit=20&page_start=0',
             'https://movie.douban.com/explore#!type=movie&tag=%E6%81%90%E6%80%96&sort=recommend&page_limit=20&page_start=0',
             'https://movie.douban.com/explore#!type=movie&tag=%E6%B2%BB%E6%84%88&sort=recommend&page_limit=20&page_start=0']

data = {'movie_num': [], 'movie_name': [], 'movie_score': []}

# 획득한 데이터를 텍스트 파일에 저장하다.
f = open('movie_data.txt', 'w')
for url in main_urls:
	bser = Browser('chrome', headless=True)
	bser.visit(url)
	# wait
	time.sleep(5)
	bs = BS(bser.html, 'lxml')
	movie_list = bs.find('div', attrs={'class': 'list'})
	for i in range(MOVIE_DATA_NUM):
		try:
			movie_url = movie_list.find_all('a')[i].attrs['href']
			movie_name = movie_list.find_all('img')[i].attrs['alt']
			movie_score = movie_list.find_all('strong')[i].text
			# 정규 표현식으로 영화에 대응하는 url을 찾다.
			# (예：'https://movie.douban.com/subject/26363254/?tag=动作 &from=gaia video'
			# 지금 26363254를 뽑아내겠다.)
			get_num_reg = re.compile('https://movie.douban.com/subject/(\d{1,10})/.+?')
			movie_num = get_num_reg.findall(movie_url)[0]
			data['movie_num'].append(movie_num)
			data['movie_name'].append(movie_name)
			data['movie_score'].append(movie_score)
			data_writeline = str(movie_num)+' '+str(movie_name)+' '+str(movie_score)+'\n'
			f.write(data_writeline)
			print(movie_name)
		except:
			# print("ERROR：", url)
			pass
	bser.quit()
	time.sleep(2)
f.close()
