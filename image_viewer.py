import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tk_file
from PIL import Image, ImageTk
import os

# creating tkinter window 建立視窗
root = tk.Tk()
root.geometry('700x550')   # ('width x height') 以像素為單位
root.title('Tkinter Hub')  # 視窗標題


def popup_menu(e):
    '''
    在 ButtonPress event 的位置貼上選單 (點擊位置為選單左上角)
    :param e: ButtonPress event
    :return: None
    '''
    menu_btn1.tk_popup(x=e.x_root, y=e.y_root)
    # tk_popup 為 class Menu 的方法 --> Post the menu at position X,Y with entry ENTRY. return None
    print(type(e))  # <class 'tkinter.Event'>
    print(e)        # <ButtonPress event state=Mod1 num=1 x=17 y=14>

images_list = []
images_vars = []

def load_images():
    '''
    提供使用者選擇資料夾並載入裡面的圖片，顯示底部可點選的小圖片
    :return: None
    '''
    dir_path = tk_file.askdirectory()    # 提供使用者選擇一個資料夾，返回該路徑  -> return str

    # 取得路徑
    images_files = os.listdir(dir_path)  # os.listdir -> return list (包含指定路徑資料夾中所有文件和文件夾的清單)
    # print(images_files)                # ['螢幕擷取畫面 2023-07-15 214633.png', '螢幕擷取 ... 畫面 2023-07-20 230135.png']

    for r in range(0, len(images_files)):
        # 跳過不是 png 或 jpg 的檔案
        if '.png' not in images_files[r] and '.jpg' not in images_files[r] :
            print('忽略的檔案有:'+ images_files[r])
            continue

        # 開啟圖片
        img1 = Image.open(dir_path + '/' + images_files[r])

        # 設定大圖顯示的尺寸 size_ <class 'tuple'>
        size_x = int(img1.size[0] / img1.size[1] * 400)
        size_y = int(img1.size[1]/img1.size[0]*680)
        if size_y > 400:
            size_ = (size_x, 400)
        else:
            size_ = (680, size_y)

        # 將 [小圖物件, 大圖物件] 一個個加入images_list中
        images_list.append([
            ImageTk.PhotoImage(                   # 底部小圖的PhotoImage物件
                img1.resize((50, 50),             # 更改圖片尺寸--> 小圖尺寸
                                Image.LANCZOS)),
            ImageTk.PhotoImage(                   # 中間顯示大圖的PhotoImage物件
                img1.resize(size_,                # 更改圖片尺寸--> 大圖尺寸
                                 Image.LANCZOS))  # 改變大小時的 Filters --> 圖像調整大小方法resize() 採用一個resample參數，該參數告訴應使用哪個過濾器進行重新採樣。
        ])

        # images_vars.append(f'img_{r}')
        images_vars.append(images_files[r])       # 將檔名依序加入images_vars串列中

    # 建立底部小圖片按鈕
    for n in range(len(images_vars)):
        # 建立小圖案按鈕
        globals()[images_vars[n]] = tk.Button(slider, image=images_list[n][0], bd=0,    # 選擇小尺寸的圖案、邊框粗細為 0
                                              command=lambda n_=n: display_images(n_))  # 按鈕點擊時執行 lambda 函式
        '''
        解釋 lambda n_= n: display_images(n_)
        ---------------------------------
        def lambda (n_= n):              # lambda 函式有一個參數 n_，預設值為 for迴圈的 n 變數
            return display_images(n_)    # 函式為一級物件 可被回傳
        
        lambda()
        '''
        # globals()[images_vars[n]].pack(side=tk.LEFT)
        globals()[images_vars[n]].grid(row=0, column=n)   # grid格狀版面佈局 ( 同一列，欄位依序矲下去)
    canvas.update_idletasks()                             # 更新窗口顯示
    canvas.config(scrollregion=slider.bbox())             # 改變畫布配置 --> 滾動範圍為邊框範圍 (有新的圖案按鈕置入會變更範圍)
    # print(slider.bbox())                                # 列印 框架的範圍 (左上角x, y, 右下角x, y)

def display_images(index):
    '''
    更改中間 Label 配置，顯示圖片
    :param index: 要顯示的圖片在清單中的索引
    :return: None
    '''
    image_display_lb.config(image=images_list[index][1])        # 顯示大圖
    root.title(images_vars[index])  # 變更視窗標題為圖片檔名


# 創建左上角按鈕 ≡
menu_btn = tk.Button(root, text='≡', bd=0, font=('Bold', 15))   # <class 'tkinter.Button'> 建立Button物件( master: 按鈕的父容器。, text=顯示文字, bd=邊框粗細, font=字型設定)
menu_btn.pack(side=tk.TOP, anchor=tk.W, pady=20, padx=20)       # 加入視窗中
menu_btn.bind('<Button-1>', popup_menu)                         # 綁定, 事件為左鍵點擊, 執行在該位置顯示目錄

# 創建一個選單
menu_btn1 = tk.Menu(root, tearoff=False)                         # 建立主選單 (加入的視窗物件, tearoff=False 消除虛線)
menu_btn1.add_command(label='Open Folder', command=load_images)  # 主選單項目 (label:顯示文字, command:執行函式)
# add_command --> Add command menu item. 添加命令菜單項。

# 建立標籤放置在視窗中央 --> 此標籤是要顯示點選的大圖用的
image_display_lb = tk.Label(root)
image_display_lb.pack(anchor=tk.CENTER)

# 建立畫布 --> 放置底部圖片按鈕用的
canvas = tk.Canvas(root, height=60, width=700)
canvas.pack(side=tk.BOTTOM, fill=tk.X)                      # fill=tk.X 表示和放置的父元件(視窗)同寬

# 建立滾動條 --> 控制底部圖案按鈕的顯示
x_scroll_bar = ttk.Scrollbar(root, orient=tk.HORIZONTAL)    # orient=tk.HORIZONTAL 水平滾動
x_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X)                # fill=tk.X 表示和放置的父元件(視窗)同寬
x_scroll_bar.config(command=canvas.xview)                   # command 滾動條移動時調用 canvas.xview 根據內容向左或向右調整窗口中的視圖

canvas.config(xscrollcommand=x_scroll_bar.set)              # canvas 的捲動綁定 x_scroll_bar
# canvas.bind('<Configure>', lambda e: canvas.bbox('all'))  # <Configure> : canvas 發生變化時就會調用 lambda e

# 建立框架與窗口
slider = tk.Frame(canvas)
canvas.create_window((0, 0), window=slider, anchor=tk.NW)   # (0, 0) --> create_window左上角在canvas的位置
# 在底部的畫布上建立窗口 --> 窗口用於在畫布上擺放小部件


root.mainloop()   # 使用 mainloop() 將 root 放在主迴圈中一直執行，直到使用者關閉該視窗才會停止運作
