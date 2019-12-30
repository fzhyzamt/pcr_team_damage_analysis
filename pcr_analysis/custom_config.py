#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re

"""
config example:
customer_name_map.json
{
  "boss_name": {
    "奧爾獅狮": "奧爾獅",
    "獸人會長": "獸人酋長"
  },
  "team_name": {
    "日": "白"
  }
}
customer_day_boss.json
{
  "times": [
    {
      "day": 23,
      "last": "6-飛龍"
    },
    {
      "day": 24,
      "last": "12-泰坦龍龜"
    },
    {
      "day": 25,
      "last": "17-奧爾獅"
    },
    {
      "day": 26,
      "last": "22-泰坦龍龜"
    },
    {
      "day": 27,
      "last": "27-奧爾獅"
    },
    {
      "day": 28,
      "last": "32-奧爾獅"
    },
    {
      "day": 29,
      "last": "38-沙陸樹懶"
    },
    {
      "day": 30,
      "last": "999-UE"
    }
  ],
  "bossSort": {
    "飛龍": 1,
    "沙陸樹懶": 2,
    "獸人酋長": 3,
    "泰坦龍龜": 4,
    "奧爾獅": 5
  }
}
"""


def parse_boss_name(s: str) -> str:
    if s in _load_name()['boss_name']:
        return _load_name()['boss_name'][s]
    return s


def parse_team_name(s: str) -> str:
    if s in _load_name()['team_name']:
        return _load_name()['team_name'][s]
    return s


def get_boss_time(boss_round: str, boss_name: str) -> int:
    boss_round_int = int(re.search(r'\d+', boss_round).group())
    time_config = _load_time()

    last: int = 0
    for t in time_config['times']:
        config_round_int = int(t['last'].split('-')[0])
        config_boss_name = t['last'].split('-')[1]

        if boss_round_int < config_round_int:
            return t['day']

        if boss_round_int > config_round_int:
            continue

        if time_config['bossSort'][boss_name] <= time_config['bossSort'][config_boss_name]:
            return t['day']
        last = t['day']
    return last


_cache_name = None


def _load_name():
    global _cache_name
    if _cache_name:
        return _cache_name
    with open('resources/customer_name_map.json', 'r', encoding='utf-8') as f:
        _cache_name = json.load(f)
    return _cache_name


_cache_time = None


def _load_time():
    global _cache_time
    if _cache_time:
        return _cache_time
    with open('resources/customer_day_boss.json', 'r', encoding='utf-8') as f:
        _cache_time = json.load(f)
    return _cache_time
