import json
import chardet

def main():
  files = ('newsafr.json', 'newscy.json', 'newsfr.json', 'newsit.json')
  for file in files:
    news = load(file)
    print(news['rss']['channel']['title'], '\n')
    words = get_words(news)
    words_ratings = to_rate(words)
    for i, rating in zip(range(10), reversed(sorted(words_ratings))):
      print('{:>15} {}'.format(words_ratings[rating], rating))
    print()
    

def to_rate(words):
  rated_words = list()
  ratings = list()
  for word in words:
    if word not in rated_words:
      rated_words.append(word)
      ratings.append(words.count(word))
  return dict(zip(ratings, rated_words))
    
    
def get_words(news):
  all_text = ''
  for item in news['rss']['channel']['item']:
      all_text += item['title']['__cdata'] + ' ' + item['description']['__cdata']
  return list(filter(lambda x: len(x) > 6, list(map(lambda x: x.strip(',.<br>'), all_text.split()))))
    
    
def load(file):
  with open(file, 'rb') as f:
    bytes = f.read()
    return json.loads(bytes.decode(chardet.detect(bytes)['encoding']))
    #print(news_block['rss']['channel']['title'])
    
    
main()