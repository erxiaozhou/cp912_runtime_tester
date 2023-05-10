#!/home/zph/anaconda3/bin/python
import sys
from debug_util import wasms_dir2wats
argv = sys.argv
input_dir = argv[1]
output_dir = argv[2]
wasms_dir2wats(input_dir, output_dir)
