import json
import sys
import os
import requests
from time import sleep
import configparser
import datetime
from sam_buyV2 import address_list, getRecommendStoreListByLocation

config = configparser.ConfigParser()
config.read('config.ini', "utf-8")

# ## init config ###

# 填写个人信息
deviceid = config.get('userInfo', 'deviceid')
authtoken = config.get('userInfo', 'authtoken')
trackinfo = config.get('userInfo', 'trackinfo')
keyword = '保供'


def init():
    # global address
    # global store
    address = address_list()
    store, uid = getRecommendStoreListByLocation(address.get('latitude'), address.get('longitude'))
    print('#初始化完成.')
    return address, store, uid


def search(keyword, address, store, uid):
    print('### 搜索物品关键词:{}'.format(keyword))
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/goods-portal/spu/search'
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    ret = requests.post(url=myUrl, headers=headers, json={
        "channelType": 2,
        "addressVO": {},
        "filter": [],
        "keyword": keyword,
        "excludeSpuIds": [],
        "pageNum": 1,
        "pageSize": 20,
        "sort": "0",
        "sortType": "",
        "storeInfoVOList": store,
        "uid": uid,
        "userUid": uid,
        "appId": "any",
        "saasId": "1111"
    })

    myRet = json.loads(ret.text)
    searchData = myRet['data']
    return searchData


if __name__ == '__main__':
    date_list = []
    for i in range(0, 7):
        date_list.append(
            (datetime.datetime.now() + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        )
    # 初始化
    address, store, uid = init()

    while 1:
        searchData = search(keyword, address, store, uid)
        dataList = searchData['dataList']
        if len(dataList) > 0:
            print("*** 你要的货物如下：\n")
            for data in dataList:
                print("{} 有货:{} 运输:{} 价格:{} {}".format(data["title"], data["isAvailable"], data["deliveryAttr"],
                                                        data["priceInfo"][0]["price"], data["subTitle"]))
            file = "nb.mp3"
            if sys.platform == 'darwin':
                # macOS
                os.system("open " + file)
            else:
                os.system(file)
            print("*** 快去加购物车吧：\n")
            # os.system(file)
            exit()
            break
        else:
            sleep(5)
            print("*** 没有：\n")
            continue
