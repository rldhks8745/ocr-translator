import requests
import json

def translate( text ) :
    request_url = "https://openapi.naver.com/v1/papago/n2mt"
    text = text

    headers = {"X-Naver-Client-Id": "pTUgzu6jo6VDYqYvTdP0", "X-Naver-Client-Secret": "CNEWNgh20a"}
    params = {"source": "en", "target": "ko", "text": text}
    response = requests.post(request_url, headers=headers, data=params)

    result = response.json()

    print(result)
    return result["message"]["result"]["translatedText"]