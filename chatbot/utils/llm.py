from google.generativeai import configure, GenerativeModel
from django.conf import settings
from .similarity import get_high_similarity_quotes, get_high_similarity_keywords

# Gemini API Key를 settings에서 가져옴
GEMINI_API_KEY = settings.GEMINI_API_KEY

def generate_philosophical_advice(text: str, num_quotes: int = 3):
    """
    철학적 명언을 활용하여 사용자의 고민에 대한 상담 응답을 생성합니다.
    
    Args:
        text (str): 사용자의 고민/질문
        num_quotes (int): 최종적으로 참조할 철학적 명언의 수
    
    Returns:
        str: 철학적 조언이 담긴 응답
    """
    # 1. 키워드 기반으로 10개의 유사한 철학적 명언 검색
    initial_quotes = get_high_similarity_keywords(text, 10)
    
    # 2. 검색된 10개의 명언에 대해 직접 텍스트 유사도로 재순위화
    # 검색된 명언들의 ID만 추출
    quote_ids = [quote['id'] for quote in initial_quotes]
    
    # 3. 텍스트 유사도 기반으로 재순위화하여 상위 num_quotes개 선택
    reranked_quotes = []
    for quote_id in quote_ids:
        # 원본 명언 찾기
        original_quote = next((q for q in initial_quotes if q['id'] == quote_id), None)
        if original_quote:
            # 직접 텍스트 유사도 계산
            similarity = get_high_similarity_quotes(original_quote['quote'], 1)[0]['similarity']
            reranked_quotes.append({
                'id': original_quote['id'],
                'quote': original_quote['quote'],
                'author': original_quote['author'],
                'similarity': similarity
            })
    
    # 유사도 기준으로 내림차순 정렬하고 상위 num_quotes개 선택
    reranked_quotes.sort(key=lambda x: x['similarity'], reverse=True)
    final_quotes = reranked_quotes[:num_quotes]
    
    # 검색된 명언들을 문자열로 변환
    quotes_context = ""
    for i, quote in enumerate(final_quotes, 1):
        quotes_context += f"{i}. \"{quote['quote']}\" - {quote['author']}\n"
    
    # API 키 설정
    configure(api_key=GEMINI_API_KEY)
    
    # Gemini 모델 초기화
    model = GenerativeModel('models/gemini-2.0-flash')
    
    # 프롬프트 구성
    prompt = f"""당신은 질문-답변(Question-Answering)을 수행하는 고민 상담 AI 어시스턴트입니다. 당신의 임무는 주어진 문맥(context) 에서 주어진 질문(question) 에 답하는 것입니다.
검색된 다음 문맥(Context) 을 사용하여 질문(Question) 에 답하세요.
문맥(context) 은 철학자들의 명언 입니다. 주어진 질문(Question)에 대해 철학적인 조언을 해주세요.
말투는 성경에서 나오는 말투로 말하세요. 질문자를 당신보다 낮은 사람으로 대하세요.
반드시 한글로 답변해 주세요. 답변(Answer) 에 "'철학자 이름'가 말하기를 '명언 내용'이라고 하였다." 라는 문장을 포함하세요

#Context:
{quotes_context}

#Question:
{text}

#Answer:"""
    
    # 모델에 프롬프트 전송하고 응답 받기
    response = model.generate_content(prompt)
    
    return response.text

def chat_with_philosophy(user_query, num_quotes: int = 3):
    """
    채팅 형식으로 철학적 상담을 제공하는 함수
    
    Args:
        user_query (str): 사용자의 메시지
        num_quotes (int): 참조할 철학적 명언의 수
    
    Returns:
        str: 철학적 조언이 담긴 응답
    """
    if not user_query:
        return "질문을 입력해주세요."
    
    # 철학적 조언 생성
    response = generate_philosophical_advice(user_query, num_quotes)
    
    return response
