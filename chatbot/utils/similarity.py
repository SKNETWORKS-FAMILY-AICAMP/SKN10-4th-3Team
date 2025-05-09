
from django.db import connection
from .vectorizer import OpenAI_vectorizer
from .extract_keyword import get_keyword

# 코사인 유사도 계산을 위한 Raw SQL
def get_high_similarity_quotes(text: str, top_k: int):
    # Get the embedding for the input text
    text_emb = OpenAI_vectorizer(text)
    
    # SQL query to find similar quotes based on embedding similarity
    query = f'''
        WITH cosine_sim AS (
            SELECT 
                id,
                quote,
                author,
                1 - (quote_emb <=> %s) AS similarity
            FROM public."chatbot_philosophydata"
        )
        SELECT id, quote, author, similarity
        FROM cosine_sim
        ORDER BY similarity DESC
        LIMIT {top_k};
    '''
    
    # Execute raw SQL through Django ORM
    with connection.cursor() as cursor:
        cursor.execute(query, [text_emb])
        results = cursor.fetchall()
    
    # Convert results to list of dictionaries
    results = [
        {
            "id": id,
            "quote": quote,
            "author": author,
            "similarity": round(similarity, 2)
        } for id, quote, author, similarity in results
    ]
    
    return results

def get_high_similarity_keywords(text: str, top_k: int):
    # 키워드 추출
    keywords = get_keyword(text)

    # Get the embedding for the input text
    keywords_emb = OpenAI_vectorizer(keywords)
    
    # SQL query to find similar quotes based on embedding similarity
    query = f'''
        WITH cosine_sim AS (
            SELECT 
                id,
                quote,
                author,
                quote_keywords,
                1 - (keywords_emb <=> %s) AS similarity
            FROM public."chatbot_philosophydata"
        )
        SELECT id, quote, author, quote_keywords, similarity
        FROM cosine_sim
        ORDER BY similarity DESC
        LIMIT {top_k};
    '''
    
    # Execute raw SQL through Django ORM
    with connection.cursor() as cursor:
        cursor.execute(query, [keywords_emb])
        results = cursor.fetchall()
    
    # Convert results to list of dictionaries
    results = [
        {
            "id": id,
            "quote": quote,
            "author": author,
            "quote_keywords": quote_keywords,
            "similarity": round(similarity, 2)
        } for id, quote, author, quote_keywords, similarity in results
    ]
    
    return results
