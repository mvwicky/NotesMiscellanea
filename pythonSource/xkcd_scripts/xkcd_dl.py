import os
import sys

import requests

from bs4 import BeautifulSoup, SoupStrainer


def fmt_name(inp):
    not_allowed_chars = '<>:"/\\|?*'  # Explicity not allowed characters
    for char in not_allowed_chars:
        inp = inp.replace(char, '')
    for char in ', ':  # I personally don't want these
        inp = inp.replace(char, '')
    return inp


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
    nums = []
    if (len(sys.argv) > 1):
        for arg in sys.argv[1:]:
            if arg.isnumeric():
                nums.append(int(arg))
            else:
                print('Arguments must be a sequence of numbers')
                return -1
        print('Comics to get: {}'.format(nums))
    else:
        print('Getting all')
    base_url = 'http://xkcd.com/'
    save_folder = 'xkcd'
    if not os.path.exists(os.path.abspath(save_folder)):
        try:
            os.makedirs(os.path.abspath(save_folder))
        except:
            print('Could not create save folder')
            return -1
        else:
            print('Folder Created: {}'.format(os.path.abspath(save_folder)))
    pairs = []
    img = SoupStrainer('div', id='comic')
    if nums:
        for num in nums:
            url = ''.join([base_url, str(num), '/'])
            res = requests.get(url)
            if res.status_code == 404:
                print('Could not get comic #: {}'.format(num))
                continue
            else:
                soup = BeautifulSoup(res.content, 'lxml', parse_only=img)
                for elem in soup('img'):
                    if 'comics' in elem.get('src'):
                        img_url = ''.join(['http:', elem.get('src')])
                        comic_name = fmt_name(elem.get('alt'))
                        file_name = 'xkcd_{}_{}.png'.format(num, comic_name)
                        file_path = os.path.abspath(os.path.join(save_folder,
                                                                 file_name))
                        pairs.append((img_url, file_path))
                        print(img_url, file_path)
    else:
        num = 1
        url = ''.join([base_url, str(num), '/'])
        res = requests.get(url)
        while res.status_code != 404:
            soup = BeautifulSoup(res.content, 'lxml', parse_only=img)
            for elem in soup('img'):
                if 'comics' in elem.get('src'):
                    img_url = ''.join(['http:', elem.get('src')])
                    comic_name = fmt_name(elem.get('alt'))
                    file_name = 'xkcd_{}_{}'.format(num, comic_name)
                    file_path = os.path.abspath(os.path.join(save_folder,
                                                             file_name))
                    pairs.append((img_url, file_path))
                    print(img_url, file_path)
            num += 1
            url = ''.join([base_url, str(num), '/'])
            res = requests.get(url)

    print('Getting {} comics'.format(len(pairs)))
    total_size = 0
    for pair in pairs:
        msg_tup = (pair[0].replace('http:', ''), os.path.split(pair[1])[1])
        msg = ' -> '.join(msg_tup)
        print(msg)
        with open(pair[1], 'wb') as comic:
            res = requests.get(pair[0], stream=True)
            if res.headers.get('content-length') is None:
                comic.write(res.content)
            else:
                total_size += float(res.headers.get('content-length'))
                for data in res.iter_content():
                    comic.write(data)
                ts_msg = size_msg(total_size)
                print('Total Data Downloaded: {}'.format(ts_msg))


if __name__ == '__main__':
    main()
