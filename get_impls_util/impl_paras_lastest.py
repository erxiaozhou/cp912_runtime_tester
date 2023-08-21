from extract_dump import iwasmHalfClassicInterpDumpData
from extract_dump import wasmiHalfDumpData
from extract_dump import wasm3HalfDumpData
from extract_dump import wasmedgeHalfDumpData
from extract_dump import wasmerHalfDumpData
from extract_dump import iwasmHalfFastInterpDumpData
from extract_dump import wavmHalfDumpData
from pathlib import Path


runtimes_base_dir = '/home/std_runtime_test/lastest_runtimes'
runtimes_base_dir = Path(runtimes_base_dir)
# TODO  先编译通，再改config

impl_paras_lastest = {
    'wasmer_default_dump':{
        # TODO externrf / funcref 的 dump 没写完
        'dump_dir': runtimes_base_dir / 'ld_wasmer_lastest',
        'standard_dir': runtimes_base_dir / 'ori_wasmer_lastest',
        'bin_relative_path': 'target/release/wasmer',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} run {}  --enable-all -e to_test',
        'err_channel': 'stderr',
        'dump_extractor': wasmerHalfDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    },
    'wasmi_interp': {
        # TODO externrf / funcref 的 dump 没写
        'dump_dir': runtimes_base_dir / 'ld_wasmi_lastest',
        'standard_dir': runtimes_base_dir / 'ori_wasmi_lastest',
        'bin_relative_path': 'target/debug/wasmi_cli',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} {}  to_test',
        'err_channel': 'stderr',
        'dump_extractor': wasmiHalfDumpData,
        'support_multi_mem': False,
        'support_ref': True,
        'support_v128': False
    },
    'iwasm_classic_interp_dump':{
        # TODO externrf / funcref 的 dump 可能要检查
        # TODO 支持  v128 和 multi-mem 的编译版本
        # 
        'dump_dir': runtimes_base_dir / 'ld_iwasm_interp_classic_lastest',
        'standard_dir': runtimes_base_dir / 'ori_iwasm_interp_classic_lastest',
        'bin_relative_path': 'product-mini/platforms/linux/build/iwasm',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} --heap-size=0 -f to_test {}',
        'err_channel': 'stdout',
        'dump_extractor': iwasmHalfClassicInterpDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': False  # ?
    },
    'iwasm_fast_interp_dump':{
        # TODO externrf / funcref 的 dump 可能要检查
        'dump_dir': runtimes_base_dir / 'ld_iwasm_interp_fast_lastest',
        'standard_dir': runtimes_base_dir / 'ori_iwasm_interp_fast_lastest',
        'bin_relative_path': 'product-mini/platforms/linux/build/iwasm',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} --heap-size=0 -f to_test {}',
        'err_channel': 'stdout',
        'dump_extractor': iwasmHalfFastInterpDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': False  # ?
    },
    'iwasm_multi_jit_dump':{
        # TODO externrf / funcref 的 dump 可能要检查
        'dump_dir': runtimes_base_dir / 'ld_iwasm_jit_lastest',
        'standard_dir': runtimes_base_dir / 'ori_iwasm_jit_lastest',
        'bin_relative_path': 'product-mini/platforms/linux/build/iwasm',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} --heap-size=0 -f to_test {}',
        'err_channel': 'stdout',
        'dump_extractor': iwasmHalfFastInterpDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': False  # ?
    },
    'wasm3_dump':{
        'dump_dir': runtimes_base_dir / 'ld_wasm3_lastest',
        'standard_dir': runtimes_base_dir / 'ori_wasm3_lastest',
        'bin_relative_path': 'build/wasm3',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} --func to_test {}',
        'err_channel': 'stderr',
        'dump_extractor': wasm3HalfDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': False
    },
    'WasmEdge_disableAOT_newer':{
        'dump_dir': runtimes_base_dir / 'ld_WasmEdge_disableAOT_lastest',
        'standard_dir': runtimes_base_dir / 'ori_WasmEdge_disableAOT_lastest',
        'bin_relative_path': 'build/tools/wasmedge/wasmedge',
        'dump_vstack_rpath': 'dump_result/dump_vstack',
        'dump_instante_rpath': 'dump_result/dump_instantiation',
        'std_cmd': '{} --reactor {} to_test',
        'err_channel': 'stdout',
        'dump_extractor': wasmedgeHalfDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    },
    'WAVM_default':{
        'dump_dir': runtimes_base_dir / 'ld_WAVM_can_print_lastest',
        'standard_dir': runtimes_base_dir / 'ori_WAVM_can_print_lastest',
        'bin_relative_path': 'build/bin/wavm',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'std_cmd': '{} run --function=to_test {}',
        'err_channel': 'stderr',
        'dump_extractor': wavmHalfDumpData,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    }
}