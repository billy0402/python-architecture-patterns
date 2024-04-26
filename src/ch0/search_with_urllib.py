import json
from urllib.parse import urlencode
from urllib.request import urlopen

params = dict(q='Sausages', format='json')
handle = urlopen('http://api.duckduckgo.com' + '?' + urlencode(params))
raw_text = handle.read().decode('utf8')
parsed = json.loads(raw_text)

results = parsed['RelatedTopics']
for result in results:
    if 'Text' in result:
        print(result['FirstURL'] + ' - ' + result['Text'])
