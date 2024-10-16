import subprocess
import os
import json
import sys
from termcolor import colored
import cv2
import pytesseract
import string
import random



def delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")

def load_config():
    try:
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        print("Config file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error decoding JSON in config file.")
        sys.exit(1)

config = load_config()
LD_CONSOLE_PATH = config["AUTO"]["path_ldconsole"]
LD_WORKING_DIRECTORY = config["AUTO"]["path_ld"]

def execute_ldconsole_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return result.stderr.strip()
    except Exception as e:
        return str(e)
    

def runCMD_LD_SCREEN(command):
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)) + "\\temp")
        full_command = LD_CONSOLE_PATH + " " + command  # Thêm lệnh vào danh sách
        print(colored(full_command, "light_blue"))
        result = execute_ldconsole_command(full_command)
        return result
    except Exception as e:
        print(colored(f"An error occurred: {str(e)}", "red"))
    finally:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))


def runCMD_LD(command):
    try:
        os.chdir(LD_WORKING_DIRECTORY)
        full_command = LD_CONSOLE_PATH + " " + command  # Thêm lệnh vào danh sách
        print(colored(full_command, "light_blue"))
        result = execute_ldconsole_command(full_command)
        # print(result)
        return result
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))


def createLD(nameLD):
    runCMD_LD("add --name " + nameLD)


def copyLD(nameLD, from_ld):
    runCMD_LD("copy --name " + nameLD + f"  --from {from_ld}")


def modLD(nameLD):
    runCMD_LD("modify --name " + nameLD + " --resolution 540,960,240")


def removeLD(nameLD):
    runCMD_LD("remove --name " + nameLD)


def runLD(nameLd):
    runCMD_LD("launch --name " + nameLd)


def quitLD(nameLd):
    runCMD_LD("quit --name " + nameLd)


def quitAllLD():
    runCMD_LD("quitall")



def runADB(nameLD, command):
    lenh = "\"" + command + "\""
    runCMD_LD("adb --name " + nameLD + " --command " + lenh)


def click(nameLD, x, y):
    lenh = "\"" + "shell input tap " + str(x) + " " + str(y) + "\""
    runCMD_LD("adb --name " + nameLD + " --command " + lenh)


def sendText(nameLD, text):
    lenh = "\"" + "shell input text '" + text + "'" + "\""
    runCMD_LD("adb --name " + nameLD + " --command " + lenh)


def pressKey(nameLD, key):
    lenh = "\"" + "shell input keyevent " + key + "\""
    runCMD_LD("adb --name " + nameLD + " --command " + lenh)


def scroll(nameLD, x1, y1, x2, y2, time):
    lenh = "\"" + "shell input touchscreen swipe " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(
        y2) + " " + str(time) + "\""
    runCMD_LD("adb --name " + nameLD + " --command " + lenh)


def openApp(nameLD, package):
    runCMD_LD("runapp --name " + nameLD + " --packagename " + package)


def clearDataApp(nameLD, package):
    lenh = "\"" + "shell pm clear " + package + "\""
    runCMD_LD("adb --name " + nameLD + " --command " + lenh)


# Proxy
def removeProxy(nameLD):
    lenh = "\"" + "shell settings delete global http_proxy " + "\""
    runCMD_LD("adb --name " + nameLD + " --command " + lenh)


def setProxy(nameLD, proxy):
    lenh = "\"" + "shell settings put global http_proxy " + proxy + "\""
    runCMD_LD("adb --name " + nameLD + " --command " + lenh)


def reboot(nameLD):
    lenh = "\"" + "shell reboot" + "\""
    runCMD_LD("adb --name " + nameLD + " --command " + lenh)
# End Proxy


def installApp(nameLD, package):
    runCMD_LD("installapp --name " + nameLD + " --packagename " + package)


def uninstallApp(nameLD, package):
    runCMD_LD("uninstallapp  --name " + nameLD + " --packagename " + package)


def randomNameLD(length=9):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def takeScreen(nameLD):
    lenh = "\"" + "shell screencap -p /sdcard/" + nameLD + ".png" + "\""
    runCMD_LD("adb --name " + nameLD + " --command " + lenh)


def getScreen(nameLD):
    lenh = "\"" + "pull /sdcard/" + nameLD + ".png" + "\""
    runCMD_LD_SCREEN("adb --name " + nameLD + " --command " + lenh)


def getLDPlayerPID(nameLD):
    try:
        # Chạy lệnh list2 để lấy thông tin về tất cả các LDPlayer
        output = runCMD_LD("list2")
        # Tách các dòng trong output
        lines = output.splitlines()
        print(lines)
        # Duyệt qua từng dòng để tìm LDPlayer có tên nameLD
        for line in lines:
            if nameLD in line:
                print(line)
                # Tách thông tin từ mỗi dòng
                parts = line.split(',')
                if parts[1] == nameLD:
                    pid = parts[5]
                    return pid
        # Nếu không tìm thấy LDPlayer với tên nameLD
        print(f"Không tìm thấy LDPlayer với tên {nameLD}")
        return None
    except Exception as e:
        print(f"Lỗi lấy PID: {str(e)}")
        return None


def image_exists(image_path):
    return os.path.exists(image_path)


def checkTextImage(text, image_path):
    try:
        if image_exists(image_path):
            # Đọc ảnh
            image = cv2.imread(image_path)
            # Chuyển ảnh sang ảnh xám
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Sử dụng pytesseract để nhận dạng văn bản
            image_text = pytesseract.image_to_string(gray_image)
            # Kiểm tra xem chuỗi văn bản có xuất hiện trong ảnh hay không
            return text.lower() in image_text.lower()
        else:
            print("Không thấy ảnh Android")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
