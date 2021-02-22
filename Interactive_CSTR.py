
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
    raiz = Tk()
    gui = Window(raiz)
    gui.raiz.mainloop()
    return None

class Window:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.resizable(1,1)
        self.raiz.title("APM  Continuously Stirred Tank Reactor (CSTR)")
        self.raiz.geometry('1350x750+0+0')


##   =====================================           VARIABLES          ===============================

        # -------------------------------    DATAS    ----------------------------------------


        self.q_copy = DoubleVar(value=100.00); self.V_copy = DoubleVar(value=1.00); self.rho_copy = DoubleVar(value=1000.00)
        self.Cp_copy = DoubleVar(value=0.239); self.mdelH_copy = DoubleVar(value=5e4); self.EoverR_copy = DoubleVar(value=8750.0);
        self.k0_copy = DoubleVar(value=7.2e10); self.UA_copy = DoubleVar(value=5e4);
        self.Tf_copy = DoubleVar(value=360.0);

        # ------------------------------       STEADY STATE VALUES      -----------------------

        self.T_ss_copy = DoubleVar(value=377.7587);
        self.u_ss_copy = DoubleVar(value=300.0);
        self.Ca_ss_copy = DoubleVar(value=0.137525);



        # -------------------------------         MODELING PROCESS          -------------------------------

        self.Caf_copy = DoubleVar(value=1.0);self.Stp1_copy = DoubleVar(value=303.0); self.Stp2_copy = DoubleVar(value=297.0);
        self.Stp3_copy = DoubleVar(value=300.0); self.Kp_copy = DoubleVar();self.Tp_copy = DoubleVar();self.Lp_copy = DoubleVar();
        self.Kc_copy = DoubleVar();self.Ti_copy = DoubleVar();self.Td_copy = DoubleVar();

        self.Tc = DoubleVar(value=300.0) ; self.T=DoubleVar(value=300.0); self.Ca=DoubleVar(value=1.0);self.Atenty=StringVar('')

        self.SP1_copy=DoubleVar(value=310.00); self.SP2_copy=DoubleVar(value=335.00)



##  ========================================        GUI        ===============================================================  ##



        Column0=Label(self.raiz, width=3);Column0.grid(row=0,column=0,rowspan=18)
#        Column3=Label(self.raiz, width=5);Column3.grid(row=0,column=3,rowspan=18)
        Column7=Label(self.raiz, width=10);Column7.grid(row=0,column=9,rowspan=18)


        labComp=Label(self.raiz, text="-----    DATAS    -------", borderwidth=2, relief="groove",font= 'arial 11 bold',width=20);
        labComp.grid(row=2,column=1,columnspan=3,sticky="sewn",padx=0,pady=10)

        Fe=ttk.Entry(self.raiz,textvariable=self.q_copy, validate="focusout", validatecommand=self.kk, width=10);Fe.grid(row=3,column=2,padx=0,pady=2); Fe.config(justify="left") #Comp1.insert(10,20.8)
        lblFe=ttk.Label(self.raiz, text="q(m3/hs)="); lblFe.grid(row=3,column=1,sticky="e",padx=0,pady=2)
        lblFe_d=ttk.Label(self.raiz, text="Volumetric Flowrate"); lblFe_d.grid(row=3,column=3,sticky="w",padx=0,pady=2)

        V=ttk.Entry(self.raiz,textvariable=self.V_copy, validate="focusout", validatecommand=self.kk, width=10);V.grid(row=4,column=2,padx=0,pady=2); V.config(justify="left")#; #Comp2.insert(10,0.0)
        lblV=ttk.Label(self.raiz, text="V(m^3)="); lblV.grid(row=4,column=1,sticky="e",padx=0,pady=2)
        lblV=ttk.Label(self.raiz, text="Volume of CSTR"); lblV.grid(row=4,column=3,sticky="w",padx=0,pady=2)

        Dem=ttk.Entry(self.raiz,textvariable=self.rho_copy, validate="focusout", validatecommand=self.kk, width=10);Dem.grid(row=5,column=2,padx=0,pady=2); Dem.config(justify="left")#; #Comp3.insert(10, 0.0)
        lblDem=ttk.Label(self.raiz, text="rho(kg/m^3)="); lblDem.grid(row=5, column=1, sticky="e", padx=0, pady=2)
        lblDem_d=ttk.Label(self.raiz, text="Density of A --> B Mixture"); lblDem_d.grid(row=5, column=3, sticky="w", padx=0, pady=2)

        Cp=ttk.Entry(self.raiz,textvariable=self.Cp_copy, validate="focusout", validatecommand=self.kk, width=10);Cp.grid(row=6,column=2,padx=0,pady=2); Cp.config(justify="left")#; #Comp3.insert(10, 0.0)
        lblCp=ttk.Label(self.raiz, text="Cp(J/kg-°K)="); lblCp.grid(row=6, column=1, sticky="e", padx=0, pady=2)
        lblCp_d=ttk.Label(self.raiz, text="Heat Capacity of A --> B Mixture"); lblCp_d.grid(row=6, column=3, sticky="w", padx=0, pady=2)

        DH=ttk.Entry(self.raiz,textvariable=self.mdelH_copy, validate="focusout", validatecommand=self.kk, width=10);DH.grid(row=7,column=2,padx=0,pady=2); DH.config(justify="left")#; Comp4.insert(10,0.0)
        lblDH=ttk.Label(self.raiz,text="DH(J/mol)="); lblDH.grid(row=7,column=1,sticky="e",padx=0,pady=2)
        lblDH_d=ttk.Label(self.raiz, text="Heat of reaction for A --> B"); lblDH_d.grid(row=7, column=3, sticky="w", padx=0, pady=2)

        E_R=ttk.Entry(self.raiz,textvariable=self.EoverR_copy, validate="focusout", validatecommand=self.kk, width=10);E_R.grid(row=8,column=2,padx=0,pady=2); E_R.config(justify="left")#; Comp5.insert(10,0.0)
        lblE_R=Label(self.raiz, text="E/R(°K)="); lblE_R.grid(row=8,column=1,sticky="e",padx=0,pady=2)
        lblE_R_d=ttk.Label(self.raiz, text="E=Activation Energy/R=Cte Gases"); lblE_R_d.grid(row=8, column=3, sticky="w", padx=0, pady=2)

        k0=ttk.Entry(self.raiz,textvariable=self.k0_copy, validate="focusout", validatecommand=self.kk, width=10);k0.grid(row=9,column=2,padx=0,pady=2); k0.config(justify="left")#; ko.insert(10,0.0)
        lblk0=ttk.Label(self.raiz, text="ko(1/sec) ="); lblk0.grid(row=9,column=1,sticky="e",padx=0,pady=2)
        lblk0_d=ttk.Label(self.raiz, text="Pre-exponential factor"); lblk0_d.grid(row=9, column=3, sticky="w", padx=0, pady=2)

        UA=ttk.Entry(self.raiz,textvariable=self.UA_copy, validate="focusout", validatecommand=self.kk, width=10);UA.grid(row=10,column=2,padx=0,pady=2); UA.config(justify="left")#;# Comp7.insert(10,0.0)
        lblUA=Label(self.raiz, text="UA(W/°K)="); lblUA.grid(row=10,column=1,sticky="e",padx=0,pady=2)
        lblUA_d=ttk.Label(self.raiz, text="Overall Heat Transfer Coefficient"); lblUA_d.grid(row=10, column=3, sticky="w", padx=0, pady=2)


        # -------------------------------        SS Initial Conditions         -------------------------------

        lbCargaDatos=Label(self.raiz,text="-- SS Initial Conditions --", borderwidth=2, relief="groove",font= 'arial 10 bold',width=20)
        lbCargaDatos.grid(row=11,column=1,columnspan=3,sticky="sewn",padx=0,pady=15)

        lblCa_0_Value=Label(self.raiz,textvariable=self.Ca_ss_copy, borderwidth=2, relief="sunken", width=9, fg="green");
        lblCa_0_Value.grid(row=12, column=2, pady=2, padx=0, sticky='w'); lblCa_0_Value.config(justify="left")
        lblCa_0=ttk.Label(self.raiz, text="Ca_ss(mol/dm3)="); lblCa_0.grid(row=12,column=1,sticky="e",padx=0,pady=2)
        lblCa_0_d=ttk.Label(self.raiz, text="Concentration of A in CSTR"); lblCa_0_d.grid(row=12, column=3, sticky="w", padx=0, pady=2),#font= 'arial 10 bold'

        btCondIniciales = tk.Button(self.raiz, text="-- Steady State --",command = self.iniConditions,font= 'arial 10 bold',foreground = "green")
        btCondIniciales.grid(row=12, column=3,sticky="e",padx=0,pady=0);#btTunePID.config(justify="center", foreground="green")

        lblT_0_Value=Label(self.raiz,textvariable=self.T_ss_copy, borderwidth=2, relief="sunken", width=9, fg="green");
        lblT_0_Value.grid(row=13, column=2, pady=2, padx=0, sticky='w'); lblCa_0_Value.config(justify="left")
        lblT_0=ttk.Label(self.raiz, text="T_ss="); lblT_0.grid(row=13,column=1,sticky="e",padx=0,pady=2)
        lblT_0_d=ttk.Label(self.raiz, text="SS Temperature in CSTR"); lblT_0_d.grid(row=13, column=3, sticky="w", padx=0, pady=2)

        Tce_0=ttk.Entry(self.raiz,textvariable=self.u_ss_copy, validate="focusout", validatecommand=self.kk, width=10);Tce_0.grid(row=14,column=2,padx=0,pady=2); Tce_0.config(justify="left") #Comp0.insert(10,15.5)
        lblTce_0=ttk.Label(self.raiz, text="Tc_ss(°K)="); lblTce_0.grid(row=14,column=1,sticky="e",padx=0,pady=2)
        labTce_0_d=ttk.Label(self.raiz, text="SS Temperature of cooling jacket"); labTce_0_d.grid(row=14,column=3,sticky="w",padx=0,pady=2)

        Tf=ttk.Entry(self.raiz,textvariable=self.Tf_copy, validate="focusout", validatecommand=self.kk, width=10);Tf.grid(row=15,column=2,padx=0,pady=2); Tf.config(justify="left")#; Comp8.insert(10,0.0)
        lblTf=ttk.Label(self.raiz, text="Tf(°k)="); lblTf.grid(row=15,column=1,sticky="e",padx=0,pady=2)
        lblTf_d=ttk.Label(self.raiz, text="Feed Temperature"); lblTf_d.grid(row=15, column=3, sticky="w", padx=0, pady=2)

        Caf=ttk.Entry(self.raiz,textvariable=self.Caf_copy, validate="focusout", validatecommand=self.kk, width=10);Caf.grid(row=16,column=2,padx=0,pady=2); Caf.config(justify="left")#; Comp8.insert(10,0.0)
        lblCaf=ttk.Label(self.raiz, text="Caf(mol/m3)="); lblCaf.grid(row=16,column=1,sticky="e",padx=0,pady=2)
        lblCaf_d=ttk.Label(self.raiz, text="Feed Concentration"); lblCaf_d.grid(row=16, column=3, sticky="w", padx=0, pady=2)

        Stp1=ttk.Entry(self.raiz,textvariable=self.Stp1_copy, validate="focusout", validatecommand=self.kk, width=10);Stp1.grid(row=17,column=2,padx=0,pady=2); Stp1.config(justify="left")#; Comp8.insert(10,0.0)
        lblStp1=ttk.Label(self.raiz, text="Step1(1:10]="); lblStp1.grid(row=17,column=1,sticky="e",padx=0,pady=2)
        lblStp1_d=ttk.Label(self.raiz, text="Step N°1 en Tc"); lblStp1_d.grid(row=17, column=3, sticky="w", padx=0, pady=2)

        Stp2=ttk.Entry(self.raiz,textvariable=self.Stp2_copy, validate="focusout", validatecommand=self.kk, width=10);Stp2.grid(row=18,column=2,padx=0,pady=2); Stp2.config(justify="left")#; Comp8.insert(10,0.0)
        lblStp2=ttk.Label(self.raiz, text="Step2 [10:19]="); lblStp2.grid(row=18,column=1,sticky="e",padx=0,pady=2)
        lblStp2_d=ttk.Label(self.raiz, text="Step N°2 en Tc"); lblStp2_d.grid(row=18, column=3, sticky="w", padx=0, pady=2)

        Stp3=ttk.Entry(self.raiz,textvariable=self.Stp3_copy, validate="focusout", validatecommand=self.kk, width=10);Stp3.grid(row=19,column=2,padx=0,pady=2); Stp3.config(justify="left")#; Comp8.insert(10,0.0)
        lblStp3=ttk.Label(self.raiz, text="Stp3 [19:]="); lblStp3.grid(row=19,column=1,sticky="e",padx=0,pady=2)
        lblStp3_d=ttk.Label(self.raiz, text="Step N°3 on Tc"); lblStp3_d.grid(row=19, column=3, sticky="w", padx=0, pady=2)


        # ----------------------  Test - MODELING and TUNNING        -------------------------------

        btDoubleTest= ttk.Button(self.raiz, text="Double Test",command = self.graphStep)
        btDoubleTest.grid(row=20, column=0,sticky="w",padx=5,pady=5)

        btModel = ttk.Button(self.raiz, text="Modeling",command = self.graphModel)
        btModel.grid(row=20, column=1,sticky="w",padx=5,pady=5)


        lblKp=ttk.Label(self.raiz, text="Kp="); lblKp.grid(row=21,column=0,sticky="w",padx=0,pady=2); lblKp.config(justify="left")
        lblKp_Value=Label(self.raiz,textvariable=self.Kp_copy, borderwidth=2, relief="sunken", width=9, fg="green");
        lblKp_Value.grid(row=21, column=0, pady=2, padx=0, sticky='e'); lblKp_Value.config(justify="right")
        lblKp_d=ttk.Label(self.raiz, text="Ganancia"); lblKp_d.grid(row=21, column=1, sticky="w", padx=0, pady=2)

        lblTp_Value=Label(self.raiz,textvariable=self.Tp_copy, borderwidth=2, relief="sunken", width=9, fg="green");
        lblTp_Value.grid(row=22, column=0, pady=2, padx=0, sticky='e'); lblTp_Value.config(justify="left")
        lblTp=ttk.Label(self.raiz, text="Tp="); lblTp.grid(row=22,column=0,sticky="w",padx=0,pady=2)
        lblTp_d=ttk.Label(self.raiz, text="Cte de tiempo"); lblTp_d.grid(row=22, column=1, sticky="w", padx=0, pady=2)

        lblLp_Value=Label(self.raiz,textvariable=self.Lp_copy, borderwidth=2, relief="sunken", width=9, fg="green");
        lblLp_Value.grid(row=23, column=0, pady=2, padx=0, sticky='e'); lblLp_Value.config(justify="left")
        lblLp=ttk.Label(self.raiz, text="Lp="); lblLp.grid(row=23,column=0,sticky="w",padx=0,pady=2)
        lblLp_d=ttk.Label(self.raiz, text="Lag Time"); lblLp_d.grid(row=23, column=1, sticky="w", padx=0, pady=2)



        btTunePID = ttk.Button(self.raiz, text="Tunning PID",command = self.TunePID)
        btTunePID.grid(row=20,columnspan=2, column=2,sticky="we",padx=5,pady=5);#btTunePID.config(justify="center", foreground="green")

        lblSP1=ttk.Label(self.raiz, text="Sp1[0:10]:"); lblSP1.grid(row=21,column=2,sticky="e",padx=0,pady=2); lblSP1.config(justify="right")
        SP1_Value=ttk.Entry(self.raiz,textvariable=self.SP1_copy, validate="focusout", validatecommand=self.kk, width=10);
        SP1_Value.grid(row=21,column=3,padx=0,pady=2,sticky='w'); SP1_Value.config(justify="left", foreground="green")

        lblSP2=ttk.Label(self.raiz, text="Sp2[10:]:"); lblSP2.grid(row=22,column=2,sticky="e",padx=0,pady=2); lblSP2.config(justify="right")
        SP2_Value=ttk.Entry(self.raiz,textvariable=self.SP2_copy, validate="focusout", validatecommand=self.kk, width=10);
        SP2_Value.grid(row=22,column=3,padx=0,pady=2,sticky='w'); SP2_Value.config(justify="left", foreground="green")



        lblKc=ttk.Label(self.raiz, text="Kc="); lblKc.grid(row=23,column=2,sticky="e",padx=0,pady=2); lblKc.config(justify="right")
        Kc_Value=ttk.Entry(self.raiz,textvariable=self.Kc_copy, validate="focusout", validatecommand=self.kk, width=10);
        Kc_Value.grid(row=23,column=3,padx=0,pady=2,sticky='w'); Kc_Value.config(justify="left", foreground="green")
        lblKc_d=ttk.Label(self.raiz, text="Proportional Gain"); lblKc_d.grid(row=23, column=3, sticky="w", padx=70, pady=2)
        lblKc_d.config(justify="right")

        lblTi=ttk.Label(self.raiz, text="Ti="); lblTi.grid(row=24,column=2,sticky="e",padx=0,pady=2); lblTi.config(justify="right")
        Ti_Value=ttk.Entry(self.raiz,textvariable=self.Ti_copy, validate="focusout", validatecommand=self.kk, width=10);
        Ti_Value.grid(row=24,column=3,padx=0,pady=2,sticky='w'); Ti_Value.config(justify="left", foreground="green")
        lblTi_d=ttk.Label(self.raiz, text="T Integral"); lblTi_d.grid(row=24, column=3, sticky="w", padx=70, pady=2)
        lblTi_d.config(justify="right")

        lblTd=ttk.Label(self.raiz, text="Td="); lblTd.grid(row=25,column=2,sticky="e",padx=0,pady=2); lblTd.config(justify="right")
        Td_Value=ttk.Entry(self.raiz,textvariable=self.Td_copy, validate="focusout", validatecommand=self.kk, width=10);
        Td_Value.grid(row=25,column=3,padx=0,pady=2,sticky='w'); Td_Value.config(justify="left", foreground="green")
        lblTd_d=ttk.Label(self.raiz, text="T Derivative"); lblTd_d.grid(row=25, column=3, sticky="w", padx=70, pady=2)
        lblTd_d.config(justify="right")


#        lblTp_d=ttk.Label(self.raiz, text="Cte de tiempo"); lblTp_d.grid(row=22, column=1, sticky="w", padx=0, pady=2)
#        lblTp_d=ttk.Label(self.raiz, text="Cte de tiempo"); lblTp_d.grid(row=22, column=1, sticky="w", padx=0, pady=2)

#        tk.Tk.iconbitmap(self.raiz,default="APM.ico")

    def kk(self):
##        #y=self.Y0.get()
##        self.q_copy.set('%6.2f'%self.q_copy.get());self.V.set('%6.2f'%self.V_copy.get());self.Cp_copy.set('%8.4f'%self.Cp_copy.get())
##        self.mdelH_copy.set('%6.2f'%self.mdelH_copy.get());self.rho_copy.set('%6.2f'%self.rho_copy.get());self.EoverR_copy.set('%6.2f'%self.EoverR_copy.get());self.ko_copy.set('%6.2f'%self.ko_copy.get());
##        self.UA_copy.set('%6.2f'%self.UA_copy.get());self.Tf_copy.set('%6.2f'%self.Tf_copy.get());self.Caf_copy.set('%6.2f'%self.Caf_copy.get())
##        self.Y12.set('%6.2f'%self.Y12.get());self.Y13.set('%6.2f'%self.Y13.get());self.Y14.set('%6.2f'%self.Y14.get());self.Y15.set('%6.2f'%self.Y15.get())
##        #self.P.set('%8.2f'%self.P.get());self.T.set('%8.2f'%self.T.get()) #;self.Y14.set('%6.2f'%self.Y14.get());self.Y15.set('%6.2f'%self.Y15.get())
        return True

    # define CSTR model
    def cstr(self,x,t,u,Tf,Caf):
        # Inputs (3):
        # Temperature of cooling jacket (K)
        Tc = u
        # Tf = Feed Temperature (K)
        # Caf = Feed Concentration (mol/m^3)

        # States (2):
        # Concentration of A in CSTR (mol/m^3)
        Ca = x[0]
        # Temperature in CSTR (K)
        T = x[1]
        self.q=float(self.q_copy.get());self.V=float(self.V_copy.get());self.Cp=float(self.Cp_copy.get())
        self.EoverR=float(self.EoverR_copy.get());self.k0=float(self.k0_copy.get());self.UA=float(self.UA_copy.get());     
        self.mdelH=float(self.mdelH_copy.get());self.rho=float(self.rho_copy.get());
#        self.Tf_copy=float(self.Tf.get());self.Caf_copy=float(self.Caf.get());#self.Esc3=float(self.Esc3.get());     
        #self.T=float(self.T.get());self.Ca=float(self.Ca.get());self.Tc=float(self.Tc.get());     
        
#        print('type(Tc)=',type(Tc));print('type(T)=',type(T));print('type(Ca)=',type(Ca));print('type(q)=',type(self.q));
#        print('type(V)=',type(self.V));print('type(Cp)=',type(self.Cp));print('type(k0)=',type(self.k0));
#        print('type(UA)=',type(self.UA));print('type(EoverR)=',type(self.EoverR));print('type(mdelH)=',type(self.mdelH));
#        print('type(rho)=',type(self.rho));# print('type(q)=',type(q));


        # Parameters:
        # Volumetric Flowrate (m^3/sec)
#        q = 100
        # Volume of CSTR (m^3)
#        V = 100
        # Density of A-B Mixture (kg/m^3)
#        rho = 1000
        # Heat capacity of A-B Mixture (J/kg-K)
#        Cp = 0.239
        # Heat of reaction for Calor de ReaccionA->B (J/mol)
#        mdelH = 5e4
        # E - Activation energy in the Arrhenius Equation (J/mol)
        # R - Universal Gas Constant = 8.31451 J/mol-K
#        EoverR = 8750
        # Pre-exponential factor (1/sec)
#        k0 = 7.2e10
        # U - Overall Heat Transfer Coefficient (W/m^2-K)
        # A - Area - this value is specific for the U calculation (m^2)
#        UA = 5e4
        # reaction rate
        rA = self.k0*np.exp(-(self.EoverR/T))*Ca#self.k0*

        # Calculate concentration derivative
        dCadt = self.q/(self.V*100)*(Caf - Ca) - rA
        # Calculate temperature derivative
        dTdt = self.q/(self.V*100)*(Tf - T) \
                + self.mdelH/(self.rho*self.Cp)*rA\
                + self.UA/(self.V*100)/self.rho/self.Cp*(Tc-T)
        
        # Return xdot:
        xdot = np.zeros(2)
        xdot[0] = dCadt
        xdot[1] = dTdt
        return xdot


    def iniConditions(self,*args):

        m=GEKKO(remote=False)

        q=float(self.q_copy.get());V=float(self.V_copy.get());Cp=float(self.Cp_copy.get())
        EoverR=float(self.EoverR_copy.get());k0=float(self.k0_copy.get());UA=float(self.UA_copy.get());     
        mdelH=float(self.mdelH_copy.get());rho=float(self.rho_copy.get());
        Tf=float(self.Tf_copy.get());
        Tc=float(self.u_ss_copy.get());
        Caf=float(self.Caf_copy.get());



        T_1=m.Var(value=300.0)
        Ca_1=m.Var(value=1.0)

        m.Equation(q/(V*100)*(Tf - T_1)+mdelH/(rho*Cp)*(k0*2.7184**(-(EoverR/T_1))*Ca_1)+UA/(V*100)/rho/Cp*(Tc-T_1)==0)

        m.Equation(q/(V*100)*(Caf - Ca_1) - (k0*2.7184**(-(EoverR/T_1))*Ca_1)==0)

        m.solve()  #disp=False

        self.Ca_ss_copy.set('%7.4f'%Ca_1.value[0])
        self.T_ss_copy.set('%7.4f'%T_1.value[0])
        pass

    def graphStep(self,*args):
        # Steady State Initial Conditions for the States
        #    Ca_ss = 0.87725294608097
        #    T_ss = 324.475443431599

        self.Ca_ss=float(self.Ca_ss_copy.get());self.T_ss=float(self.T_ss_copy.get());self.u_ss=float(self.u_ss_copy.get())
        self.Stp1=float(self.Stp1_copy.get());self.Stp2=float(self.Stp2_copy.get());self.Stp3=float(self.Stp3_copy.get());     
        Tf=float(self.Tf_copy.get());Caf=float(self.Caf_copy.get());#self.Esc3=float(self.Esc3.get());     


        x0 = np.empty(2)
        x0[0] = self.Ca_ss
        x0[1] = self.T_ss

        # Steady State Initial Condition
        #    u_ss = 300.0
        # Feed Temperature (K)
        #    Tf = 350
        # Feed Concentration (mol/m^3)
        #    Caf = 1

        # Time Interval (min)
        t = np.linspace(0,25,251)

        # Store results for plotting
        Ca = np.ones(len(t)) * self.Ca_ss
        T = np.ones(len(t)) * self.T_ss
        u = np.ones(len(t)) * self.u_ss
        
        # Step cooling temperature to 295
        u[10:100] = self.Stp1
        u[100:190] = self.Stp2
        u[190:] = self.Stp3

        # Simulate CSTR
        for i in range(len(t)-1):
            ts = [t[i],t[i+1]]
            y = odeint(self.cstr,x0,ts,args=(u[i+1],Tf,Caf))
            Ca[i+1] = y[-1][0]
            T[i+1] = y[-1][1]
            x0[0] = Ca[i+1]
            x0[1] = T[i+1]

        # Construct results and save data file
        # Column 1 = time
        # Column 2 = cooling temperature
        # Column 3 = reactor temperature
        data = np.vstack((t,u,T)) # vertical stack
        data = data.T             # transpose data
        np.savetxt('data_doublet.txt',data,delimiter=',')
            
        plt.figure()
        plt.subplot(3,1,1)
        plt.plot(t,u,'b--',linewidth=3)
        plt.ylabel('Cooling T (°K)')
        plt.legend(['Jacket Temperature'],loc='best')

        plt.subplot(3,1,2)
        plt.plot(t,Ca,'r-',linewidth=3)
        plt.ylabel('Ca (mol/L)')
        plt.legend(['Reactor Concentration'],loc='best')

        plt.subplot(3,1,3)
        plt.plot(t,T,'k.-',linewidth=3)
        plt.ylabel('T (K)')
        plt.xlabel('Time (min)')
        plt.legend(['Reactor Temperature'],loc='best')

        plt.show()

        self.raiz.mainloop() 

#================================    MODELING first-order plus dead-time (FOPDT)     =======================#

    def graphModel(self,*args):
        data = np.loadtxt('data_doublet.txt',delimiter=',')
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
            #  thetam = model time constant
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
        x0[0] = 2.2 # Km
        x0[1] = 0.8 # taum
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





        # from identification
##        Kp = 2.16288502017
##        taup = 0.913444964569
##        thetap = 0.000121628824381

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
        plt.plot(t,ym1,'b-',linewidth=2,label='Initial Guess')
        plt.plot(t,ym2,'r--',linewidth=3,label='Optimized FOPDT')
        plt.plot(t,yp,'kx-',linewidth=2,label='Process Data')
        plt.ylabel('Output')
        plt.legend(loc='best')
        plt.subplot(2,1,2)
        plt.plot(t,u1,'bx-',linewidth=2)
        plt.plot(t,uf(t),'r--',linewidth=3)
        plt.legend(['Measured','Interpolated'],loc='best')
        plt.ylabel('Input Data')
        plt.show()

#===============================        TUNNING DEL CONTROLADOR PID        ================================#


    def TunePID(self,*args):
        # Steady State Initial Conditions for the States
#        Ca_ss = 0.87725294608097
#        T_ss = 324.475443431599

#        Ca_ss=float(self.Ca_ss_copy.get());T_ss=float(self.T_ss_copy.get());u_ss=float(self.u_ss_copy.get())
#        Kc=float(self.Esc1_copy.get());tauI=float(self.Ti_copy.get());tauD=float(self.Td_copy.get());     
#        SP1=float(self.SP1_copy.get());SP2=float(self.SP2_copy.get());#self.Esc3=float(self.Esc3.get());     

        self.Ca_ss=float(self.Ca_ss_copy.get());self.T_ss=float(self.T_ss_copy.get());self.u_ss=float(self.u_ss_copy.get())
        self.Kc=float(self.Kc_copy.get());self.tauI=float(self.Ti_copy.get());self.tauD=float(self.Td_copy.get());     
        self.SP1=float(self.SP1_copy.get());self.SP2=float(self.SP2_copy.get());#self.Esc3=float(self.Esc3.get());     

        Tf=float(self.Tf_copy.get());Caf=float(self.Caf_copy.get());#self.Esc3=float(self.Esc3.get());     

#        print('type(Ca_ss)=',type(Ca_ss));print('type(T_ss)=',type(T_ss));print('type(u_ss)=',type(u_ss))
#        print('type(Kc)=',type(Kc));print('type(tauI)=',type(tauI));print('type(tauD)=',type(tauD));
#        print('type(SP1)=',type(SP1));print('type(SP2)=',type(SP2));print('type(Tf)=',type(Tf));
#        print('type(Caf)=',type(Caf));# print('type(q)=',type(q));


        x0 = np.empty(2)
        x0[0] = self.Ca_ss
        x0[1] = self.T_ss

        # Steady State Initial Condition
#       u_ss = 300.0
        # Feed Temperature (K)
#       Tf = 350
        # Feed Concentration (mol/m^3)
#       Caf = 1

        # Time Interval (min)
        t = np.linspace(0,5,501)

        # Store results for plotting
        Ca = np.ones(len(t)) * self.Ca_ss
        T = np.ones(len(t)) * self.T_ss
        u = np.ones(len(t)) * self.u_ss


        # storage for recording values
        op = np.zeros(len(t))*self.u_ss  # controller output
        pv = np.zeros(len(t))  # process variable
        e = np.zeros(len(t))   # error
        ie = np.zeros(len(t))  # integral of the error
        dpv = np.zeros(len(t)) # derivative of the pv
        P = np.zeros(len(t))   # proportional
        I = np.zeros(len(t))   # integral
        D = np.zeros(len(t))   # derivative
        sp = np.zeros(len(t))  # set point
        sp[0:100] = self.SP1
        sp[100:] = self.SP2
        #sp[150:] = 280.0

        # Upper and Lower limits on OP
        op_hi = 350.0
        op_lo = 250.0

        pv[0] = self.T_ss
        # loop through time steps    
        for i in range(len(t)-1):
            delta_t = t[i+1]-t[i]
            e[i] = sp[i] - pv[i]
            if i >= 1:  # calculate starting on second cycle
                dpv[i] = (pv[i]-pv[i-1])/delta_t
                ie[i] = ie[i-1] + e[i] * delta_t
            P[i] = self.Kc * e[i]
            I[i] = self.Kc/self.tauI * ie[i]
            D[i] = - self.Kc * self.tauD * dpv[i]
            op[i] = op[0] + P[i] + I[i] + D[i]
            if op[i] > op_hi:  # check upper limit
                op[i] = op_hi
                ie[i] = ie[i] - e[i] * delta_t # anti-reset windup
            if op[i] < op_lo:  # check lower limit
                op[i] = op_lo
                ie[i] = ie[i] - e[i] * delta_t # anti-reset windup
            ts = [t[i],t[i+1]]
            u[i+1] = op[i]
            y = odeint(self.cstr,x0,ts,args=(u[i+1],Tf,Caf))
            Ca[i+1] = y[-1][0]
            T[i+1] = y[-1][1]
            x0[0] = Ca[i+1]
            x0[1] = T[i+1]
            pv[i+1] = T[i+1]
        op[len(t)-1] = op[len(t)-2]
        ie[len(t)-1] = ie[len(t)-2]
        P[len(t)-1] = P[len(t)-2]
        I[len(t)-1] = I[len(t)-2]
        D[len(t)-1] = D[len(t)-2]

        # Construct results and save data file
        # Column 1 = time
        # Column 2 = cooling temperature
        # Column 3 = reactor temperature
        data = np.vstack((t,u,T)) # vertical stack
        data = data.T             # transpose data
        np.savetxt('data_doublet.txt',data,delimiter=',')
            
        # Plot the results
        plt.figure()
        plt.subplot(3,1,1)
        plt.plot(t,u,'b-',linewidth=3)
        plt.ylabel('Cooling T (K)')
        plt.legend(['Jacket Temperature'],loc='best')

        plt.subplot(3,1,2)
        plt.plot(t,Ca,'g-',linewidth=2)
        plt.ylabel('Ca (mol/L)')
        plt.legend(['Reactor Concentration'],loc='best')

        plt.subplot(3,1,3)
        plt.plot(t,T,'k:',linewidth=3,label='Reactor Temperature')
        plt.plot(t,sp,'r--',linewidth=2,label='Set Point')
        plt.ylabel('T (°K)')
        plt.xlabel('Time (min)')
        plt.legend(loc='best')

        plt.show()


    pass


main()

