import pandas as pd
import requests
import json
import csv

logs = []
url = 'https://api.salesloft.com/v2/crm_activities.json'
headers = {"Authorization": "Bearer YOUR_TOKEN"}
params = {
    'sort_direction': 'DESC',
    'per_page': '100',
    'include_paging_counts': 'true',
    'updated_at[gt]': '20220410T000000-0700'
}

pages_data = requests.get(url, params=params, headers=headers)
pages_response = json.loads(pages_data.content)
pages_metadata = pages_response['metadata']
pages_paging = pages_response['metadata']['paging']
total_pages = pages_paging['total_pages']

print(pages_metadata)
print(total_pages)

for page in range(total_pages):
    current_page = page + 1
    # print(current_page)
    r = requests.get(url + f'?page={current_page}', params=params, headers=headers)
    print(r.url)
    response_json = json.loads(r.content)
    data = response_json['data']
    for i in data:
        if i['error']:
            new_log = {
                'person_id': i['person']['id'],
                'error': i['error'],
                'activity_type': i['activity_type']
            }
            logs.append(new_log)


print(logs)

df = pd.DataFrame(logs)
df.to_csv('data.csv')
# print(df)