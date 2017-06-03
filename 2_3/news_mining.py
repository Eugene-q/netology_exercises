import json
import chardet
from collections import Counter

def main():
  files = ('newsafr.json', 'newscy.json', 'newsfr.json', 'newsit.json')
  for file in files:
    news = load(file)
    print(news['rss']['channel']['title'], '\n')
    words = Counter(get_words(news))
    for word, rating in words.most_common(10):
      print('{:>15} {}'.format(word, rating))
    print()
    

def get_words(news):
  all_text = ''
  for item in news['rss']['channel']['item']:
      if isinstance(item['title'], str): all_text += item['title'] + ' ' + item['description']
      else: all_text += item['title']['__cdata'] + ' ' + item['description']['__cdata']
  return filter(lambda x: 6 < len(x) < 25, map(lambda x: x.strip(',.<br>/'), all_text.split()))
    
    
def load(file):
  with open(file, 'rb') as f:
    bytes = f.read()
    return json.loads(bytes.decode(chardet.detect(bytes)['encoding']))
    
    
main()