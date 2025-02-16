import os
import json
import random
from datetime import datetime

from tqdm import tqdm

import mllm
from danbooru_loader import 超源
from common import 统计角色


c = 统计角色(range(1, 20, 2))
要的角色 = {k for k, v in c.most_common(2000)}


random.seed(1)
os.makedirs('age_image', exist_ok=True)
l = [*tqdm(超源(子包范围=range(1, 20, 2), id范围=range(10000, 9999999), fav_count范围=range(10, 9999999), 要的tags=['1girl'], 不要的tags=['1boy', '2boys', '3boys'], 缓存=True, size=768))]
l = [i for i in l if set(i[2]['tag_string_character'].split()) & 要的角色]


年轻结果 = []
for _ in tqdm(range(1000000)):
    (name_a, image_a, meta_a), (name_b, image_b, meta_b) = random.sample(l, 2)
    if abs(datetime.fromisoformat(meta_a['created_at']).year - datetime.fromisoformat(meta_b['created_at']).year) > 1:
        continue
    res = mllm.超问([image_a, image_b], '图A和图B中，哪个女孩更年轻？请选择「图A」「图B」「一样年轻」即可。')
    年轻结果.append((name_a, name_b, res))
    if len(年轻结果) % 100 == 1:
        with open('年轻结果.json', 'w', encoding='utf8') as f:
            f.write(json.dumps(年轻结果, indent=2))
