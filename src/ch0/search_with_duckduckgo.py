import duckduckgo

for result in duckduckgo.query('Sausages').results:
    print(result.url + ' - ' + result.text)
