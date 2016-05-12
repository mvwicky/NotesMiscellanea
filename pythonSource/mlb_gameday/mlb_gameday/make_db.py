import os
import json

if __name__ == '__main__':
    path_to_events = os.path.normpath('E:\\retrosheet\\events')
    folders, files = [], dict()
    for folder in os.listdir(path_to_events):
        if folder[:4].isnumeric() and folder.endswith('eve'):
            folders.append(os.path.join(path_to_events, folder))
            year = int(folder[:4])
            files[year] = []
            events = os.path.join(path_to_events, folder)
            for eve in os.listdir(events):
                file_path = os.path.join(path_to_events, folder, eve)
                files[year].append(file_path)
    pk = 1
    to_json = []
    for year in files.keys():
        file_name = 'TEAM{}'.format(year)
        year_path = os.path.join(path_to_events, '{}eve'.format(year))
        file_path = os.path.join(year_path, file_name)
        with open(file_path, 'rt') as file:
            for row in file:
                row = row.replace('\n', '').split(',')
                team = {'model': 'retrosheet.Team',
                        'pk': pk,
                        'fields': {
                            'year': int(year),
                            'abbreviation': str(row[0]),
                            'league': str(row[1]),
                            'name': str(row[2]),
                            'city': str(row[3])
                        }}
                pk += 1
                to_json.append(team)
    with open('retrosheet/fixtures/retro.json', 'w') as retro:
        retro.write(json.dumps(to_json, indent=2))
