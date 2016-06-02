import os
import sys

import requests

if __name__ == '__main__':
    playerid_list = os.path.realpath('E:\\retrosheet\\playerid_list.csv')
    player_ids = []
    with open(playerid_list, 'rt') as id_list:
        for row in id_list:
            row = row.split(',')
            p_id = row[4].replace('"', '')
            if p_id.isnumeric():
                player_ids.append(int(p_id))
    print(len(player_ids))
    sys.exit(0)
    base_url = 'https://baseballsavant.mlb.com/statcast_search/csv'
    player_id = 608369
    season = 'all'
    # opts = {'hfGT': 'R|', 'season': season, 'player_type': 'batter',
    #        'min_pitches': 0, 'min_results': 0, 'group_by': 'name',
    #        'sort_col': 'name', 'sort_order': 'desc', 'min_abs': 0,
    #        'type': 'details', 'player_id': player_id}
    opts = {'hfGT': 'R|', 'season': season, 'player_type': 'batter',
            'group_by': 'name', 'sort_col': 'name', 'sort_order': 'desc',
            'type': 'details', 'player_id': player_id}
    file_name = '{}_data.csv'.format(player_id)
    with open(file_name, 'wb') as file:
        res = requests.get(base_url, params=opts)
        print(res.url)
        if res.headers.get('content-length') is None:
            file.write(res.content)
        else:
            for data in res.iter_content():
                file.write(data)
