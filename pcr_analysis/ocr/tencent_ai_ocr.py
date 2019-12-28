#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from typing import Dict, Any

import requests
import time
import secrets
import base64
import urllib.parse
import hashlib

with open('resources/tencent_ai_auth.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    APP_ID = config['APP_ID']
    APP_KEY = config['APP_KEY']
    del config


def ocr_generate(img_data: bytes) -> Dict[str, Any]:
    data: Dict[str, str] = {
        'app_id': APP_ID,
        'time_stamp': int(time.time()),
        'nonce_str': secrets.token_hex(16),
        'sign': '',
        'image': str(base64.b64encode(img_data), 'ascii')
    }
    data['sign'] = sign_request(data)
    result = retry_post('https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr', data=data)

    if result['ret'] == 0:
        return result['data']
    else:
        raise ValueError(str(result['ret']) + ',' + result['msg'])


def retry_post(url: str, data):
    while True:
        resp = requests.post(url, data=data)
        if resp.ok:
            result = json.loads(resp.text)
            if result['ret'] in (-2147483635, -30):
                time.sleep(1)
                continue
            return result


def sign_request(params: dict):
    sorted_keys = sorted(params.keys())

    l = []
    for key in sorted_keys:
        if not params[key]:
            continue
        l.append(key)
        l.append('=')
        l.append(urllib.parse.quote(str(params[key]), safe=''))
        l.append('&')
    l.append('app_key=')
    l.append(APP_KEY)
    s = ''.join(l)
    return hashlib.md5(bytes(s, 'ascii')).hexdigest().upper()


def test():
    with open(os.path.expanduser(r'~\Downloads\pcr\JPEG\Screenshot_2019-12-28-15-47-11-900_tw.sonet.princessconnect.jpg'), 'rb') as f:
        data = f.read()
    ocr_generate(data)


if __name__ == '__main__':
    test()
