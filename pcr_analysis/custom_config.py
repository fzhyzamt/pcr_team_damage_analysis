#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

"""
config example:
{
  "boss_name": {
    "奧爾獅狮": "奧爾獅",
    "獸人會長": "獸人酋長"
  },
  "team_name": {
    "日": "白"
  }
}

"""

def parse_boss_name(s: str) -> str:
    if s in _load()['boss_name']:
        return _load()['boss_name'][s]
    return s


def parse_team_name(s: str) -> str:
    if s in _load()['team_name']:
        return _load()['team_name'][s]
    return s


_cache = None


def _load():
    global _cache
    if _cache:
        return _cache
    with open('resources/customer_name_map.json', 'r', encoding='utf-8') as f:
        _cache = json.load(f)
    return _cache
