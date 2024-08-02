search_id = "a0d4c08ae75844aa1"
api_key = "AIzaSyBT_Pz4Gk_nKUNtgl3qNAtyFYEoiYtMtF4"

import requests

google = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_id}&q=site:https://static.buku.kemdikbud.go.id/content/pdf/bukuteks/k13/bukusiswa/&start=' + '{}'

results = []
with requests.Session() as session:
    start = 1
    while True:
        result = session.get(google.format(start)).json()
        print(result)
        if 'nextPage' in result['queries'].keys():
            start = result['queries']['nextPage'][0]['startIndex']
            print(start)
        else:
            break
        results += result['items']
print(results)