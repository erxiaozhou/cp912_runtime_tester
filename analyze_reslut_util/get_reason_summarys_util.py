from .get_reason_util import reason_base_dir2reason_summary_json
from file_util import check_dir


def get_reason_summarys(reason_summary_base_dir, reason_base_dir, exec=True):
    reason_summary_base_dir = check_dir(reason_summary_base_dir)
    full_reason_summary_path = reason_summary_base_dir / 'full_summary.json'
    only_exec_reason_summary_path = reason_summary_base_dir / 'only_exec_summary.json'
    stack_reason_summary_path = reason_summary_base_dir / 'stack_summary.json'
    if exec:
        reason_base_dir2reason_summary_json(reason_base_dir, full_reason_summary_path)
        reason_base_dir2reason_summary_json(reason_base_dir, stack_reason_summary_path, ['stack_bytes_process_nan'])
        reason_base_dir2reason_summary_json(reason_base_dir, only_exec_reason_summary_path, ['CannotExecute', 'CanExecute', 'has_timeout'])

    paths = {
        'full': full_reason_summary_path,
        'only_exec': only_exec_reason_summary_path,
        'stack': stack_reason_summary_path
    }
    return paths
