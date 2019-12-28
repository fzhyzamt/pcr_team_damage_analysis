#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import unittest


class TestResult(unittest.TestCase):
    def load_damages(self):
        with open('resources/schedule.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        damages = data['damages']
        return damages

    def test_boss_hearth(self):
        damages = self.load_damages()
        for boss_key, boss_damage in damages.items():
            total = 0
            for damage in boss_damage.values():
                total += damage
            self.assertLess(total % 10000, 1, boss_key)

    def test_team_name(self):
        damages = self.load_damages()
        names = set()
        boss_name_set = set()
        round_set = set()
        for boss_key, boss_damage in damages.items():
            round, boss_name = boss_key.split('-')
            boss_name_set.add(boss_name)
            round_set.add(round)
            for name in boss_damage.keys():
                names.add(name)

        self.assertEquals(len(names), 29, names)
        self.assertEquals(len(boss_name_set), 5, boss_name_set)
        self.assertEquals(len(round_set), 28, round_set)


if __name__ == '__main__':
    unittest.main()
