import discogs_client
import time
import json
import requests
from urlextract import URLExtract
from dotenv import load_dotenv
import os
import logging
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='bountyHunter.log', encoding='utf-8', level=logging.INFO)
page = 35
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
                                try: 
                                    if release.formats[0]["name"] == "Vinyl":
                                         tmpRewardGb = rewordInGB - 15
                                         if respDataMPstats['lowest_price']['value'] < tmpRewardGb:
                                            print("vinyl release adding shipping cost")                                            
                                            logger.info("RequId: " + str(requestId) + " Bounty: " + str(rewordInGB) + "GB")
                                            print("RequId: " + str(requestId) + "Bounty: " + str(rewordInGB) + "GB")
                                            logger.info("discogsId: " + str(discogsIds))
                                            print("discogsId: ",discogsIds)      
                                            print(release.formats)
                                            logger.info(release.formats)
                                            logger.info(str(respDataMPstats['lowest_price']['value']) + str(respDataMPstats['lowest_price']['currency']))     
                                            print(respDataMPstats['lowest_price']['value'],respDataMPstats['lowest_price']['currency'])         
                                            logger.info("Good value!")      
                                            logger.info("--------------------------------------")         
                                            print("Good value?!!!!")
                                            print("--------------------------------------------")
                                    elif respDataMPstats['lowest_price']['value'] <  rewordInGB:
                                        logger.info("RequId: " + str(requestId) + " Bounty: " + str(rewordInGB) + "GB")
                                        print("RequId: " + str(requestId) + "Bounty: " + str(rewordInGB) + "GB")
                                        logger.info("discogsId: " + str(discogsIds))
                                        print("discogsId: ",discogsIds)      
                                        print(release.formats)
                                        logger.info(release.formats)
                                        logger.info(str(respDataMPstats['lowest_price']['value']) + str(respDataMPstats['lowest_price']['currency']))     
                                        print(respDataMPstats['lowest_price']['value'],respDataMPstats['lowest_price']['currency'])         
                                        logger.info("Good value!")      
                                        logger.info("--------------------------------------")         
                                        print("Good value?!!!!")
                                        print("--------------------------------------------")
                                except KeyError:
                                    print("key error skipping")                                
                    except ValueError:
                        print("Int conversion error skipping")
                    
    print("Page:",page)
    logger.info("Page: " + page)
    page = page + 1
    