#!/usr/bin/env python3
# coding=utf-8
#
# Copyright (c) 2025 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import subprocess
import json
import sys
import argparse


def get_path_code_directory(after_dir):
    """
    拼接绝对路径工具 类
    """
    current_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_path)

    root_path = current_dir.split("/test/testfwk/developer_test")[0]

    # 拼接用户传入路径
    full_path = os.path.join(root_path, after_dir)

    return full_path


def get_build_tools_paths(root_out_dir):
    # 获取es2panda路径
    abs_es2panda_path = os.path.join(root_out_dir, 'ohos_ets', 'build-tools', 'ets2panda', 'bin', 'es2panda')
    # 获取ark_link路径
    abs_arklink_path = os.path.join(root_out_dir, 'ohos_ets', 'build-tools', 'ets2panda', 'bin', 'ark_link')
    # 获取tools目录
    tools_rel = 'test/testfwk/developer_test/libs/arkts1.2'
    abs_tools_path = get_path_code_directory(tools_rel)
    # 获取hypium目录
    hypium_rel = 'test/testfwk/arkxtest/jsunit/src_static/'
    abs_hypium_path = get_path_code_directory(hypium_rel)
    # 获取etsstdlib.abc路径
    abs_stdlib_path = os.path.join(root_out_dir, 'ohos_ets', 'build-tools', 'ets2panda', 'lib', 'etsstdlib.abc')
    # 检查工具是否存在
    critical_tools = {
        "es2panda" : abs_es2panda_path,
        "arklink" : abs_arklink_path,
        "stdlib" : abs_stdlib_path
    }

    for name, path in critical_tools.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"构建工具缺失：{name}位于{path}.请检查构建环境是否正确配置")

    return {
        "es2panda": abs_es2panda_path,
        "arklink": abs_arklink_path,
        "tools": abs_tools_path,
        "hypium": abs_hypium_path,
        "stdlib": abs_stdlib_path
    }


def generate_arktsconfig(build_paths, root_out_dir):
    # 定义基础映射关系
    path_mappings = {
        "@ohos.buffer": "ohos_ets/api/@ohos.buffer.d.ets",
        "@ohos.util.ArrayList": "ohos_ets/api/@ohos.util.ArrayList.d.ets",
        "@ohos.util.HashMap": "ohos_ets/api/@ohos.util.HashMap.d.ets",
        "@ohos.util": "ohos_ets/api/@ohos.util.d.ets",
        "@ohos.uri": "ohos_ets/api/@ohos.uri.d.ets",
        "@ohos.base": "ohos_ets/api/@ohos.base.d.ets",
        "@arkts.math.Decimal": "ohos_ets/arkts/@arkts.math.Decimal.d.ets",
        "@arkts.collections": "ohos_ets/arkts/@arkts.collections.d.ets",
        "AbilityDelegator": "test/testfwk/developer_test/libs/arkts1.2/AbilityDelegator.ets",
        "@ohos.app.ability.UIAbility": "test/testfwk/developer_test/libs/arkts1.2/@ohos.app.ability.UIAbility.ets",
        "AbilityStageMonitor": "test/testfwk/developer_test/libs/arkts1.2/AbilityStageMonitor.ets",
        "@ohos.hilog": "test/testfwk/developer_test/libs/arkts1.2/@ohos.hilog.ets",
        "@ohos.app.ability.AbilityStage": "test/testfwk/developer_test/libs/arkts1.2/@ohos.app.ability.AbilityStage.ets",
        "@ohos.systemDateTime": "test/testfwk/developer_test/libs/arkts1.2/@ohos.systemDateTime.ets",
        "@ohos.app.ability.abilityDelegatorRegistry":
            "test/testfwk/developer_test/libs/arkts1.2/@ohos.app.ability.abilityDelegatorRegistry.ets",
        "AbilityDelegatorArgs": "test/testfwk/developer_test/libs/arkts1.2/AbilityDelegatorArgs.ets",
        "@ohos.app.ability.Want": "test/testfwk/developer_test/libs/arkts1.2/@ohos.app.ability.Want.ets",
        "AbilityMonitor": "test/testfwk/developer_test/libs/arkts1.2/AbilityMonitor.ets",
        "ShellCmdResult": "test/testfwk/developer_test/libs/arkts1.2/ShellCmdResult.ets",

        "@ohos.util.Deque": "ohos_ets/api/@ohos.util.Deque.d.ets",
        "@ohos.util.HashSet": "ohos_ets/api/@ohos.util.HashSet.d.ets",
        "@ohos.util.LightWeightMap": "ohos_ets/api/LightWeightMap.d.ets",
    }

    config = {
        "compilerOptions": {
            "baseUrl": "..",
            "cacheDir": "/tmp/es2panda_cache",
            "paths": {},
            "dependencies": {
                "std/core": {"path": build_paths["stdlib"]},
                "std/math": {"path": build_paths["stdlib"]},
                "std/math/consts": {"path": build_paths["stdlib"]},
                "std/containers": {"path": build_paths["stdlib"]},
                "std/interop/js": {"path": build_paths["stdlib"]},
                "std/time": {"path": build_paths["stdlib"]},
                "std/debug": {"path": build_paths["stdlib"]},
                "std/debug/concurrency": {"path": build_paths["stdlib"]},
                "std/dfx": {"path": build_paths["stdlib"]},
                "std/testing": {"path": build_paths["stdlib"]},
                "std/concurrency": {"path": build_paths["stdlib"]},
                "std/annotations": {"path": build_paths["stdlib"]},
                "std/interop": {"path": build_paths["stdlib"]},
                "escompat": {"path": build_paths["stdlib"]},
                "arkruntime": {"path": build_paths["stdlib"]},
            }
        }
    }
    # 动态填充paths并校验
    for key, rel_path in path_mappings.items():
        if rel_path.startswith("test/"):
            full_path = get_path_code_directory(rel_path)
        else:
            full_path = os.path.join(root_out_dir,rel_path)
        # 检查文件是否存在
        if not os.path.exists(full_path):
            print(f"Warning: 路径映射'{key}'指向的文件不存在：{full_path}")
            continue

        config["compilerOptions"]["paths"][key] = [full_path]

    return config


def collect_ets_files(dir_path, exclude_dirs=None):
    if not os.path.isdir(dir_path):
        return []

    exclude = exclude_dirs or []
    default_exclude = {"testAbility", "testrunner", "_pycache_", ".git", "node_modules"}
    exclude = list(exclude) + list(default_exclude)

    ets_files = []
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if d not in exclude]
        for f in files:
            if f.endswith(".ets"):
                ets_files.append(os.path.join(root, f))
    return ets_files


def build_tools(compile_filelist, hypium_output_dir, build_paths, root_out_dir):
    """
    编译工具类
    """
    es2panda_path = build_paths["es2panda"]
    stdlib_path = build_paths["stdlib"]
    # 生成arktsconfig
    arktsconfig_json = generate_arktsconfig(build_paths, root_out_dir)
    config_file_path = os.path.join(hypium_output_dir, "arktsconfig.json")
    with open(config_file_path, 'w', encoding="utf-8") as f:
        json.dump(arktsconfig_json, f, indent=4, ensure_ascii=False)
        print(f"已生成动态配置文件：{config_file_path}")

    # 1. 创建输出目录
    output_dir = os.path.join(hypium_output_dir, "out")
    os.makedirs(output_dir, exist_ok=True)

    # 逐个执行编译命令
    for ets_file in compile_filelist:
        try:
            # 获取文件名(不带路径)
            file_name = os.path.basename(ets_file)
            base_name = os.path.splitext(file_name)[0]
            output_filepath = os.path.join(output_dir, f"{base_name}.abc")
            # 如果hypium和tools的abc文件存在则跳过编译
            if os.path.exists(output_filepath):
                print(f".abc文件已存在：'{output_filepath}',跳过编译")
                continue

            # 构造编译命令
            command = [es2panda_path, ets_file, f"--output={output_filepath}", f"--arktsconfig={config_file_path}"]
            print(f"执行命令: {' '.join(command)}")

            # 执行命令并获取输出
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # 成功编译
            print(f"成功编译'{ets_file}', 输出路径： {output_filepath}")

        except subprocess.CalledProcessError as e:
            print(f"'{ets_file}' 编译失败（返回码: {e.returncode}）")
            if e.stderr:
                print("错误输出:", e.stderr.strip())
            print(f"编译失败，流程终止。请检查上述文件。")
            raise
        except Exception as e:
            print(f"'{ets_file}'编译失败:{e}")
            break
    # 所有文件都成功编译，统计 .abc 文件数量
    count = 0
    for root, _, filenames in os.walk(output_dir):
        for filename in filenames:
            if filename.endswith(".abc"):
                count += 1

    # 判断是否全部编译成功
    if count != len(compile_filelist):
        print(f"WARNING: 预期编译 {len(compile_filelist)} 个文件，"
              f"但只找到 {count} 个 .abc 文件。")
        print("可能有文件未正确生成，流程终止。")
        raise RuntimeError("编译结果不完整，部分文件未生成 .abc 输出。")

    # 如果hypium和tools所有的文件都编译成功,则把所有abc文件link成一个abc文件
    link_abc_files(output_dir, build_paths)

    print(f"工具链编译与链接完成！在{hypium_output_dir}目录下生成hypium_tools.abc")


def collect_abc_files(output_dir):
    abc_files = []

    # 收集out目录下的.abc文件
    if os.path.exists(output_dir):
        out_files = [
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.endswith('.abc')
        ]
        abc_files.extend(out_files)

    return abc_files


def build_ets_files(hypium_output_dir, build_paths, root_out_dir):
    """
    编译hypium、tools文件
    """
    target_file = os.path.join(hypium_output_dir, "hypium_tools.abc")
    if os.path.exists(target_file):
        print(f"发现已存在的产物：{target_file}")
        return

    abs_hypium_path = build_paths["hypium"]
    abs_tools_path = build_paths["tools"]

    files_to_compile = []
    # 收集hypium源码
    files_to_compile.extend(collect_ets_files(abs_hypium_path))
    # 收集Tools源码
    if os.path.exists(abs_tools_path):
        print(f"正在扫描Tools目录{abs_tools_path}")
        files_to_compile.extend(collect_ets_files(abs_tools_path))
    else:
        print(f"Warning: Tools目录不存在{abs_tools_path}")

    if not files_to_compile:
        print("未找到可编译的 .ets 文件，跳过编译。")
        return
    build_tools(files_to_compile, hypium_output_dir, build_paths, root_out_dir)


def link_abc_files(output_dir, build_paths):
    arklink_path = build_paths["arklink"]
    abc_files = collect_abc_files(output_dir)

    if not abc_files:
        print("终止: 没有找到可连接的.abc文件")
        return

    out_path = os.path.join(os.path.dirname(output_dir), "hypium_tools.abc")

    command = [
        arklink_path,
        f"--output={out_path}",
        "--",
        *abc_files
    ]

    print(f"执行命令: {' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("状态: 链接成功\n输出:", result.stdout.strip())

    except subprocess.CalledProcessError as e:
        print("错误: 链接失败")
        print("错误详情:", e.stderr.strip())
        raise  # 可以选择抛出异常或处理错误


def main():
    print("开始编译", flush=True)
    parser = argparse.ArgumentParser(description="Compile ETS test cases and link into .abc")
    parser.add_argument("--root_out_dir", type=str, required=False,
                    help="Path to root_out_dir executable")
    args = parser.parse_args()
    try:
        build_paths = get_build_tools_paths(args.root_out_dir)
        hypium_output_dir = os.path.join(args.root_out_dir, "tests", "arktstdd", "hypium")
        os.makedirs(hypium_output_dir, exist_ok=True)
        print(f"输出目录：{hypium_output_dir}")
        # 执行hypium编译
        build_ets_files(hypium_output_dir, build_paths, args.root_out_dir)
    except Exception as e:
        print(f"工具链/hypium构建编译失败，无法继续后续流程：{e}")
        sys.exit(1)
    print("编译结束", flush=True)


if __name__ == '__main__':
    main()