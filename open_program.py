#匯入模組
#import python windows COM object module
import win32com.client as win32
#import python modules(匯入較容易執行命令的模組)
import subprocess
from subprocess import CREATE_NEW_CONSOLE
#匯入os:檔案操作、psutil:記憶體資料和暫存 等模組
import os
import psutil
import datetime
import string
#import global varibles for value pass through(匯入廣域參數)
import open_data as opd

#catia 環境名稱
class set_CATIA_workbench_env:
    def __init__(self):
        # self.catapp = win32.Dispatch("CATIA.Application")
        self.env_name = {'Part_Design': 'PrtCfg', 'Product_Assembly': 'Assembly',
                'Generative_Sheetmetal_Design': 'SmdNewDesignWorkbench', 'Drafting': 'Drw'}
        self.catapp = win32.Dispatch("CATIA.Application")
    # 開啟Part_design方式
    def Part_Design(self):
        self.catapp.Visible = True
        self.catapp.StartWorkbench(self.env_name[self.Part_Design.__name__])
        try:
            temp = self.catapp.ActiveDocument
            temp.close()
        except:
            pass
        return

#開啟檔案
def file_open(target,dir):
    #連結CATIA
    catapp = win32.Dispatch("CATIA.Application")
    document = catapp.Documents
    #將路徑設為目錄的文字宣告
    directory = str(dir)
    #directory = '\\'.join(directory.split('/'))
    print(directory)
    #gvar.folderdir = directory
    #定義零件檔檔名
    part_dir = directory+target+'.CATPart'
    print(part_dir)
    #partdoc = document.Open("%s%s.%s" % (directory,target,"CATPart"))
    #開啟該零件檔
    partdoc = document.Open(part_dir)
    return target+'.CATPart'

#建立長方體(長寬高有因方向而改變)
def Sideplate_param_change(target,value):
    catapp = win32.Dispatch("CATIA.Application")
    partdoc = catapp.ActiveDocument
    part = partdoc.Part
    parameter = part.Parameters
    #按照介面輸入的參數找出相對應的面建出板子
    length = parameter.Item(target)
    if target == "width":
        length.Value = value
    elif target == "depth":
        length.Value = value
    elif target == "height":
        length.Value = value
    part.Update()
