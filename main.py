# 人機介面
# 匯入各個模組
# 匯入tk模組
import tkinter as tk
from tkinter import messagebox
# 匯入其他主程式
import open_program as oppr
# 匯入廣域參數
import open_data as opd
# os:檔案操作、匯入較容易執行命令的模組
import os, subprocess
from subprocess import CREATE_NEW_CONSOLE
import re
import psutil
#建立所需資料的空串列
data =[]
#建立系統操作介面
class Main_Frame:
    def __init__(self, master):
        # FRAME Settings(宣告此表單；最上方標題列文字；背景顏色；位置)
        self.master = master
        self.master.title('練習使用人機介面')
        self.master.configure(background='white')
        self.master.grid_columnconfigure(1, weight=0)
        # 確認是否已有現成資料，若有則保留，無則空白
        try:
            self.entryvar1 =tk.StringVar()
            self.entryvar1.set(data[0])
            self.entryvar2 = tk.StringVar()
            self.entryvar2.set(data[1])
            self.entryvar3 = tk.StringVar()
            self.entryvar3.set(data[2])
        except:
            self.entryvar1 = tk.StringVar()
            self.entryvar2 = tk.StringVar()
            self.entryvar3 = tk.StringVar()

        # ELEMENT Settings(標題設定：所在視窗,文字內容,字型及字體大小,位置)
        self.text1 = tk.Label(self.master,
                              text='金屬中心地獄\nWelcome to our hell.',font=("Arial", 16),
                              anchor='center').grid(row=0, column=0, columnspan=5, padx=5,sticky='we')
        self.text2 = tk.Label(self.master, text='1. 寬(Width): Set Value', font=("Arial", 12)
                                    ,anchor='w').grid(row=1, column=0, columnspan=5, sticky='w')
        self.text2a = tk.Label(self.master, text='2. 高(Height): Set Value', font=("Arial", 12),
                              anchor='w').grid(row=3, column=0, columnspan=5, sticky='w')
        self.text2b = tk.Label(self.master, text='3. 深(Depth): Set Value', font=("Arial", 12),
                               anchor='w').grid(row=5, column=0, columnspan=5, sticky='w')
        self.entry1 = tk.Entry(self.master, textvariable=self.entryvar1)  # ,state='readonly')
        self.entry1.grid(row=2, column=0, padx=20, pady=20)
        self.entry2 = tk.Entry(self.master, textvariable=self.entryvar2)  # ,state='readonly')
        self.entry2.grid(row=4, column=0, padx=20, pady=20)
        self.entry3 = tk.Entry(self.master, textvariable=self.entryvar3)  # ,state='readonly')
        self.entry3.grid(row=6, column=0, padx=20, pady=20)
        self.button1 = tk.Button(self.master, text='執行\nrun', width=9,
                                 command=self.start_data).grid(row=6, column=4, padx=5)
        self.button3 = tk.Button(self.master, text='匯入參數\nSet Value',
                                 command=self.confirm_data).grid(row=4, column=4, padx=5)
        self.text3 = tk.Label(self.master, text = '線段相距距離為： ').grid(row=8, column=0,sticky='w')

    #生成子程式
    def start_data(self):
         print(data)
         if data == [] :
             tk.messagebox.showwarning('Warning', 'no data input.', parent=self.master)
             return
         if data[-1] != False:
             # Box Generation(將輸入的參數放置廣域參數中)
             opd.width = data[0]
             opd.height = data[1]
             opd.depth = data[2]

             # 宣告檔名
             folderdir = opd.system_root + opd.mother_part

             #參數可以輸入小數點
             opd.width = float(data[0])
             opd.height = float(data[1])
             opd.depth = float(data[2])
             # 建立catia環境、寬and長and深設定
             from open_program import set_CATIA_workbench_env
             env = set_CATIA_workbench_env()
             env.Part_Design()
             oppr.file_open(opd.rectangle,folderdir)
             oppr.Sideplate_param_change("height",opd.height)
             oppr.Sideplate_param_change("width", opd.width)
             oppr.Sideplate_param_change("depth", opd.depth)


    # 設定參數，將輸入的參數放至主程式串列
    def confirm_data(self):
        try:
            #確定是否有輸入數值進入方框中
            for item in range(0,len(data)):
                del data[-1]
            if self.entryvar1.get == '' or self.entryvar2.get() == '' or self.entryvar3.get() == '':
                    raise ValueError('No Input')
                    # 利用判斷式確定數值的大小
            if float(self.entryvar1.get())<=0 or float(self.entryvar2.get()) <=0 or float(self.entryvar3.get()) <=0:
                    raise ValueError('數值太小')
            if float(self.entryvar1.get()) > float(self.entryvar2.get()):
                self.text4 = tk.Label(self.master, text='寬比高長').grid(row=8, column=4, padx=5)
            elif float(self.entryvar1.get()) == float(self.entryvar2.get()):
                self.text4 = tk.Label(self.master, text='寬等於高').grid(row=8, column=4, padx=5)
            elif float(self.entryvar1.get()) < float(self.entryvar2.get()):
                self.text4 = tk.Label(self.master, text='寬比高短').grid(row=8, column=4, padx=5)
            try:
                param = [self.entryvar1.get(), self.entryvar2.get(), self.entryvar3.get()]
            except AttributeError:
                param = ['self.entryvars1.get()', 'self.entryvars2.get()', 'self.entryvars3.get()']
            for i in range(0, len(param)):
                data.append(param[i])
            else:
                data.append(True)
                print(data)
                temp = data.copy()
                messagebox.showinfo("rectangle value",'長方體參數為：\n高：{}mm\n寬：{}mm\n深：{}mm'.format(*temp))
                opd.data = data.copy()
        #顯示錯誤：沒有輸入
        except ValueError:
            tk.messagebox.showerror('WARNING', 'no Input!!', parent=self.master)

# 讓程式執行這個主程式，不執行其他瑣碎程式
def main():
    root = tk.Tk()
    app = Main_Frame(root)
    root.resizable(0, 0)
    root.mainloop()

if __name__ == '__main__':
    main()

