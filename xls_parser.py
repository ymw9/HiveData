import pandas as pd
import re
import json
from pathlib import Path


def toLowerCase(string):
    return "".join(chr(ord(c) + 32) if 65 <= ord(c) <= 90 else c for c in string)


def to_easy_csv(path):

    df = pd.read_excel(path)
    path = Path(path)
    for i in range(0, df.shape[1]):
        df.rename(columns={df.columns[i]: f'{i}'}, inplace=True)
    df.drop(index=0, inplace=True)
    df.set_index(keys=df['0'], inplace=True)
    df.drop(columns='0', inplace=True)
    data = dict(df['3'])
    with open('worker_keywords.json') as json_file:
        keys = json.load(json_file)
        for miner in keys:
            for worker in data:
                if re.search(toLowerCase(str(miner)), toLowerCase(str(worker))):
                    keys[miner].append(data[worker])
    for key in keys:
        keys[key] = sum(keys[key])
    keys = pd.DataFrame(data=keys, index=['speed'])
    keys.to_csv(str(path.parent / str(path.stem + '-processed.csv')))

if __name__ == '__main__':
    to_easy_csv('beepool_log_2021-03-29-10-00.xls')
