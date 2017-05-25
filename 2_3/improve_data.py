import json
import chardet

with open('newsit.json') as f:
  object = json.load(f)

for item in object['rss']['channel']['item']:
  item['title'] = {'__cdata': item['title']}
  item['description'] = {'__cdata': item['description']}
  
with open('newsit.json', 'w') as f:
  json.dump(object, f)