import itertools
from collections import Counter

from tqdm import tqdm
from rimo_storage.cache import disk_cache

from danbooru_loader import 超源


@disk_cache(serialize='pickle')
def 统计角色(子包范围):
    def _g():
        for name, image, meta in 超源(子包范围=子包范围, id范围=range(10000, 9999999), fav_count范围=range(10, 9999999), 要的tags=['1girl'], 不要的tags=['1boy', '2boys', '3boys'], 缓存=False, 需要图片=False):
            if meta['tag_string_character'] and ' ' not in meta['tag_string_character']:
                yield meta['tag_string_character']
    return Counter(tqdm(_g()))


def 计算年龄(x, 参考=None):
    if not 参考:
        参考 = [['shiranui_mai', 21, -0.7921182329864622], ['hatsune_miku', 16, -0.04943094447469585], ['suzumiya_haruhi', 15, 0.17505289694023843], ['kagamine_rin', 14, 0.5824689669583581], ['himesaka_noa', 12, 0.9669334825735093]]
    for q in itertools.pairwise([['_', 参考[0][1], -1]] + 参考 + [['_', 参考[-1][1], 1]]):
        (_, 年龄a, ta), (_, 年龄b, tb) = q
        if ta<=x<=tb:
            k = (x - ta) / (tb - ta)
            return 年龄a + k * (年龄b - 年龄a)
