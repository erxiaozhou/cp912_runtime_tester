from extract_dump import iwasmClassicInterpDumpedResult
from extract_dump import wasmiDumpedResult
from extract_dump import wasm3_dumped_data
from extract_dump import wasmedgeDumpedResult
from extract_dump import wasmerDumpedResult
from extract_dump import iwasmFastInterpDumpedResult
from extract_dump import wavmDumpedResult
from pathlib import Path


runtimes_base_dir = '/home/zph/DGit/wasm_projects/std_runtime_test'
runtimes_base_dir = '/home/std_runtime_test'
runtimes_base_dir = Path(runtimes_base_dir)

impl_paras_std_release = {
    'wasmer_default_dump':{
        # Sep 27
        # release-3.0.0-beta.2
        # 6ca9a39c501ed6b0b8d7c793f9fba9a0d636b147
        'dump_dir': runtimes_base_dir / 'dump_wasmer_default_release',
        'bin_relative_path': 'target/release/wasmer',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'err_channel': 'stderr',
        'std_cmd': '{} {}  --invoke to_test',
        'dump_extractor': wasmerDumpedResult,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    },
    'wasmi_interp': {
        # Sep 24
        # v0.17.0
        # fc58331904c75afaac08e89238590a9bf6cd84d3
        # added dump code; have not checked dump code
        # add dump code ; uncheck
        'dump_dir': runtimes_base_dir / 'dump_wasmi_release',
        'bin_relative_path': 'target/release/wasmi_cli',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'err_channel': 'stderr',
        'std_cmd': '{} {}  to_test',
        'dump_extractor': wasmiDumpedResult,
        'support_multi_mem': False,
        'support_ref': False,
        'support_v128': False
    },
    'iwasm_classic_interp_dump':{
        # Sep 8
        # 6820af621265413b677e450cf126bb66c9f77077
        # added dump code; have not checked dump code
        'dump_dir': runtimes_base_dir / 'dump_iwasm_interp_classic_release',
        'bin_relative_path': 'product-mini/platforms/linux/build/iwasm',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'err_channel': 'stdout',
        'std_cmd': '{} --heap-size=0 -f to_test {}',
        'dump_extractor': iwasmClassicInterpDumpedResult,
        'support_multi_mem': False,
        'support_ref': True,
        'support_v128': False  # ?
    },
    'iwasm_fast_interp_dump':{
        # Sep 8
        # 6820af621265413b677e450cf126bb66c9f77077
        # added dump code; have not checked dump code
        'dump_dir': runtimes_base_dir / 'dump_iwasm_interp_fast_release',
        'bin_relative_path': 'product-mini/platforms/linux/build/iwasm',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'err_channel': 'stdout',
        'std_cmd': '{} --heap-size=0 -f to_test {}',
        'dump_extractor': iwasmFastInterpDumpedResult,
        'support_multi_mem': False,
        'support_ref': True,
        'support_v128': False  # ?
    },
    # iwasm_jit
    # Sep 8
    # jit可以改一个靠后的版本
    # 6820af621265413b677e450cf126bb66c9f77077
    # /home/zph/DGit/wasm_projects/std_runtime_test/ori_iwasm_interp_jit
    # /home/zph/DGit/wasm_projects/std_runtime_test/dump_iwasm_interp_jit


    'wasm3_dump':{
        # Sep 14 #没改
        # fa18e9ece4dd45371deac69ded32838470a55c1b
        # added dump code; have not checked dump code
        'dump_dir': runtimes_base_dir / 'dump_wasm3_default_release',
        'bin_relative_path': 'build/wasm3',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'err_channel': 'stderr',
        'std_cmd': '{} --func to_test {}',
        'dump_extractor': wasm3_dumped_data,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': False
    },
    'WasmEdge_disableAOT_newer':{
        
    # WasmEdge 也可以不改，下面这个版本是改过的
    # Oct 8
    # 0.11.1
    # 980c52416bc53fafebcdf026cfc851a43dcb887c
        # added dump code; have not checked dump code
        'dump_dir': runtimes_base_dir / 'dump_WasmEdge_disableAOT_release',
        'bin_relative_path': 'build/tools/wasmedge/wasmedge',
        'dump_store_rpath' : 'dump_result/dump_store',
        'dump_vstack_rpath': 'dump_result/dump_vstack',
        'dump_instante_rpath': 'dump_result/dump_instantiation',
        'err_channel': 'stdout',
        'std_cmd': '{} --reactor {} to_test',
        'dump_extractor': wasmedgeDumpedResult,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    },
    # WAVM 的两个Reference存的直接就是指向对象的指针，不太好搞
    'WAVM_default':{
        # May 14
        # 没改
        # 3f9a150cac7faf28eab357a2c5b83d2ec740c7d9
        # added dump code; have not checked dump code
        'dump_dir': runtimes_base_dir / 'dump_WAVM_can_print_release',
        'bin_relative_path': 'build/bin/wavm',
        'dump_store_rpath' : 'dump_store',
        'dump_vstack_rpath': 'dump_vstack',
        'dump_instante_rpath': 'dump_instantiation',
        'err_channel': 'stderr',
        'std_cmd': '{} run --function=to_test {}',
        'dump_extractor': wavmDumpedResult,
        'support_multi_mem': True,
        'support_ref': True,
        'support_v128': True
    }
}