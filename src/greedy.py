import csv
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def get_highest_probability_sequence(model_name, word_list):
    # 모델과 토크나이저 로드
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    # 단어 리스트를 토큰화
    tokenized_words = {word: tokenizer(word, add_special_tokens=False).input_ids for word in word_list}

    # 결과 저장 리스트
    sequence = []

    # 초기 컨텍스트
    context = torch.tensor([tokenizer.bos_token_id]).unsqueeze(0)

    while tokenized_words:
        word_probabilities = {}

        # 각 단어에 대해 확률 계산
        for word, token_ids in tokenized_words.items():
            temp_context = context.clone()

            # 단어의 누적 확률 계산
            cumulative_prob = 1.0
            for token_id in token_ids:
                with torch.no_grad():
                    outputs = model(temp_context)
                    logits = outputs.logits
                token_probabilities = torch.softmax(logits[0, -1, :], dim=0)
                token_prob = token_probabilities[token_id].item()
                cumulative_prob *= token_prob
                temp_context = torch.cat([temp_context, torch.tensor([[token_id]])], dim=1)

            word_probabilities[word] = cumulative_prob

        # 가장 높은 확률의 단어 선택
        next_word = max(word_probabilities, key=word_probabilities.get)

        # 결과에 추가
        sequence.append(next_word)

        # 선택된 단어를 tokenized_words에서 제거
        del tokenized_words[next_word]

        # 선택된 단어의 토큰을 컨텍스트에 추가
        context = torch.cat([context, torch.tensor([tokenizer(next_word, add_special_tokens=False).input_ids])], dim=1)

    return sequence


# 실행 예제
model_name = "google/gemma-2-9b"  # 예시 모델 (google/gemma-2-9b로 교체 가능)

with open("sample_submission.csv", "r") as f:
    reader = csv.DictReader(f)
    sent_list = [row["text"] for row in reader]

result_list = []

for sent in sent_list:
    word_list = sent.split()
    result = get_highest_probability_sequence(model_name, word_list)
    result_list.append(" ".join(result))
    
with open("result.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["text"])
    for result in result_list:
        writer.writerow([result])