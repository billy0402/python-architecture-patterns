import requests


class Result:
    url: str
    text: str

    def __init__(self, url: str, text: str):
        self.url = url
        self.text = text


class Results:
    results: list[Result]

    def __init__(self, results: list[Result]):
        self.results = results


def query(q: str) -> Results:
    params = dict(q=q, format='json')
    parsed = requests.get('http://api.duckduckgo.com', params=params).json()
    results = parsed['RelatedTopics']
    results = [
        Result(result['FirstURL'], result['Text'])
        for result in results if 'Text' in result
    ]
    return Results(results)
