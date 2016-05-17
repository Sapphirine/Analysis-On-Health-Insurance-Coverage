__author__ = 'Yingqi'
import re
import json
import pandas as pd
from collections import defaultdict
from alchemyapi.alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()
code = {'AL': '01', 'AZ': '04', 'AR': '05', 'CA': '06', 'CO': '08', 'CT': '09', 'DC': '11', 'FL': '12', 'GA': '13',
        'ID': '16', 'IL': '17', 'IN': '18', 'IA': '19', 'KS': '20',
        'KY': '21', 'LA': '22', 'ME': '23', 'MD': '24', 'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28', 'MO': '29',
        'MT': '30', 'NE': '31', 'NV': '32', 'NJ': '34', 'NH': '33', 'NM': '35', 'NY': '36', 'DE': '10',
        'NC': '37', 'ND': '38', 'OH': '39', 'OK': '40', 'OR': '41', 'PA': '42', 'RI': '44', 'SC': '45', 'SD': '46',
        'TN': '47', 'TX': '48', 'UT': '49', 'VT': '50', 'VA': '51', 'WA': '53', 'WV': '54', 'WI': '55',
        'WY': '56'
        }

mask = defaultdict(float, [(i,1) for i in code.values()])
print(mask)
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

tweet_path = 'health.txt'
tweet_file = open(tweet_path, 'r')
tweet_data = []
i = 0
for line in tweet_file:
    try:
        tweet = json.loads(line)
        tweet_data.append(tweet)
    except:
        continue

print(tweet_data[0]['text'],tweet_data[0]['user']['location'], type(tweet_data[0]))

for twi in tweet_data:
    # with open("health_info.txt", 'a', encoding='utf-8') as en:
    #     en.write(twi['text'] + str(twi['user']['location']) + '\n')
    if twi['user']['location']:
        if twi['user']['location'].split():
            if len(twi['user']['location'].split()[-1]) == 2 and twi['user']['location'].split()[-1].isupper():
                try:
                    state = code[twi['user']['location'].split()[-1]]
                    print(state)
                except:
                    continue
                response = alchemyapi.sentiment("text", twi['text'])
                try:
                    if 'score' in response["docSentiment"].keys():
                        mask[state] += float(response['docSentiment']['score'])/100
                        print(response['docSentiment']['score'])
                except:
                    pass
print(mask)
# for twi in tweet_data:
#     # if twi['lang'] == 'en':
#     #     with open("English.txt", 'a', encoding='utf-8') as en:
#     #         en.write(twi['text'] + '\n')
#     try:
#         if word_in_text('ibm', twi['text']) and twi['lang'] == 'en':
#             with open("ibm.txt", 'a', encoding='utf-8') as py:
#                 py.write(twi['text'] + '\n')
#         if word_in_text('microsoft', twi['text']) and twi['lang'] == 'en':
#             with open("microsoft.txt", 'a', encoding='utf-8') as py:
#                 py.write(twi['text'] + '\n')
#         if word_in_text('apple', twi['text']) and twi['lang'] == 'en':
#             with open("apple.txt", 'a', encoding='utf-8') as py:
#                 py.write(twi['text'] + '\n')
#         if word_in_text('google', twi['text']) and twi['lang'] == 'en':
#             with open("google.txt", 'a', encoding='utf-8') as py:
#                 py.write(twi['text'] + '\n')
#         if word_in_text('amazon', twi['text']) and twi['lang'] == 'en':
#             with open("amazon.txt", 'a', encoding='utf-8') as py:
#                 py.write(twi['text'] + '\n')
#     except:
#         pass