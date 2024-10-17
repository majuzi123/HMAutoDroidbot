### :book: [中文文档](https://github.com/XixianLiang/HMDroidbot/blob/master/README_cn.md)


## :memo: About
HMDroidbot (HM stands for HarmonyOS, Droid stands for Android) is a lightweight test input generator for HarmonyOS (and Android). It forks from [Droidbot](https://github.com/honeynet/droidbot) and supports HarmonyOS NEXT devices.
It can send random or scripted input events to test an HarmonyOS app, achieve higher code coverage more quickly, and generate a UI transition graph (UTG) after testing.

## :smiling_face_with_three_hearts: Awesome Features 
:boom: Support coverage report for HarmonyOS now! Including ability, page, *etc.* and some HarmonyOS-specific metrics! See the sample report below!

![image](https://github.com/user-attachments/assets/1dfbb6f8-c9ab-48b2-8043-5474719a7466)

:boom: Support both Android and HarmonyOS NEXT devices. Use the flag `-is_harmonyos` to specify the target system.

:boom: Support configuring with YAML file. Easy to get start with.

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

       :one: *(Optional)* You can setup a virtual envirnment before installation. See [venv module](https://realpython.com/python-virtual-environments-a-primer/) for details.

       In macOS or Linux:
       ```shell
       python3 -m venv droidenv
       source droidenv/bin/activate
       ```

       In Windows:
       ```powershell
       python3 -m venv droidenv
       .\droidenv\Scripts\activate
       ```

        :two: The following `pip` command will automatic grep and install the required packages for you.
        
        ```shell
        git clone https://github.com/XixianLiang/HMDroidbot.git
        cd HMDroidbot
        pip install -e .
        ```
        
        :three: If successfully installed, you should be able to execute `droidbot -h`. (If failed to run `droidbot` cmd, try to use `python3 -m droidbot.start -h` instead).

2. **Quick Start (Only available in WSL now):**

    :wave: Simply run the `run_sample.sh` file we provided to download the sample hap and try HMDroidbot!
    ```bash
    bash run_sample.sh
    ```

3. **Setting up `config.yml`**
   
   Use the correct param based on your PC operating system.

    **(Required)** `env` is necessary to lanuch HMDroidbot
   ```bash
   # config.yml
   env: <windows, macOS or Linux>
   ```

    **(Optional)** You can configure other parameters in the `config.yml` file to run Droidbot more conveniently, avoiding the need to specify them via command-line arguments. See ***Run HMDroidbot by yml configuration*** below.


1. **Start HMDroidbot:**

    **:+1: (Recommended) Run HMDroidbot by configuring `config.yml` file. Here's an example `config.yml` configuration.**
    ```bash
    # env: the system of your PC (e.g. windows, macOS, Linux)
    env: macOS

    # system: the target harmonyOS
    system: harmonyOS

    device: 23E**********1843
    output_dir: output
    app_path: app/sample.hap
    count: 1000
    ```

    Then, simply run `droidbot` or `python -m droidbot.start` to start.

    **Run HMDroidbot by `python -m`**
    ```bash
    python3 -m droidbot.start -a <path_to_hap> -o output_dir -is_harmonyos
    ```
    
    **Run HMDroidbot by `droidbot`**
    ```bash
    droidbot -a <path_to_hap> -o output_dir -is_harmonyos
    ```
    
    That's it! You will find much useful information, including the UTG, generated in the output dir.

    + If you are using multiple devices, you may need to use `-t <device_serial>` to specify the target device. The easiest way to determine a device's serial number is calling `hdc list targets`.
    + You may find the `-debug` tag useful while you are trying to debug the source code.
    + Use `-log` flag to get the hilog in HarmonyOS, which can be found in the report directory.
    + You may find other useful features in `droidbot -h`.

    **Example Starting Scripts**
    ```bash
    # Start by droidbot cmd
    droidbot -a app/sample.hap -o output -t 23E**********1843 -count 1000 -is_harmonyos -debug

    # Start by running module. Easy to debug!
    # execute the following command in the HMDroidbot dir, which should include the setup.py.
    python -m droidbot.start -a app/sample.hap -o output -t 23E**********1843 -count 1000 -is_harmonyos -debug
    ```

    **vscode `launch.json` example**

   <img width="1134" alt="image" src="https://github.com/user-attachments/assets/bffde3f3-deea-41fb-9087-fb7eb3772bd5">

    
## Trouble shooting
We used WSL to develop this project. so the hdc tool we used in this project is actually `hdc.exe` by adding `/mnt/.../hdc.exe` on windows to the WSL PATH.

Due to HarmonyOS NEXT being in beta, the process of configuring the hdc environment is somewhat complex (especially on WSL). The overall idea for WSL configuration is to install the hdc tool on the host system and export the `hdc.exe` from the host system path through the WSL `mnt` path (since the phone is connected to the host system, this eliminates the need to configure USB port forwarding). If you encounter any issues while setting up the environment, please feel free to contact us.

## :mega: Info
Currently, HMDroidbot is maintained by [华东师范大学-移动软件分析与测试小组](https://mobile-app-analysis.github.io/). 

This project is led by [Xixian Liang](https://xixianliang.github.io/resume/) and [Mengli Ming](https://ml-ming.dev/). We are supervised by Prof. [Ting Su](https://tingsu.github.io/). Feel free to contact us if you have any questions or advices.

Join the QQ group (ID 904153331) to contact us and get the latest info.

<img width="284" alt="image" src="https://github.com/user-attachments/assets/c42c2bdf-6c3d-4774-a2a4-34adcc84cfe7">

## Acknowledgement

- [Droidbot](https://github.com/honeynet/droidbot)
- [awesome-hdc](https://github.com/codematrixer/awesome-hdc)
- The development of this project receives generous help and advice from the HUAWEI engineers.

## License

This project is based on the original MIT License (see `LICENSE` file) and includes my contributions, which are governed by [Xixian Liang](https://github.com/XixianLiang) (see `LICENSE_NEW` file).
