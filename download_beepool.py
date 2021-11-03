import requests
import datetime
import logging
import os
import time
from xls_parser import to_easy_csv
from casher import casher

logging.basicConfig(level=logging.NOTSET)


def get_xls():
    url = 'https://www.beepool.org/download/workers?coin=ETH&wallet=captainpool'
    r = requests.get(url, allow_redirects=True)
    current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    target_path = os.path.join(os.getcwd(), f'beepool_log_{current_time}.xls')
    open(target_path, 'wb').write(r.content)
    logging.info(f'Download the beepool statistics at {current_time}')
    to_easy_csv(f'beepool_log_{current_time}.xls')
    flag = False
    while not flag:
        if os.path.getsize(target_path) > 100:
            flag = True
            logging.info(f'successfully dump the beepool worker data to {target_path}')
        else:
            logging.info('failed to download the beepool worker data')
            logging.info('removing existing corrupt data')
            try:
                os.remove(target_path)
            except FileNotFoundError:
                pass
            try:
                os.remove(target_path.split('.')[0])
            except FileNotFoundError:
                pass
            logging.info('re-downloading in 10 seconds')
            time.sleep(10)
            current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
            open(os.path.join(os.getcwd(), f'beepool_log_{current_time}.xls'), 'wb').write(r.content)
            to_easy_csv(f'beepool_log_{current_time}.xls')
    casher()


if __name__ == '__main__':
    get_xls()


