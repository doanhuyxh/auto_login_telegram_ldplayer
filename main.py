import os
import time
import requests
import shutil
import libs.ld_script as ld
import libs.open_cv as cv
import libs.tesseract as tess
from termcolor import colored


def clear_all_pycache():
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_path = os.path.join(root, dir_name)
                print(f"Removing {pycache_path}")
                shutil.rmtree(pycache_path, ignore_errors=True)


clear_all_pycache()


def GetScreenShot(nameLD):
    ld.takeScreen(nameLD)
    ld.getScreen(nameLD)
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libs", "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return os.path.join(temp_dir, f"{nameLD}.png")


def ClearMultitasking(nameLD):
    ld.pressKey(nameLD, "KEYCODE_APP_SWITCH")
    for _ in range(5):
        ld.scroll(nameLD, 100, 100, 100, 800, 1000)
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "images", "xoa_tat_ca.png"
    )
    Click_Images(nameLD, template_path)


def CallOtp(phone):
    otp = None
    try:
        res = requests.get(f"http://192.168.105.249:5000/api/get_otp?phone_number={phone}")
        data = res.json()
        otp = data.get("data")
    except Exception as ex:
        print(colored(f"Can not get otp: {ex}", "red"))
    return otp


def Click_Text(nameLD, text, time_check=5):
    for i in range(time_check):
        try:
            image_path = GetScreenShot(nameLD)
            pos = tess.get_text_positions(text, image_path)
            if pos is not None:
                x, y = pos
                ld.click(nameLD, x, y)
                break
            else:
                print(colored(f"finding {text} : {i}", "yellow"))
                time.sleep(2)
                if i == time_check - 1:
                    return False
        except Exception as ex:
            print(colored(f"finding {text} : {i}", "yellow"))
            time.sleep(2)
            if i == time_check - 1:
                return False
    return True


def Click_Images(nameLd, template, timeCheck=5):
    for i in range(timeCheck):
        try:
            image_path = GetScreenShot(nameLd)
            pos = cv.find_template_in_image(template, image_path)
            if pos is not None:
                x, y = pos
                ld.click(nameLD, x, y)
                break
            else:
                print(colored(f"finding next icon : {i}", "yellow"))
                time.sleep(2)
                if i == timeCheck - 1:
                    return False
        except Exception as ex:
            print(colored(f"finding next icon : {i}", "yellow"))
            time.sleep(2)
            if i == timeCheck - 1:
                return False
    return True


def LogIn(nameLD, phoneNumber):
    # click bat dau
    check = Click_Text(nameLD, "Start")
    if check == False:
        return False

    # click nut thong bao tiep tuc quyen calls
    Click_Text(nameLD, "Continue")

    # click nut thong bao tiep tuc quyen quan ly goi thoai
    Click_Text(nameLD, "TUCHOI")

    # vao man hinh nhap so dien thoai
    # xoa ky tu neu co
    for _ in range(3):
        ld.pressKey(nameLD, "KEYCODE_DEL")

    ld.sendText(nameLD, phoneNumber)

    # Nhan tiep tuc
    check = Click_Images(
        nameLD, f"{os.path.dirname(os.path.abspath(__file__))}\\images\\next.png"
    )

    time.sleep(2)
    ld.click(nameLD, 450, 418)  # nut yes

    check = Click_Text(nameLD, "Continue")
    if check == False:
        return False

    check = Click_Text(nameLD, "TUCHOI")
    if check == False:
        return False

    check = Click_Text(nameLD, "TUCHOI")
    if check == False:
        return False

    # call otp
    print(colored("Cho doc otp", "blue"))
    otp = CallOtp(phoneNumber)
    ld.sendText(nameLD, otp)  # Gui otp

    # bị dính màn hình google
    check_email = tess.get_text_positions("Google", GetScreenShot(nameLD))
    if check_email is not None:
        with open("error.txt", "a") as f:
            f.write(f"{phoneNumber} -- Bị dính email\n")
        return False

    # cho nhap ma 2fa
    Click_Text(nameLD, "Verification")
    ld.sendText(nameLD, "Biproaz123...")
    Click_Images(
        nameLD, f"{os.path.dirname(os.path.abspath(__file__))}\\images\\next.png"
    )
    check = Click_Images(
        nameLD,
        f"{os.path.dirname(os.path.abspath(__file__))}\\images\\icon_search_home_tele.png",
    )
    return check


nameLD = "Telegram"


with open("phone_number.txt", "r") as f:
    phone_number = f.readlines()

    for phone in phone_number:
        ClearMultitasking(nameLD)
        ld.pressKey(nameLD, "KEYCODE_HOME")
        phone = phone.strip()
        print(f"Log in {phone}")
        Click_Text(nameLD, phone)
        check = LogIn(nameLD, phone)
        if check == False:
            print(f"Can not find {phone}")
            with open("error.txt", "a") as f:
                f.write(f"{phone}\n")
        
