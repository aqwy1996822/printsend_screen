import win32api, win32con, win32gui
import time
from PIL import ImageGrab
from send_email import Email
from getpass import getuser
import argparse
from datetime import datetime
from ctypes import windll, wintypes, byref, sizeof
from socket import gethostname
user32 = windll.user32
user32.SetProcessDPIAware()

def get_window_rect(hwnd):
    try:
        f = windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(wintypes.HWND(hwnd),
          wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          byref(rect),
          sizeof(rect)
          )
        return rect.left, rect.top, rect.right, rect.bottom

def clock_at_night(timehour,night_start,night_end):
    if night_start>night_end:
        if timehour>night_start or timehour<night_end:
            return True
        else:
            return False
    else:
        if timehour>night_start and timehour<night_end:
            return True
        else:
            return False
def get_window_pos(name):
    handle = win32gui.FindWindow(0, name)
    #获取窗口句柄
    if handle == 0:
        return None
    else:
        win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
        win32gui.SetForegroundWindow(handle)
        time.sleep(2)
        #返回坐标值和handle
        x1, y1, x2, y2=get_window_rect(handle)
        # x1 = int(x1 * 1.25)+9
        # y1 = int(y1 * 1.25)+9
        # x2 = int(x2 * 1.25)-9
        # y2 = int(y2 * 1.25)-9
        img_ready = ImageGrab.grab((x1, y1, x2, y2))
        win32gui.ShowWindow(handle, win32con.SW_MINIMIZE)
        return img_ready
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=float, default=30, help='time_step to print and send screen')
    parser.add_argument('-ns', type=int, default=1, help='night start clock')
    parser.add_argument('-ne', type=int, default=9, help='night end clock')
    args = parser.parse_args()

    hostname =gethostname()
    user_name = getuser()
    email_sender=Email()
    time_step_min=args.t
    night_start=args.ns
    night_end = args.ne
    program_name='Anaconda Powershell Prompt (anaconda3)'
    fujian_path="C:/Users/"+user_name+"/"+program_name + ".png"
    old_mousepos=win32api.GetCursorPos()
    while True:
        mousepos=win32api.GetCursorPos()
        print("鼠标指针位置",mousepos)
        timehour = int(datetime.now().hour)
        if not clock_at_night(timehour,night_start,night_end):
            if mousepos[0]==old_mousepos[0] and mousepos[1]==old_mousepos[1]:
                img_ready = get_window_pos(program_name)
                if not img_ready==None:
                    img_ready.save(fujian_path)
                    email_sender.send(["电脑名:"+hostname,"用户名:"+user_name,"程序名"+program_name],[fujian_path])
                else:
                    print(program_name,"未找到")
            else:
                print(time_step_min,"分钟内有鼠标移动，不干扰操作")
                email_sender.send(
                    ["电脑名:" + hostname,
                     "用户名:" + user_name, "正在使用，请勿打扰"], [])
            old_mousepos = mousepos
            print("等待", time_step_min, '分钟后再次尝试推送')
        else:
            print("现在"+str(timehour)+"点 是暂停推送的夜间时段:",str(night_start)+':00-'+str(night_end)+":00 区间")
        time.sleep(60 * time_step_min)

