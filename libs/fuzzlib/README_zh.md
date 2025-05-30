# 测试框架Fuzzing安全测试指导

- [Fuzzing简介](#section7730298375831)
- [Fuzzing测试关注的风险接口](#section00067164921)
- [使用测试框架DTFuzz](#section0009871491)
  - [配置启动测试框架](#section005187487501)
  - [单个Fuzz用例初始化](#section372106507189)
  - [Fuzz用例编写](#section98175917)
  - [Fuzz用例编译](#section00816581589)
  - [Fuzz用例执行](#section7510974319)
- [测试结果与日志](#section016190470)

## Fuzzing简介<a name="section7730298375831"></a>

模糊测试（fuzzing test）是一种软件测试技术，其核心思想是将自动或半自动生成的随机数据输入到一个程序中，并监视程序异常，如崩溃，断言（assertion）失败，以发现可能的程序错误，比如内存泄漏，访问越界等。

Fuzzing测试框架使用了LLVM编译器框架中的[libFuzzer](https://llvm.org/docs/LibFuzzer.html)作为Fuzzing引擎进行构建，libFuzzer是一个基于LLVM编译时路径插桩，可以对被测库API进行路径引导测试的Fuzzing引擎。

使用Fuzzing测试框架，需要完成fuzzer测试用例初始化、fuzzer用例编写、fuzzer用例编译和fuzzer用例执行几步。



## Fuzzing测试关注的风险接口<a name="section00067164921"></a>

开发者应该了解自身模块的接口数据输入是基于不可信的来源输入，特别是针对

- 解析处理远程发送来的TCP/UDP或者蓝牙等协议数据
- 通过复杂的文件解码处理等，包括音视频、图片解码、解压缩等
- IPC跨进程的数据输入处理

通过Fuzzing的覆盖引导能力，可以有效的探测和消减外部输入造成的内存安全问题，也可以极大的增强系统稳定性。



## 使用测试框架开展Fuzzing<a name="section0009871491"></a>

### 配置启动测试框架<a name="section005187487501"></a>

参考[ 开发者测试组件](https://gitee.com/openharmony/testfwk_developer_test/blob/master/README_zh.md)中的描述完成测试框架安装、设备连接配置，并在linux环境下通过

```
./start.sh
```

启动测试框架。



### 单个Fuzz用例初始化<a name="section372106507189"></a>

1. Fuzz测试用例生成

   执行gen命令用于fuzzer源文件生成，会自动生成fuzzer源文件、fuzzer配置文件和corpus语料，目录结构如下

   ```
   calculator_fuzzer/
   ├── corpus                        # Fuzz语料目录
   │   ├── init                      # Fuzz语料
   ├── BUILD.gn                      # Fuzz用例编译配置
   ├── calculator_fuzzer.cpp              # Fuzz用例源文件
   ├── calculator_fuzzer.h                # Fuzz用例头文件
   ├── project.xml                   # Fuzz选项配置文件
   ```

2. 命令参数说明，参数可以指定fuzzer名称和fuzzer路径

   ```
   gen -t TESTTYPE -fn FUZZERNAME -dp DIRECTORYPATH
   ```

   | 参数 | 描述       | 说明           | 备注                                       |
   | ---- | ---------- | -------------- | ------------------------------------------ |
   | -t   | testtype   | 测试类型       | 目前仅支持"FUZZ"                           |
   | -fn  | fuzzername | fuzzer名称     | 为显式区分Fuzz用例，名称必须以测试套前缀小写 + _fuzzer形式命名 |
   | -dp  | dirpath    | fuzzer生成路径 | 路径不存在则自动创建目录                   |

3. gen命令示例，-t、-fn和-dp均为必选项

   ```
   gen -t FUZZ -fn calculator_fuzzer -dp base/account/os_account/test/fuzztest/osaccount
   ```
   
   这里以os_accont模块作为示例演示fuzz，执行完毕后会在base/account/os_account/test/fuzztest/osaccount目录下生成一个Fuzz用例demo。



### Fuzz用例编写<a name="section98175917"></a>

1. 源文件编写

   Fuzz用例主要在**${fuzzer名称}.cpp**源文件中，一个Fuzz用例仅支持一个接口进行fuzz测试。

   源文件包含两个接口：

   | 接口                            | 说明                             |
   | ------------------------------- | -------------------------------- |
   | LLVMFuzzerTestOneInput          | Fuzz入口函数，由Fuzz框架调用     |
   | DoSomethingInterestingWithMyAPI | 被测试接口，实现各业务被测试逻辑 |

   ![img](../../public_sys-resources/icon-note.gif) **说明：** DoSomethingInterestingWithMyAPI接口名称允许依据业务逻辑修改。两接口参数data和size为fuzz测试标准化参数，不可修改。

   ```
   #include "calculator_fuzzer.h"
   
   #include <stddef.h>
   #include <stdint.h>
   
   const int FUZZ_DATA_LEN = 3;
   const int FUZZ_FST_DATA = 0;
   const int FUZZ_SND_DATA = 1;
   const int FUZZ_TRD_DATA = 2;
   const int FUZZ_FTH_DATA = 3;
   
   namespace OHOS {
       bool DoSomethingInterestingWithMyAPI(const uint8_t* data, size_t size)
       {
           bool result = false;
           if (size >= FUZZ_DATA_LEN) {
               result = data[FUZZ_FST_DATA] == 'F' &&
                   data[FUZZ_SND_DATA] == 'U' &&
                   data[FUZZ_TRD_DATA] == 'Z' &&
                   data[FUZZ_FTH_DATA] == 'Z';
           }
           return result;
       }
   }
   
   /* Fuzzer entry point */
   extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
   {
       /* Run your code on data */
       OHOS::DoSomethingInterestingWithMyAPI(data, size);
       return 0;
   }
   ```
   ### 注意：当data需强制转换为字符串类型时，需要携带size，例如:
   ```
   std::string result((const char*) data, size);
   ```



2. BUILD.gn编写

   基于[ohos_fuzztest]配置Fuzz模板，例如：

   需要注意的是fuzz_config_file, 使用gen命令生成的BUILD.GN文件中没有指明，需要写完测试套后加在BUILD.gn中

   ```
   ohos_fuzztest("CalculatorFuzzTest") {     #定义测试套名称CalculatorFuzzTest
     module_out_path = module_output_path
     fuzz_config_file = "//base/account/os_account/test/fuzztest/osaccount/calculator_fuzzer"
     include_dirs = []
     cflags = [
       "-g",
       "-O0",
       "-Wno-unused-variable",
       "-fno-omit-frame-pointer",
     ]
     sources = [ "calculator_fuzzer.cpp" ]
   }
   ```

   [group]引用测试套，例如：

   ```
   group("fuzztest") {
     testonly = true
     deps = []
     
     deps += [
       # deps file
       ":CalculatorFuzzTest",     #引用测试套
     ]
   }
   ```
   **注意：** 
   - #### 测试套名称必须采用大驼峰风格，并且必须以FuzzTest结尾，测试套前缀与fuzzer目录名相对应（例如：calculator_fuzzer，只能有一个下划线）。
   - module_out_path为测试套编译输出目录，内容为部件+模块名，例如"os_account/os_account"。
   

3. Fuzz配置编写

   project.xml为DTFuzz参数配置文件，提供基于libFuzzer参数的动态配置，更多参数配置可参考[libFuzzer参数配置](https://llvm.org/docs/LibFuzzer.html#options)：

   ```
   <!-- maximum length of a test input -->
   <max_len>1000</max_len>
   <!-- maximum total time in seconds to run the DTFuzz -->
   <max_total_time>300</max_total_time>
   <!-- memory usage limit in Mb -->
   <rss_limit_mb>4096</rss_limit_mb>
   ```
   需要注意的是这里fuzz测试用例设置的默认的运行时间为300s, 实际使用中可以根据自己使用需要进行更改。
   

### Fuzz用例编译<a name="section00816581589"></a>

添加Fuzz用例编译到模块的test_list中：

1. 在需要DTFuzz测试的对应模块bundle.json中添加Fuzz用例路径，如在bundle.json添加：

   ```
   "tests": [
     "//test/developer_test/examples/calculator/test:unittest",
     "//test/developer_test/examples/calculator/test:fuzztest", #添加DTFuzz用例路径
     "//test/developer_test/examples/detector/test:unittest",
     "//test/developer_test/examples/sleep/test:performance",
     "//test/developer_test/examples/distributedb/test:distributedtest"
   ]
   ```

2. 在用例路径下的BUILD.gn添加group，例如在os_account/test/fuzztest/osaccount/calculator_fuzzer的BUILD.gn中添加

   ```
   group("fuzztest") {
     testonly = true
     deps = []
     
     deps += [ "calculator_fuzzer:fuzztest" ]
   }
   ```
3. 编译时添加--build-target选项，如

   ```
   ./build.sh --product-name rk3568 --build-target CalculatorFuzzTest
   ```
   

### Fuzz用例执行<a name="section7510974319"></a>

Fuzz能力集成，在测试类型-t中新增FUZZ类型，执行Fuzz测试指令示例，其中-t为必选，-ss和-tm为可选

```
run -t FUZZ -ss developer_test -tm calculator
```

| 参数 | 描述       | 说明     | 备注                     |
| ---- | ---------- | -------- | ------------------------ |
| -t   | TESTTYPE   | 测试类型 |                          |
| -ss  | SUBSYSTEM  | 子系统   | 被测试子系统             |
| -tm  | TESTMODULE | 模块     | 被测试模块，如calculator |

- Windows环境脱离源码执行

  首先将testfwk_developer_test 和 testfwk_xdevice 两个仓库的代码下载到本地，这里假设放到D盘并在D:\test 目录下创建developer_test, xdevice和tests三个目录，developer_test和xdevice目录分别存放对应仓库的代码。

  Windows环境可通过归档DTFuzz用例配置文件project.xml、语料corpus和可执行文件执行DTFuzz。

  1. 归档用例配置文件、语料以及用例可执行文件

     新建目录，如： 
     #### 注意：必须是\tests目录

     ```
     D:\test\tests
     ```

     用例可执行文件为DTFuzz源文件编译产出文件，以二进制形式存储在out/release/tests/fuzztest下。测试用例的配置文件均编译输出在out/release/tests/res目录下对应的xxxx_fuzzer目录中。（release为对应的产品名，如编译rk3568则在out/rk3568下面）
     将fuzztest目录以及res目录直接拷贝到该路径下即可。

     
  2. 配置用例路径
  
     在developer_test\config\user_config.xml中配置用例归档路径：
  
     ```
     <!-- configure test cases path -->
     <test_cases>
       <dir>D:\test\tests</dir>     #用例可执行文件归档路径
     </test_cases>
     ```
  
  3. 执行用例
  
     在developer_test下执行./start.bat开启测试框架，执行DTFuzz命令示例
  
     ```
     run -t FUZZ -ts CalculatorFuzzTest
     ```
     
     

## 测试结果与日志<a name="section016190470"></a>

- 通过在测试框架中执行测试指令，即可以生成测试日志和测试报告。

- 测试结果

  测试用例的结果会直接显示在控制台上，执行一次的测试结果根路径如下：

  ```
  reports/xxxx-xx-xx-xx-xx-xx
  ```

  测试用例格式化结果

  ```
  result/
  ```

  测试用例日志

  ```
  log/plan_log_xxxx-xx-xx-xx-xx-xx.log
  ```

  测试报告汇总

  ```
  summary_report.html
  ```

  测试报告详情

  ```
  details_report.html
  ```
