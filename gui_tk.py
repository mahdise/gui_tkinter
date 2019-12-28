
#input library

import tkinter as tk
# from PIL import ImageTk,Image
from tkinter.filedialog import askopenfilename
import pandas as pd
import numpy as np
from copy import deepcopy
import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
from decimal import Decimal
from _cffi_backend import callback
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import r2_score





##################################




# list for  Y_pred_prod, Y_pred_pack, Y_pred_prod_pack_list in second version


########### main frame ################################
main  = tk.Tk()
'''
main frame where all the function amd widget are situated
'''
################## height and width of the main frame ################
hei_m=1200
wi_m=2200
'''
main frame size in height and weight
'''
############################### canvas for background   #######################
canvas = tk.Canvas(main, height=hei_m,width=wi_m,bg="#ffffff")
canvas.pack()
'''
canvas on main frame for background color,icon and other image 
'''
# icon =Image.open('image_path')
# icon = ImageTk.PhotoImage(icon)
# icon_label=tk.Label(main, image=icon)
# icon_label.place(relx=0.76)

'''

icon as a image and lable where icon is establish

'''
rightupframe = tk.Frame(main,bg="#ffffff", bd=5)
rightupframe.place(relx=0, rely=0.10,relwidth=0.40,relheight=0.1)

leftupframe = tk.Frame(main,bg="#ffffff ", bd=5)
leftupframe.place(relx=.40, rely=0.13,relwidth=0.20,relheight=0.04)

'''
this frame is in the right upper side and for load and train, predict,retrain button.
'''

########################## browse func and button ########

  
def import_excel_data():
       
    excel_file_path = askopenfilename()
    
    loadData = pd.read_excel(excel_file_path)
    return loadData

'''
this function is for load the new csv and excel file 

'''

def pred_re():
    global proodValue, packageValue, proodName
    proodValue, packageValue, proodName= test_model(import_excel_data())
    proodValue = proodValue.T.to_dict(orient='list')
    packageValue = packageValue.T.to_dict(orient='list')
#    proodName = Y_pred_prod_pack_list.T.to_dict(orient='list')
    for key in proodName:
        listboxForPro.insert('end', key)
    return proodValue, packageValue, proodName
######## demo list #############

####### under construct #############################
frameProd = tk.Frame(main, bg='#ffffff', bd=5)
frameProd.place(rely=0.18,relwidth=.40,relheight=0.30)

LabelPN = tk.Label(frameProd,text = 'Product Name',bg='#ffffff')
LabelPN.place(relx=0.40,rely=0.01,relwidth=.20,relheight=0.10)

listboxForPro = tk.Listbox(frameProd,selectmode=tk.MULTIPLE)
listboxForPro.place(rely=0.15,relwidth=1,relheight=0.85)

#################### inside elements ###############


############################# checkbox #################


def callBackFunc():
    if(chkValue.get()):
        pkgLst()
        pkgvalue()
    else:
        pkgLst()
        prodvalue()

chkValue = tk.BooleanVar() 
chkValue.set(False)

checkProd=tk.Checkbutton(leftupframe, text="Products\Packeges", variable=chkValue,command=callBackFunc,bg='#ffffff')
checkProd.place(relwidth=0.40,relheight=1)

#######################################################
frame = tk.Frame(main, bg='#ffffff', bd=5)
frame.place(rely=0.50,relwidth=.40,relheight=0.50)
'''
frame for list of prediction package and package_listbox
'''
package_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE)
package_listbox.place(relwidth=1,relheight=1)

def selectOut(evt):
    callBackFunc()


########## get prod value and show in the canvas frame ##########
def prodvalue():
    selection = listboxForPro.curselection()
    for gridLevel in canvasFrame.grid_slaves():
        if int(gridLevel.grid_info()["row"]) >= 0:
            gridLevel.grid_forget()
    rowCount = 0
    for name , value in proodValue.items():
        for nameSe in selection:
            list_index= [list(proodValue.keys())[list_num] for list_num in selection  ]

            if name==listboxForPro.get(nameSe):
                tableEn = tk.Entry(canvasFrame, text="")
                tableEn.grid(row=rowCount, column=0, sticky="nsew")
                tableEn.insert(tk.END, '%s' % (name))
                for index, elements in enumerate(value):
                    tableEn = tk.Entry(canvasFrame, text="")
                    tableEn.grid(row=rowCount, column=(index+1), sticky="nsew")
                    tableEn.insert(tk.END, '%d.%d' % (elements ,(index+1)))
                rowCount+=1
    selected_plot(list_index ,proodValue)


###### pakage list  function ###########################
   
def pkgLst():
    package_listbox.delete(0,'end')
    selection = listboxForPro.curselection()
    for name , value in proodName.items():
 
        for nameSe in selection:
            if name==listboxForPro.get(nameSe):
                for index, elements in enumerate(value): 
                    package_listbox.insert('end', elements)

def pkgvalue():
    lst=package_listbox.get(0, tk.END)
    for gridLevel in canvasFrame.grid_slaves():
        if int(gridLevel.grid_info()["row"]) >= 0:
            gridLevel.grid_forget()


    rowCount = 0
    for name , value in packageValue.items():
        
        for  key, ele in enumerate(lst):
     
            if name==ele:
                
                tableEn = tk.Entry(canvasFrame, text="")
                tableEn.grid(row=rowCount, column=0, sticky="nsew")
                tableEn.insert(tk.END, '%s' % (name))
                for index, elements in enumerate(value):
                    tableEn = tk.Entry(canvasFrame, text="")
                    tableEn.grid(row=rowCount, column=(index+1), sticky="nsew")
                    tableEn.insert(tk.END, '%d.%d' % (elements ,(index+1)))
                rowCount+=1
                
    selected_plot(lst ,packageValue)
def DoNotClick(evt):
    print ('...............BackEndPrint...........')
listboxForPro.bind('<<ListboxSelect>>', selectOut)
package_listbox.bind('<<ListboxSelect>>', DoNotClick)
   

############################ output frame ###############################

output_frame = tk.Frame(main, bd=5,bg='#ffffff ')
output_frame.place(relx=0.4, rely=0.17,relwidth=0.58,relheight=0.75)


        
     
photoFrame = tk.Frame(output_frame,  bg="#ffffff",width=1050, height=200)
photoFrame.grid()
photoFrame.rowconfigure(0, weight=1) 
photoFrame.columnconfigure(0, weight=1) 
'''
photo frame for canvas
'''

photoCanvas = tk.Canvas(photoFrame, bg="#ffffff",width=1050, height=200)
photoCanvas.grid(row=0, column=0, sticky="nsew")

canvasFrame = tk.Frame(photoCanvas, bg="#ffffff",width=1050, height=200)
photoCanvas.create_window(0, 0, window=canvasFrame, anchor='nw')

def update_scrollregion(event):
    photoCanvas.configure(scrollregion=photoCanvas.bbox("all"))

photoScroll = tk.Scrollbar(photoFrame, orient=tk.HORIZONTAL)
photoScroll.config(command=photoCanvas.xview)

photoScrollx = tk.Scrollbar(photoFrame, orient=tk.VERTICAL)
photoScrollx.config(command=photoCanvas.yview)


   

photoScroll.grid(row=1, column=0, sticky="ew")
photoScrollx.grid(row=0, column=1, sticky="nsew")


photoCanvas.config(xscrollcommand=photoScroll.set)
photoCanvas.config(yscrollcommand=photoScrollx.set)

canvasFrame.bind("<Configure>", update_scrollregion) 

plotframe = tk.Frame(output_frame, bg="#ffffff")
plotframe.place( rely=0.30,relwidth=1,relheight=0.70)
   

 

def selected_plot ( col, df):
    
    new_df= pd.DataFrame (df, columns= col )
    figure1 = plt.Figure(figsize=(12,8), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, plotframe)
    bar1.get_tk_widget().place(relwidth=1,relheight=1)
    new_df.plot(kind='bar', legend=True, ax=ax1,fontsize=8)
    ax1.set_title('Weekly Product Sales', fontsize=8)
    ax1.set_ylabel('Order Quantity KG', fontsize=8)
    ax1.set_xlabel('Week',fontsize=8)
    ax1.set_ylim([0, int(max(new_df.max())+max(new_df.max())*0.2)])
    for p in ax1.patches:
        ax1.annotate('{:.2E}'.format(Decimal(str(p.get_height()))), (p.get_x(), p.get_height()+50),rotation=90)


'''
function for plot the predic value
'''


def tarinAga():
    listPrediction1 = retrain_model(import_excel_data())
    dicPridiction1 = listPrediction1.T.to_dict(orient='list')
    rowCount = 0 
    for key , value in dicPridiction1.items():
#            list_index= [list(dicPridiction1.keys())[list_num] for list_num in listPrediction1  ]

        

        tableEn = tk.Entry(canvasFrame, text="")
        tableEn.grid(row=rowCount, column=0, sticky="nsew")
        tableEn.insert(tk.END, '%s' % (key))
  
        for index, elements in enumerate(value):
        
            
            tableEn = tk.Entry(canvasFrame, text="")
            tableEn.grid(row=rowCount, column=(index+1), sticky="nsew")
            tableEn.insert(tk.END, '%d.%d' % (elements ,(index+1)))
            
        rowCount+=1
#    selected_plot( listPrediction1.columns,dicPridiction1 ) 
    
           



loadTrBtn=tk.Button(rightupframe, text='Load and Predict',command=pred_re)
loadTrBtn.place(relx=0.10,rely=0.10,relwidth=0.30, relheight=0.60)
   

###################################    finish #############
reTraBtn=tk.Button(rightupframe, text='Re-Train',command=tarinAga)
reTraBtn.place(relx=0.60,rely=0.10,relwidth=0.30, relheight=0.60)


   
main.mainloop()

 
    
    

    
###########################  plot ###################
#https://stackoverflow.com/questions/47152542/tkinter-canvas-scrollbar-with-grid
#https://stackoverflow.com/questions/9589867/python-tkinter-change-the-canvas-size-after-inital-declaration
#https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-checkbutton/
    


