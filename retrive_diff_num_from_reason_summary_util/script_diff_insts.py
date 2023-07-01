from file_util import save_json
from pathlib import Path
import re


dir_ = '/media/hdd_xj1/cp910_data/main_testing_v18_340_9811_no_mutation/diff_tcs'
dir_ = Path(dir_)

name_p = re.compile(r'(.*)_\d+')
inst_names = set()
for p in dir_.iterdir():
    stem = p.stem
    name = name_p.findall(stem)[0]
    inst_names.add(name)
save_json('inst_names.json', list(inst_names))
