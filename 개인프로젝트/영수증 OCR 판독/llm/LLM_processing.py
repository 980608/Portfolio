from openai import OpenAI
from dotenv import load_dotenv,find_dotenv
from typing import List, Literal
from pydantic import BaseModel, Field, model_validator
import os
import json

load_dotenv(dotenv_path="D:/AI_Coach/backend/KEY/.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_receipt(ocr_text):

    prompt = f"""
다음은 영수증 OCR 결과이다.

{ocr_text}

규칙:
1. 구매처 추출
2. 구매 날자 추출
3. 구매 품목 추출
4. 가격 추출
5. 구매 수량 추출
6. 총액 추출
7. 카테고리 생성(식품,카페,교통)
8. JSON 형식으로 반환
9. 만약에 1~6번 중 인식 못한건 0으로 출력해줘
예시:

{{
  "storeName":"GS25",
  "purchaseAt":"2026.06.01"
  "items":[
    {{
      "name":"바나나우유",
      "price":1500,
      "quantity":1
    }}
  ],
  "totalPrice":1500
  "category":"식품"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {"raw_response": content}
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    