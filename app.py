import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import streamlit.components.v1 as components
import base64
import fitz  # PyMuPDF for PDF handling
import cv2
from pdf2image import convert_from_bytes
from image_analyzer import analyze_image, analyze_law
import os
from datetime import datetime
import time
import json
from hardcoding import *

def image_analysis(file_path):
    target_stair = "피난층" if (st.session_state.selected_floor == "피난층" or st.session_state.selected_floor == "Niveau d'évacuation" or st.session_state.selected_floor == "Exit Level") else "지상층" if (st.session_state.selected_floor == "지상층" or st.session_state.selected_floor == "Étage" or st.session_state.selected_floor == "Ground") else "지하층"
    target_law = korean_law if (st.session_state.selected_law == "대한민국법" or st.session_state.selected_law == "Loi coréenne" or st.session_state.selected_law == "Korean Law" ) else france_law if (st.session_state.selected_law == "프랑스법" or st.session_state.selected_law == "Loi française" or st.session_state.selected_law == "French Law") else usa_law
    selected_language = "한국" if (country == "🇰🇷 대한민국") else "프랑스" if (country == "🇫🇷 France") else "미국"
    selected_language_in_prompt = "Korean" if (country == "🇰🇷 대한민국") else "France" if (country == "🇫🇷 France") else "English"
    
    print("^^^ chat ^^^")
    question_door = door_prompt(selected_language_in_prompt)
    with st.spinner("출입문 분석 중..." if selected_language == "한국" else "Analyse des portes en cours..." if selected_language == "프랑스" else "Analyzing doors..."):
        answer_door = analyze_image(file_path, question_door)
    print(answer_door)
    print("vvv chat vvv")

    print("^^^ chat ^^^")
    question_stair=stair_prompt(selected_language_in_prompt)
    with st.spinner("계단 분석 중..." if selected_language == "한국" else "Analyse des escaliers en cours..." if selected_language == "프랑스" else "Analyzing stairs..."):
        answer_stair = analyze_image(file_path, question_stair)
    print(answer_stair)
    print("vvv chat vvv")

    print("^^^ chat ^^^")
    question_diverse=diverse_prompt(selected_language_in_prompt)
    with st.spinner("추가 요소 분석 중..." if selected_language == "한국" else "Analyse des éléments supplémentaires en cours..." if selected_language == "프랑스" else "Analyzing additional elements..."):
        answer_diverse = analyze_image(file_path, question_diverse)
    print(answer_diverse)
    print("vvv chat vvv")

    print("^^^ chat ^^^")
    question_final = final_prompt(selected_language_in_prompt, target_law, target_stair, answer_door, answer_stair, answer_diverse)
    with st.spinner("법규 준수 여부 분석 중..." if selected_language == "한국" else "Analyse de la conformité aux réglementations en cours..." if selected_language == "프랑스" else "Analyzing regulatory compliance..."):
        answer_final = analyze_law(file_path, question_final)
    print(answer_final)
    st.markdown("---")
    st.markdown("### 📋 최종 분석 결과" if selected_language == "한국" else "### 📋 Résultat de l'analyse finale" if selected_language == "프랑스" else "### 📋 Final Analysis Result")
    st.write(f"{answer_final}")
    
    st.markdown("---")
    st.markdown("### 🔍 상세 분석 결과" if selected_language == "한국" else "### 🔍 Résultats détaillés" if selected_language == "프랑스" else "### 🔍 Detailed Analysis")
    
    st.markdown("#### 🚪 출입문 분석" if selected_language == "한국" else "#### 🚪 Analyse des portes" if selected_language == "프랑스" else "#### 🚪 Door Analysis")
    st.write(f"{answer_door}")
    
    st.markdown("#### 🪜 계단 분석" if selected_language == "한국" else "#### 🪜 Analyse des escaliers" if selected_language == "프랑스" else "#### 🪜 Stair Analysis")
    st.write(f"{answer_stair}")
    
    st.markdown("#### 📐 추가 요소 분석" if selected_language == "한국" else "#### 📐 Analyse des éléments supplémentaires" if selected_language == "프랑스" else "#### 📐 Additional Elements Analysis")
    st.write(f"{answer_diverse}")
    print("vvv chat vvv")

# Load JSON files
with open('korean_law.json', 'r', encoding='utf-8') as f:
    korean_law = json.load(f)

with open('france_law.json', 'r', encoding='utf-8') as f:
    france_law = json.load(f)

with open('usa_law.json', 'r', encoding='utf-8') as f:
    usa_law = json.load(f)

# 페이지 설정
st.set_page_config(
    page_title="Code Scan",
    page_icon="🖼️",
    layout="wide"
)

# 커스텀 CSS 추가
st.markdown(STYLE, unsafe_allow_html=True)

# 약관 본문(임시 텍스트, 마크다운)
terms_md = '''
**제1조(목적)**\n이 약관은 CODE SCAN 서비스(이하 '서비스')의 이용조건 및 절차, 이용자와 회사의 권리·의무 및 책임사항을 규정함을 목적으로 합니다.\n\n**제2조(이용계약의 성립)**\n서비스를 이용하고자 하는 자는 본 약관에 동의함으로써 이용계약이 성립됩니다.\n\n**제3조(서비스의 제공 및 변경)**\n회사는 서비스의 내용을 변경할 수 있으며, 변경 시 사전에 공지합니다.\n\n**제4조(이용자의 의무)**\n이용자는 관계법령, 본 약관의 규정, 이용안내 및 서비스와 관련하여 공지한 주의사항을 준수하여야 합니다.\n\n**제5조(면책조항)**\n회사는 서비스 제공과 관련하여 고의 또는 중대한 과실이 없는 한 책임을 지지 않습니다.\n'''

# 약관 경고문, 버튼, 본문(8개 항목) 다국어 텍스트 정의
terms_texts = {
    "🇰🇷 대한민국": {
        "warn": "※ 본 약관에 동의하지 않을 경우 서비스 이용에 제한이 있을 수 있습니다.",
        "button": "동의하고 시작하기",
        "body": '''
**1. 법적 책임 고지**  
CODE SCAN은 초기 건축 설계단계에서 참고용으로 제공되는 무료 도구입니다. 제공되는 분석 결과는 법적 효력을 가지지 않으며, 설계 승인, 인허가 심사, 법령 적합 판정을 대체하지 않습니다. 사용자 또는 제3자가 이 서비스를 이용하거나 신뢰하여 발생한 어떠한 직접적 또는 간접적 손해에 대해서도 회사는 책임을 지지 않습니다.

**2. 비전문 도구 고지**  
CODE SCAN은 건축사, 소방기술사, 감리자 등 전문가의 판단을 보완하기 위한 참고 도구입니다. 사용자는 분석 결과를 최종 판단이나 설계 결정을 위한 절대적 기준으로 삼지 않아야 하며, 반드시 전문 검토를 병행해야 합니다.

**3. 데이터 정확성 및 한계 고지**  
본 앱은 AI 기반 이미지 자동 분석 도구로서, 도면의 해상도, 표기 방식, 문서 구조 등에 따라 분석 정확도가 달라질 수 있습니다. 일부 객체(예: 문 방향, 계단폭 등)는 인식률이 낮거나 분석이 제한될 수 있으며, AI 모델의 특성상 결과의 완전성과 최신성은 보장되지 않습니다.

**4. 저작권 및 라이선스 고지**  
CODE SCAN이 제공하는 콘텐츠(설명문, 분석 알고리즘, UI 등)의 저작권은 회사에 귀속되며, 무단 복제, 재가공, 재배포, 크롤링 등을 금지합니다. 본 서비스는 Tesseract OCR, OpenCV, Roboflow 등 오픈소스를 사용하며, 각 오픈소스 라이선스 조건에 따라 사용되고 있습니다.

**5. 국가별 법규 적용 고지**  
CODE SCAN은 한국(건축법), 미국(NFPA 101), 프랑스(ERP 1)의 공개된 피난 관련 건축 기준을 기반으로 자동 분석을 제공합니다. 각국 및 지역의 실제 적용 법규는 시점, 건물용도, 규모 등에 따라 상이할 수 있으며, 본 앱은 이를 모두 반영하지 않습니다. 이 앱에 포함된 모든 법규 기준은 공식 문서에서 발췌된 요약 정보이며, 원문 확인 및 최종 설계 검토는 반드시 해당 국가의 공식 해석 기관 또는 전문가를 통해 이루어져야 합니다.

각 법규의 공식 문서는 다음 사이트를 통해 열람할 수 있습니다:
- 한국: www.law.go.kr
- 미국: www.nfpa.org
- 프랑스: www.legifrance.gouv.fr

**6. 데이터 처리 및 보안 고지**  
CODE SCAN은 사용자가 업로드한 도면 이미지 또는 PDF를 일시적으로 서버에 저장하여 분석을 수행합니다. 수집된 데이터는 자동 삭제되며, 개인 식별정보는 저장되지 않습니다. 서비스 품질 개선을 위해 분석 결과 일부를 익명화하여 내부 통계 목적으로 활용할 수 있습니다.

**7. 서비스 제공 조건 고지**  
CODE SCAN은 무료로 제공되며, 서버 점검, 기술적 장애, 정책 변경 등의 이유로 일시적 서비스 중단이 발생할 수 있습니다. 회사는 사전 통보 없이 기능을 수정하거나 서비스 운영을 중단할 수 있습니다. 무료 서비스 특성상 일정 수준 이상의 품질, 연속성, 대응 서비스는 보장되지 않습니다.

**8. 광고 및 외부 연동 고지**  
본 서비스는 무료 운영 유지를 위해 일부 광고를 포함할 수 있으며, 외부 링크나 콘텐츠로 연결될 수 있습니다. 외부 사이트에서 제공하는 정보나 서비스에 대해서는 CODE SCAN이 통제하지 않으며, 그 신뢰도와 안전성에 대한 책임을 지지 않습니다.'''
    },
    "🇫🇷 France": {
        "warn": "※ Si vous n'acceptez pas ces conditions, l'accès au service peut être limité.",
        "button": "Accepter et commencer",
        "body": '''
**1. Avertissement légal**  
CODE SCAN est un outil gratuit fourni à titre indicatif lors de la phase initiale de conception architecturale. Les résultats n'ont aucune valeur légale et ne remplacent pas l'approbation des plans, l'examen réglementaire ou la conformité légale. L'entreprise décline toute responsabilité pour tout dommage direct ou indirect résultant de l'utilisation ou de la confiance accordée à ce service.

**2. Outil non professionnel**  
CODE SCAN est un outil d'aide destiné à compléter le jugement des architectes, ingénieurs en sécurité incendie et contrôleurs techniques. Les utilisateurs ne doivent pas se fier exclusivement aux résultats pour des décisions finales et doivent toujours consulter un professionnel.

**3. Limites de précision des données**  
Cette application utilise l'IA pour l'analyse automatique des images. La précision peut varier selon la résolution, la notation ou la structure des plans. Certains objets (ex : sens des portes, largeur des escaliers) peuvent être mal reconnus ou non analysés. L'exhaustivité et l'actualité des résultats ne sont pas garanties.

**4. Droits d'auteur et licences**  
Les contenus fournis par CODE SCAN (textes, algorithmes, interface) sont protégés par le droit d'auteur. Toute reproduction, modification ou redistribution est interdite. Ce service utilise des logiciels open source (Tesseract OCR, OpenCV, Roboflow) conformément à leurs licences respectives.

**5. Portée des réglementations nationales**  
CODE SCAN propose une analyse automatique basée sur les normes d'évacuation de la Corée (loi sur la construction), des États-Unis (NFPA 101) et de la France (ERP 1). Les réglementations applicables peuvent varier selon le lieu, l'usage ou la taille du bâtiment. Les critères présentés sont des résumés extraits des documents officiels ; la vérification finale doit être effectuée par un organisme ou un expert compétent.

Consultez les textes officiels sur :
- Corée : www.law.go.kr
- États-Unis : www.nfpa.org
- France : www.legifrance.gouv.fr

**6. Traitement des données et confidentialité**  
CODE SCAN stocke temporairement les images ou PDF téléchargés pour analyse. Les données sont automatiquement supprimées et aucune information personnelle n'est conservée. Certaines données anonymisées peuvent être utilisées à des fins statistiques internes.

**7. Conditions de service**  
CODE SCAN est gratuit. Des interruptions temporaires peuvent survenir pour maintenance, problèmes techniques ou changements de politique. L'entreprise peut modifier ou interrompre le service sans préavis. La qualité, la continuité et le support ne sont pas garantis.

**8. Publicité et liens externes**  
Ce service peut contenir des publicités ou des liens externes pour assurer sa gratuité. CODE SCAN n'est pas responsable du contenu ou de la fiabilité des sites externes.'''
    },
    "🇺🇸 United States": {
        "warn": "※ If you do not agree to the terms, you may be restricted from using the service.",
        "button": "Agree and Start",
        "body": '''
**1. Legal Disclaimer**  
CODE SCAN is a free tool provided for reference at the initial stage of architectural design. The analysis results have no legal effect and do not replace design approval, regulatory review, or legal compliance. The company is not liable for any direct or indirect damages resulting from the use of or reliance on this service.

**2. Not a Professional Tool**  
CODE SCAN is intended to supplement the judgment of architects, fire safety engineers, and supervisors. Users should not rely solely on the analysis results for final decisions and must always seek professional review.

**3. Accuracy Limitation**  
This app uses AI-based image analysis, and accuracy may vary depending on drawing resolution, notation, and document structure. Some objects (e.g., door direction, stair width) may be poorly recognized or not analyzed. Completeness and timeliness of results are not guaranteed.

**4. Copyright Notice**  
All content provided by CODE SCAN (descriptions, algorithms, UI, etc.) is copyrighted. Unauthorized reproduction, modification, redistribution, or crawling is prohibited. This service uses open-source software (Tesseract OCR, OpenCV, Roboflow) under their respective licenses.

**5. Jurisdiction Scope Notice**  
CODE SCAN provides automatic analysis based on public fire evacuation standards from Korea (Building Act), the US (NFPA 101), and France (ERP 1). Actual applicable regulations may vary by time, building use, and scale. All legal criteria in this app are summarized from official documents; final review must be conducted by the relevant national authority or a professional.

Official documents can be found at:
- Korea: www.law.go.kr
- US: www.nfpa.org
- France: www.legifrance.gouv.fr

**6. Data Usage & Privacy**  
CODE SCAN temporarily stores uploaded drawing images or PDFs for analysis. Collected data is automatically deleted, and no personal information is stored. Some anonymized results may be used for internal statistics to improve service quality.

**7. Service Scope & Stability**  
CODE SCAN is provided free of charge. Temporary service interruptions may occur due to maintenance, technical issues, or policy changes. The company may modify or discontinue the service without notice. No guarantee is provided for quality, continuity, or support.

**8. Ads & External Links**  
This service may include ads or external links to maintain free operation. CODE SCAN is not responsible for the reliability or safety of external sites or content.'''
    }
}

# 동의 상태 확인 및 분기
if "agreed" not in st.session_state:
    st.session_state["agreed"] = False

# 동의 버튼 클릭 시 실행될 함수
def handle_agreement():
    st.session_state["agreed"] = True

# 헤더 컨테이너 (타이틀과 언어 선택)
st.markdown("""
    <div class="header-container">
        <h1 class="title">CODE SCAN</h1>
        <div class="lang-selector">
""", unsafe_allow_html=True)

country = st.selectbox(
    "🌐",
    ["🇰🇷 대한민국", "🇫🇷 France", "🇺🇸 United States"],
    label_visibility="collapsed"
)

st.markdown("</div></div>", unsafe_allow_html=True)

# 전체 너비를 차지하는 구분선
st.markdown('<hr style="border: 1px solid black; margin: 8px 0 24px 0;">', unsafe_allow_html=True)

if not st.session_state["agreed"]:
    # 약관 경고문
    st.markdown(f"<div style='font-size:16px; color:#d9534f; margin-bottom:16px;'>{terms_texts[country]['warn']}</div>", unsafe_allow_html=True)
    # 약관 본문
    st.markdown(terms_texts[country]["body"])
    # 동의 버튼
    if st.button(terms_texts[country]["button"], key="agree_btn", use_container_width=True):
        handle_agreement()
        # 화면을 맨 위로 스크롤하는 JavaScript 코드 추가
        st.empty()  # 현재 컨텐츠를 지우고
        time.sleep(1)
        st.rerun()  # 페이지를 새로고침
else:
    # 국가별 텍스트 설정
    texts = {
        "🇰🇷 대한민국": {
            "subtitle": "도면을 업로드하여 피난안전 분석을 시작하세요",
            "description": "이미지를 드래그하거나 클릭하여 업로드하세요",
            "floor_title": "층별 구분",
            "floor_options": ["피난층", "지하층", "지상층"],
            "law_title": "국가별 법규",
            "law_options": ["대한민국법", "프랑스법", "미국법"]
        },
        "🇫🇷 France": {
            "subtitle": "Téléversez un plan pour commencer l'analyse de sécurité incendie",
            "description": "Faites glisser ou cliquez pour importer une image",
            "floor_title": "Niveau",
            "floor_options": ["Niveau d'évacuation", "Souterrain", "Étage"],
            "law_title": "Réglementation",
            "law_options": ["Loi coréenne", "Loi française", "Loi américaine"]
        },
        "🇺🇸 United States": {
            "subtitle": "Upload your architectural drawing to start analysis",
            "description": "Drag and drop a file or click to upload",
            "floor_title": "Floor Level",
            "floor_options": ["Exit Level", "Basement", "Ground"],
            "law_title": "Regulations",
            "law_options": ["Korean Law", "French Law", "U.S. Law"]
        }
    }

    # 선택된 국가에 따른 텍스트 표시
    st.markdown(f'<div class="subtitle">{texts[country]["subtitle"]}</div>', unsafe_allow_html=True)

    # 세션 상태 초기화
    if "selected_floor" not in st.session_state:
        st.session_state.selected_floor = texts[country]["floor_options"][0]
    if "selected_law" not in st.session_state:
        st.session_state.selected_law = texts[country]["law_options"][0]

    # 층별 구분 버튼
    st.markdown(f'<div class="law-title-subheader">{texts[country]["floor_title"]}</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(texts[country]["floor_options"][0], key="floor_exit", use_container_width=True, 
                    help="", type="primary" if st.session_state.selected_floor == texts[country]["floor_options"][0] else "secondary"):
            st.session_state.selected_floor = texts[country]["floor_options"][0]
            st.rerun()
    with col2:
        if st.button(texts[country]["floor_options"][1], key="floor_basement", use_container_width=True,
                    help="", type="primary" if st.session_state.selected_floor == texts[country]["floor_options"][1] else "secondary"):
            st.session_state.selected_floor = texts[country]["floor_options"][1]
            st.rerun()
    with col3:
        if st.button(texts[country]["floor_options"][2], key="floor_ground", use_container_width=True,
                    help="", type="primary" if st.session_state.selected_floor == texts[country]["floor_options"][2] else "secondary"):
            st.session_state.selected_floor = texts[country]["floor_options"][2]
            st.rerun()


    # 국가별 법규 버튼
    st.markdown(f'<div class="law-title-subheader">{texts[country]["law_title"]}</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(texts[country]["law_options"][0], key="law_korean", use_container_width=True,
                    help="", type="primary" if st.session_state.selected_law == texts[country]["law_options"][0] else "secondary"):
            st.session_state.selected_law = texts[country]["law_options"][0]
            st.rerun()
    with col2:
        if st.button(texts[country]["law_options"][1], key="law_french", use_container_width=True,
                    help="", type="primary" if st.session_state.selected_law == texts[country]["law_options"][1] else "secondary"):
            st.session_state.selected_law = texts[country]["law_options"][1]
            st.rerun()
    with col3:
        if st.button(texts[country]["law_options"][2], key="law_us", use_container_width=True,
                    help="", type="primary" if st.session_state.selected_law == texts[country]["law_options"][2] else "secondary"):
            st.session_state.selected_law = texts[country]["law_options"][2]
            st.rerun()


    # 이미지 업로드 섹션
    # st.header("Image Upload")
    st.markdown(f'<div class="law-title-subheader">Image Upload</div>', unsafe_allow_html=True)

    # 이미지 업로더 위젯 (PDF 지원 추가)
    uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg', 'pdf'])

    if uploaded_file is not None:
        # 파일 확장자 확인
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # 현재 시간을 파일명에 추가하여 고유한 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join("uploaded_files", filename)
        
        # 파일 저장
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File saved successfully as: {filename}")
        
        # 이미지 컨테이너 스타일 정의
        st.markdown("""
            <style>
            .image-container {
                position: relative;
                width: 100%;
                margin-bottom: 20px;
            }
            .filename {
                position: absolute;
                bottom: 0;
                right: 0;
                background-color: rgba(255, 255, 255, 0.8);
                padding: 4px 8px;
                font-family: "Source Sans Pro", sans-serif;
                font-size: 14px;
                color: #262730;
            }
            </style>
        """, unsafe_allow_html=True)
        
        if file_extension in ['png', 'jpg', 'jpeg']:
            # 이미지 파일 처리
            image = Image.open(uploaded_file)
            
            # PIL Image를 OpenCV 형식으로 변환
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # 흑백 변환
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # OpenCV 이미지를 PIL Image로 다시 변환
            gray_pil_image = Image.fromarray(gray_image)
            
            # 이미지와 파일명을 포함하는 컨테이너
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(gray_pil_image, use_column_width=True)
            st.markdown(f'<div class="filename">{uploaded_file.name}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 이미지 정보 표시
            st.subheader("Image Information")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"Filename: {uploaded_file.name}")
                st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")
            
            with col2:
                st.write(f"Image size: {image.size}")
                st.write(f"Image mode: {image.mode}")

            image_analysis(file_path)
                
        elif file_extension == 'pdf':
            # PDF 파일 처리
            pdf_bytes = uploaded_file.read()
            
            # PDF를 이미지로 변환 (첫 페이지만)
            pdf_images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
            if pdf_images:
                # 첫 페이지 이미지 가져오기
                pdf_image = pdf_images[0]
                
                # PIL Image를 OpenCV 형식으로 변환
                cv_image = cv2.cvtColor(np.array(pdf_image), cv2.COLOR_RGB2BGR)
                
                # 흑백 변환
                gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
                
                # OpenCV 이미지를 PIL Image로 다시 변환
                gray_pil_image = Image.fromarray(gray_image)
                
                # PDF 미리보기와 파일명을 포함하는 컨테이너
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(gray_pil_image, use_column_width=True)
                st.markdown(f'<div class="filename">{uploaded_file.name}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # PDF 정보 표시
                st.subheader("PDF Information")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"Filename: {uploaded_file.name}")
                    st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")
                
                with col2:
                    # PDF 페이지 수 확인
                    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
                    st.write(f"Total pages: {len(pdf_document)}")
                    st.write(f"Page size: {pdf_document[0].rect}")
                
                image_analysis(file_path)

    # 하단 고지문 다국어 텍스트 정의
    footer_texts = MULTY_LANGUAGE

    # 하단 고지 (요약)
    st.markdown(f"""
        <div class="disclaimer">
            {footer_texts[country]['summary']}
        </div>
    """, unsafe_allow_html=True)

    # 전체 고지문 (확장형)
    with st.expander(footer_texts[country]['expander_label']):
        st.markdown(f"""
            <div class="disclaimer-content">
            {footer_texts[country]['full']}
            </div>
        """, unsafe_allow_html=True)
