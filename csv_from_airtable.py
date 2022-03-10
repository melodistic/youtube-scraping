import requests
import pandas as pd
base_id = "appdmQl5OgLBOX1IB"
table_name = "tblVKLaFZ1nRz6TL9"
API_KEY = "keyLAJQI8EI5uOf28"
url = "https://api.airtable.com/v0/" + base_id + "/" + table_name + "?api_key=" + API_KEY
response = requests.get(url)
data = []
for i in response.json()['records']:
    field = i['fields']
    data.append([field['id'],field['title'],field['mood']])
df = pd.DataFrame(data,columns=["id","title","mood"])
df.to_csv("list.csv",index=False)