from openai import OpenAI
import os
from dotenv import load_dotenv
import base64

# .env 파일 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_path):
    """이미지를 base64로 인코딩하는 함수"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path, prompt):
    """이미지를 분석하는 함수
    
    Args:
        image_path (str): 분석할 이미지 파일의 경로
        prompt (str): 이미지에 대한 분석 요청 프롬프트
        
    Returns:
        str: GPT의 분석 결과
    """
    try:
        # 이미지를 base64로 인코딩
        base64_image = encode_image(image_path)
        
        # GPT-4 Vision 모델과 대화
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"에러가 발생했습니다: {str(e)}" 
    
def analyze_law(image_path, prompt):
    """이미지를 분석하는 함수
    
    Args:
        image_path (str): 분석할 이미지 파일의 경로
        prompt (str): 이미지에 대한 분석 요청 프롬프트
        
    Returns:
        str: GPT의 분석 결과
    """
    try:
        # 이미지를 base64로 인코딩
        base64_image = encode_image(image_path)
        
        # GPT-4 Vision 모델과 대화
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI analyst specialized in architectural drawings and their compliance with applicable building and fire safety regulations.

Your core objectives are as follows:

Analyze whether the given drawing complies with relevant legal standards, based on its structure, spatial layout, dimensions, entrances, staircases, corridors, and evacuation routes, referencing each regulation at the clause level.

If a violation is suspected, you must clearly present the violation and its basis in the following format.

To avoid providing incorrect information, if the drawing lacks sufficient detail, you must respond with "Assessment Deferred" and specify what additional information is needed to proceed with the evaluation.
"""
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"에러가 발생했습니다: {str(e)}" 

