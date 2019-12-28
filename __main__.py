#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import pcr_analysis
import os


def main():
    os.makedirs('resources', exist_ok=True)

    schedule = Schedule()
    schedule.load_schedule()
    screen_path = os.path.expanduser(r'~\Downloads\pcr\JPEG')
    for file_name in os.listdir(screen_path):
        print(f'start parse {file_name}')
        print('=' * 80)
        schedule.analysis(os.path.join(screen_path, file_name))
        schedule.dump_schedule()

    print(schedule.data)


class Schedule:
    def __init__(self):
        self.data = {
            'damages': {}
        }
        self.config_path = 'resources/schedule.json'

    def load_schedule(self):
        if not os.path.exists(self.config_path):
            return
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def dump_schedule(self):
        with open(self.config_path, 'w+', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def analysis(self, file_path: str):
        damage_list = pcr_analysis.analysis_photo(file_path)
        for damage in damage_list:
            if damage.boss_key not in self.data['damages']:
                self.data['damages'][damage.boss_key] = {}
            self.data['damages'][damage.boss_key][damage.name] = damage.damage


if __name__ == '__main__':
    main()
