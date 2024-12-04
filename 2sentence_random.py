import pandas as pd
import random

# 원본 데이터
# CSV 데이터를 DataFrame으로 읽기
data = pd.read_csv('sentences.csv')

# 문장의 단어를 섞는 함수
def shuffle_sentence(sentence):
    words = sentence.split()
    random.shuffle(words)
    return ' '.join(words)

# 새로운 DataFrame 생성 (랜덤 ID와 섞인 문장)
shuffled_data = pd.DataFrame()
shuffled_data['ID'] = data['ID']
shuffled_data['Sentecne'] = data['Sentence']
shuffled_data['Sentence_shuffle'] = data['Sentence'].apply(shuffle_sentence)

# 섞인 데이터를 새 CSV 파일로 저장
shuffled_data.to_csv('shuffled_sentences.csv', index=False)

# 결과 확인
print(shuffled_data)