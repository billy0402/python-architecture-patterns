import requests

params = dict(q='Sausages', format='json')
parsed = requests.get('http://api.duckduckgo.com', params=params).json()

results = parsed['RelatedTopics']
for result in results:
    if 'Text' in result:
        print(result['FirstURL'] + ' - ' + result['Text'])
