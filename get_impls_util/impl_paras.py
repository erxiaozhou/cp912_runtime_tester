from extract_dump import iwasmClassicInterpDumpedResult
from extract_dump import wasmiDumpedResult
from extract_dump import wasm3_dumped_data
from extract_dump import wasmedgeDumpedResult
from extract_dump import wasmerDumpedResult
from extract_dump import iwasmFastInterpDumpedResult
from extract_dump import wavmDumpedResult
impl_paras = {
    'wasmer_default_dump':{
        'dump_dir': '/home/zph/DGit/wasm_projects/runtime_test/wasmer_default',
        'standard_dir': '/home/zph/DGit/wasm_projects/runtime_test/ori_wasmer_default',
        'bin_relative_path': 'target/release/wasmer',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'cmd': '{} {} -i to_test',
        'dump_cmd':  '{} {} -i to_test 2> {}',
        'ori_log_path': 'dpd_wasmer_err_log',
        'dump_extractor': wasmerDumpedResult,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    },
    'wasmi_interp': {
        'dump_dir': '/home/zph/DGit/wasm_projects/runtime_test/wasmi_interp',
        'standard_dir': '/home/zph/DGit/wasm_projects/runtime_test/ori_wasmi',  # TODO to rename
        'bin_relative_path': 'target/debug/wasmi_cli',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'cmd': '{} {} to_test',
        'dump_cmd':  '{} {} to_test 2> {}',
        'ori_log_path': 'dpd_wasmi_err_log',
        'dump_extractor': wasmiDumpedResult,
        'support_multi_mem': False,
        'support_ref': False,
        'support_v128': False
    },
    'iwasm_classic_interp_dump':{
        'dump_dir': '/home/zph/DGit/wasm_projects/runtime_test/iwasm_interp_classic',
        'standard_dir': '/home/zph/DGit/wasm_projects/runtime_test/ori_iwasm_interp_classic',
        'bin_relative_path': 'product-mini/platforms/linux/build/iwasm',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'cmd': '{} --heap-size=0 -f to_test {}',
        'dump_cmd':  '{} --heap-size=0 -f to_test {} > {}',
        'ori_log_path': 'dpd_iwasm_classic_err_log',
        'dump_extractor': iwasmClassicInterpDumpedResult,
        'support_multi_mem': False,
        'support_ref': True,
        'support_v128': False  # ?
    },
    'iwasm_fast_interp_dump':{
        'dump_dir': '/home/zph/DGit/wasm_projects/runtime_test/iwasm_interp_fast',
        'standard_dir': '/home/zph/DGit/wasm_projects/runtime_test/ori_iwasm_interp_fast',
        'bin_relative_path': 'product-mini/platforms/linux/build/iwasm',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'cmd': '{} --heap-size=0 -f to_test {}',
        'dump_cmd':  '{} --heap-size=0 -f to_test {} > {}',
        'ori_log_path': 'dpd_iwasm_fast_err_log',
        'dump_extractor': iwasmFastInterpDumpedResult,
        'support_multi_mem': False,
        'support_ref': True,
        'support_v128': False  # ?
    },
    'wasm3_dump':{
        'dump_dir': '/home/zph/DGit/wasm_projects/runtime_test/wasm3_default',
        'standard_dir': '/home/zph/DGit/wasm_projects/runtime_test/ori_wasm3_default',
        'bin_relative_path': 'build/wasm3',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'cmd': '{} --func to_test {}',
        'dump_cmd':  '{} --func to_test {} 2> {}',
        'ori_log_path': 'dpd_wasm3_err_log',
        'dump_extractor': wasm3_dumped_data,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': False
    },
    # 'WasmEdge_disableAOT':{
    #     'dump_dir': '/home/zph/DGit/wasm_projects/runtime_test/WasmEdge_runtimes/WasmEdge_disableAOT',
    #     'standard_dir': '/home/zph/DGit/wasm_projects/runtime_test/WasmEdge_runtimes/ori_WasmEdge_disableAOT',
    #     'bin_relative_path': 'build/tools/wasmedge/wasmedge',
    #     'dump_store_rpath' : 'dump_result/dump_store',
    #     'dump_vstack_rpath': 'dump_result/dump_vstack',
    #     'cmd': '{} --reactor {} to_test',
    #     'dump_cmd':  '{} --reactor {} to_test > {}',
    #     'ori_log_path': 'dpd_wasmedge_err_log',
    #     'dump_extractor': wasmedge_dumped_data,
    #     'support_ref': True,
    #     'support_v128': True
    # },
    'WasmEdge_disableAOT_newer':{
        'dump_dir': '/home/zph/DGit/wasm_projects/runtime_test/WasmEdge_runtimes/WasmEdge_disableAOT_newer',
        'standard_dir': '/home/zph/DGit/wasm_projects/runtime_test/WasmEdge_runtimes/ori_WasmEdge_disableAOT',
        'bin_relative_path': 'build/tools/wasmedge/wasmedge',
        'dump_store_rpath' : 'dump_result/dump_store',
        'dump_vstack_rpath': 'dump_result/dump_vstack',
        'cmd': '{} --reactor {} to_test',
        'dump_cmd':  '{} --reactor {} to_test > {}',
        'ori_log_path': 'dpd_wasmedge_err_log',
        'dump_extractor': wasmedgeDumpedResult,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    },
    # WAVM 的两个Reference存的直接就是指向对象的指针，不太好搞
    'WAVM_default':{
        'dump_dir': '/home/zph/DGit/wasm_projects/runtime_test/WAVM_runtimes/WAVM_dump_default',
        'standard_dir': '/home/zph/DGit/wasm_projects/runtime_test/WAVM_runtimes/ori_WAVM_can_print',
        'bin_relative_path': 'build/bin/wavm',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'cmd': '{} run --function=to_test {}',
        'dump_cmd':  '{} run --function=to_test {} 2> {}',
        'ori_log_path': 'dpd_wavm_err_log',
        'dump_extractor': wavmDumpedResult,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    }
}