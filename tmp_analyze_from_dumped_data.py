from run_dir_testing.run_dir_testing_util import analyze
from run_dir_testing.tester_util import testerExecPaths
from pathlib import Path


result_base_dir = Path('/host_data/rerun/v18_limit_by_log_mutation_v23_0')
exec_paths = testerExecPaths.from_result_base_dir(result_base_dir, False)
analyze(result_base_dir, exec_paths)
