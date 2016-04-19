import os

import requests


def size_msg(size_in_bytes):
    int_bytes = int(size_in_bytes)
    if int_bytes in range(0, 1000):
        return '{} bytes'.format(size_in_bytes)
    elif int_bytes in range(1001, int(1e6)):
        kb = size_in_bytes / 1000
        return '{}kB'.format(kb)
    elif int_bytes in range(int(1e6)+1, int(1e9)):
        mb = size_in_bytes / 1e6
        return '{}MB'.format(mb)
    elif int_bytes in range(int(1e9)+1, int(1e12)):
        gb = size_in_bytes / 1e9
        return '{}GB'.format(gb)
    else:
        return '{} bytes'.format(size_in_bytes)


def main():
    file_name = 'time.csv'
    save_folder = 'time_frames'
    if not os.path.exists(os.path.abspath(save_folder)):
        try:
            os.makedirs(os.path.abspath(save_folder))
        except:
            print('Could not create save folder')
            return -1
        else:
            print('Folder Created: {}'.format(os.path.abspath(save_folder)))

    total_size = 0
    with open(file_name, 'rt', newline='\n') as time:
        for row in time:
            row = row.replace('\r', '').replace('\n', '')
            fields = row.split(',')
            frame_name = 'time_{}.png'.format(fields[0])
            url = fields[6] if fields[6] else fields[5]
            frame_path = os.path.abspath(os.path.join(save_folder,
                                                      frame_name))
            msg_tup = (url.replace('http:', ''), os.path.split(frame_path)[1])
            msg = ' -> '.join(msg_tup)
            print(msg)
            with open(frame_path, 'wb') as frame:
                res = requests.get(url, stream=True)
                if res.headers.get('content-length') is None:
                    frame.write(res.content)
                else:
                    total_size += float(res.headers.get('content-length'))
                    for data in res.iter_content():
                        frame.write(data)
                    ts_msg = size_msg(total_size)
                    print('Total Data Downloaded: {}'.format(ts_msg))


if __name__ == '__main__':
    main()
