import discogs_client
import time
import json
import requests
from urlextract import URLExtract
from dotenv import load_dotenv
import os
load_dotenv()

page = 8
while True :
    url = "https://redacted.ch/ajax.php?action=requests&media[]=7&bitrates[]=8&page="+str(page)
    payload = {}
    headers = {
    'Authorization': os.getenv('RED_API_KEY')
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    respData = json.loads(response.text)
    for request in respData['response']['results']:
        requestId = request['requestId']
        rewordInGB = request['bounty'] / 1000000000
        if "www.discogs.com/release/" in request['description']:
            for line in request['bbDescription'].splitlines():
                if "www.discogs.com/release/" in line:
                    extractor = URLExtract()
                    arrayOfUrlSplitBySlash = extractor.find_urls(line)[0].replace("[/url]","").split("-")[0].split("/")
                    discogsIds = arrayOfUrlSplitBySlash[len(arrayOfUrlSplitBySlash)-1]
                    d = discogs_client.Client('ExampleApplication/0.1')
                    try:
                        release = d.release(int(discogsIds))
                        if release.marketplace_stats.num_for_sale is not None:
                            if release.marketplace_stats.num_for_sale > 0:
                                time.sleep(1)
                                responseMPStats = requests.request("GET", "https://api.discogs.com/marketplace/stats/"+discogsIds+"?curr_abbr=EUR", headers={}, data={})
                                respDataMPstats = json.loads(responseMPStats.text)
                                if respDataMPstats['lowest_price']['value'] < rewordInGB:
                                    print("RequId: ",requestId,"Bounty: ", rewordInGB,"GB")
                                    print("discogsId: ",discogsIds)           
                                    print(respDataMPstats['lowest_price']['value'],respDataMPstats['lowest_price']['currency'])                        
                                    print("Good value?!!!!")
                                print("--------------------------------------------")
                    except ValueError:
                        print("Int conversion error skipping")
                    
    print("Page:",page)
    page = page + 1
    