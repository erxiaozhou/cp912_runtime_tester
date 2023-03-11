from pathlib import Path
from file_util import path_read
from .dump_data_util import dump_data
from path_group_util import result_path_group


def is_failed_content(content):
    assert isinstance(content, str)
    content = content.lower()
    if 'error' in content:
        return True
    elif 'failed' in content:
        return True
    elif 'exception' in content:
        return True
    elif 'aborted' in content:
        return True
    elif 'fault' in content:
        return True
    else:
        return False


class common_result_initializer(dump_data):
    def __init__(self, paths, has_timeout, features=None):
        super().__init__()
        assert isinstance(paths, result_path_group)
        self.paths = paths
        self.has_timeout = has_timeout
        self.features = features
        self.common_initialize()

    def common_initialize(self):
        self._init_log()
        self._init_has_failed_content()
        self._init_features()
        self._init_can_initialize()
        self._init_has_instance()

    def _init_log(self):
        content = path_read(self.log_path)
        self.log_content = content

    def _init_has_failed_content(self):
        self.log_has_failed_content = is_failed_content(self.log_content)

    def _init_features(self):
        features = {k:v for k, v in self.features.items()}
        self.features = features
    
    def _init_can_initialize(self):
        # ! 还是很奇怪
        if Path(self.store_path).exists():
            if Path(self.vstack_path).exists():
                self.can_initialize = True
                return
        self.can_initialize = False

    def _init_has_instance(self):
        self.has_instance = has_instance(self.has_instance_path)
    
    def to_dict(self, path=None):
        new_data = dump_data()
        for k in new_data.__dict__.keys():
            new_data.__dict__[k] = self.__dict__[k]
        return new_data.to_dict(path)

    # paths
    @property
    def store_path(self):
        return self.paths.store_path

    @property
    def vstack_path(self):
        return self.paths.vstack_path
    
    @property
    def log_path(self):
        return self.paths.log_path

    @property
    def has_instance_path(self):
        return self.paths.inst_path


def has_instance(path):
    has_instance_ = False
    path = Path(path)
    if path.exists():
        with open(path,'rb') as f:
            content = f.read()
        assert bytearray(content) == bytearray([0xff, 0xff, 0xff, 0xff])
        has_instance_ = True
    else:
        pass
    return has_instance_
