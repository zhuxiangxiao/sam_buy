import json
import requests
from time import sleep

# ## init config ###
# 填写个人信息

deviceid = 'x'
authtoken = 'x'
trackinfo = 'x'
deliveryType = '0'  # 1：极速达 2：全城配送
cartDeliveryType = 1  # 1：极速达 2：全城配送


# ## init config over ###

def getAmout(goodlist):
    global amout
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/settlement/getSettleInfo'
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '45',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'latitude': address.get('latitude'),
        'longitude': address.get('longitude'),
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    data = {
        "goodsList": goodlist,
        "uid": uid,
        "addressId": addressList_item.get('addressId'),
        "deliveryInfoVO": {
            "storeDeliveryTemplateId": good_store.get('storeDeliveryTemplateId'),
            "deliveryModeId": good_store.get('deliveryModeId'),
            "storeType": good_store.get('storeType')
        },
        "cartDeliveryType": cartDeliveryType,
        "storeInfo": {
            "storeId": good_store.get('storeId'),
            "storeType": good_store.get('storeType'),
            "areaBlockId": good_store.get('areaBlockId')
        },
        "couponList": [],
        "isSelfPickup": 0,
        "floorId": 1,
    }

    try:
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data))
        myRet = json.loads(ret.text)
        amout = myRet['data'].get('totalAmount')
        return amout
    except Exception as e:
        print('getAmout [Error]: ' + str(e))


def address_list():
    global addressList_item
    print('###初始化地址')
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/sams-user/receiver_address/address_list'
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
    ret = requests.get(url=myUrl, headers=headers)
    myRet = json.loads(ret.text)
    addressList = myRet['data'].get('addressList')
    addressList_item = []

    for i in range(0, len(addressList)):
        addressList_item.append({
            'addressId': addressList[i].get("addressId"),
            'mobile': addressList[i].get("mobile"),
            'name': addressList[i].get("name"),
            'countryName': addressList[i].get('countryName'),
            'provinceName': addressList[i].get('provinceName'),
            'cityName': addressList[i].get('cityName'),
            'districtName': addressList[i].get('districtName'),
            'receiverAddress': addressList[i].get('receiverAddress'),
            'detailAddress': addressList[i].get('detailAddress'),
            'latitude': addressList[i].get('latitude'),
            'longitude': addressList[i].get('longitude')
        })
        print('[' + str(i) + ']' + addressList[i].get("name") + addressList[i].get("mobile") + addressList[i].get(
            "districtName") + addressList[i].get("receiverAddress") + addressList[i].get("detailAddress"))
    print('根据编号选择地址:')
    s = int(input())
    addressList_item = addressList_item[s]
    # print(addressList_item)
    return addressList_item


def getRecommendStoreListByLocation(latitude, longitude):
    global uid
    global good_store

    storeList_item = []
    print('###初始化商店')
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/merchant/storeApi/getRecommendStoreListByLocation'
    data = {
        'longitude': longitude,
        'latitude': latitude}
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '45',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'latitude': latitude,
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'
    }
    try:
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data))
        myRet = json.loads(ret.text)
        storeList = myRet['data'].get('storeList')
        for i in range(0, len(storeList)):
            storeList_item.append(
                {
                    'storeType': storeList[i].get("storeType"),
                    'storeId': storeList[i].get("storeId"),
                    'areaBlockId': storeList[i].get('storeAreaBlockVerifyData').get("areaBlockId"),
                    'storeDeliveryTemplateId': storeList[i].get('storeRecmdDeliveryTemplateData').get(
                        "storeDeliveryTemplateId"),
                    'deliveryModeId': storeList[i].get('storeDeliveryModeVerifyData').get("deliveryModeId"),
                    'storeName': storeList[i].get("storeName")
                })
            print('[' + str(i) + ']' + storeList_item[i].get("storeId") + storeList_item[i].get("storeName"))
        print('根据编号下单商店:')
        s = int(input())
        good_store = storeList_item[s]
        uidUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/sams-user/user/personal_center_info'
        ret = requests.get(url=uidUrl, headers={
            'Host': 'api-sams.walmartmobile.cn',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
            'device-name': 'iPhone14,3',
            'device-os-version': '15.4',
            'device-id': deviceid,
            'latitude': latitude,
            'device-type': 'ios',
            'auth-token': authtoken,
            'app-version': '5.0.45.1'
        })
        # print(ret.text)
        uidRet = json.loads(ret.text)
        uid = uidRet['data']['memInfo']['uid']
        return storeList_item, uid
        # print(storeList_item)

    except Exception as e:
        print('getRecommendStoreListByLocation [Error]: ' + str(e))
        return False


def getUserCart(addressList, storeList, uid):
    global goodlist
    global amount

    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/cart/getUserCart'
    data = {
        # YOUR SELF
        "uid": uid, "deliveryType": deliveryType, "deviceType": "ios", "storeList": storeList, "parentDeliveryType": 1,
        "homePagelongitude": addressList.get('longitude'), "homePagelatitude": addressList.get('latitude')
    }
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '704',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'latitude': address.get('latitude'),
        'longitude': address.get('longitude'),
        'track-info': trackinfo,
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'

    }
    try:
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data))
        # print(ret.text)
        myRet = json.loads(ret.text)
        # print(myRet['data'].get('capcityResponseList')[0])
        normalGoodsList = (myRet['data'].get('floorInfoList')[0].get('normalGoodsList'))
        # time_list = myRet['data'].get('capcityResponseList')[0].get('list')
        for i in range(0, len(normalGoodsList)):
            spuId = normalGoodsList[i].get('spuId')
            storeId = normalGoodsList[i].get('storeId')
            quantity = normalGoodsList[i].get('quantity')
            goodlistitem = {
                "spuId": spuId,
                "storeId": storeId,
                "isSelected": 'true',
                "quantity": quantity,
            }
            print('目前有库存：' + normalGoodsList[i].get('goodsName') + '\t#数量：' + str(quantity) + '\t#金额：' + str(
                int(normalGoodsList[i].get('price')) / 100) + '元')
            goodlist.append(goodlistitem)
            amount = int(getAmout(goodlist))

        print('###获取购物车商品成功,总金额：' + str(int(amount) / 100))

        if Capacity_index > 0:
            getCapacityData()
            return False
        else:
            return True
    except Exception as e:
        print('getUserCart [Error]: ' + str(e))
        return False


def getCapacityData():
    global startRealTime
    global endRealTime

    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/delivery/portal/getCapacityData'
    data = {
        # YOUR SELF
        "perDateList": ["2022-04-13", "2022-04-14", "2022-04-15", "2022-04-16", "2022-04-17", "2022-04-18",
                        "2022-04-19"], "storeDeliveryTemplateId": good_store.get('storeDeliveryTemplateId')
    }
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '156',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'longitude': address.get('longitude'),
        'latitude': address.get('latitude'),
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'

    }
    try:
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data))
        # print(ret.text)
        myRet = json.loads(ret.text)
        print('#无库存释放,等待中')
        status = (myRet['data'].get('capcityResponseList')[0].get('dateISFull'))
        time_list = myRet['data'].get('capcityResponseList')[0].get('list')
        for i in range(0, len(time_list)):
            if not time_list[i].get('timeISFull'):
                startRealTime = time_list[i].get('startRealTime')
                endRealTime = time_list[i].get('endRealTime')
                # print(startRealTime)
                print('#【成功】获取配送时间')
                order(startRealTime, endRealTime)
                return True
    except Exception as e:
        print('getCapacityData [Error]: ' + str(e))
        return False


def order(startRealTime, endRealTime):
    global index
    print('下单：' + startRealTime)
    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/settlement/commitPay'
    data = {"goodsList": goodlist,
            "invoiceInfo": {},
            "cartDeliveryType": cartDeliveryType, "floorId": 1, "amount": amount, "purchaserName": "",
            "settleDeliveryInfo": {"expectArrivalTime": startRealTime, "expectArrivalEndTime": endRealTime,
                                   "deliveryType": deliveryType}, "tradeType": "APP", "purchaserId": "", "payType": 0,
            "currency": "CNY", "channel": "wechat", "shortageId": 1, "isSelfPickup": 0, "orderType": 0,
            "uid": uid, "appId": "wx57364320cb03dfba", "addressId": addressList_item.get('addressId'),
            "deliveryInfoVO": {"storeDeliveryTemplateId": good_store.get('storeDeliveryTemplateId'),
                               "deliveryModeId": good_store.get('deliveryModeId'),
                               "storeType": good_store.get('storeType')}, "remark": "",
            "storeInfo": {"storeId": good_store.get('storeId'), "storeType": good_store.get('storeType'),
                          "areaBlockId": good_store.get('areaBlockId')},
            "shortageDesc": "其他商品继续配送（缺货商品直接退款）", "payMethodId": "1486659732"}
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Content-Length': '1617',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'longitude': address.get('longitude'),
        'latitude': address.get('latitude'),
        'track-info': trackinfo,
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'

    }

    try:
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data))
        print(ret.text)
        myRet = json.loads(ret.text)
        status = myRet.get('success')
        if status:
            print('【成功】哥，咱家有菜了~')
            import os
            file = r"nb.mp3"
            os.system(file)
            exit()
        else:
            if myRet.get('code') == 'STORE_HAS_CLOSED':
                sleep(60)
                getCapacityData()
                return
            elif myRet.get('code') == 'LIMITED':
                index += 1
                if index > 5:
                    index = 0
                    getCapacityData()
                order(startRealTime, endRealTime)
                return
            elif myRet.get('code') == 'OUT_OF_STOCK':
                print('warning OUT_OF_STOCK')
                getUserCart(addressList_item, good_store, uid)
                return
            else:
                getCapacityData()
                return

    except Exception as e:
        print('order [Error]: ' + str(e))
        getCapacityData()
        return False


def init():
    # global address
    # global store
    address = address_list()
    store, uid = getRecommendStoreListByLocation(address.get('latitude'), address.get('longitude'))
    return address, store, uid


if __name__ == '__main__':
    count = 0
    index = 0
    Capacity_index = 0
    startRealTime = ''
    endRealTime = ''
    goodlist = []
    # 初始化
    address, store, uid = init()
    if getUserCart(address, store, uid):
        # getCapacityData
        while 1:
            count += 1
            print('count:' + str(count))
            getCapacityData()
            sleep(5)
