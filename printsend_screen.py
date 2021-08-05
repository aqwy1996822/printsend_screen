import win32api, win32con, win32gui
import time
from PIL import ImageGrab
from send_email import Email
import getpass
import argparse
def get_window_pos(name):
    handle = win32gui.FindWindow(0, name)
    #获取窗口句柄
    if handle == 0:
        return None
    else:
        win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        win32gui.SetForegroundWindow(handle)
        time.sleep(1)
        #返回坐标值和handle
        x1, y1, x2, y2=win32gui.GetWindowRect(handle)
        x1 = int(x1 * 1.25)+9
        y1 = int(y1 * 1.25)+9
        x2 = int(x2 * 1.25)-9
        y2 = int(y2 * 1.25)-9
        img_ready = ImageGrab.grab((x1, y1, x2, y2))
        win32gui.ShowWindow(handle, win32con.SW_MINIMIZE)
        return img_ready
if __name__=="__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=float, default=30, help='time_step to print and send screen')
    args = parser.parse_args()

    user_name = getpass.getuser()
    email_sender=Email()
    time_step_min=args.t
    program_name='Anaconda Powershell Prompt (anaconda3)'
    fujian_path="C:/Users/"+user_name+"/"+program_name + ".jpg"
    old_mousepos=(0,0)
    while True:
        mousepos=win32api.GetCursorPos()
        print(mousepos)
        if mousepos[0]==old_mousepos[0] and mousepos[1]==old_mousepos[1]:
            img_ready = get_window_pos(program_name)
            if not img_ready==None:
                img_ready.save(fujian_path)
                email_sender.send("画面来源\t"+user_name+"\t"+program_name,[fujian_path])
            else:
                print(program_name,"未找到")
        else:
            print(time_step_min,"分钟内有鼠标移动，不干扰操作")
        old_mousepos = mousepos
        time.sleep(60*time_step_min)
