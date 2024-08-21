## :memo: About
HMDroidbot (HM stands for HarmonyOS, Droid stands for Android) is a lightweight test input generator for HarmonyOS (and Android). It forks from [Droidbot](https://github.com/honeynet/droidbot) and supports HarmonyOS NEXT devices.
It can send random or scripted input events to test an HarmonyOS app, achieve higher code coverage more quickly, and generate a UI transition graph (UTG) after testing.

## :smiling_face_with_three_hearts: Awesome Features 
:boom: Support coverage report for HarmonyOS now! Including ability, page, *etc.* and some HarmonyOS-specific metrics! See the sample report below!

![image](https://github.com/user-attachments/assets/1dfbb6f8-c9ab-48b2-8043-5474719a7466)

:boom: Support both Android and HarmonyOS devices. Use the flag `-is_harmonyos` to specify the target system.

:boom: Source code improvement. Easier to read and debug. Added typing to the source code and colorized the log. Use `-debug` flag to print the debug level log to the terminal!

:boom: Use `-log` flag to get the hilog from the device. Check it in the report directory!

## Prerequisite

1. `Python 3.10+`
2. `HDC cmdtool 3.1.0a+`

## How to use

1. **Make sure you have:**

    + `.hap` file path of the app you want to analyze.

    We provided some sample hap for testing [here](https://github.com/XixianLiang/HarmonyOS_NEXT_apps).

    + A device or an emulator connected to your host machine via `hdc`. Use `hdc list targets` to checkout the connected device.
  
    + The `SYSTEM` variable is correctly chosen. See [trouble shooting](https://github.com/XixianLiang/HMdroidbot?tab=readme-ov-file#trouble-shooting).
  
    + Install the required packages.

        Clone this repo and install with `pip`.

       The `pip` command will automatic grep and install the required packages for you.
        
        ```shell
        git clone git@github.com:honeynet/droidbot.git
        cd HMdroidbot
        pip install -e .
        ```
        
        If successfully installed, you should be able to execute `droidbot -h`. (If failed to run `droidbot` cmd, try to use `python3 -m droidbot.start -h` instead).

2. **Quick Start (Only available in WSL now):**

    :wave: Simply run the `run_sample.sh` file we provided to download the sample hap and try HMDroidbot!
    ```bash
    bash run_sample.sh
    ```

2. **Start HMDroidbot:**

    :+1: Run droidbot by `python -m`.
    ```bash
    python3 -m droidbot.start -a <absolute_path_to_hap> -o output_dir -is_harmonyos
    ```
    
    :-1: Run droidbot by `droidbot`
    ```bash
    droidbot -a <absolute_path_to_hap> -o output_dir -is_harmonyos
    ```


    
    > Attention! -a is used to specify the path to hap, please use absolute path here!
    That's it! You will find much useful information, including the UTG, generated in the output dir.

    + If you are using multiple devices, you may need to use `-t <device_serial>` to specify the target device. The easiest way to determine a device's serial number is calling `hdc list targets`.
    + You may find the `-debug` tag useful while you are trying to debug the source code.
    + Use `-log` flag to get the hilog in HarmonyOS, which can be found in the report directory.
    + You may find other useful features in `droidbot -h`.

    **Example Starting Scripts**
    ```bash
    # Start by droidbot cmd
    droidbot -a <absolute_path_to_hap> -o output -t 23E**********1843 -count 1000 -is_harmonyos -debug

    # Start by running module. Easy to debug!
    # execute the following command in the HMDroidbot dir, which should include the setup.py.
    python -m droidbot.start -a <absolute_path_to_hap> -o output -t 23E**********1843 -count 1000 -is_harmonyos -debug
    ```

    **vscode Debug file example**
   <img width="1134" alt="image" src="https://github.com/user-attachments/assets/bffde3f3-deea-41fb-9087-fb7eb3772bd5">

    
## Trouble shooting
You should use the correct `SYSTEM` variable in `droidbot/adapter/hdc.py`.

<img width="687" alt="image" src="https://github.com/user-attachments/assets/b8de8da9-7d95-4e1e-b032-8cb5a5b00bc3">

We used WSL to develop this project. so the hdc tool we used in this project is actually `hdc.exe` by adding `/mnt/.../hdc.exe` on windows to the WSL PATH.

It's a little bit complicated to setup the hdc envirnmnet since the HarmonyOS NEXT is on its beta version. If you have any trouble in setting up your envirnment, feel free to contact me. 

## :mega: Info
Currently, HMDroidbot is maintained by [华东师范大学-移动软件分析与测试小组](https://mobile-app-analysis.github.io/). 

This project is led by [Xixian Liang](https://xixianliang.github.io/resume/) and [Mengli Ming](https://ml-ming.dev/). We are supervised by Prof. [Ting Su](https://tingsu.github.io/). Feel free to contact us if you have any questions or advices.

## Acknowledgement

- [Droidbot](https://github.com/honeynet/droidbot)
- [awesome-hdc](https://github.com/codematrixer/awesome-hdc)
- The development of this project receives generous help and advice from the HUAWEI engineers.

## License

This project is based on the original MIT License (see `LICENSE` file) and includes my contributions, which are governed by [Xixian Liang](https://github.com/XixianLiang) (see `LICENSE_NEW` file).
