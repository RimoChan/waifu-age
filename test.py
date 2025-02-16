import os
import json
import random

from tqdm import tqdm
from PIL import Image

import mllm
from common import 统计角色, 计算年龄
from danbooru_loader import 超源


人年龄 = json.load(open('人年龄.json'))


def 平均年龄(s):
    l = []
    for k, v in 人年龄.items():
        if s in k:
            l.append([v[0], v[1], k])
    print(sorted(l))
    return sum([i[0] for i in l]) / len(l)


print(f'{平均年龄("blue_archive")=}')
print(f'{平均年龄("azur_lane")=}')



c = 统计角色(range(1, 20, 2))
要的角色 = {k for k, v in c.most_common(2000)}


random.seed(1)
os.makedirs('age_image', exist_ok=True)
l = [*tqdm(超源(子包范围=[1], id范围=range(10000, 9999999), fav_count范围=range(10, 9999999), 要的tags=['1girl'], 不要的tags=['1boy', '2boys', '3boys'], 缓存=True, size=768))]
l = [i for i in l if set(i[2]['tag_string_character'].split()) & 要的角色]

image_a = Image.open("图/rimo.jpg")
print(mllm.超问([image_a], '请估计图中的角色的年龄。仅输出几岁即可。'))
image_a.thumbnail((768, 768))
胜 = []
b权重 = 0.20628556266399364
for _ in tqdm(range(100)):
    name_b, image_b, meta_b = random.choice(l)
    k = 1 if random.random() < 0.5 else -1
    if k == 1:
        字 = mllm.超问([image_a, image_b], '图A和图B中，哪个女孩更年轻？请选择「图A」「图B」「一样年轻」即可。')
    else:
        字 = mllm.超问([image_b, image_a], '图A和图B中，哪个女孩更年轻？请选择「图A」「图B」「一样年轻」即可。')
    if 字 == '图a':
        胜.append(k)
    elif 字 == '图b':
        胜.append(-k * b权重)
print(胜)
print(sum(胜)/len(胜))
print(计算年龄(sum(胜)/len(胜)))
