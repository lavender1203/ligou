import json
import requests
import time
from src import redis
from src.webhook import send_text
from src.util import logger


"""
POST https://wxapi.lig.cn/product/home2/getProductList HTTP/1.1
Authorization: 
platform: android
appversion: 2.4.2
systemVersion: 6.0.1
deviceModel: Nexus 5X
versionCode: 82
Content-Type: application/json; charset=utf-8
Content-Length: 180
Host: wxapi.lig.cn
Connection: Keep-Alive
Accept-Encoding: gzip
User-Agent: okhttp/3.12.3

{"ak":"trd0kcfkyf1a1vbccneezdnggg3trf39hqj81yey2xb7g40jbxjkjeapfucj5rhf","id":"104","pageNum":1,"pageSize":20,"sign":"1c107e8a7eb47a46f9166c3649bf2d00","timestamp":"1667446529958"}
"""

def main():
    # 1.获取首页数据
    url = "https://wxapi.lig.cn/product/home2/getProductList"
    url = "https://wxapi.lig.cn/product/home2/getDataProductList"
    headers = {
    "Authorization": "",
    "platform": "android",
    "appversion": "2.4.2",
    "systemVersion": "6.0.1",
    "deviceModel": "Nexus 5X",
    "versionCode": "82",
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": "180",
    "Host": "wxapi.lig.cn",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.12.3"
    }
    timestamp = int(time.time()*1000)
    for page in range(1):
        data = {
            "ak":"trd0kcfkyf1a1vbccneezdnggg3trf39hqj81yey2xb7g40jbxjkjeapfucj5rhf", # base64
            # "id":"104",
            "categoryPlatform":1,
            "listId": 1320,
            "pageNum": page + 1,
            "pageSize":20,
            # "sign":"1c107e8a7eb47a46f9166c3649bf2d00", # md5
            "sign": "ea99b2cb57003b87b79127860a21f292",
            "timestamp": timestamp
        }
        r = requests.post(url=url, headers=headers, json=data)
        time.sleep(10)
        if r.status_code == 200:
            # 拿到某个id类别的所有产品
            batch_products = r.json()["data"]
            # 选其中一个产品进行测试
            for product in batch_products:
                pro = {
                    "price": product["price"],  # 原价
                    "couponPrice": product["couponPrice"],  # 折扣价
                    "couponAmount": product["couponAmount"],  # 优惠券
                    "maxCommission": product["maxCommission"],  # 分享后最高可赚金额
                    "productId": product["productId"], # 产品id
                    "productImg": product["productImg"],   # 图片地址
                    "productBuyUrl": product["productBuyUrl"],   # 购买链接
                    "productName": product["productName"],   # 产品名称
                    "mallName": product["mallName"],   # 店铺名
                    "comments": product["comments"],   # 评论数
                    "goodCommentsShare": product["goodCommentsShare"],  # 好评率 0-100
                    "couponUrl": product["couponUrl"]   # 优惠购买链接
                }
                # 过滤规则：折扣价和优化卷变动重新推送
                key_name = "product"
                need_send = redis.client.hset(key_name, pro["productId"], json.dumps(pro))
                if need_send:
                    # 推送消息
                    msg = f'新增优惠产品：{product["productName"]}, {product["productImg"]}'
                    msg = f'#### 好物分享 \n {product["productName"]}\n > ![screenshot]({product["productImg"]})\n > #### 折扣价：{product["couponPrice"]}元   原价：{product["price"]}元\n #### 点击 [购买]({product["couponUrl"]}) \n'
                    logger.info(msg)
                    send_text(msg)
            if len(batch_products) == 0:
                logger.info("商品已查完.")
                return
        else:
            logger.error("网络出错!")



if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    main()
    # str_encoder = "trd0kcfkyf1a1vbccneezdnggg3trf39hqj81yey2xb7g40jbxjkjeapfucj5rhf"
    # decoder = base64.b64decode(str_encoder)
    # print(decoder) # 我是一个字符串