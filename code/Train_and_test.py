import pickle
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras import backend as K

# 저장된 훈련 데이터와 태그 데이터를 열다.
with open('x_data.p', 'rb') as x_f:
	x_data = pickle.load(x_f)
with open('y_label.p', 'rb') as y_f:
	y_label = pickle.load(y_f)

inputdim = x_data.shape[1]
# 모델링
model = Sequential()
model.add(Dense(1024, input_dim=inputdim))
model.add(Activation('sigmoid'))
model.add(Dense(512))
model.add(Activation('sigmoid'))
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dense(5))
model.add(Activation('softmax'))
# 컴파일
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
# 훈련（이전 200개의 데이터를 다음 테스트로 유지한다.), 25차
model.fit(x_data[200:, :], y_label[200:, :], batch_size=50, epochs=25, verbose=True)
# 모형 보존
model.save('douban_predict_score.h5')


# 테스트
# 저장된 훈련 데이터와 태그 데이터를 열다.
with open('x_data.p', 'rb') as x_f:
	x_data = pickle.load(x_f)
with open('y_label.p', 'rb') as y_f:
	y_label = pickle.load(y_f)
db_model = load_model('douban_predict_score.h5')
f = open('Predict_result.txt', 'w')
c_num = 0
for k in range(200):
	temp = list(db_model.predict(x_data[k:k+1, :])[0])
	score = temp.index(max(temp))+1
	for i in range(5):
		if y_label[k:k+1, :][0][i] == 1:
			act_score = i+1
	result = True if abs(act_score-score) == 0 else False
	if result:
		c_num += 1
	print('Number %d：' % (k+1))
	print('Predict Result：', temp) 
	print('---->Predict Score：%d' % score)
	print('Actual Score：%d' % act_score)
	print('Equal?：', result)
	print('-'*30)
	f.write('Number %d：' % (k+1) + '\n')
	f.write('Predict Result：' + str(temp) + '\n') 
	f.write('---->Predict Score：%d' % score + '\n')
	f.write('Actual Score：%d' % act_score + '\n')
	f.write('Equal?：' + str(result) + '\n')
	f.write('-'*50 + '\n')
print('Accuracy：%.lf' % (c_num/2))
f.write('Accuracy：%.lf' % (c_num/2))
# 비우다.
K.clear_session()
f.close()

