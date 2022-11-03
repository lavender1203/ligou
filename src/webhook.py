import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
from src.util import logger

 
def send_text(countent_text):
    timestamp = str(round(time.time() * 1000))
    secret = 'SEC77a83f33584c11f4041b37a6c186087b26ab74cfc6304e0525b77e2bb36129f1'  #签名id
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f"https://oapi.dingtalk.com/robot/send?access_token=d7f95d0000009c1a74a3a01020f66d3ba9906fbfa06c4568ce2f4cdba9682ac1&timestamp={timestamp}&sign={sign}"
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
    "msgtype":"text",
    "at": {"atMobiles": ["18381001111"], #群中@的人员
         "isAtAll": True},
    "text": {"content": countent_text}, "msgtype": "text"}
    data = {
     "msgtype": "markdown",
     "markdown": {
         "title":"立购联盟：新消息",
         "text": countent_text
     },
      "at": {
          "atMobiles": [
              "150XXXXXXXX"
          ],
          "atUserIds": [
              "user123"
          ],
          "isAtAll": True
      }
 }
    try:
        r = requests.post(url, headers=headers, data=json.dumps(data))
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        logger.error(e)
# dx=f"-----------------------------测试数据--------------------------------"
# send_text(dx)