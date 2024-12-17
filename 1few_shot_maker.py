import re
import csv
import string
title_exceptions = ['Mr', 'Mrs', 'Ms', 'Dr', 'Prof', 'Sr', 'Jr']
for i in string.ascii_uppercase:
    if (i!='a'):
        title_exceptions.append(i)
print(title_exceptions)
def remove_special_chars(sentences):
    cleaned_sentences = []
    for sentence in sentences:
        # 문장 시작 부분의 따옴표 제거
        cleaned = re.sub(r'^["\']+', '', sentence)
        cleaned = re.sub(r'[!\.\,\:\?\-\;]+', '', cleaned)
        # 나머지 따옴표 제거
        cleaned = re.sub(r'[""''"\']+', '', cleaned)
        # 줄바꿈 제거 및 앞뒤 공백 제거
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        cleaned_sentences.append(cleaned)
    return cleaned_sentences

def sentences_to_dict(paragraph):
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK A CHRISTMAS CAROL IN PROSE; BEING A GHOST STORY OF CHRISTMAS ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK A CHRISTMAS CAROL IN PROSE; BEING A GHOST STORY OF CHRISTMAS ***"
    
    start_index = paragraph.find(start_marker) + len(start_marker)
    end_index = paragraph.find(end_marker)
    content = paragraph[start_index:end_index].strip()
    
    # 수정된 문장 분리 로직
    sentences = []
    buffer = []
    for word in content.split():
        if any(word.startswith(title) for title in title_exceptions):
            # 알려진 약어로 시작하는 경우 버퍼에 추가
            buffer.append(word)
        elif word.endswith('.'):  # 문장의 끝 감지
            buffer.append(word)
            sentences.append(' '.join(buffer))
            buffer = []
        else:
            buffer.append(word)
    
    # 마지막 버퍼 처리
    if buffer:
        sentences.append(' '.join(buffer))
    
    cleaned_sentences = remove_special_chars(sentences)
    return {idx: sentence for idx, sentence in enumerate(cleaned_sentences, start=1) if sentence}

def dict_to_csv(dict_data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Sentence'])
        for id, sentence in dict_data.items():
            writer.writerow([id, sentence.lower()])

with open('books.txt', 'r', encoding='utf-8') as file:
    text = file.read()
paragraph = text

# 문장 분리 후 딕셔너리 생성
dict_sentences = sentences_to_dict(paragraph)
#print(dict_sentences)

# 딕셔너리를 CSV 파일로 저장
dict_to_csv(dict_sentences, 'sentences.csv')
print("CSV 파일 생성 완료")