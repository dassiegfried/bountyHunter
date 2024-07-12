
import json
import requests
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(filename='xmrBettingAnanalysis.log', encoding='utf-8', level=logging.INFO)
totalFrontWins=0
totalBackWins=0
currentBlock = 1
totalTies=0
while currentBlock < 3191339:
    time.sleep(0.1)
    url = "http://10.0.0.34:8081/api/block/"+str(currentBlock)
    payload = {}
    headers = {}
    response = ""
    while response == "":
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            break
        except:
            print("error on request sleeping and retrying")
            time.sleep(5)
            continue
    respData = json.loads(response.text)
    logger.info("Current Block: "+str(currentBlock))
    print("Current Block: "+str(currentBlock))
    logger.info("FrontWins,BackWins,totalTies: "+str(totalFrontWins)+","+str(totalBackWins)+","+str(totalTies))
    print("FrontWins,BackWins,totalTies: "+str(totalFrontWins)+","+str(totalBackWins)+","+str(totalTies))
    currentBlock = currentBlock + 1
    frontSum=0
    backSum=0
    for i in range(0, len(respData['data']['hash'])):
        if (respData['data']['hash'][i].isdigit()):
            if i < 32 :
                frontSum+= int(respData['data']['hash'][i])
            elif i >= 32:
                backSum+= int(respData['data']['hash'][i])
            else:
                print("SHULD NOT BE HERE!")
        else:
            continue
    if frontSum > backSum:
        totalFrontWins += 1
    elif backSum > frontSum:
        totalBackWins +=1
    else: 
        totalTies+=1
    frontSum=0
    backSum=0
print(totalFrontWins,totalBackWins)