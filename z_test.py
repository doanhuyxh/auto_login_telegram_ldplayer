import os
import time
import libs.ld_script as ld
import libs.open_cv as cv
import libs.tesseract as tess

nameLD= "Telegram"
#ld.pressKey(nameLD, "KEYCODE_APP_SWITCH")
#ld.pressKey(nameLD, "KEYCODE_HOME")
# ld.copyLD(nameLD, "goc")
# ld.modLD(nameLD)

# ld.runLD(nameLD)

#ld.openApp(nameLD, "org.telegram.messenger")

ld.takeScreen(nameLD)
ld.getScreen(nameLD)
image_path = os.path.dirname(os.path.abspath(__file__))+"\\libs\\temp\\"+nameLD+".png"
print(tess.ocr_image("./temp/"+nameLD+".png"))
pos = tess.get_text_positions("Google", "./temp/"+nameLD+".png")
print(pos)
# x,y = pos
# ld.click(nameLD, x,y)

#ld.pressKey(nameLD, "KEYCODE_DEL")

#ld.sendText(nameLD, "84523395871")



template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "xoa_tat_ca.png")
print(f"{template_path}")

pos= cv.find_template_in_image(f"{template_path}", image_path)
print(pos)

#ld.pressKey(nameLD, "KEYCODE_ENTER")