# 获取token
import base64
import json

import requests


def get_token(client_id, client_secret):
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials"
    params = {"client_id": client_id, "client_secret": client_secret}
    res = requests.get(url, params=params)
    result = res.json()
    return result['access_token']


# 读取图片，转换成base64
def read_pic(name):
    with open('./%s' % name, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return s


# 融合图片
def merge(token, template, target):
    url = 'https://aip.baidubce.com/rest/2.0/face/v1/merge'
    request_url = url + '?access_token=' + token
    params = {
        "image_template": {
            "image": template,
            "image_type": "BASE64",
            "quality_control": "NORMAL"
        },
        "image_target": {
            "image": target,
            "image_type": "BASE64",
            "quality_control": "NORMAL"
        },
        "merge_degree": "HIGH"
    }
    params = json.dumps(params)
    headers = {'content-type': 'application/json'}
    result = requests.post(request_url, data=params, headers=headers).json()
    if result['error_code'] == 0:
        res = result["result"]["merge_image"]
        down_pic(res)
    else:
        print(str(result['error_code']) + result['error_msg'])


# 下载图片
def down_pic(data):
    imagedata = base64.b64decode(data)
    file = open('./results.jpg', "wb")
    file.write(imagedata)

if __name__ == '__main__':
    girl = read_pic('girls.jpg')
    boy = read_pic('boy.jpg')
    token = get_token("e6c8YIqfDGYze4czxd76MERj", "59jGvvQEWvvpNRb2Yyl4SdnW3opHG25H")
    merge(token, boy, girl)
