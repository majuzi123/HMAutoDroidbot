## :memo: About
HMDroidbot (HM stands for HarmonyOS) is a lightweight test input generator for HarmonyOS. It forks from [Droidbot](https://github.com/honeynet/droidbot) and supports HarmonyOS NEXT devices.
It can send random or scripted input events to an HarmonyOS app, achieve higher test coverage more quickly, and generate a UI transition graph (UTG) after testing.

## :smiling_face_with_three_hearts: Awesome Features 
:boom: Support HarmonyOS report now! Including ability, bundle, *etc.* and some HarmonyOS-specific criteria! See the sample report below!

![image](https://github.com/user-attachments/assets/1dfbb6f8-c9ab-48b2-8043-5474719a7466)

:boom: Support both Android and HarmonyOS devices. Use the flag `-is_harmonyos` to specify the target system.

:boom: Source code improvment. Easier to read and debug. Added typing to the source code and colorized the log. Use `-debug` flag to print the debug level log to the terminal!

:boom: Use `-log` flag to get the hilog from the device. Check it in the report directory!

## Future Develop plan
:negative_squared_cross_mark: Better layout dump. Currently HMDroidbot uses hdc cmd to dump hierachy, which is inefficient and has highly hindered the testing effect. In the near future, we will try to make full use of the HarmonyOS sdk to accelerate this progress. Please keep an eye on our project.

:negative_squared_cross_mark: We're doing static analysis among harmonyOS apps. Some harmonyOS-specific criteria like page-cov will be added into this project.

:negative_squared_cross_mark: HDC cmd is not allowed to reset the text. The sending text action is not implemented and will be supported soon.

## Prerequisite

1. `Python 3.10+`
2. `HDC cmdtool 3.1.0a+`

## How to install

Clone this repo and install with `pip`:

```shell
git clone 
cd droidbot/
pip install -e .
```

If successfully installed, you should be able to execute `droidbot -h`.

## How to use

1. **Make sure you have:**

    + `.hap` file path of the app you want to analyze.

    We provided some sample hap for testing [here](https://github.com/XixianLiang/HarmonyOS_NEXT_apps).

    + A device or an emulator connected to your host machine via `hdc`.

2. **Quick Start**

    :wave: Simply run the `run_sample.sh` file we provided to download the sample hap and try HMDroidbot!
    ```bash
    bash run_sample.sh
    ```

2. **Start HMDroidBot:**
    
    Basic command
    ```bash
    droidbot -a <absolute_path_to_hap> -o output_dir -is_harmonyos
    ```
    > Attention! -a is used to specify the path to hap, please use absolute path here!
    That's it! You will find much useful information, including the UTG, generated in the output dir.

    + If you are using multiple devices, you may need to use `-d <device_serial>` to specify the target device. The easiest way to determine a device's serial number is calling `hdc list targets`.
    + You may find the `-debug` tag useful while you are trying to debug the source code.
    + Use `-log` flag to get the hilog in HarmonyOS, which can be found in the report directory.
    + You may find other useful features in `droidbot -h`.

    **Example Starting Scripts**
    ```bash
    # Start by droidbot cmd
    droidbot -a <absolute_path_to_hap> -o output -d 23E**********1843 -count 1000 -is_harmonyos -debug

    # Start by running module. Easy to debug!
    # execute the following command in the HMDroidbot dir, which should include the setup.py.
    python -m droidbot.start -a <absolute_path_to_hap> -o output -d 23E**********1843 -count 1000 -is_harmonyos -debug
    ```
    
## Trouble shooting
Switch the `HDC_EXEC` variable from `hdc.exe` to `hdc` if you're using hdc tools for linux.

We used WSL to develop this project. so the hdc tool we used in this project is actually `hdc.exe` by adding `/mnt/.../hdc.exe` on windows to the WSL PATH.

## :mega: Info
Currently, HMDroidbot is maintained by [ECNU-SE-LAB mobile apps testing group (华东师范大学软件工程实验室 mobile apps 分析与测试小组)](https://mobile-app-analysis.github.io/). We are doing research on ArkTS static anaylsis for WTG(Window transition graph) and its usage for guided app testing.

This project is led by [Xixian Liang (App Testing)](https://xixianliang.github.io/resume/) and [Mengli Ming (Static Analysis)](https://ml-ming.dev/). We are supervised by prof. [Ting Su](https://tingsu.github.io/). Feel free to contact us if you have any question or advice.

## Acknowledgement

- [Droidbot](https://github.com/honeynet/droidbot)
- [awesome-hdc](https://github.com/codematrixer/awesome-hdc)
- The development of this project receives generous help and advice from the HUAWEI engineers.
