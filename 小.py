import json
import pickle
from pathlib import Path
from functools import lru_cache
from collections import Counter

from common import 计算年龄


@lru_cache()
def pickle_load(path):
    return pickle.load(open(path, 'rb'))


def meta(x):
    return pickle_load(f'tags缓存/{int(x)%1000}.pickle')[int(x)]


全人 = {}
zs = []
for a, b, 字 in json.load(open('年轻结果.json', encoding='utf8')):
    a_name = meta(Path(a).stem)['tag_string_character']
    b_name = meta(Path(b).stem)['tag_string_character']
    if not a_name or not b_name or ' ' in a_name or ' ' in b_name:
        continue
    全人[a_name] = []
    全人[b_name] = []
    zs.append(字)
计数 = Counter(zs)
b权重 = 计数['图a'] / (计数['图a'] + 计数['图b'])
print(f'{b权重=}')


zs = []
for a, b, 字 in json.load(open('年轻结果.json', encoding='utf8')):
    a_name = meta(Path(a).stem)['tag_string_character']
    b_name = meta(Path(b).stem)['tag_string_character']
    if not a_name or not b_name or ' ' in a_name or ' ' in b_name:
        continue
    if 字 == '图a':
        全人[a_name].append(1)
        全人[b_name].append(-1)
    elif 字 == '图b':
        全人[a_name].append(-b权重)
        全人[b_name].append(b权重)



人得分 = {}
人年龄 = {}


for k, v in 全人.items():
    if sum(abs(i) for i in v) >= 1:
        t = sum(v) / sum(abs(i) for i in v)
        人年龄[k] = [计算年龄(t), t]


with open('人年龄.json', 'w', encoding='utf8') as f:
    f.write(json.dumps(人年龄, indent=2))
