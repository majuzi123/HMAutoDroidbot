## :memo: 关于
HMDroidbot（HM代表HarmonyOS，Droid代表Android）是一个轻量级的测试输入生成器，适用于HarmonyOS（兼容Android）。它是从[Droidbot](https://github.com/honeynet/droidbot) fork出来的，支持HarmonyOS NEXT设备。
它可以发送随机或脚本化的输入事件来测试HarmonyOS应用程序，更快地实现更高的代码覆盖率，并在测试后生成一个UI跳转关系图（UTG）。

## :smiling_face_with_three_hearts: 功能特性
:boom: 现已支持HarmonyOS的覆盖率报告！包括ability、pages等以及一些HarmonyOS特定的指标！请参见下面的示例报告！

![image](https://github.com/user-attachments/assets/1dfbb6f8-c9ab-48b2-8043-5474719a7466)

:boom: 支持Android和HarmonyOS NEXT设备。使用标志 `-is_harmonyos` 来指定目标系统。

:boom: 源代码改进。更易于阅读和调试。为源代码添加了类型注解并对日志进行了上色。使用 `-debug` 标志将调试级别日志打印到终端！

:boom: 使用 `-log` 标志从设备获取hilog。请在报告目录中查看！

## 前提条件

1. `Python 3.10+`
2. `HDC cmdtool 3.1.0a+`

## 使用方法

1. **确保您拥有：**

    + 要分析的应用程序的 `.hap` 文件路径。

    我们提供了一些[用于测试的示例hap](https://github.com/XixianLiang/HarmonyOS_NEXT_apps)。

    + 一台通过 `hdc` 连接到主机的设备或模拟器。使用 `hdc list targets` 检查连接的设备。

    + 根据系统正确选择 `SYSTEM` 变量。请参见下文 **故障排除** 章节。

    + 安装所需的包。

        clone 此仓库并使用 `pip` 安装。

        :one: *（可选）* 你可以先设置一个虚拟环境，详情请见 python 的 [venv 模块](https://realpython.com/python-virtual-environments-a-primer/)

       **macOS 或 Linux 系统:**
       ```shell
       python3 -m venv droidenv
       source droidenv/bin/activate
       ```

       **Windows系统:**
       ```powershell
       python3 -m venv droidenv
       .\droidenv\Scripts\activate
       ```

        :two: 下面的 `pip` 命令将自动抓取并安装所需的包。
        
        ```shell
        git clone https://github.com/XixianLiang/HMDroidbot.git
        cd HMDroidbot
        pip install -e .
        ```
        
        :three: 如果安装成功，您应该能够执行 `droidbot -h`。（如果无法运行 `droidbot` 命令，请尝试使用 `python3 -m droidbot.start -h` 代替）。

2. **快速开始（目前仅在WSL中可用，只有真机可用，模拟器目前无法使用）：**

    :wave: 只需运行我们提供的 `run_sample.sh` 文件以下载示例hap包并尝试HMDroidbot！
    ```bash
    bash run_sample.sh
    ```

3. **启动HMDroidbot：**

    通过 `python -m` 运行droidbot。
    ```bash
    python3 -m droidbot.start -a <hap的绝对路径> -o output_dir -is_harmonyos
    ```
    
    通过 `droidbot` 运行droidbot。
    ```bash
    droidbot -a <hap的绝对路径> -o output_dir -is_harmonyos
    ```

    > 注意！-a 用于指定hap的路径，请在这里使用绝对路径！相对路径暂不支持。
    测试开始后，您将在输出目录中实时找到许多有用的信息，包括生成的UTG。

    + 如果您使用多个设备，您可能需要使用 `-t <device_serial>` 来指定目标设备。确定设备序列号的最简单方法是调用 `hdc list targets`。
    + 在调试源代码时， `-debug` 很有用。
    + 使用 `-log` 标志获取HarmonyOS中的hilog，可以在报告目录中找到这个文件。
    + 您可以在 `droidbot -h` 中找到其他有用的功能。
    + 如果您使用模拟器，是没有序列号的，当使用hdc list targets命令时应该得到的是一个本地回环地址ip和端口：127.0.0.1:5555，
   您可能需要使用 `-t 127.0.0.1:5555` 来指定目标设备。

    **示例启动脚本**
    ```bash
    # 通过droidbot命令启动
    droidbot -a <hap的绝对路径> -o output -t 23E**********1843 -count 1000 -is_harmonyos -debug

    # 通过运行模块启动。易于调试！
    # 在HMDroidbot目录中执行以下命令。
    python -m droidbot.start -a <hap的绝对路径> -o output -t 23E**********1843 -count 1000 -is_harmonyos -debug
   
   # 如果您使用模拟器，执行以下命令：
   python -m droidbot.start -a <absolute_path_to_hap> -o output -t 127.0.0.1:5555 -count 1000 -is_harmonyos -debug
    ```

    **vscode `launch.json` 文件示例**

   <img width="1134" alt="image" src="https://github.com/user-attachments/assets/bffde3f3-deea-41fb-9087-fb7eb3772bd5">

    
## 故障排除
您应该在 `droidbot/adapter/hdc.py` 中使用正确的 `SYSTEM` 变量。

<img width="687" alt="image" src="https://github.com/user-attachments/assets/b8de8da9-7d95-4e1e-b032-8cb5a5b00bc3">

我们使用WSL开发该项目，因此我们在此项目中使用的hdc工具实际上是通过在Windows上添加 `/mnt/.../hdc.exe` 到WSL路径的 `hdc.exe`。

由于HarmonyOS NEXT处于测试版，配置hdc环境的过程有点复杂（尤其在WSL上）。WSL的配置总体思路是将hdc工具装在主系统，并从WSL的`mnt`路径下将主系统路径下的`hdc.exe` export出去（因为手机连在主系统上，这样做不用再配置USB口的转发），如果您在配置环境时遇到任何问题，请随时与我联系。

## :mega: 信息
目前，HMDroidbot由[华东师范大学-移动软件分析与测试小组](https://mobile-app-analysis.github.io/)维护。

该项目的主要负责人是[梁锡贤](https://xixianliang.github.io/resume/)和[明孟立](https://ml-ming.dev/)。我们的指导老师是[苏亭教授](https://tingsu.github.io/)。如果您有任何问题或建议，请随时与我们联系。

加入QQ交流群 （群号 904153331）来联系我们并获取最新资讯。

<img width="284" alt="image" src="https://github.com/user-attachments/assets/c42c2bdf-6c3d-4774-a2a4-34adcc84cfe7">

## 致谢

- [Droidbot](https://github.com/honeynet/droidbot)
- [awesome-hdc](https://github.com/codematrixer/awesome-hdc)
- 本项目的开发得到了华为工程师的慷慨帮助和建议。

## 许可证

本项目基于原始MIT许可证（请参见 `LICENSE` 文件），并包括我的贡献，受[Xixian Liang](https://github.com/XixianLiang)的管理（请参见 `LICENSE_NEW` 文件）。
