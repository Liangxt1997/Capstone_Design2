import pickle
import jieba
import numpy as np

# 저장된 댓글 데이터를 pickle로 읽는다.
with open('comments.p', 'rb') as f:
	comments = pickle.load(f)

# 데이터를 깨끗이 하고 불필요한 기호를 삭제한다.
def filterword(filterdata):
	symbol = '，。“”~！@#￥%……&*（）——+=【】{}、|；：‘’《》？!#$^&()[]{};:",.<>/?\\-\n'
	for sym in symbol:
		filterdata = filterdata.replace(sym, '')
		filterdata = filterdata.strip(' ')
	return filterdata

# 어휘 표를 구축하고 중복을 제거한다.
# 태그 데이터를 변환한다.
y_label = []
voca = []
ori_filtered = []
for film in comments:
	for socre_i in comments[film][0]:
		y_label.append([0, 0, 0, 0, 0])
		# 1-5점
		score = int(int(socre_i)/10)
		y_label[-1][score-1] = 1
	for comment_i in comments[film][1]:
		filter_comment = filterword(comment_i)
		cutted_comment = jieba.lcut(filter_comment)
		ori_filtered.append(cutted_comment)
		for each in cutted_comment:
			if len(each)>0:
				if each not in voca:
					voca.append(each)
voca = list(set(voca))

x_data = []
for each in ori_filtered:
	voca_vector = [0] * len(voca)
	for word in each:
		voca_vector[voca.index(word)] += 1
	x_data.append(voca_vector)

# numpy 배열 형식으로 변환한다.
x_data = np.array(x_data)
y_label = np.array(y_label)
# print(x_data.shape, y_label.shape)

# 전환된 데이터를 저장하면 다음 호출이 편리하다.
with open('x_data.p', 'wb') as x_f:
	pickle.dump(x_data, x_f)
with open('y_label.p', 'wb') as y_f:
	pickle.dump(y_label, y_f)
with open('voca.p', 'wb') as v_f:
	pickle.dump(voca, v_f)
