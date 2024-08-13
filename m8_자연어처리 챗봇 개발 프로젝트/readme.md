# CSV 파일 읽기
# 우대 조건 제공(CSV에서 읽어온 우대 조건을 기반으로 사용자가 선택할 수 있도록 제공)
# 우대 금리 계산(사용자가 선택한 우대 조건에 따라 각 상품별 최종 금리를 계산)
# 최종 추천 상품 제공(최종적으로 우대 금리를 반영한 추천 상품 상위 3개를 출력하고, ChatGPT API를 통해 추가 정보(기본 금리 상위 3개)를 제공)
import openai
import pandas as pd

# 1. OpenAI API 키 설정
openai.api_key = ''

# 2. CSV 파일 불러오기
file_path = 'interest_rate_data.csv'  # 실제 CSV 파일 경로
data = pd.read_csv(file_path)

# 3. 시스템 프롬프트 설정
system_prompt = """
  당신은 은행 저축은행의 예금, 적금, 파킹통장 상품을 추천해주는 에이전트입니다.
  당신은 은행 업무에 전문적입니다.

  *프로세스*
  1. 사용자에게 간단한 인적사항을 입력받습니다. 예를 들면, 나이, 예금 혹은 적금하고자 하는 금액, 기간 등 입니다.
  2. 해당 조건에 적합한 상품을 찾습니다.
  3. 찾은 상품을 *상품을 추천해주는 형태* 와 같이 응답합니다.
  4. 우대 조건이 있는 상품의 경우, 우대 조건들을 고객에게 알려주고, 고객이 선택한 조건에 따라 최대로 받을 수 있는 우대 금리를 계산합니다.
  5. 최종적으로 기본 금리 상품 상위 3개와 우대 조건을 고려한 상품 상위 3개를 추천합니다.

  *상품을 추천해주는 형태*
  - 우대 조건이 있는 상품 중에 최고 우대 금리가 가장 높은 상품 상위 3개를 추천합니다.
  - 우대 조건이 있는 상품 추천 응답은
    '상품명 - 은행명'
    '금리'
    '가입대상'
    '상품 안내'
    '우대 조건'
    의 형태로 답변합니다.
  - 동시에 우대 조건이 없는 상품 중에 세후 이자율이 가장 높은 상품 상위 3개를 추천합니다.
  - 상품 추천 응답은
    '상품명 - 은행명'
    '금리'
    '가입대상'
    '상품 안내'
    의 형태로 답변합니다.

  *금융 상품의 특성*
  - 1금융권 : KDB산업은행, NH농협은행, 신한은행, 우리은행, SC제일은행, 하나은행, IBK기업은행, KB국민은행, 한국씨티은행, Sh수협은행, iM뱅크(구 대구은행), BNK부산은행, 광주은행, 제주은행, 전북은행, BNK경남은행, 케이뱅크, 카카오뱅크, 토스뱅크
  - 2금융권 : 

  *성격*
  - 당신은 항상 친절한 은행상담원과 같은 성격을 가지고 있습니다.
  - 당신은 언제나 한글로 응답을 하고 언제나 존댓말을 사용합니다.
"""

# 4. 사용자 프롬프트 예시
user_prompt = "나는 20살 여자고, 매달 20만원 씩 적금을 12개월동안 할 거 같은데 나한테 추천해줄만한 적금 상품이 있을까?"

# 5. Chat API 호출
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.5,
    top_p=0.8,
)

# 6. 우대 조건을 고객에게 제시하고 선택받기
response_text = response['choices'][0]['message']['content']
print(response_text)

# 우대 조건을 제공할 때 상품별로 제공
for index, row in data.iterrows():
    print(f"\n상품명: {row['상품명']} - {row['은행명']}")
    print(f"기본 금리: {row['기본 금리']}")
    conditions = []
    for i in range(1, 4):
        if pd.notna(row[f'우대 조건 {i}']):
            conditions.append(f"{i}: {row[f'우대 조건 {i}']} ({row[f'우대 조건 {i} 금리']}%)")
    print("우대 조건:")
    print(", ".join(conditions))

# 7. 사용자가 선택한 우대 조건을 받아 우대 금리 계산
user_selected_conditions = {
    "상품 A": ["1", "2"],  # 예시로 사용자가 선택한 조건
    "상품 B": ["1"]
}

# 8. 각 상품별 최종 금리 계산
final_rates = {}
for index, row in data.iterrows():
    product_name = row['상품명']
    base_rate = float(row['기본 금리'].replace('%', ''))
    bonus_rate = 0.0
    
    if product_name in user_selected_conditions:
        for condition in user_selected_conditions[product_name]:
            bonus_rate += float(row[f'우대 조건 {condition} 금리'].replace('%', ''))
    
    final_rates[product_name] = base_rate + bonus_rate

# 9. 최종 추천 상품 목록 (우대 조건 포함)
sorted_products = sorted(final_rates.items(), key=lambda item: item[1], reverse=True)
top_3_products = sorted_products[:3]

print("\n최종 추천 상품 목록 (우대 금리 포함):")
for product, rate in top_3_products:
    print(f"{product}: {rate:.2f}%")

# 10. Chat API를 다시 호출하여 최종 추천 상품 목록을 가져오기
final_prompt = f"""
사용자가 선택한 우대 조건을 고려하여 최종적으로 추천하는 상품 상위 3개는 다음과 같습니다:
{', '.join([f'{product}: {rate:.2f}%' for product, rate in top_3_products])}
"""

final_response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": final_prompt}
    ],
    temperature=0.5,
    top_p=0.8,
)

# 11. 최종 추천 상품 출력
print("\n최종 추천 상품 목록:")
print(final_response['choices'][0]['message']['content'])


=> 설명: OpenAI의 GPT-4 모델을 호출하여 사용자에게 답변을 생성합니다. system_prompt와 user_prompt를 메시지로 전달하여 챗봇이 역할을 이해하고 사용자의 질문에 맞는 답변을 생성하도록 합니다. temperature와 top_p는 생성된 답변의 다양성을 조절하는 파라미터입니다.
=> 설명: 이전 단계에서 생성된 응답(response)에서 텍스트 내용을 추출하여 출력합니다. 이 텍스트는 챗봇이 사용자에게 제공하는 우대 조건이나 기타 정보를 포함할 수 있습니다.
=> 설명: CSV 파일의 각 행을 반복(iterrows)하면서 상품 정보를 출력합니다. 각 상품의 기본 금리와 우대 조건을 사용자에게 보여줍니다. pd.notna는 특정 우대 조건이 존재하는지 확인합니다. 이 정보를 바탕으로 사용자는 어떤 조건이 본인에게 적용되는지 선택할 수 있습니다.
=> 설명: user_selected_conditions는 사용자가 선택한 우대 조건을 저장하는 딕셔너리입니다. 각 상품에 대해 사용자가 선택한 우대 조건 번호를 기록합니다. 예를 들어, 상품 A의 경우 사용자가 "자동이체"와 "급여 이체" 조건을 선택했다는 뜻입니다.
=> 설명: user_selected_conditions는 사용자가 선택한 우대 조건을 저장하는 딕셔너리입니다. 각 상품에 대해 사용자가 선택한 우대 조건 번호를 기록합니다. 예를 들어, 상품 A의 경우 사용자가 "자동이체"와 "급여 이체" 조건을 선택했다는 뜻입니다.
=> 설명: 최종 추천 상품 목록을 사용해 다시 ChatGPT API를 호출합니다. 사용자가 선택한 우대 조건을 반영한 최종 추천 상품 목록을 챗봇에게 전달하여 최종 응답을 생성합니다.
=> 설명: 최종 응답을 출력하여 사용자에게 최적의 금융 상품을 추천합니다. 이 결과는 챗봇이 최종적으로 제공하는 금융 상품 목록입니다.
====> 요약
이 코드는 사용자가 제공한 CSV 파일의 금융 상품 정보를 기반으로, 우대 조건을 선택한 후 최적의 금융 상품을 추천하는 과정을 구현합니다. CSV 파일에서 정보를 읽어와 각 상품의 우대 금리를 계산하고, 그 결과를 사용자에게 보여줍니다. ChatGPT API를 통해 사용자와의 대화 흐름을 유지하면서 최종적인 금융 상품 추천을 제공합니다.
