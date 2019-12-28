#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import unittest


class TestResult(unittest.TestCase):
    def test_boss_hearth(self):
        with open('resources/schedule.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        damages = data['damages']
        for boss_key, boss_damage in damages.items():
            total = 0
            for damage in boss_damage.values():
                total += damage
            self.assertLess(total % 10000, 1, boss_key)


if __name__ == '__main__':
    unittest.main()
