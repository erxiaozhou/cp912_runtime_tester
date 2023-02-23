from wasm_impls import common_runtime
from impl_paras import impl_paras
from impl_paras_std import impl_paras_std


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
    imlp_names = list(impl_paras_std.keys())
    imlps = []
    for name in imlp_names:
        imlp = common_runtime.from_dict(name, impl_paras_std[name])
        imlps.append(imlp)
    return imlps