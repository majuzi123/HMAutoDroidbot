## About
HMDroidBot (HM stands for HarmonyOS) is a lightweight test input generator for HarmonyOS. It forks from [Droidbot](https://github.com/honeynet/droidbot) and supports HarmonyOS NEXT devices.
It can send random or scripted input events to an HarmonyOS app, achieve higher test coverage more quickly, and generate a UI transition graph (UTG) after testing.

## :smiling_face_with_three_hearts: Awesome Features 
:boom: Surport HarmonyOS report now! Including ability, bundle, etc.. And the HarmonyOS-specific analysis criteria page! See the sample report below!

![image](https://github.com/user-attachments/assets/b8359efc-6d1b-4dff-95d4-551744e25131)

:boom: Support both Android and HarmonyOS devices. Use the flag `-is_harmonyos` to specify the target system.

:boom: Source code improvment. Easier to read and debug. Added typing to the source code and colorized the logging.

## Future Develop plan
:negative_squared_cross_mark: Better layout dump. Currently HMDroidbot uses hdc cmd to dump hierachy. Which is inefficient and has highly hindered the testing effect. In the near future, we will try to make full use of the HarmonyOS sdk and accelerate this progress. Please keep an eye on our project.

:negative_squared_cross_mark: We're doing static analysis among harmonyOS apps. Some harmonyOS-specific criteria like page cov will be added into this project.

:negative_squared_cross_mark: HDC cmd is not allowed to reset the text. The sending text action is not implemented and will be supported soon.

## Prerequisite

1. `Python 3.10+`
2. `HDC cmdtool`

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
    + A device or an emulator connected to your host machine via `hdc`.

2. **Start HMDroidBot:**
    
    Basic command
    ```bash
    droidbot -a <path_to_hap> -o output_dir -is_harmonyos
    ```
    That's it! You will find much useful information, including the UTG, generated in the output dir.

    + If you are using multiple devices, you may need to use `-d <device_serial>` to specify the target device. The easiest way to determine a device's serial number is calling `hdc list targets`.
    + You may find the `-debug` tag useful while you trying to debug the source code.
    + You may find other useful features in `droidbot -h`.

    **Example Scipt**
    ```bash
    # Start by droidbot cmd
    droidbot -a PATH_TO_hap_FILE -o output -d 23E**********1843 -count 1000 -is_harmonyos -debug

    # Start by running module. Easy to debug!
    python -m droidbot.start -a PATH_TO_.hap -o output -d 23E**********1843 -count 1000 -is_harmonyos -debug
    ```

## :mega: Info
Currently, HMDroidbot is maintained by [ECNU-SE-LAB mobile apps testing group (华东师范大学软件工程实验室 mobile apps 分析与测试小组)](https://mobile-app-analysis.github.io/). We are doing research on ArkTS static anaylsis for WTG(Window transition graph) and it's usage for guided app testing.

This project is lead by [Xixian Liang (App Testing)](https://xixianliang.github.io/resume/) and [Mengli Ming (Static Analysis)](https://ml-ming.dev/). We are supervised by [prof. Tiug Su](https://tingsu.github.io/). Feel free to contact us if you have any question or advice.

## Acknowledgement

- [Droidbot](https://github.com/honeynet/droidbot)
- [awesome-hdc](https://github.com/codematrixer/awesome-hdc)
- The development of this project receives generous help and advice from the HUAWEI engineers.