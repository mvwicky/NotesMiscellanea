import os
import sys

import requests
from bs4 import BeautifulSoup

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from bokeh.plotting import figure, output_file, show


if __name__ == '__main__':
    hp_width = (17.0 / 12) / 2

    sz = {'top': [], 'bot': []}
    p = {'x': [], 'z': []}
    pfx = {'x': [], 'z': []}
    strikes = {'x': [], 'z': []}
    balls = {'x': [], 'z': []}
    spin = {'rate': [], 'dir': []}

    base_url = 'http://gd2.mlb.com/components/game/mlb/year_2016/month_05'
    for day in range(13, 16):
        game = '/day_{}/gid_2016_05_{}_slnmlb_lanmlb_1/'.format(day, day)
        url = ''.join([base_url, game, 'inning/inning_all.xml'])
        res = requests.get(url)
        if res.status_code == 404:
            print('Got 404')
            sys.exit(-1)
        soup = BeautifulSoup(res.content, 'xml')
        for pitch in soup('pitch'):
            if pitch.get('sz_top') and pitch.get('sz_top'):
                sz['top'].append(float(pitch.get('sz_top')))
                sz['bot'].append(float(pitch.get('sz_bot')))
            if pitch.get('pfx_x') and pitch.get('pfx_z'):
                pfx['x'].append(float(pitch.get('pfx_x')))
                pfx['z'].append(float(pitch.get('pfx_z')))
            t = pitch.get('type')
            des = pitch.get('des')
            if t == 'S' and des == 'Called Strike':
                if pitch.get('px') and pitch.get('pz'):
                    strikes['x'].append(float(pitch.get('px')))
                    strikes['z'].append(float(pitch.get('pz')))
            elif t == 'B':
                if pitch.get('px') and pitch.get('pz'):
                    balls['x'].append(float(pitch.get('px')))
                    balls['z'].append(float(pitch.get('pz')))
            if pitch.get('spin_rate') and pitch.get('spin_dir'):
                spin['rate'].append(float(pitch.get('spin_rate')))
                spin['dir'].append(float(pitch.get('spin_dir')))

    assert (len(sz['top']) == len(sz['bot']))
    print(len(sz['top']))
    print(len(sz['bot']))
    nn = np.linspace(0, len(sz['top']), num=len(sz['top']))

    avg_top = np.average(sz['top'])
    avg_bot = np.average(sz['bot'])

    nn_sz_h = np.linspace(start=min(strikes['x'] + balls['x']),
                          stop=max(strikes['x'] + balls['x']))
    nn_sz_v = np.linspace(start=min(strikes['z'] + balls['z']),
                          stop=max(strikes['z'] + balls['z']))

    top = [avg_top for _ in nn_sz_h]
    bot = [avg_bot for _ in nn_sz_h]
    left = [-hp_width for _ in nn_sz_v]
    right = [hp_width for _ in nn_sz_v]

    print('avg. sz_top:', avg_top)
    print('avg. sz_bot:', avg_bot)

    output_file('strike_zone.html', title='called strikes')
    zone_map = figure(title='balls and strikes',
                      x_axis_label='x',
                      y_axis_label='y')
    zone_map.circle(strikes['x'], strikes['z'],
                    legend='Called Strikes', color='red', size=3)
    zone_map.circle(balls['x'], strikes['z'],
                    legend='Called Balls', color='blue', size=3)
    zone_map.line(nn_sz_h, top, color='green')
    zone_map.line(nn_sz_h, bot, color='green')
    zone_map.line(left, nn_sz_v, color='green')
    zone_map.line(right, nn_sz_v, color='green')
    show(zone_map)
