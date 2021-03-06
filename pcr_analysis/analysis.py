#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import Dict, List, Any
from pcr_analysis import custom_config

UN_NUM_PTN = re.compile(r'[^\d]')


class Damage:
    def __init__(self, boss: str, round: str, name: str, damage: int, boss_day: int):
        self.boss = boss
        self.round = round
        self.name = name
        self.damage = damage
        self.boss_day = boss_day

    @property
    def boss_key(self) -> str:
        return str(self.boss_day) + '-' + self.round + '-' + self.boss

    def __str__(self):
        return f'{self.boss_day} {self.round}-{self.boss} `{self.name}` {self.damage}'


class Analysis:
    INT_PTN = re.compile(r'\d+')

    def __init__(self, data: Dict):
        self.data = data
        self.item_list: List[Dict[str, Any]] = self.data['item_list']
        self.item_list_len = len(self.item_list)
        self.index = 0

        self.boss_name: str = ''
        self.round: str = ''
        self.boss_day: int = 0
        self.damage_list: List[Damage] = []

    def parse(self) -> List[Damage]:
        self.parse_boss_name()
        self.parse_round()
        self.parse_time()
        self.parse_damage_list()

        return self.damage_list

    def parse_damage_list(self):
        temp = []
        for item in self.item_list:
            if item['itemcoord'][0]['x'] < 500:
                continue
            temp.append((item['itemcoord'][0]['y'], item))
        sorted(temp)

        name: str = ''
        for _, item in temp:
            if item['itemcoord'][0]['x'] > 1400:
                if not name:
                    continue
                damage = Analysis._parse_damage_num(item['itemstring'])
                self.damage_list.append(Damage(self.boss_name, self.round, name, damage, self.boss_day))
                name = ''
            else:
                name = Analysis._remove_symbol(item['itemstring'])
                name = custom_config.parse_team_name(name)

    def parse_boss_name(self):
        for item in self.item_list:
            if item['itemcoord'][0]['x'] > 300:
                continue
            if not Analysis.INT_PTN.search(item['itemstring']):
                boss_name = item['itemstring']
                boss_name = Analysis._remove_symbol(boss_name)
                self.boss_name = custom_config.parse_boss_name(boss_name)
                break
        else:
            raise ValueError('未找到boss名')

    def parse_round(self):
        for item in self.item_list:
            if item['itemcoord'][0]['x'] > 300 or item['itemcoord'][0]['x'] < 50:
                continue
            self.round = f"第{Analysis.INT_PTN.search(item['itemstring']).group()}周目"
            break
        else:
            raise ValueError('未找到周目')

    def parse_time(self):
        self.boss_day = custom_config.get_boss_time(self.round, self.boss_name)

    @staticmethod
    def _parse_damage_num(s):
        s = UN_NUM_PTN.sub('', s)
        return int(s)

    @staticmethod
    def _remove_symbol(s: str) -> str:
        return re.sub(r'[,，.\s]+', '', s)


def analysis_ocr_result(data: Dict):
    analysis = Analysis(data)
    return analysis.parse()
