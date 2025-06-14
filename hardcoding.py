def door_prompt(selected_language_in_prompt):
    return f"""
You are an expert in architectural floor plan analysis.

Given a floor plan image, identify:

1. Total number of visible entrance/exit doors.
2. Width of each door (in meters or feet).
3. Distance between each door pair.
4. Opening direction (e.g., inward, sliding).

Briefly explain how each result was derived using symbols, arcs, gaps, or annotations.

Respond in this format:

---  
Door Analysis Report  
- Total Doors: [Number]  
- Widths:  
  Door 1: [Width]  
  Door 2: [Width]  
  ...  
- Distances:  
  Door 1 ↔ Door 2: [Distance]  
  Door 2 ↔ Door 3: [Distance]  
  ...  
- Opening Directions:  
  Door 1: [Direction]  
  Door 2: [Direction]  
  ...  
- Notes:  
  [Assumptions or unclear parts]  
---

Respond in {selected_language_in_prompt}.
"""


def stair_prompt(selected_language_in_prompt):
    return f"""
You are an expert in evacuation code analysis.  
Analyze the floor plan image and generate a concise report including:

1. Number and location of staircases  
2. Estimated width of each staircase  
3. Evacuation flow pattern (balanced or concentrated)  
4. Brief reasoning for each point (symbols, arrows, layout, etc.)

Structure the report as follows:
- Summary  
- Findings (1–3)  
- Reasoning  
- Conclusion

Be clear and note any uncertainty. Output in {selected_language_in_prompt}.

"""

def diverse_prompt(selected_language_in_prompt):
    return f"""
You are a fire code compliance analyst.

Review the uploaded floor plan and generate a concise fire safety report covering:

1. **Corridor Clear Width**:  
   - Measure main corridors' clear width (wall-to-wall, exclude obstructions).  
   - Check compliance with NFPA 101 or local code.

2. **Egress Travel Distance**:  
   - Measure from farthest point to nearest exit.  
   - Note if path includes turns or obstacles.  
   - Compare with max code-allowed distance.

3. **Exit Door Accessibility**:  
   - Check if exits are reachable from all areas.  
   - Confirm number, spacing, and exit type.

For each, include:
- Coordinates or labels (if visible)  
- Short reasoning  
- Code reference (if any)

⚠️ Use markdown format:  
## 1. Corridor Clear Width  
## 2. Egress Travel Distance  
## 3. Exit Door Accessibility  
## Conclusion

Output in {selected_language_in_prompt}.
Be brief and technical.

"""

def final_prompt(selected_language_in_prompt, target_law, target_stair, answer_door, answer_stair, answer_diverse):
    return f"""
    You are an expert in analyzing architectural drawings for fire safety compliance. Based on the information below, determine whether the given image complies with the applicable fire safety code, and provide clear reasoning for your judgment.

### Analysis Target Information:
- Applicable Fire Code: {target_law}
- Target Floor: {target_stair}
- Language: {selected_language_in_prompt}

### Detailed Analysis Results:
1. Door Analysis  
   - Number of doors, door width, distance between doors, door opening direction  
   → {answer_door}

2. Stair Analysis  
   - Number, location, width of stairs, and whether evacuation flow is concentrated  
   → {answer_stair}

3. Additional Factors  
   - Effective corridor width, evacuation distance, availability of external exit doors  
   → {answer_diverse}

### Output Instructions:
- Final Judgment: Clearly state whether the drawing **complies** or **does not comply** with {target_law}.
- Provide a brief explanation for each item as supporting evidence for your judgment.
- The entire output should be written in {selected_language_in_prompt}.

    """

STYLE="""
    <style>
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        width: 100%;
        padding: 0;
    }
    .title {
        font-size: 64px;
        margin: 0;
        padding: 0;
        line-height: 1;
    }
    .lang-selector {
        margin: 0;
        padding: 0;
        margin-left: auto;
        display: flex;
        align-items: center;
    }
    div[data-baseweb="select"] {
        width: 200px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-baseweb="select"] > div {
        width: 200px !important;
        padding: 0 !important;
    }
    .stSelectbox {
        width: 200px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .stSelectbox > div {
        margin: 0 !important;
        padding: 0 !important;
    }
    .stSelectbox > div > div {
        margin: 0 !important;
        padding: 0 !important;
    }
    .disclaimer {
        font-size: 12px;
        color: gray;
        text-align: left;
        margin-top: 48px;
        margin-bottom: 24px;
        padding: 0;
        width: 100%;
    }
    .disclaimer-content {
        font-size: 13px;
        line-height: 1.6;
        text-align: left;
        padding: 0 24px;
    }
    .disclaimer-content h4 {
        margin-top: 16px;
        margin-bottom: 8px;
        color: #666;
    }
    .disclaimer-content p {
        margin-bottom: 12px;
    }
    /* expander 위쪽 간격만 조정 */
    section.main .streamlit-expander {
        margin-top: 12px !important;
    }
    /* Add styles for selected buttons */
    .selected-button {
        background-color: #262730 !important;
        color: white !important;
    }
    .selected-button:hover {
        background-color: #262730 !important;
        color: white !important;
    }
    /* Add style for law title subheader */
    .law-title-subheader {
        font-size: 1.2rem !important;
        margin-top: 1rem !important;
    }
    /* Add style for subtitle */
    .subtitle {
        font-size: 2rem !important;
    }
    .stFileUploader > label {
        display: none !important;
    }
    </style>
"""

MULTY_LANGUAGE={
        "🇰🇷 대한민국": {
            "summary": "CODE SCAN은 건축 도면을 기반으로 피난안전 항목을 자동 분석하는 참고용 무료 도구입니다. 본 결과는 실제 인허가를 대체하지 않으며, 전문가 검토가 필요합니다. 분석 정확성 및 법적 책임은 제한됩니다. 이용 시 본 고지에 동의한 것으로 간주합니다.",
            "expander_label": "전체 고지문 보기",
            "full": '''
**1. 법적 책임 한정 고지 (Legal Disclaimer)**\nCODE SCAN은 초기 건축 설계단계에서 참고용으로 제공되는 무료 도구입니다. 제공되는 분석 결과는 법적 효력을 가지지 않으며, 설계 승인, 인허가 심사, 법령 적합 판정을 대체하지 않습니다. 사용자 또는 제3자가 이 서비스를 이용하거나 신뢰하여 발생한 어떠한 직접적 또는 간접적 손해에 대해서도 회사는 책임을 지지 않습니다.\n\n**2. 비전문 보조 도구 고지 (Not a Professional Tool)**\nCODE SCAN은 건축사, 소방기술사, 감리자 등 전문가의 판단을 보완하기 위한 참고 도구입니다. 사용자는 분석 결과를 최종 판단이나 설계 결정을 위한 절대적 기준으로 삼지 않아야 하며, 반드시 전문 검토를 병행해야 합니다.\n\n**3. 데이터 정확성 및 한계 고지 (Accuracy Limitation)**\n본 앱은 AI 기반 이미지 자동 분석 도구로서, 도면의 해상도, 표기 방식, 문서 구조 등에 따라 분석 정확도가 달라질 수 있습니다. 일부 객체(예: 문 방향, 계단폭 등)는 인식률이 낮거나 분석이 제한될 수 있으며, AI 모델의 특성상 결과의 완전성과 최신성은 보장되지 않습니다.\n\n**4. 저작권 및 라이선스 고지 (Copyright Notice)**\nCODE SCAN이 제공하는 콘텐츠(설명문, 분석 알고리즘, UI 등)의 저작권은 회사에 귀속되며, 무단 복제, 재가공, 재배포, 크롤링 등을 금지합니다. 본 서비스는 Tesseract OCR, OpenCV, Roboflow 등 오픈소스를 사용하며, 각 오픈소스 라이선스 조건에 따라 사용되고 있습니다.\n\n**5. 국가별 법규 적용 고지 (Jurisdiction Scope Notice)**\nCODE SCAN은 한국(건축법), 미국(NFPA 101), 프랑스(ERP 1)의 공개된 피난 관련 건축 기준을 기반으로 자동 분석을 제공합니다. 각국 및 지역의 실제 적용 법규는 시점, 건물용도, 규모 등에 따라 상이할 수 있으며, 본 앱은 이를 모두 반영하지 않습니다. 이 앱에 포함된 모든 법규 기준은 공식 문서에서 발췌된 요약 정보이며, 원문 확인 및 최종 설계 검토는 반드시 해당 국가의 공식 해석 기관 또는 전문가를 통해 이루어져야 합니다.\n\n각 법규의 공식 문서는 다음 사이트를 통해 열람할 수 있습니다:\n- 한국: www.law.go.kr\n- 미국: www.nfpa.org\n- 프랑스: www.legifrance.gouv.fr\n\n**6. 데이터 처리 및 보안 고지 (Data Usage & Privacy)**\nCODE SCAN은 사용자가 업로드한 도면 이미지 또는 PDF를 일시적으로 서버에 저장하여 분석을 수행합니다. 수집된 데이터는 자동 삭제되며, 개인 식별정보는 저장되지 않습니다. 서비스 품질 개선을 위해 분석 결과 일부를 익명화하여 내부 통계 목적으로 활용할 수 있습니다.\n\n**7. 서비스 제공 조건 고지 (Service Scope & Stability)**\nCODE SCAN은 무료로 제공되며, 서버 점검, 기술적 장애, 정책 변경 등의 이유로 일시적 서비스 중단이 발생할 수 있습니다. 회사는 사전 통보 없이 기능을 수정하거나 서비스 운영을 중단할 수 있습니다. 무료 서비스 특성상 일정 수준 이상의 품질, 연속성, 대응 서비스는 보장되지 않습니다.\n\n**8. 광고 및 외부 연동 고지 (Ads & External Links)**\n본 서비스는 무료 운영 유지를 위해 일부 광고를 포함할 수 있으며, 외부 링크나 콘텐츠로 연결될 수 있습니다. 외부 사이트에서 제공하는 정보나 서비스에 대해서는 CODE SCAN이 통제하지 않으며, 그 신뢰도와 안전성에 대한 책임을 지지 않습니다.'''
        },
        "🇫🇷 France": {
            "summary": "CODE SCAN est un outil gratuit de référence basé sur les plans de construction pour l'analyse de la sécurité incendie. Les résultats ne remplacent pas les autorisations officielles et nécessitent une validation professionnelle. L'exactitude de l'analyse et la responsabilité légale sont limitées. L'utilisation implique l'acceptation de cet avis.",
            "expander_label": "Afficher l'avis complet",
            "full": '''
**1. Limitation de responsabilité légale**\nCODE SCAN est un outil gratuit fourni à titre indicatif lors de la phase initiale de conception architecturale. Les résultats n'ont aucune valeur légale et ne remplacent pas l'approbation des plans, l'examen réglementaire ou la conformité légale. L'entreprise décline toute responsabilité pour tout dommage direct ou indirect résultant de l'utilisation ou de la confiance accordée à ce service.\n\n**2. Outil d'assistance non professionnel**\nCODE SCAN est un outil d'aide destiné à compléter le jugement des architectes, ingénieurs en sécurité incendie et contrôleurs techniques. Les utilisateurs ne doivent pas se fier exclusivement aux résultats pour des décisions finales et doivent toujours consulter un professionnel.\n\n**3. Limites de précision des données**\nCette application utilise l'IA pour l'analyse automatique des images. La précision peut varier selon la résolution, la notation ou la structure des plans. Certains objets (ex : sens des portes, largeur des escaliers) peuvent être mal reconnus ou non analysés. L'exhaustivité et l'actualité des résultats ne sont pas garanties.\n\n**4. Droits d'auteur et licences**\nLes contenus fournis par CODE SCAN (textes, algorithmes, interface) sont protégés par le droit d'auteur. Toute reproduction, modification ou redistribution est interdite. Ce service utilise des logiciels open source (Tesseract OCR, OpenCV, Roboflow) conformément à leurs licences respectives.\n\n**5. Portée des réglementations nationales**\nCODE SCAN propose une analyse automatique basée sur les normes d'évacuation de la Corée (loi sur la construction), des États-Unis (NFPA 101) et de la France (ERP 1). Les réglementations applicables peuvent varier selon le lieu, l'usage ou la taille du bâtiment. Les critères présentés sont des résumés extraits des documents officiels ; la vérification finale doit être effectuée par un organisme ou un expert compétent.\n\nConsultez les textes officiels sur :\n- Corée : www.law.go.kr\n- États-Unis : www.nfpa.org\n- France : www.legifrance.gouv.fr\n\n**6. Traitement des données et confidentialité**\nCODE SCAN stocke temporairement les images ou PDF téléchargés pour analyse. Les données sont automatiquement supprimées et aucune information personnelle n'est conservée. Certaines données anonymisées peuvent être utilisées à des fins statistiques internes.\n\n**7. Conditions de service**\nCODE SCAN est gratuit. Des interruptions temporaires peuvent survenir pour maintenance, problèmes techniques ou changements de politique. L'entreprise peut modifier ou interrompre le service sans préavis. La qualité, la continuité et le support ne sont pas garantis.\n\n**8. Publicité et liens externes**\nCe service peut contenir des publicités ou des liens externes pour assurer sa gratuité. CODE SCAN n'est pas responsable du contenu ou de la fiabilité des sites externes.'''
        },
        "🇺🇸 United States": {
            "summary": "CODE SCAN is a free reference tool based on architectural drawings for analyzing fire safety elements. The results do not replace official permits and require professional review. Analysis accuracy and legal responsibility are limited. Use of this tool implies acceptance of this disclaimer.",
            "expander_label": "View full disclaimer",
            "full": '''
**1. Legal Disclaimer**\nCODE SCAN is a free tool provided for reference at the initial stage of architectural design. The analysis results have no legal effect and do not replace design approval, regulatory review, or legal compliance. The company is not liable for any direct or indirect damages resulting from the use of or reliance on this service.\n\n**2. Not a Professional Tool**\nCODE SCAN is intended to supplement the judgment of architects, fire safety engineers, and supervisors. Users should not rely solely on the analysis results for final decisions and must always seek professional review.\n\n**3. Accuracy Limitation**\nThis app uses AI-based image analysis, and accuracy may vary depending on drawing resolution, notation, and document structure. Some objects (e.g., door direction, stair width) may be poorly recognized or not analyzed. Completeness and timeliness of results are not guaranteed.\n\n**4. Copyright Notice**\nAll content provided by CODE SCAN (descriptions, algorithms, UI, etc.) is copyrighted. Unauthorized reproduction, modification, redistribution, or crawling is prohibited. This service uses open-source software (Tesseract OCR, OpenCV, Roboflow) under their respective licenses.\n\n**5. Jurisdiction Scope Notice**\nCODE SCAN provides automatic analysis based on public fire evacuation standards from Korea (Building Act), the US (NFPA 101), and France (ERP 1). Actual applicable regulations may vary by time, building use, and scale. All legal criteria in this app are summarized from official documents; final review must be conducted by the relevant national authority or a professional.\n\nOfficial documents can be found at:\n- Korea: www.law.go.kr\n- US: www.nfpa.org\n- France: www.legifrance.gouv.fr\n\n**6. Data Usage & Privacy**\nCODE SCAN temporarily stores uploaded drawing images or PDFs for analysis. Collected data is automatically deleted, and no personal information is stored. Some anonymized results may be used for internal statistics to improve service quality.\n\n**7. Service Scope & Stability**\nCODE SCAN is provided free of charge. Temporary service interruptions may occur due to maintenance, technical issues, or policy changes. The company may modify or discontinue the service without notice. No guarantee is provided for quality, continuity, or support.\n\n**8. Ads & External Links**\nThis service may include ads or external links to maintain free operation. CODE SCAN is not responsible for the reliability or safety of external sites or content.'''
        }
    }