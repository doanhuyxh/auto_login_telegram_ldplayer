import os
import time
import requests
import shutil
import libs.ld_script as ld
import libs.open_cv as cv
import libs.tesseract as tess
from termcolor import colored

def clear_all_pycache():
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
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

def CallOtp(phone):
    otp = None
    res = requests.get(f"http://192.168.105.249:5000/api/get_otp?phone_number={phone}")
    data = res.json()
    otp = data.get("data")
    return otp

def Click_Text(nameLD, text, time_check = 5):
    for i in range(time_check):
        image_path = GetScreenShot(nameLD)
        pos= tess.get_text_positions(text, image_path)
        if pos is not None:
            x,y = pos
            ld.click(nameLD, x, y)
            break
        else:
            print(colored(f"finding {text} : {i}", 'yellow'))
            time.sleep(2)
            if i == time_check-1:
                return False
    return True

def Click_Images(nameLd, template, timeCheck =5):
    for i in range(timeCheck):
        image_path = GetScreenShot(nameLd)
        pos= cv.find_template_in_image(template, image_path)
        if pos is not None:
            x,y = pos
            ld.click(nameLD, x, y)
            break
        else:
            print(colored(f"finding next icon : {i}", 'yellow'))
            time.sleep(2)
            if i == timeCheck-1:
                return False
    return True

def LogIn(nameLD, phoneNumber):
    
    # click bat dau
    check  = Click_Text(nameLD, "Start")
    if check == False:
        return False
    
    #click nut thong bao tiep tuc quyen calls
    Click_Text(nameLD, "Continue")        

    #click nut thong bao tiep tuc quyen quan ly goi thoai
    Click_Text(nameLD, "TUCHOI")
    
    # vao man hinh nhap so dien thoai
    # xoa ky tu neu co
    for _ in range(3):
        ld.pressKey(nameLD, "KEYCODE_DEL")
    
    ld.sendText(nameLD, phoneNumber)

    #Nhan tiep tuc
    check = Click_Images(nameLD, f"{os.path.dirname(os.path.abspath(__file__))}\\images\\next.png")
    
    time.sleep(2)
    ld.click(nameLD, 450, 418) # nut yes
    
    check = Click_Text(nameLD, "Continue")
    if check == False:
        return False
    
    
    check = Click_Text(nameLD, "TUCHOI")
    if check == False:
        return False
    
    check = Click_Text(nameLD, "TUCHOI")
    if check == False:
        return False
    
    print(colored("Cho doc otp", "blue"))
    otp = CallOtp(phoneNumber)
    #call otp
    ld.sendText(nameLD, otp) # Gui otp

    # cho nhap ma 2fa
    Click_Text(nameLD, "Verification")
    ld.sendText(nameLD, "Biproaz123...")
    Click_Images(nameLD, f"{os.path.dirname(os.path.abspath(__file__))}\\images\\next.png")
    check = Click_Images(nameLD, f"{os.path.dirname(os.path.abspath(__file__))}\\images\\icon_search_home_tele.png")
    return check


nameLD = "ld9"
ld.copyLD(nameLD, "goc")
ld.modLD(nameLD)
ld.runLD(nameLD)

for i in range(20):
    try:
        path = GetScreenShot(nameLD)
        pos= cv.find_template_in_image(f"{os.path.dirname(os.path.abspath(__file__))}\\images\\telegram.png", path)
        print(pos)
        if pos is None:
            print("dang cho man hinh chinh")
            time.sleep(2)
        else:
            break
    except Exception as ex:
        time.sleep(2)


ld.openApp(nameLD,"org.telegram.messenger")
check = LogIn(nameLD, "16098646010")

if check:
    print("Login thanh cong")
else:
    print("Login that bai")

