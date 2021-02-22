import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox 
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize
from scipy.interpolate import interp1d
from gekko import GEKKO

def main():
    raiz = tk.Tk()
    gui = Window(raiz)
    gui.raiz.mainloop()
    return None

class Window:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.resizable(1,1)
        self.raiz.title("APM  Binary Distillation Column:Cyclohexane & n-heptane")
        self.raiz.geometry('600x750+700+0')


##   =====================================           VARIABLES          ===============================

        # -------------------------------    DATAS    ----------------------------------------
        self.Feed_copy = DoubleVar(value=1.00); self.X_Feed_copy = DoubleVar(value=0.5); self.Fr_DF_copy = DoubleVar(value=0.5)
        self.vol_copy = DoubleVar(value=1.6); self.acond_copy = DoubleVar(value=0.5); self.atray_copy = DoubleVar(value=0.25);
        self.areb_copy = DoubleVar(value=1.0)

        # -------------------------------         MODELING PROCESS          -------------------------------
        self.Stp1_copy = DoubleVar(value=1.0); self.Stp2_copy = DoubleVar(value=5.0);self.Stp3_copy = DoubleVar(value=3.0)
        self.Kp_copy = DoubleVar();self.Tp_copy = DoubleVar();self.Lp_copy = DoubleVar();

        self.SP1_copy=DoubleVar(value=0.97); self.Deltha_X_Feed_copy=DoubleVar(value=0.42);
        self.Kc_copy = DoubleVar();self.Ti_copy = DoubleVar();self.Td_copy = DoubleVar();

        # ------------------------------       STEADY STATE VALUES      -----------------------
        self.rr_ss_copy = DoubleVar(value=3.0);
        self.x_ss0=DoubleVar(value=0.935)
        self.x_ss1=DoubleVar(value=0.900)
        self.x_ss2=DoubleVar(value=0.862)
        self.x_ss3=DoubleVar(value=0.821)
        self.x_ss4=DoubleVar(value=0.779)
        self.x_ss5=DoubleVar(value=0.738)
        self.x_ss6=DoubleVar(value=0.698)
        self.x_ss7=DoubleVar(value=0.661)
        self.x_ss8=DoubleVar(value=0.628)
        self.x_ss9=DoubleVar(value=0.599)
        self.x_ss10=DoubleVar(value=0.574)
        self.x_ss11=DoubleVar(value=0.553)
        self.x_ss12=DoubleVar(value=0.535)
        self.x_ss13=DoubleVar(value=0.521)
        self.x_ss14=DoubleVar(value=0.510)
        self.x_ss15=DoubleVar(value=0.501)
        self.x_ss16=DoubleVar(value=0.494)
        self.x_ss17=DoubleVar(value=0.485)
        self.x_ss18=DoubleVar(value=0.474)
        self.x_ss19=DoubleVar(value=0.459)
        self.x_ss20=DoubleVar(value=0.441)
        self.x_ss21=DoubleVar(value=0.419)
        self.x_ss22=DoubleVar(value=0.392)      
        self.x_ss23=DoubleVar(value=0.360)
        self.x_ss24=DoubleVar(value=0.324)
        self.x_ss25=DoubleVar(value=0.284)
        self.x_ss26=DoubleVar(value=0.243)
        self.x_ss27=DoubleVar(value=0.201)
        self.x_ss28=DoubleVar(value=0.161)
        self.x_ss29=DoubleVar(value=0.125)    
        self.x_ss30=DoubleVar(value=0.092)
        self.x_ss31=DoubleVar(value=0.064)

##  ========================================        GUI        ============================================

        Column0=Label(self.raiz, width=3);Column0.grid(row=0,column=0,rowspan=18)
        Column7=Label(self.raiz, width=10);Column7.grid(row=0,column=9,rowspan=18)


        labComp=Label(self.raiz, text="-----   DATAS  -------", borderwidth=2, relief="groove",font= 'arial 11 bold',width=20);
        labComp.grid(row=2,column=1,columnspan=3,sticky="sewn",padx=0,pady=10)

        Fe=ttk.Entry(self.raiz,textvariable=self.Feed_copy, validate="focusout", validatecommand=self.kk, width=10);Fe.grid(row=3,column=2,padx=0,pady=2); Fe.config(justify="left") #Comp1.insert(10,20.8)
        lblFe=ttk.Label(self.raiz, text="Feed ="); lblFe.grid(row=3,column=1,sticky="e",padx=0,pady=2)
        lblFe_d=ttk.Label(self.raiz, text="Feed Flowrate (mol/min)"); lblFe_d.grid(row=3,column=3,sticky="w",padx=0,pady=2)

        Xhx_Fe=ttk.Entry(self.raiz,textvariable=self.X_Feed_copy, validate="focusout", validatecommand=self.kk, width=10);Xhx_Fe.grid(row=4,column=2,padx=0,pady=2); Xhx_Fe.config(justify="left")#; #Comp2.insert(10,0.0)
        lblXhx_Fe=ttk.Label(self.raiz, text="x_Feed="); lblXhx_Fe.grid(row=4,column=1,sticky="e",padx=0,pady=2)
        lblXhx_Fe=ttk.Label(self.raiz, text="Mole Fraction of Feed"); lblXhx_Fe.grid(row=4,column=3,sticky="w",padx=0,pady=2)

        Fr_DF=ttk.Entry(self.raiz,textvariable=self.Fr_DF_copy, validate="focusout", validatecommand=self.kk, width=10);Fr_DF.grid(row=5,column=2,padx=0,pady=2); Fr_DF.config(justify="left")#; #Comp3.insert(10, 0.0)
        lblFr_DF=ttk.Label(self.raiz, text="Fr_DF="); lblFr_DF.grid(row=5, column=1, sticky="e", padx=0, pady=2)
        lblFr_DF_d=ttk.Label(self.raiz, text="Fr_DF= D/Feed (D=Distillate)"); lblFr_DF_d.grid(row=5, column=3, sticky="w", padx=0, pady=2)

        voltd=ttk.Entry(self.raiz,textvariable=self.vol_copy, validate="focusout", validatecommand=self.kk, width=10);voltd.grid(row=6,column=2,padx=0,pady=2); voltd.config(justify="left")#; #Comp3.insert(10, 0.0)
        lblvoltd=ttk.Label(self.raiz, text="vol="); lblvoltd.grid(row=6, column=1, sticky="e", padx=0, pady=2)
        lblvoltd_d=ttk.Label(self.raiz, text="Relative Volatility = (yA/xA)/(yB/xB) = KA/KB = alpha(A,B)"); lblvoltd_d.grid(row=6, column=3, sticky="w", padx=0, pady=2)

        Mt_C=ttk.Entry(self.raiz,textvariable=self.acond_copy, validate="focusout", validatecommand=self.kk, width=10);Mt_C.grid(row=7,column=2,padx=0,pady=2); Mt_C.config(justify="left")#; Comp4.insert(10,0.0)
        lblMt_C=ttk.Label(self.raiz,text="Mt_C(mol)="); lblMt_C.grid(row=7,column=1,sticky="e",padx=0,pady=2)
        lblMt_C_d=ttk.Label(self.raiz, text="Total Molar Holdup in the Condenser"); lblMt_C_d.grid(row=7, column=3, sticky="w", padx=0, pady=2)

        Mt_B=ttk.Entry(self.raiz,textvariable=self.atray_copy, validate="focusout", validatecommand=self.kk, width=10);Mt_B.grid(row=8,column=2,padx=0,pady=2); Mt_B.config(justify="left")#; Comp5.insert(10,0.0)
        lblMt_B=Label(self.raiz, text="Mt_B(mol)="); lblMt_B.grid(row=8,column=1,sticky="e",padx=0,pady=2)
        lblMt_B_d=ttk.Label(self.raiz, text="Total Molar Holdup on each Tray"); lblMt_B_d.grid(row=8, column=3, sticky="w", padx=0, pady=2)

        Mt_R=ttk.Entry(self.raiz,textvariable=self.areb_copy, validate="focusout", validatecommand=self.kk, width=10);Mt_R.grid(row=9,column=2,padx=0,pady=2); Mt_R.config(justify="left")#; ko.insert(10,0.0)
        lblMt_R=ttk.Label(self.raiz, text="Mt_Rb(mol)="); lblMt_R.grid(row=9,column=1,sticky="e",padx=0,pady=2)
        lblMt_R_d=ttk.Label(self.raiz, text="Total Molar Holdup in the Reboiler"); lblMt_R_d.grid(row=9, column=3, sticky="w", padx=0, pady=2)



        lbStdyStt=Label(self.raiz,text="-- Steady State --", borderwidth=2, relief="groove",font= 'arial 10 bold',width=20)
        lbStdyStt.grid(row=10,column=1,columnspan=3,sticky="sewn",padx=0,pady=15)

        btInitMFraction = tk.Button(self.raiz, text="SS Initial Molar Fraction",command = self.openWin2,font= 'arial 10 bold',foreground = "green")
        btInitMFraction.grid(row=11, column=2,columnspan=3,sticky="w",padx=0,pady=0);#btTunePID.config(justify="center", foreground="green")

        RR_0=ttk.Entry(self.raiz,textvariable=self.rr_ss_copy, validate="focusout", validatecommand=self.kk, width=10);RR_0.grid(row=12,column=2,padx=0,pady=2); RR_0.config(justify="left") #Comp0.insert(10,15.5)
        lblRR_0=ttk.Label(self.raiz, text="RRss="); lblRR_0.grid(row=12,column=1,sticky="e",padx=0,pady=2)
        labRR_0_d=ttk.Label(self.raiz, text="Seady State Reflux Ratio (L/D)_ss"); labRR_0_d.grid(row=12,column=3,sticky="w",padx=0,pady=2)

        Stp1=ttk.Entry(self.raiz,textvariable=self.Stp1_copy, validate="focusout", validatecommand=self.kk, width=10);Stp1.grid(row=13,column=2,padx=0,pady=2); Stp1.config(justify="left")#; Comp8.insert(10,0.0)
        lblStp1=ttk.Label(self.raiz, text="Step1(1:10]="); lblStp1.grid(row=13,column=1,sticky="e",padx=0,pady=2)
        lblStp1_d=ttk.Label(self.raiz, text="Step N°1 in RR"); lblStp1_d.grid(row=13, column=3, sticky="w", padx=0, pady=2)

        Stp2=ttk.Entry(self.raiz,textvariable=self.Stp2_copy, validate="focusout", validatecommand=self.kk, width=10);Stp2.grid(row=14,column=2,padx=0,pady=2); Stp2.config(justify="left")#; Comp8.insert(10,0.0)
        lblStp2=ttk.Label(self.raiz, text="Step2 [10:19]="); lblStp2.grid(row=14,column=1,sticky="e",padx=0,pady=2)
        lblStp2_d=ttk.Label(self.raiz, text="Step N°2 in RR"); lblStp2_d.grid(row=14, column=3, sticky="w", padx=0, pady=2)

        Stp3=ttk.Entry(self.raiz,textvariable=self.Stp3_copy, validate="focusout", validatecommand=self.kk, width=10);Stp3.grid(row=15,column=2,padx=0,pady=2); Stp3.config(justify="left")#; Comp8.insert(10,0.0)
        lblStp3=ttk.Label(self.raiz, text="Step3 [19:]="); lblStp3.grid(row=15,column=1,sticky="e",padx=0,pady=2)
        lblStp3_d=ttk.Label(self.raiz, text="Step N°3 in RR"); lblStp3_d.grid(row=15, column=3, sticky="w", padx=0, pady=2)

        btDoubleTest = ttk.Button(self.raiz, text="Double Test",command = self.graphStep)
        btDoubleTest.grid(row=16, column=0,sticky="w",padx=5,pady=5)

        btModeling = ttk.Button(self.raiz, text="Modeling",command = self.graphModel)
        btModeling.grid(row=16, column=1,sticky="w",padx=5,pady=5)


        lblKp=ttk.Label(self.raiz, text="Kp="); lblKp.grid(row=17,column=0,sticky="w",padx=0,pady=2); lblKp.config(justify="left")
        lblKp_Value=Label(self.raiz,textvariable=self.Kp_copy, borderwidth=2, relief="sunken", width=9, fg="green");
        lblKp_Value.grid(row=17, column=0, pady=2, padx=0, sticky='e'); lblKp_Value.config(justify="right")
        lblKp_d=ttk.Label(self.raiz, text="Gain Process"); lblKp_d.grid(row=17, column=1, sticky="w", padx=0, pady=2)

        lblTp_Value=Label(self.raiz,textvariable=self.Tp_copy, borderwidth=2, relief="sunken", width=9, fg="green");
        lblTp_Value.grid(row=18, column=0, pady=2, padx=0, sticky='e'); lblTp_Value.config(justify="left")
        lblTp=ttk.Label(self.raiz, text="Tp="); lblTp.grid(row=18,column=0,sticky="w",padx=0,pady=2)
        lblTp_d=ttk.Label(self.raiz, text="time constant"); lblTp_d.grid(row=18, column=1, sticky="w", padx=0, pady=2)

        lblLp_Value=Label(self.raiz,textvariable=self.Lp_copy, borderwidth=2, relief="sunken", width=9, fg="green");
        lblLp_Value.grid(row=19, column=0, pady=2, padx=0, sticky='e'); lblLp_Value.config(justify="left")
        lblLp=ttk.Label(self.raiz, text="Lp="); lblLp.grid(row=19,column=0,sticky="w",padx=0,pady=2)
        lblLp_d=ttk.Label(self.raiz, text="Lag Time"); lblLp_d.grid(row=19, column=1, sticky="w", padx=0, pady=2)



        btTunePID = ttk.Button(self.raiz, text="Tunning PID",command = self.TunePID)
        btTunePID.grid(row=16,columnspan=2, column=2,sticky="we",padx=5,pady=5);#btTunePID.config(justify="center", foreground="green")

        lblSP1=ttk.Label(self.raiz, text="Sp[10:]:"); lblSP1.grid(row=17,column=2,sticky="e",padx=0,pady=2); lblSP1.config(justify="right")
        SP1_Value=ttk.Entry(self.raiz,textvariable=self.SP1_copy, validate="focusout", validatecommand=self.kk, width=10);
        SP1_Value.grid(row=17,column=3,padx=0,pady=2,sticky='w'); SP1_Value.config(justify="left", foreground="green")

        lblSP2=ttk.Label(self.raiz, text="Deltha_X_Feed[50:]:"); lblSP2.grid(row=18,column=2,sticky="e",padx=0,pady=2); lblSP2.config(justify="right")
        SP2_Value=ttk.Entry(self.raiz,textvariable=self.Deltha_X_Feed_copy, validate="focusout", validatecommand=self.kk, width=10);
        SP2_Value.grid(row=18,column=3,padx=0,pady=2,sticky='w'); SP2_Value.config(justify="left", foreground="green")



        lblKc=ttk.Label(self.raiz, text="Kc="); lblKc.grid(row=19,column=2,sticky="e",padx=0,pady=2); lblKc.config(justify="right")
        Kc_Value=ttk.Entry(self.raiz,textvariable=self.Kc_copy, validate="focusout", validatecommand=self.kk, width=10);
        Kc_Value.grid(row=19,column=3,padx=0,pady=2,sticky='w'); Kc_Value.config(justify="left", foreground="green")
        lblKc_d=ttk.Label(self.raiz, text="Proportional Cte"); lblKc_d.grid(row=19, column=3, sticky="w", padx=70, pady=2)
        lblKc_d.config(justify="right")

        lblTi=ttk.Label(self.raiz, text="Ti="); lblTi.grid(row=20,column=2,sticky="e",padx=0,pady=2); lblTi.config(justify="right")
        Ti_Value=ttk.Entry(self.raiz,textvariable=self.Ti_copy, validate="focusout", validatecommand=self.kk, width=10);
        Ti_Value.grid(row=20,column=3,padx=0,pady=2,sticky='w'); Ti_Value.config(justify="left", foreground="green")
        lblTi_d=ttk.Label(self.raiz, text="T Integral"); lblTi_d.grid(row=20, column=3, sticky="w", padx=70, pady=2)
        lblTi_d.config(justify="right")

        lblTd=ttk.Label(self.raiz, text="Td="); lblTd.grid(row=21,column=2,sticky="e",padx=0,pady=2); lblTd.config(justify="right")
        Td_Value=ttk.Entry(self.raiz,textvariable=self.Td_copy, validate="focusout", validatecommand=self.kk, width=10);
        Td_Value.grid(row=21,column=3,padx=0,pady=2,sticky='w'); Td_Value.config(justify="left", foreground="green")
        lblTd_d=ttk.Label(self.raiz, text="T Derivative"); lblTd_d.grid(row=21, column=3, sticky="w", padx=70, pady=2)
        lblTd_d.config(justify="right")


##        tk.Tk.iconbitmap(self.raiz,default="APM.ico")


    def openWin2(self):
        win=tk.Toplevel()
#        win.geometry('420x500+0+0')
        win.title('APM  Column SS Initial Composition')
#        win.grid()

        global x_ss 
        
        # create a Main Frame
        wrapper11=LabelFrame(win)
#        wrapper2=LabelFrame(win)
        
        #Create a Canvas
        mycanvas=tk.Canvas(wrapper11, width=500, height=450)
        mycanvas.grid()
        
        #Add a Scrollbar to the Canvas
        yscrollbar=ttk.Scrollbar(wrapper11,orient='vertical', command=mycanvas.yview)
        yscrollbar.grid(column=4)
        
        #Configure the Canvas
        mycanvas.configure(yscrollcommand=yscrollbar.set)
        mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))

        #Create ANOTHER Frame INSIDE the Canvas
        wrapper1=Frame(mycanvas)
        mycanvas.create_window((0,0),window=wrapper1, anchor='nw',height=750,width=1000)

        wrapper11.pack(fill='both',expand='yes',padx=10,pady=10)

        Column0=ttk.Label(wrapper1, text=' ', width=3);Column0.grid(row=0,column=0,rowspan=18)
        Column3=ttk.Label(wrapper1, text=' ', width=5);Column3.grid(row=0,column=5,rowspan=18)
        Column7=ttk.Label(wrapper1, text=' ', width=10);Column7.grid(row=0,column=9,rowspan=18)

        labComp=ttk.Label(wrapper1, text="-----------Steady State Initial Molar Fraction on Trays    ------------");
        labComp.grid(row=2,column=1,columnspan=5,sticky="w"+"s"+"n"+"e",padx=10,pady=10)

        lblComp0=ttk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [0] :"); lblComp0.grid(row=3,column=1,sticky="e",padx=10,pady=0)
        txtComp0=ttk.Entry(wrapper1,textvariable=self.x_ss0, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=3,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=ttk.Label(wrapper1, text="SS Initial Molar Fraction Distillate"); lblComp0.grid(row=3,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [1] :"); lblComp0.grid(row=4,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss1, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=4,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [1]"); lblComp0.grid(row=4,column=3,sticky="e",padx=10,pady=0)

        lblComp0=ttk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [2] :"); lblComp0.grid(row=5,column=1,sticky="e",padx=10,pady=0)
        txtComp0=ttk.Entry(wrapper1,textvariable=self.x_ss2, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=5,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=ttk.Label(wrapper1, text="SS Initial Molar Fraction Tray [2]"); lblComp0.grid(row=5,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [3] :"); lblComp0.grid(row=6,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss3, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=6,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [3]"); lblComp0.grid(row=6,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [4] :"); lblComp0.grid(row=7,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss4, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=7,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [4]"); lblComp0.grid(row=7,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [5] :"); lblComp0.grid(row=8,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss5, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=8,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [5]"); lblComp0.grid(row=8,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [6] :"); lblComp0.grid(row=9,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss6, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=9,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [6]"); lblComp0.grid(row=9,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [7] :"); lblComp0.grid(row=10,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss7, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=10,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [7]"); lblComp0.grid(row=10,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [8] :"); lblComp0.grid(row=11,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss8, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=11,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [8]"); lblComp0.grid(row=11,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [9] :"); lblComp0.grid(row=12,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss9, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=12,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [9]"); lblComp0.grid(row=12,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [10] :"); lblComp0.grid(row=13,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss10, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=13,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [10]"); lblComp0.grid(row=13,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [11] :"); lblComp0.grid(row=14,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss11, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=14,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [11]"); lblComp0.grid(row=14,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [12] :"); lblComp0.grid(row=15,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss12, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=15,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [12]"); lblComp0.grid(row=15,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [13] :"); lblComp0.grid(row=16,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss13, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=16,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [13]"); lblComp0.grid(row=16,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [14] :"); lblComp0.grid(row=17,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss14, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=17,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [14]"); lblComp0.grid(row=17,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [15] :"); lblComp0.grid(row=18,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss15, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=18,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [15]"); lblComp0.grid(row=18,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [16] :"); lblComp0.grid(row=19,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss16, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=19,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [16]"); lblComp0.grid(row=19,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [17] :"); lblComp0.grid(row=20,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss17, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=20,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [17]"); lblComp0.grid(row=20,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [18] :"); lblComp0.grid(row=21,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss18, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=21,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [18]"); lblComp0.grid(row=21,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [19] :"); lblComp0.grid(row=22,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss19, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=22,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [19]"); lblComp0.grid(row=22,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [20] :"); lblComp0.grid(row=23,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss20, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=23,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [20]"); lblComp0.grid(row=23,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [21] :"); lblComp0.grid(row=24,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss21, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=24,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [21]"); lblComp0.grid(row=24,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [22] :"); lblComp0.grid(row=25,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss22, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=25,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [22]"); lblComp0.grid(row=25,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [23] :"); lblComp0.grid(row=26,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss23, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=26,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [23]"); lblComp0.grid(row=26,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [24] :"); lblComp0.grid(row=27,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss24, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=27,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [24]"); lblComp0.grid(row=27,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [25] :"); lblComp0.grid(row=28,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss25, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=28,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [25]"); lblComp0.grid(row=28,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [26] :"); lblComp0.grid(row=29,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss26, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=29,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [26]"); lblComp0.grid(row=29,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [27] :"); lblComp0.grid(row=30,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss27, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=30,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [27]"); lblComp0.grid(row=30,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [28] :"); lblComp0.grid(row=31,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss28, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=31,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [28]"); lblComp0.grid(row=31,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [29] :"); lblComp0.grid(row=32,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss28, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=32,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [29]"); lblComp0.grid(row=32,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [30] :"); lblComp0.grid(row=33,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss30, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=33,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Tray [30]"); lblComp0.grid(row=33,column=3,sticky="e",padx=10,pady=0)

        lblComp0=tk.Label(wrapper1, text="nC\u2086H\u2081\u2084 [31] :"); lblComp0.grid(row=34,column=1,sticky="e",padx=10,pady=0)
        txtComp0=tk.Entry(wrapper1,textvariable=self.x_ss31, validate="focusout", validatecommand=self.kk, width=10);
        txtComp0.grid(row=34,column=2,padx=10,pady=0); txtComp0.config(justify="left") #Comp0.insert(10,15.5)
        lblComp0=tk.Label(wrapper1, text="SS Initial Molar Fraction Reboyler [31]"); lblComp0.grid(row=34,column=3,sticky="e",padx=10,pady=0)

        x_ss =np.array([self.x_ss0.get(),self.x_ss1.get(),self.x_ss2.get(),self.x_ss3.get(),self.x_ss4.get(),self.x_ss5.get(),\
                        self.x_ss6.get(),self.x_ss7.get(),self.x_ss8.get(),self.x_ss9.get(),self.x_ss10.get(),self.x_ss11.get(),\
                        self.x_ss12.get(),self.x_ss13.get(),self.x_ss14.get(),self.x_ss15.get(),self.x_ss16.get(),self.x_ss17.get(),\
                        self.x_ss18.get(),self.x_ss19.get(),self.x_ss20.get(),self.x_ss21.get(),self.x_ss22.get(),self.x_ss23.get(),\
                        self.x_ss24.get(),self.x_ss25.get(),self.x_ss26.get(),self.x_ss27.get(),self.x_ss28.get(),self.x_ss29.get(),\
                        self.x_ss30.get(),self.x_ss31.get()])
#        print('x_ss=',x_ss)        

    def kk(self):

##        #y=self.Y0.get()
##        self.q_copy.set('%6.2f'%self.q_copy.get());self.V.set('%6.2f'%self.V_copy.get());self.Cp_copy.set('%8.4f'%self.Cp_copy.get())
##        self.mdelH_copy.set('%6.2f'%self.mdelH_copy.get());self.rho_copy.set('%6.2f'%self.rho_copy.get());self.EoverR_copy.set('%6.2f'%self.EoverR_copy.get());self.ko_copy.set('%6.2f'%self.ko_copy.get());
##        self.UA_copy.set('%6.2f'%self.UA_copy.get());self.Tf_copy.set('%6.2f'%self.Tf_copy.get());self.Caf_copy.set('%6.2f'%self.Caf_copy.get())
##        self.Y12.set('%6.2f'%self.Y12.get());self.Y13.set('%6.2f'%self.Y13.get());self.Y14.set('%6.2f'%self.Y14.get());self.Y15.set('%6.2f'%self.Y15.get())
##        self.P.set('%8.2f'%self.P.get());self.T.set('%8.2f'%self.T.get()) #;self.Y14.set('%6.2f'%self.Y14.get());self.Y15.set('%6.2f'%self.Y15.get())

        pass
        return True

    # define CSTR model
    def distill(self,x,t,rr,Feed,x_Feed):

        Fr_DF=float(self.Fr_DF_copy.get());Feed=float(self.Feed_copy.get());vol=float(self.vol_copy.get())
        atray=float(self.atray_copy.get());acond=float(self.acond_copy.get());areb=float(self.areb_copy.get());     

        # Inputs (3):
        # Reflux ratio is the Manipulated variable
        # Reflux Ratio (L/D)
        # rr = p(1)

        # Disturbance variables (DV)
        # Feed Flowrate (mol/min)
        # Feed = p(2)

        # Mole Fraction of Feed
        # x_Feed = p(3)

        # States (32):
        # x(0) - Reflux Drum Liquid Mole Fraction of Component A
        # x(1) - Tray 1 - Liquid Mole Fraction of Component A
        # .
        # .
        # .
        # x(16) - Tray 16 - Liquid Mole Fraction of Component A (Feed)
        # .
        # .
        # .
        # x(30) - Tray 30 - Liquid Mole Fraction of Component A
        # x(31) - Reboiler Liquid Mole Fraction of Component A

        # Parameters
        # Distillate Flowrate (mol/min)

        D=Fr_DF*Feed # Fr_DF=0.5; Feed=1.0
        # Flowrate of the Liquid in the Rectification Section (mol/min)
        L=rr*D
        # Vapor Flowrate in the Column (mol/min)
        V=L+D
        # Flowrate of the Liquid in the Stripping Section (mol/min)
        FL=Feed+L
##        # Relative Volatility = (yA/xA)/(yB/xB) = KA/KB = alpha(A,B)
##        vol=1.6
##        # Total Molar Holdup in the Condenser
##        atray=0.25
##        # Total Molar Holdup on each Tray
##        acond=0.5
##        # Total Molar Holdup in the Reboiler
##        areb=1.0
##        # Vapor Mole Fractions of Component A
        # From the equilibrium assumption and mole balances
        # 1) vol = (yA/xA) / (yB/xB)
        # 2) xA + xB = 1
        # 3) yA + yB = 1
        y = np.empty(len(x))
        for i in range(32):
            y[i] = x[i] * vol/(1.0+(vol-1.0)*x[i])

        # Compute xdot
        xdot = np.empty(len(x))
        xdot[0] = 1/acond*V*(y[1]-x[0])
        for i in range(1,16):
            xdot[i] = 1.0/atray*(L*(x[i-1]-x[i])-V*(y[i]-y[i+1]))
        xdot[16] = 1/atray*(Feed*x_Feed+L*x[15]-FL*x[16]-V*(y[16]-y[17]))
        for i in range(17,31):
            xdot[i] = 1.0/atray*(FL*(x[i-1]-x[i])-V*(y[i]-y[i+1]))
        xdot[31] = 1/areb*(FL*x[30]-(Feed-D)*x[31]-V*y[31])
        return xdot

    def graphStep(self,*args):

        rr_ss=float(self.rr_ss_copy.get());Feed=float(self.Feed_copy.get());X_Feed=float(self.X_Feed_copy.get())
        Stp1=float(self.Stp1_copy.get());Stp2=float(self.Stp2_copy.get());Stp3=float(self.Stp3_copy.get());     
        SP_ss=x_ss[0];#self.Esc3=float(self.Esc3.get());     
        x0 = x_ss

        # Time Interval (min)
        t = np.linspace(0,50,500)

        # Store results for plotting
        xd = np.ones(len(t)) * x_ss[0]
        rr = np.ones(len(t)) * rr_ss
        ff = np.ones(len(t)) * Feed
        xf = np.ones(len(t)) * X_Feed
        sp = np.ones(len(t)) * SP_ss

        # Step in reflux ratio
        rr[10:] = Stp1
        rr[180:] = Stp2
        rr[360:] = Stp3

        # Simulate
        for i in range(len(t)-1):
            ts = [t[i],t[i+1]]
            y = odeint(self.distill,x0,ts,args=(rr[i],ff[i],xf[i]))
            xd[i+1] = y[-1][0]
            x0 = y[-1]

        # Plot the results
        #plt.clf()
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(t,rr,'b--',linewidth=3)#t[0:i+1],rr[0:i+1],
        plt.ylabel(r'$RR$')
        plt.legend(['Reflux ratio'],loc='best')

        plt.subplot(2,1,2)
        plt.plot(t,sp,'k.-',linewidth=1)#t[0:i+1],sp[0:i+1],
        plt.plot(t,xd,'r-',linewidth=3) #t[0:i+1],xd[0:i+1]
        plt.ylabel(r'$x_d\;(mol/L)$')
        plt.legend(['Starting composition','Distillate composition'],loc='best')
        plt.xlabel('Time (hr)')
        plt.ion()
        plt.show()
        #plt.draw()
        #plt.pause(0.05)

        # Construct results and save data file
        # Column 1 = time
        # Column 2 = reflux ratio
        # Column 3 = distillate composition
        data = np.vstack((t,rr,xd)) # vertical stack
        data = data.T             # transpose data
        np.savetxt('data_doubleTest.txt',data,delimiter=',')

        self.raiz.mainloop() 

##  ================================         MODELING PROCESS          =============================  ##

    def graphModel(self,*args):
        data = np.loadtxt('data_doubleTest.txt',delimiter=',')
        u0 = data[0,1]
        yp0 = data[0,2]
        t = data[:,0].T
        u1 = data[:,1].T
        yp = data[:,2].T

        # specify number of steps
        ns = len(t)
        delta_t = t[1]-t[0]
        # create linear interpolation of the u data versus time
        uf = interp1d(t,u1)

        # define first-order plus dead-time approximation    
        def fopdt(y,t,uf,Km,taum,thetam):
            # arguments
            #  y      = output
            #  t      = time
            #  uf     = input linear function (for time shift)
            #  Km     = model gain
            #  taum   = model time constant
            #  thetam = model Lag time constant
            # time-shift u
            try:
                if (t-thetam) <= 0:
                    um = uf(0.0)
                else:
                    um = uf(t-thetam)
            except:
                #print('Error with time extrapolation: ' + str(t))
                um = u0
            # calculate derivative
            dydt = (-(y-yp0) + Km * (um-u0))/taum
            return dydt

        # simulate FOPDT model with x=[Km,taum,thetam]
        def sim_model(x):
            # input arguments
            Km = x[0]
            taum = x[1]
            thetam = x[2]
            # storage for model values
            ym = np.zeros(ns)  # model
            # initial condition
            ym[0] = yp0
            # loop through time steps    
            for i in range(0,ns-1):
                ts = [delta_t*i,delta_t*(i+1)]
                y1 = odeint(fopdt,ym[i],ts,args=(uf,Km,taum,thetam))
                ym[i+1] = y1[-1]
            return ym

        # define objective
        def objective(x):
            # simulate model
            ym = sim_model(x)
            # calculate objective
            obj = 0.0
            for i in range(len(ym)):
                obj = obj + (ym[i]-yp[i])**2    
            # return result
            return obj

        # initial guesses
        x0 = np.zeros(3)
        x0[0] = 1.0 # Km
        x0[1] = 10.0 # taum
        x0[2] = 0.0 # thetam

        # show initial objective
        print('Initial SSE Objective: ' + str(objective(x0)))

        # optimize Km, taum, thetam
        # bounds on variables
        bnds = ((-1.0e10, 1.0e10), (0.01, 1.0e10), (0.0, 5.0))
        solution = minimize(objective,x0,method='SLSQP',bounds=bnds)
        x = solution.x

        # show final objective
        print('Final SSE Objective: ' + str(objective(x)))

        print('Kp: ' + str(x[0]))
        print('taup: ' + str(x[1]))
        print('thetap: ' + str(x[2]))
        self.Kp_copy.set('%4.2f'%x[0])
        self.Tp_copy.set('%4.2f'%x[1])
        self.Lp_copy.set('%4.2f'%x[2])

        # design PI controller
#       tauc = max(0.1*taup,0.8*thetap)
        tauc = max(0.1*x[1],0.8*x[2])    
        Kc = (1.0/x[0])*(x[1]/(x[2]+tauc))
        tauI = x[1]/8.0
        self.Kc_copy.set('%4.2f'%Kc)
        self.Ti_copy.set('%4.2f'%tauI)
        self.Td_copy.set(0.000012)

        print('Kc: ' + str(Kc))
        print('tauI: ' + str(tauI))

        # calculate model with updated parameters
        ym1 = sim_model(x0)
        ym2 = sim_model(x)
        # plot results
        plt.figure()
        plt.subplot(2,1,1)
#        plt.plot(t,ym1,'b-',linewidth=2,label='Initial Guess')
        plt.plot(t,ym2,'r--',linewidth=2,label='Modelo 1° Orden')
        plt.plot(t,yp,'kx-',linewidth=2,label='T Datos Proceso')
        plt.ylabel('T(°K) (Temperatura Reactor)')
        plt.legend(loc='best')
        plt.subplot(2,1,2)
        plt.plot(t,u1,'bx-',linewidth=2)
        plt.plot(t,uf(t),'r--',linewidth=1)
        plt.legend(['Tce Datos proceso','Modelo'],loc='best')
        plt.ylabel('Tce (°k) (Temp Camiza)')
        plt.show()

##  ===============================            TUNNING  PID              ================================  ##

    def TunePID(self,*args):

        rr_ss=float(self.rr_ss_copy.get());Feed=float(self.Feed_copy.get());X_Feed=float(self.X_Feed_copy.get())
        Deltha_X_Feed=float(self.Deltha_X_Feed_copy.get());SP1=float(self.SP1_copy.get())     
        SP_ss=x_ss[0];#self.Esc3=float(self.Esc3.get());     
        x0 = x_ss

        # Time Interval (min)
        ns = 101
        t = np.linspace(0,100,ns)

        xd = np.ones(len(t)) * x_ss[0]
        rr = np.ones(len(t)) * rr_ss
        ff = np.ones(len(t)) * Feed
        xf = np.ones(len(t)) * X_Feed
        sp = np.ones(len(t)) * SP_ss
        # Store results for plotting
        xd = np.ones(len(t)) * x_ss[0]
        rr = np.ones(len(t)) * rr_ss
        ff = np.ones(len(t)) * Feed
        xf = np.ones(len(t)) * X_Feed

        # Step in reflux ratio
        #rr[10:] = 4.0
        #rr[40:] = 2.0
        #rr[70:] = 3.0

        # Feed Concentration (mol frac)
        xf[50:] = Deltha_X_Feed

        # Feed flow rate
        #ff[80:] = 1.0

        delta_t = t[1]-t[0]

        # storage for recording values
        op = np.ones(ns)*3.0  # controller output
        pv = np.zeros(ns)  # process variable
        e = np.zeros(ns)   # error
        ie = np.zeros(ns)  # integral of the error
        dpv = np.zeros(ns) # derivative of the pv
        P = np.zeros(ns)   # proportional
        I = np.zeros(ns)   # integral
        D = np.zeros(ns)   # derivative
        sp = np.ones(ns)*SP_ss  # set point
        sp[10:] = SP1

        # PID (tuning)
        Kc = 60
        tauI = 4
        tauD = 0.0

        # Upper and Lower limits on OP
        op_hi = 10.0
        op_lo = 1.0

        # loop through time steps    
        for i in range(1,ns):
            e[i] = sp[i] - pv[i]
            if i >= 1:  # calculate starting on second cycle
                dpv[i] = (pv[i]-pv[i-1])/delta_t
                ie[i] = ie[i-1] + e[i] * delta_t
            P[i] = Kc * e[i]
            I[i] = Kc/tauI * ie[i]
            D[i] = - Kc * tauD * dpv[i]
            op[i] = op[0] + P[i] + I[i] + D[i]
            if op[i] > op_hi:  # check upper limit
                op[i] = op_hi
                ie[i] = ie[i] - e[i] * delta_t # anti-reset windup
            if op[i] < op_lo:  # check lower limit
                op[i] = op_lo
                ie[i] = ie[i] - e[i] * delta_t # anti-reset windup

            # distillation solution (1 time step)
            rr[i] = op[i]
            ts = [t[i-1],t[i]]
            y = odeint(self.distill,x0,ts,args=(rr[i],ff[i],xf[i]))
            xd[i] = y[-1][0]
            x0 = y[-1]

            if i<ns-1:
                pv[i+1] = y[-1][0]

        #op[ns] = op[ns-1]
        #ie[ns] = ie[ns-1]
        #P[ns] = P[ns-1]
        #I[ns] = I[ns-1]
        #D[ns] = D[ns-1]    

        # Construct results and save data file
        # Column 1 = time
        # Column 2 = reflux ratio
        # Column 3 = distillate composition
        data = np.vstack((t,rr,xd)) # vertical stack
        data = data.T             # transpose data
        np.savetxt('data.txt',data,delimiter=',')

        # Plot the results
        plt.figure()
        plt.subplot(3,1,1)
        plt.plot(t,rr,'b--',linewidth=3)
        plt.ylabel(r'$RR$')
        plt.legend(['Reflux ratio'],loc='best')

        plt.subplot(3,1,2)
        plt.plot(t,xf,'k:',linewidth=3,label='Feed composition')
        plt.plot(t,ff,'g-.',linewidth=3,label='Feed flow (mol/min)')
        plt.ylabel('Feed')
        plt.ylim([0.4,1.1])
        plt.legend(loc='best')

        plt.subplot(3,1,3)
        plt.plot(t,xd,'r-',linewidth=3)
        plt.plot(t,sp,'k.-',linewidth=1)
        plt.ylabel(r'$x_d\;(mol/L)$')
        plt.legend(['Distillate composition','Set point'],loc='best')
        plt.xlabel('Time (min)')
        plt.savefig('distillation.png')
        plt.show()

    pass

main()

