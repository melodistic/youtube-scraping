import requests
import pandas as pd
base_id = "BASE_IE"
table_name = "TABLE_NAME"
API_KEY = "API_KEY"
url = "https://api.airtable.com/v0/" + base_id + "/" + table_name + "?api_key=" + API_KEY
response = requests.get(url)
data = []
for i in response.json()['records']:
    field = i['fields']
    data.append([field['id'].strip(),field['title'].strip(),field['mood'].strip()])
while response.json().get('offset'):
    response = requests.get(url + "&offset=" + response.json()['offset'])
    for i in response.json()['records']:
        field = i['fields']
        data.append([field['id'].strip(),field['title'].strip(),field['mood'].strip()])
df = pd.DataFrame(data,columns=["id","title","mood"])
df.to_csv("list.csv",index=False)
