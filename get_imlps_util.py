from wasm_impl_util import common_runtime
from wasm_impl_util import uninst_runtime
from impl_paras import impl_paras
from impl_paras_std import impl_paras_std
from impl_paras_std_release import impl_paras_std_release

# def get_newer_imlps():
#     imlp_names = list(impl_paras.keys())
#     imlps = []
#     for name in imlp_names:
#         imlp = common_runtime.from_dict(name, impl_paras[name])
#         imlps.append(imlp)
#     return imlps


# def get_newer_imlps_skip_wasm3():
#     imlp_names = list(impl_paras.keys())
#     imlps = []
#     for name in imlp_names:
#         if 'wasm3' in name:
#             continue
#         imlp = common_runtime.from_dict(name, impl_paras[name])
#         imlps.append(imlp)
#     return imlps


def get_std_imlps():
    imlps = []
    for name in impl_paras_std.keys():
        imlp = common_runtime.from_dict(name, impl_paras_std[name])
        imlps.append(imlp)
    return imlps


def get_std_uninst_imlps():
    imlps = []
    for name in impl_paras_std.keys():
        imlp = uninst_runtime.from_std_dict(name, impl_paras_std[name])
        imlps.append(imlp)
    return imlps


def get_lastest_uninst_imlps():
    imlps = []
    for name in impl_paras_std.keys():
        imlp = uninst_runtime.from_lastest_dict(name, impl_paras_std[name])
        imlps.append(imlp)
    return imlps


def get_std_release_impls():
    imlps = []
    for name in impl_paras_std_release.keys():
        imlp = common_runtime.from_dict(name, impl_paras_std_release[name])
        imlps.append(imlp)
    return imlps
