import requests, json, csv
import pandas as pd
from collections import defaultdict
from scipy.stats.stats import pearsonr
from scipy import stats
import os

code = {'AL': '01', 'AZ': '04', 'AR': '05', 'CA': '06', 'CO': '08', 'CT': '09', 'DC': '11', 'FL': '12', 'GA': '13',
        'ID': '16', 'IL': '17', 'IN': '18', 'IA': '19', 'KS': '20',
        'KY': '21', 'LA': '22', 'ME': '23', 'MD': '24', 'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28', 'MO': '29',
        'MT': '30', 'NE': '31', 'NV': '32', 'NJ': '34', 'NH': '33', 'NM': '35', 'NY': '36', 'DE': '10',
        'NC': '37', 'ND': '38', 'OH': '39', 'OK': '40', 'OR': '41', 'PA': '42', 'RI': '44', 'SC': '45', 'SD': '46',
        'TN': '47', 'TX': '48', 'UT': '49', 'VT': '50', 'VA': '51', 'WA': '53', 'WV': '54', 'WI': '55',
        'WY': '56'
        }

def get_data(year,state):
    url = 'http://api.census.gov/data/timeseries/healthins/sahie?get=COUNTY,GEOID,PCTUI_PT,STABREV,NAME&for=county:*&in=state:'+ code[state] +'&time='+str(year)+'&key=fe2444ef1a1a486e97a6e38e49f6b47bc435aab5'
    response = requests.get(url)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df.set_index(df['GEOID'])
    df = df[1:]
    return df


def get_data_child(year, state):
    url = 'http://api.census.gov/data/timeseries/healthins/sahie?get=COUNTY,GEOID,AGECAT,PCTUI_PT,STABREV,NAME&for=county:*&in=state:' + \
          code[state] + '&time=' + str(year) + '&key=fe2444ef1a1a486e97a6e38e49f6b47bc435aab5'
    response = requests.get(url)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df.set_index(df['GEOID'])
    df = df[1:]
    # print(df['AGECAT'])
    df = df.loc[df['AGECAT'] == '4']
    return df

def get_data_female(year, state):
    url = 'http://api.census.gov/data/timeseries/healthins/sahie?get=COUNTY,GEOID,SEXCAT,PCTUI_PT,STABREV,NAME&for=county:*&in=state:'+ code[state] +'&time='+str(year)+'&key=fe2444ef1a1a486e97a6e38e49f6b47bc435aab5'
    response = requests.get(url)
    data = json.loads(response.text)
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]
    df = df.set_index(df['GEOID'])
    df = df[1:]
    df = df.loc[df['SEXCAT'] == '1']
    return df


def get_poverty(year, state):
    if year == 2011:
        state = state.lower()
    url = 'https://www.census.gov/did/www/saipe/downloads/estmod' + str(year)[-2:] + '/est' + str(year)[
                                                                                              -2:] + '_' + state + '.txt'
    response = requests.get(url).text
    pover = []
    for line in response.split('\n'):
        li = line.split()
        if len(li) > 5:
            if len(li[1]) == 2:
                pad = '0'
            elif len(li[1]) == 1:
                pad = '00'
            elif len(li[1]) == 3:
                pad = ''
            pover.append((li[0] + pad + li[1], li[5]))
    df = pd.DataFrame(pover[1:], columns=['GEOID', 'poverty_rate'])
    return df


def merged(year, state,cat=None):
    if cat == 'mid':
        df = get_data_child(year,state)
    elif cat == 'male':
        df = get_data_female(year,state)
    else:
        df = get_data(year, state)
    df = df.merge(get_poverty(year, state))
    df = df.set_index(df['GEOID'])
    return df


def merge_by_county(state,cat=None):
    coeff = {}
    frames = {}
    predicted = {}
    uncovered = defaultdict(list)
    poverty = defaultdict(list)
    for y in range(2007, 2014):
        frames[y] = merged(y, state,cat)
    geo = list(frames[2007].index.values)
    for county in geo:
        for y in range(2007, 2014):
            uncovered[county].append(float(frames[y].ix[county]['PCTUI_PT']))
            poverty[county].append(100 - float(frames[y].ix[county]['poverty_rate']))
    for c in uncovered:
        coeff[c] = pearsonr(uncovered[c], poverty[c])
        slope1, inter1, r1, p1, stderr1 = stats.linregress(uncovered[c], list(range(2007,2014)))
        slope2, inter2, r2, p2, stderr2 = stats.linregress(poverty[c], list(range(2007,2014)))
        predicted[c] = (uncovered[c][-1] + slope1, poverty[c][-1] + slope2)
    # print(coeff)
    with open(state + 'predic.csv', 'w') as file:
        dum = csv.writer(file, lineterminator='\n')
        for c in uncovered:
            # dum.writerow([c, uncovered[c][-1] / 100, poverty[c][-1] / 100, coeff[c][0]])
            dum.writerow([c, predicted[c][0], predicted[c][1]])
    print(predicted)



# df = get_data_female(2013, 'NY')
# print(df)
# df = df.merge(get_poverty(2013,'NY'))
# df = df.set_index(df['GEOID'])
#
# df = df.drop('GEOID',1)
# geo = list(df.index.values)
# print(df)
# print(geo)
# merge_by_county('TX')
os.chdir(r'/IDS/data')
print(os.getcwd())
for s in code:
    print(s)
    merge_by_county(s)
