# This is the interface for hdc
import subprocess
import logging
import re
from .adapter import Adapter
import time
import os
import pathlib
try:
    from shlex import quote # Python 3
except ImportError:
    from pipes import quote # Python 2

# ! Use the correct SYSTEM variable according to your system
# SYSTEM = "Linux" 
SYSTEM = "windows"


if SYSTEM == "windows":
    HDC_EXEC = "hdc.exe"
elif SYSTEM == "Linux":
    HDC_EXEC = "hdc"


class HDCException(Exception):
    """
    Exception in HDC connection
    """
    pass


class HDC(Adapter):
    """
    interface of HDC
    """
    global HDC_EXEC
    # * HDC command for device info. See the doc below.
    # * https://github.com/codematrixer/awesome-hdc?tab=readme-ov-file#%E6%9F%A5%E7%9C%8B%E8%AE%BE%E5%A4%87%E4%BF%A1%E6%81%AF
    UP = 0
    DOWN = 1
    DOWN_AND_UP = 2
    MODEL_PROPERTY = "const.product.model"
    DEVICE_PROPERTY = "const.product.name"
    VERSION_OS_PROPERTY = "const.product.software.version"
    CPU_STRUCTER_PROPERTY = "const.product.cpu.abilist"
    # VERSION_SDK_PROPERTY = ''
    # VERSION_RELEASE_PROPERTY = ''

    def __init__(self, device=None):
        """
        initiate a HDC connection from serial no
        the serial no should be in output of `hdc devices`
        :param device: instance of Device
        :return:
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        if device is None:
            from droidbot.device import Device
            device = Device()
        self.device = device

        self.cmd_prefix = [HDC_EXEC, "-t", device.serial]

    
    def set_up(self):
        self.logger.info(f"[CONNECTION] Setting up Adapter hdc.")
        # make the temp path in output dir to store the dumped layout result
        temp_path = os.getcwd() + "/" + self.device.output_dir + "/temp"
        if os.path.exists(temp_path):
            import shutil
            shutil.rmtree(temp_path)
        os.mkdir(temp_path)

    def tear_down(self):
        pass
        # temp_path = os.getcwd() + "/" + self.device.output_dir + "/temp"
        # if os.path.exists(temp_path):
        #     import shutil
        #     shutil.rmtree(temp_path)


    def run_cmd(self, extra_args):
        """
        run a hdc command and return the output
        :return: output of hdc command
        @param extra_args: arguments to run in hdc
        """
        if isinstance(extra_args, str):
            extra_args = extra_args.split()
        if not isinstance(extra_args, list):
            msg = "invalid arguments: %s\nshould be list or str, %s given" % (extra_args, type(extra_args))
            self.logger.warning(msg)
            raise HDCException(msg)

        args = [HDC_EXEC]
        # args = [] + self.cmd_prefix    TODO 写到有设备号的时候用这一行
        args += extra_args

        self.logger.debug('Runing command:')
        self.logger.debug(" ".join([str(arg) for arg in args]))
        r = subprocess.check_output(args).strip()
        if not isinstance(r, str):
            r = r.decode()
        self.logger.debug('Return value:')
        self.logger.debug(r)
        return r


    def shell(self, extra_args):
        """
        run an `hdc shell` command
        @param extra_args:
        @return: output of hdc shell command
        """
        if isinstance(extra_args, str):
            extra_args = extra_args.split()
        if not isinstance(extra_args, list):
            msg = "invalid arguments: %s\nshould be list or str, %s given" % (extra_args, type(extra_args))
            self.logger.warning(msg)
            raise HDCException(msg)

        shell_extra_args = ['shell'] + [ quote(arg) for arg in extra_args ]
        return self.run_cmd(shell_extra_args)

    def check_connectivity(self):
        """
        check if hdc is connected
        :return: True for connected
        """
        #TODO not support this method
        r = self.run_cmd("list targets")
        return not r.startswith("[Empty]")

    def connect(self):
        """
        connect hdc
        """
        self.logger.debug("connected")

    def disconnect(self):
        """
        disconnect hdc
        """
        self.logger.info("[CONNECTION] %s is disconnected" % self.__class__.__name__)

    def get_property(self, property_name):
        """
        get the value of property
        @param property_name:
        @return:
        """
        return self.shell(["param", "get", property_name])

    def get_model_number(self):
        """
        Get device model number. e.g. SM-G935F
        """
        return self.get_property(HDC.MODEL_PROPERTY)

    def get_sdk_version(self):
        """
        Get version of SDK
        """
        raise NotImplementedError
        return int(self.get_property(HDC.VERSION_SDK_PROPERTY))
    
    def get_device_name(self):
        """
        Get the device Name
        """
        return self.get_property(HDC.DEVICE_PROPERTY)

    def get_release_version(self):
        """
        Get release version, e.g. 4.3, 6.0
        """
        raise NotImplementedError
        return self.get_property(HDC.VERSION_RELEASE_PROPERTY)

    def get_installed_apps(self):
        """
        Get the package names and apk paths of installed apps on the device
        :return: a dict, each key is a package name of an app and each value is the file path to the apk
        """
        app_lines = self.shell("bm dump -a").splitlines()
        installed_bundle = []
        for app_line in app_lines:
            installed_bundle.append(app_line.strip())
        return installed_bundle

    def get_display_density(self):
        display_info = self.get_display_info()
        if 'density' in display_info:
            return display_info['density']
        else:
            return -1.0

    def __transform_point_by_orientation(self, xy, orientation_orig, orientation_dest):
        (x, y) = xy
        if orientation_orig != orientation_dest:
            if orientation_dest == 1:
                _x = x
                x = self.get_display_info()['width'] - y
                y = _x
            elif orientation_dest == 3:
                _x = x
                x = y
                y = self.get_display_info()['height'] - _x
        return x, y

    def get_orientation(self):
        """
        ## ! Function not implemented
        #### TODO hdc rotate cmd not found 
        """
        import inspect
        self.logger.debug(f"function:get_orientation not implemented. Called by {inspect.stack()[1].function}")
        return 1

    def unlock(self):
        """
        Unlock the screen of the device
        """
        self.shell("uitest uiInput keyEvent Home")
        self.shell("uitest uiInput keyEvent Back")

    def press(self, key_code):
        """
        Press a key
        """
        self.shell("uitest uiInput keyEvent %s" % key_code)

    def touch(self, x, y, orientation=-1, event_type=DOWN_AND_UP):
        if orientation == -1:
            orientation = self.get_orientation()
        self.shell("uitest uiInput click %d %d" %
                   self.__transform_point_by_orientation((x, y), orientation, self.get_orientation()))

    def long_touch(self, x, y, duration=2000, orientation=-1):
        """
        Long touches at (x, y)
        """
        if orientation == -1:
            orientation = self.get_orientation()
        self.shell("uitest uiInput longClick %d %d" %
                   self.__transform_point_by_orientation((x, y), orientation, self.get_orientation()))

    def drag(self, start_xy, end_xy, duration, orientation=-1):
        """
        Sends drag event n PX (actually it's using C{input swipe} command.
        @param start_xy: starting point in pixel
        @param end_xy: ending point in pixel
        @param duration: duration of the event in ms
        @param orientation: the orientation (-1: undefined)
        """
        (x0, y0) = start_xy
        (x1, y1) = end_xy
        if orientation == -1:
            orientation = self.get_orientation()
        (x0, y0) = self.__transform_point_by_orientation((x0, y0), orientation, self.get_orientation())
        (x1, y1) = self.__transform_point_by_orientation((x1, y1), orientation, self.get_orientation())

        self.shell("uitest uiInput swipe %d %d %d %d %d" % (x0, y0, x1, y1, duration))
        
    def type(self, text):
        # hdc shell uitest uiInput inputText 100 100 hello
        if isinstance(text, str):
            escaped = text.replace("%s", "\\%s")
            encoded = escaped.replace(" ", "%s")
        else:
            encoded = str(text)
        # TODO find out which characters can be dangerous, and handle non-English characters
        self.shell("input text %s" % encoded)

    """
    The following function is especially for HarmonyOS NEXT
    """
    @staticmethod
    def __safe_dict_get(view_dict, key, default=None):
        value = view_dict[key] if key in view_dict else None
        return value if value is not None else default
    
    @staticmethod
    def get_relative_path(absolute_path:str) -> str:
        """
        return the relative path in win style
        """
        workspace = pathlib.Path(os.getcwd())

        if SYSTEM == "windows":
            relative_path = pathlib.PureWindowsPath(pathlib.Path(absolute_path).relative_to(workspace))
            return relative_path
        elif SYSTEM == "Linux":
            return pathlib.Path(absolute_path).relative_to(workspace)
    
    def dump_view(self)->str:
        """
        Using uitest to dumpLayout, and return the remote path of the layout file
        :Return: remote path
        """
        r = self.shell("uitest dumpLayout")
        remote_path = r.split(":")[-1]
        return remote_path

    def get_views(self, views_path):
        """
        bfs the view tree and turn it into the android style
        views list
        ### :param: view path
        """
        from collections import deque
        self.views = []


        with open(views_path, "r", encoding="utf-8") as f:
            import json
            self.views_raw = json.load(f)

        # process the root node
        self.views_raw["attributes"]["parent"] = -1

        # add it into a queue to bfs
        queue = deque([self.views_raw])
        temp_id = 0

        while queue:
            node:dict = queue.popleft()

            # process the node and add the hierachy info so that Droidbot can
            # recongnize while traversing
            node["attributes"]["temp_id"] = temp_id
            node["attributes"]["child_count"] = len(node["children"])
            node["attributes"]["children"] = list()

            # process the view, turn it into android style and add to view list
            self.views.append(self.get_adb_view(node["attributes"]))

            # bfs the tree
            for child in node["children"]:
                child["attributes"]["parent"] = temp_id
                if "bundleName" in node["attributes"]:
                    child["attributes"]["bundleName"] = HDC.__safe_dict_get(node["attributes"], "bundleName")
                    assert HDC.__safe_dict_get(node["attributes"], "pagePath") is not None, "pagePath not exist"
                    child["attributes"]["pagePath"] = HDC.__safe_dict_get(node["attributes"], "pagePath")
                queue.append(child)
            
            temp_id += 1
        
        # get the 'children' attributes
        self.get_view_children()

        return self.views
        
    def get_view_children(self):
        """
        get the 'children' attributes by the 'parent'
        """
        for view in self.views:
            temp_id = HDC.__safe_dict_get(view, "parent")
            if temp_id > -1:
                self.views[temp_id]["children"].append(view["temp_id"])
                assert self.views[temp_id]["temp_id"] == temp_id
    
    def get_adb_view(self, raw_view:dict):
        """
        process the view and turn it into the android style
        """
        view = dict()
        for key, value in raw_view.items():
            # adapt the attributes into adb form
            if key in ["visible", "checkable", "enabled", "clickable", \
                       "scrollable", "selected", "focused", "checked"]:
                view[key] = True if value in ["True", "true"] else False
                continue
            if key == "longClickable":
                view["long_clickable"] = bool(value)
                continue
            if key == "bounds":
                view[key] = self.get_bounds(value)
                view["size"] = self.get_size(value)
                continue
            if key == "bundleName":
                view["package"] = value
                continue
            if key == "description":
                view["content_description"] = value
                continue
            if key == "type":
                view["class"] = value
                continue
            if key == "key":
                view["resource_id"] = value
                continue
            view[key] = value
    
        return view
    
    def get_bounds(self, raw_bounds:str):
        # capturing the coordinate of the bounds and return 2-dimensional list
        # e.g.  "[10,20][30,40]" -->  [[10, 20], [30, 40]]
        import re
        size_pattern = r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]"
        match = re.search(size_pattern, raw_bounds)
        if match:
            return [[int(match.group(1)), int(match.group(2))], \
                    [int(match.group(3)), int(match.group(4))]]
    
    def get_size(self, raw_bounds:str):
        bounds = self.get_bounds(raw_bounds)
        return f"{bounds[1][0]-bounds[0][0]}*{bounds[1][1]-bounds[0][1]}"