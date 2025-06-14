from openai import OpenAI
import os
from dotenv import load_dotenv
from image_analyzer import analyze_image

# .env 파일 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_gpt(prompt):
    try:
        # GPT 모델과 대화
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 사용할 모델
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # 응답 반환
        return response.choices[0].message.content
    except Exception as e:
        return f"에러가 발생했습니다: {str(e)}"

def main():
    print("OpenAI와 대화를 시작합니다.")
    print("1. 일반 대화")
    print("2. 이미지 분석")
    print("종료하려면 'quit'를 입력하세요.")
    
    while True:
        choice = input("\n선택하세요 (1 또는 2): ")
        
        if choice.lower() == 'quit':
            print("대화를 종료합니다.")
            break
            
        if choice == "1":
            user_input = input("\n당신: ")
            if user_input.lower() == 'quit':
                print("대화를 종료합니다.")
                break
            response = chat_with_gpt(user_input)
            print("\nGPT:", response)
            
        elif choice == "2":
            image_path = input("\n분석할 이미지의 경로를 입력하세요: ")
            prompt = input("이미지에 대해 어떤 분석을 원하시나요? ")
            response = analyze_image(image_path, prompt)
            print("\nGPT:", response)
            
        else:
            print("잘못된 선택입니다. 1 또는 2를 입력해주세요.")

if __name__ == "__main__":
    main()
