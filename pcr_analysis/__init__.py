#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from typing import List, Any

from pcr_analysis.analysis import Damage
from pcr_analysis.ocr import tencent_ai_ocr
from pcr_analysis import analysis


def analysis_photo(file_path: str) -> List[Damage]:
    ocr_result = __load_cache(file_path)
    if not ocr_result:
        with open(file_path, 'rb') as f:
            img_data = f.read()
        ocr_result = tencent_ai_ocr.ocr_generate(img_data)
        __dump_cache(file_path, ocr_result)
    return analysis.analysis_ocr_result(ocr_result)


def __load_cache(file_name: str):
    if not os.path.exists(__cache_path(file_name)):
        return
    with open(__cache_path(file_name), 'r', encoding='utf-8') as f:
        return json.load(f)


def __dump_cache(file_path: str, data: Any):
    if not data:
        return
    with open(__cache_path(file_path), 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def __cache_path(file_path: str) -> str:
    if not os.path.exists('resources/ocr'):
        os.makedirs('resources/ocr')
    return os.path.join('resources/ocr/', os.path.basename(file_path)) + '.json'
