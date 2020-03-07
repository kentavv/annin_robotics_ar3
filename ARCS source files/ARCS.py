############################################################################
## ARCS ver 1.0 ###########################################################
############################################################################
""" ARCS - Annin Robot Control Software
    Copyright (c) 2019, Chris Annin
    All rights reserved.

    You are free to share, copy and redistribute in any medium
    or format.  You are free to remix, transform and build upon
    this material.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistribution of this software in source or binary forms shall be free
          of all charges or fees to the recipient of this software.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.
        * you must give appropriate credit and indicate if changes were made. You may do
          so in any reasonable manner, but not in any way that suggests the
          licensor endorses you or your use.
		* Selling robots, robot parts, or any versions of robots or software based on this 
		  work is strictly prohibited.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL CHRIS ANNIN BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    chris.annin@gmail.com
"""
##########################################################################
### VERSION DOC ##########################################################
##########################################################################
''' 

'''
##########################################################################
##########################################################################


from tkinter import *
import tkinter.ttk
import pickle
import serial
import time
import threading
import queue
import math
import tkinter.messagebox
import webbrowser
import numpy as np
import datetime


root = Tk()
root.wm_title("ARCS - Annin Robotics Control Software Ver 1.0")
root.iconbitmap(r'AR.ico')
root.resizable(width=True, height=True)
#root.geometry('1360x720+0+0')
root.geometry('1440x720+0+0')
root.runTrue = 0

global JogStepsStat
JogStepsStat = IntVar()
global J1OpenLoopStat
J1OpenLoopStat = IntVar()
global J2OpenLoopStat
J2OpenLoopStat = IntVar()
global J3OpenLoopStat
J3OpenLoopStat = IntVar()
global J4OpenLoopStat
J4OpenLoopStat = IntVar()
global J5OpenLoopStat
J5OpenLoopStat = IntVar()
global J6OpenLoopStat
J6OpenLoopStat = IntVar()


global xboxUse

############################################################################
### DEFINE TABS ############################################################
############################################################################

#nb = tkinter.ttk.Notebook(root, width=1360, height=700)
nb = tkinter.ttk.Notebook(root, width=1440, height=700)
nb.place(x=0, y=0)

tab1 = tkinter.ttk.Frame(nb)
nb.add(tab1, text=' Main Controls ')

tab2 = tkinter.ttk.Frame(nb)
nb.add(tab2, text='  Calibration  ')

tab3 = tkinter.ttk.Frame(nb)
nb.add(tab3, text=' Inputs Outputs ')

tab4 = tkinter.ttk.Frame(nb)
nb.add(tab4, text='   Registers    ')

tab5 = tkinter.ttk.Frame(nb)
nb.add(tab5, text='   Vision    ')

tab6 = tkinter.ttk.Frame(nb)
nb.add(tab6, text='      Log      ')

tab7 = tkinter.ttk.Frame(nb)
nb.add(tab7, text='   Info    ')

tab10 = tkinter.ttk.Frame(nb)
#nb.add(tab10, text='   Testing    ')



###############################################################################################################################################################
### COMMUNICATION DEFS ################################################################################################################# COMMUNICATION DEFS ###
###############################################################################################################################################################


def setCom(): 
  try:
    global ser 
    global J1StepCur
    global J2StepCur
    global J3StepCur
    global J4StepCur
    global J5StepCur
    global J6StepCur    
    port = "COM" + comPortEntryField.get()  
    baud = 115200    
    ser = serial.Serial(port,baud)
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - COMMUNICATIONS STARTED WITH TEENSY 3.5")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
    savePosData()
  except:
    almStatusLab.config(text="UNABLE TO ESTABLISH COMMUNICATIONS WITH TEENSY 3.5", bg = "yellow")
    almStatusLab2.config(text="UNABLE TO ESTABLISH COMMUNICATIONS WITH TEENSY 3.5", bg = "yellow")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - UNABLE TO ESTABLISH COMMUNICATIONS WITH TEENSY 3.5")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
    savePosData()

def setCom2(): 
  try:
    global ser2 
    global J1StepCur
    global J2StepCur
    global J3StepCur
    global J4StepCur
    global J5StepCur
    global J6StepCur    
    port = "COM" + com2PortEntryField.get()  
    baud = 115200    
    ser2 = serial.Serial(port,baud)
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - COMMUNICATIONS STARTED WITH MEGA 2560")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
    savePosData()
  except:
    almStatusLab.config(text="UNABLE TO ESTABLISH COMMUNICATIONS WITH MEGA 2560", bg = "yellow")
    almStatusLab2.config(text="UNABLE TO ESTABLISH COMMUNICATIONS WITH MEGA 2560", bg = "yellow")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - UNABLE TO ESTABLISH COMMUNICATIONS WITH MEGA 2560")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
    savePosData()




###############################################################################################################################################################  
### EXECUTION DEFS ######################################################################################################################### EXECUTION DEFS ###  
############################################################################################################################################################### 

def runProg():
  def threadProg():
    global rowinproc
    try:
      curRow = tab1.progView.curselection()[0]
      if (curRow == 0):
        curRow=1
    except:
      curRow=1
      tab1.progView.selection_clear(0, END)
      tab1.progView.select_set(curRow)
    tab1.runTrue = 1
    while tab1.runTrue == 1:
      if (tab1.runTrue == 0):
        runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
      else:
        runStatusLab.config(text='PROGRAM RUNNING', bg = "green")
      rowinproc = 1
      executeRow()
      time.sleep(.02)	  
      selRow = tab1.progView.curselection()[0]
      last = tab1.progView.index('end')
      #removed color row coding due to speed
      #for row in range (0,selRow):
      #  tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
      #tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
      #for row in range (selRow+1,last):
      #  tab1.progView.itemconfig(row, {'fg': 'black'})
      tab1.progView.selection_clear(0, END)
      selRow += 1
      tab1.progView.select_set(selRow)
      curRow += 1
      try:
        selRow = tab1.progView.curselection()[0]
        curRowEntryField.delete(0, 'end')
        curRowEntryField.insert(0,selRow)
      except:
        curRowEntryField.delete(0, 'end')
        curRowEntryField.insert(0,"---") 
        tab1.runTrue = 0
        runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
  t = threading.Thread(target=threadProg)
  t.start()
  
def stepFwd():
    executeRow() 
    selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
      tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
    tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
    for row in range (selRow+1,last):
      tab1.progView.itemconfig(row, {'fg': 'black'})
    tab1.progView.selection_clear(0, END)
    selRow += 1
    tab1.progView.select_set(selRow)
    time.sleep(.2)
    try:
      selRow = tab1.progView.curselection()[0]
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,selRow)
    except:
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,"---")
 
def stepRev():
    executeRow()  
    selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
      tab1.progView.itemconfig(row, {'fg': 'black'})
    tab1.progView.itemconfig(selRow, {'fg': 'red'})
    for row in range (selRow+1,last):
      tab1.progView.itemconfig(row, {'fg': 'tomato2'})
    tab1.progView.selection_clear(0, END)
    selRow -= 1
    tab1.progView.select_set(selRow)
    time.sleep(.2)
    try:
      selRow = tab1.progView.curselection()[0]
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,selRow)
    except:
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,"---")  
    
def stopProg():
  lastProg = ""
  tab1.runTrue = 0 
  if (tab1.runTrue == 0):
    runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
  else:
    runStatusLab.config(text='PROGRAM RUNNING', bg = "green")  
  
def executeRow():
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global calStat
  global rowinproc
  global LineDist
  global Xv
  global Yv
  global Zv
  global commandCalc
  global blockEncPosCal
  selRow = tab1.progView.curselection()[0]
  tab1.progView.see(selRow+2)
  data = list(map(int, tab1.progView.curselection()))
  command=tab1.progView.get(data[0])
  cmdType=command[:6]
  ##Call Program##
  if (cmdType == "Call P"):
    tab1.lastRow = tab1.progView.curselection()[0]
    tab1.lastProg = ProgEntryField.get()
    programIndex = command.find("Program -")
    progNum = str(command[programIndex+10:])
    ProgEntryField.delete(0, 'end')
    ProgEntryField.insert(0,progNum)
    loadProg()
    time.sleep(.4) 
    index = 0
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(index) 
  ##Return Program##
  if (cmdType == "Return"):
    lastRow = tab1.lastRow
    lastProg = tab1.lastProg
    ProgEntryField.delete(0, 'end')
    ProgEntryField.insert(0,lastProg)
    loadProg()
    time.sleep(.4) 
    index = 0
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(lastRow)  
  ##Servo Command##
  if (cmdType == "Servo "):
    servoIndex = command.find("number ")
    posIndex = command.find("position: ")
    servoNum = str(command[servoIndex+7:posIndex-4])
    servoPos = str(command[posIndex+10:])
    command = "SV"+servoNum+"P"+servoPos+"\n"
    ser2.write(command.encode())
    ser2.flushInput()
    time.sleep(.2)
    ser2.read() 
  ##If Input On Jump to Tab##
  if (cmdType == "If On "):
    inputIndex = command.find("Input-")
    tabIndex = command.find("Tab-")
    inputNum = str(command[inputIndex+6:tabIndex-9])
    tabNum = str(command[tabIndex+4:])
    command = "JFX"+inputNum+"T"+tabNum+"\n"   
    ser2.write(command.encode())
    ser2.flushInput()
    time.sleep(.2)
    value = ser2.readline()
    if (value == b'T'):
      index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
      index = index-1
      tab1.progView.selection_clear(0, END)
      tab1.progView.select_set(index)
  ##If Input Off Jump to Tab##
  if (cmdType == "If Off"):
    inputIndex = command.find("Input-")
    tabIndex = command.find("Tab-")
    inputNum = str(command[inputIndex+6:tabIndex-9])
    tabNum = str(command[tabIndex+4:])
    command = "JFX"+inputNum+"T"+tabNum+"\n"   
    ser2.write(command.encode())
    ser2.flushInput()
    time.sleep(.2)
    value = ser2.readline()
    if (value == b'F'):
      index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
      index = index-1
      tab1.progView.selection_clear(0, END)
      tab1.progView.select_set(index)
  ##Jump to Row##
  if (cmdType == "Jump T"):
    tabIndex = command.find("Tab-")
    tabNum = str(command[tabIndex+4:])
    index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(index)  
  ##Set Output ON Command##
  if (cmdType == "Out On"):
    outputIndex = command.find("Out On = ")
    outputNum = str(command[outputIndex+9:])
    command = "ONX"+outputNum+"\n"
    ser2.write(command.encode())
    ser2.flushInput()
    time.sleep(.2)
    ser2.read() 
  ##Set Output OFF Command##
  if (cmdType == "Out Of"):
    outputIndex = command.find("Out Off = ")
    outputNum = str(command[outputIndex+10:])
    command = "OFX"+outputNum+"\n"
    ser2.write(command.encode())
    ser2.flushInput()
    time.sleep(.2)
    ser2.read() 
  ##Wait Input ON Command##
  if (cmdType == "Wait I"):
    inputIndex = command.find("Wait Input On = ")
    inputNum = str(command[inputIndex+16:])
    command = "WIN"+inputNum+"\n"
    ser2.write(command.encode())
    ser2.flushInput()
    time.sleep(.2)
    ser2.read() 
  ##Wait Input OFF Command##
  if (cmdType == "Wait O"):
    inputIndex = command.find("Wait Off Input = ")
    inputNum = str(command[inputIndex+17:])
    command = "WON"+inputNum+"\n"
    ser2.write(command.encode())
    ser2.flushInput()
    time.sleep(.2)
    ser2.read() 
  ##Wait Time Command##
  if (cmdType == "Wait T"):
    timeIndex = command.find("Wait Time = ")
    timeSeconds = str(command[timeIndex+12:])
    command = "WTS"+timeSeconds+"\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(.2)
    ser.read() 
  ##Set Register##  
  if (cmdType == "Regist"):
    regNumIndex = command.find("Register ")
    regEqIndex = command.find(" = ")
    regNumVal = str(command[regNumIndex+9:regEqIndex])
    regEntry = "R"+regNumVal+"EntryField"
    testOper = str(command[regEqIndex+3:regEqIndex+5])
    if (testOper == "++"):
      regCEqVal = str(command[regEqIndex+5:])
      curRegVal = eval(regEntry).get()
      regEqVal = str(int(regCEqVal)+int(curRegVal))      
    elif (testOper == "--"):
      regCEqVal = str(command[regEqIndex+5:])
      curRegVal = eval(regEntry).get()
      regEqVal = str(int(curRegVal)-int(regCEqVal))
    else:
      regEqVal = str(command[regEqIndex+3:])    
    eval(regEntry).delete(0, 'end')
    eval(regEntry).insert(0,regEqVal)
  ##Set Stor Position##  
  if (cmdType == "Store "):
    regNumIndex = command.find("Store Position ")
    regElIndex = command.find("Element")
    regEqIndex = command.find(" = ")
    regNumVal = str(command[regNumIndex+15:regElIndex-1])
    regNumEl = str(command[regElIndex+8:regEqIndex])
    regEntry = "SP_"+regNumVal+"_E"+regNumEl+"_EntryField"
    testOper = str(command[regEqIndex+3:regEqIndex+5])
    if (testOper == "++"):
      regCEqVal = str(command[regEqIndex+4:])
      curRegVal = eval(regEntry).get()
      regEqVal = str(float(regCEqVal)+float(curRegVal))      
    elif (testOper == "--"):
      regCEqVal = str(command[regEqIndex+5:])
      curRegVal = eval(regEntry).get()
      regEqVal = str(float(curRegVal)-float(regCEqVal))
    else:
      regEqVal = str(command[regEqIndex+3:])    
    eval(regEntry).delete(0, 'end')
    eval(regEntry).insert(0,regEqVal)
  ## Get Vision ##
  if (cmdType == "Get Vi"):
    testvis()	
  ##If Register Jump to Row##
  if (cmdType == "If Reg"):
    regIndex = command.find("If Register ")
    regEqIndex = command.find(" = ")
    regJmpIndex = command.find(" Jump to Tab ")    
    regNum = str(command[regIndex+12:regEqIndex])
    regEq = str(command[regEqIndex+3:regJmpIndex])
    tabNum = str(command[regJmpIndex+13:])
    regEntry = "R"+regNum+"EntryField"
    curRegVal = eval(regEntry).get()
    if (curRegVal == regEq):
      index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
      tab1.progView.selection_clear(0, END)
      tab1.progView.select_set(index)  
  ##Calibrate Command##   
  if (cmdType == "Calibr"):
    calRobotAll()
    if (calStat == 0):
      stopProg()
  ##Move J Command##  
  if (cmdType == "Move J"):  
    J1newIndex = command.find("X) ")
    J2newIndex = command.find("Y) ")
    J3newIndex = command.find("Z) ")
    J4newIndex = command.find("W) ")
    J5newIndex = command.find("P) ")
    J6newIndex = command.find("R) ")
    TRnewIndex = command.find("T) ")	
    SpeedIndex = command.find("Speed-")
    ACCdurIndex = command.find("Ad")
    ACCspdIndex = command.find("As")
    DECdurIndex = command.find("Dd")
    DECspdIndex = command.find("Ds")
    WristConfIndex = command.find("$")
    CX = float(command[J1newIndex+3:J2newIndex-1])
    CY = float(command[J2newIndex+3:J3newIndex-1])
    CZ = float(command[J3newIndex+3:J4newIndex-1])
    CRx = float(command[J4newIndex+3:J5newIndex-1])
    CRy = float(command[J5newIndex+3:J6newIndex-1])
    CRz = float(command[J6newIndex+3:TRnewIndex-1])
    Track = float(command[TRnewIndex+3:SpeedIndex-1])
    newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
    ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
    ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
    DECdur = command[DECdurIndex+3:DECspdIndex-1]
    DECspd = command[DECspdIndex+3:WristConfIndex-1]
    WC = command[WristConfIndex+1:]
    TCX = 0
    TCY = 0 
    TCZ = 0
    TCRx = 0
    TCRy = 0
    TCRz = 0
    Code = 0	
    MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
  ##Offs J Command##  
  if (cmdType == "OFFS J"): 
    SPnewInex = command.find("[SP:")  
    SPendInex = command.find("] [")
    J1newIndex = command.find("X) ")
    J2newIndex = command.find("Y) ")
    J3newIndex = command.find("Z) ")
    J4newIndex = command.find("W) ")
    J5newIndex = command.find("P) ")
    J6newIndex = command.find("R) ")
    TRnewIndex = command.find("T) ")	
    SpeedIndex = command.find("Speed-")
    ACCdurIndex = command.find("Ad")
    ACCspdIndex = command.find("As")
    DECdurIndex = command.find("Dd")
    DECspdIndex = command.find("Ds")
    WristConfIndex = command.find("$")
    SP = str(command[SPnewInex+4:SPendInex])
    CXa = eval("SP_"+SP+"_E1_EntryField").get()
    CYa = eval("SP_"+SP+"_E2_EntryField").get()
    CZa = eval("SP_"+SP+"_E3_EntryField").get()
    CRxa = eval("SP_"+SP+"_E4_EntryField").get()
    CRya = eval("SP_"+SP+"_E5_EntryField").get()
    CRza = eval("SP_"+SP+"_E6_EntryField").get()
    CX = float(CXa) + float(command[J1newIndex+3:J2newIndex-1])
    CY = float(CYa) + float(command[J2newIndex+3:J3newIndex-1])
    CZ = float(CZa) + float(command[J3newIndex+3:J4newIndex-1])
    CRx = float(CRxa) + float(command[J4newIndex+3:J5newIndex-1])
    CRy = float(CRya) + float(command[J5newIndex+3:J6newIndex-1])
    CRz = float(CRza) + float(command[J6newIndex+3:TRnewIndex-1])
    Track = float(command[TRnewIndex+3:SpeedIndex-1])
    newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
    ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
    ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
    DECdur = command[DECdurIndex+3:DECspdIndex-1]
    DECspd = command[DECspdIndex+3:WristConfIndex-1]
    WC = command[WristConfIndex+1:]
    TCX = 0
    TCY = 0 
    TCZ = 0
    TCRx = 0
    TCRy = 0
    TCRz = 0
    Code = 0	
    MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)   
  ##Move SP Command##  
  if (cmdType == "Move S"): 
    SPnewInex = command.find("[SP:")  
    SPendInex = command.find("] [")
    TRnewIndex = command.find("T) ")	
    SpeedIndex = command.find("Speed-")
    ACCdurIndex = command.find("Ad")
    ACCspdIndex = command.find("As")
    DECdurIndex = command.find("Dd")
    DECspdIndex = command.find("Ds")
    WristConfIndex = command.find("$")
    SP = str(command[SPnewInex+4:SPendInex])
    CX = float(eval("SP_"+SP+"_E1_EntryField").get())
    CY = float(eval("SP_"+SP+"_E2_EntryField").get())
    CZ = float(eval("SP_"+SP+"_E3_EntryField").get())
    CRx = float(eval("SP_"+SP+"_E4_EntryField").get())
    CRy = float(eval("SP_"+SP+"_E5_EntryField").get())
    CRz = float(eval("SP_"+SP+"_E6_EntryField").get())
    Track = float(command[TRnewIndex+3:SpeedIndex-1])
    newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
    ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
    ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
    DECdur = command[DECdurIndex+3:DECspdIndex-1]
    DECspd = command[DECspdIndex+3:WristConfIndex-1]
    WC = command[WristConfIndex+1:]
    TCX = 0
    TCY = 0 
    TCZ = 0
    TCRx = 0
    TCRy = 0
    TCRz = 0
    Code = 0	
    MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
  ##OFFS SP Command##  
  if (cmdType == "OFFS S"): 
    SPnewInex = command.find("[SP:")  
    SPendInex = command.find("] offs")
    SP2newInex = command.find("[*SP:")  
    SP2endInex = command.find("]  [")
    TRnewIndex = command.find("T) ")	
    SpeedIndex = command.find("Speed-")
    ACCdurIndex = command.find("Ad")
    ACCspdIndex = command.find("As")
    DECdurIndex = command.find("Dd")
    DECspdIndex = command.find("Ds")
    WristConfIndex = command.find("$")
    SP = str(command[SPnewInex+4:SPendInex])
    SP2 = str(command[SP2newInex+5:SP2endInex])
    CX = float(eval("SP_"+SP+"_E1_EntryField").get()) + float(eval("SP_"+SP2+"_E1_EntryField").get())
    CY = float(eval("SP_"+SP+"_E2_EntryField").get()) + float(eval("SP_"+SP2+"_E2_EntryField").get())
    CZ = float(eval("SP_"+SP+"_E3_EntryField").get()) + float(eval("SP_"+SP2+"_E3_EntryField").get())
    CRx = float(eval("SP_"+SP+"_E4_EntryField").get()) + float(eval("SP_"+SP2+"_E4_EntryField").get())
    CRy = float(eval("SP_"+SP+"_E5_EntryField").get()) + float(eval("SP_"+SP2+"_E5_EntryField").get())
    CRz = float(eval("SP_"+SP+"_E6_EntryField").get()) + float(eval("SP_"+SP2+"_E6_EntryField").get())	
    Track = float(command[TRnewIndex+3:SpeedIndex-1])
    newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
    ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
    ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
    DECdur = command[DECdurIndex+3:DECspdIndex-1]
    DECspd = command[DECspdIndex+3:WristConfIndex-1]
    WC = command[WristConfIndex+1:]
    TCX = 0
    TCY = 0 
    TCZ = 0
    TCRx = 0
    TCRy = 0
    TCRz = 0
    Code = 0	
    MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
  ##Move L Command##  
  if (cmdType == "Move L"): 
    blockEncPosCal = 1  
    J1newIndex = command.find("X) ")
    J2newIndex = command.find("Y) ")
    J3newIndex = command.find("Z) ")
    J4newIndex = command.find("W) ")
    J5newIndex = command.find("P) ")
    J6newIndex = command.find("R) ")
    TRnewIndex = command.find("T) ")	
    SpeedIndex = command.find("Speed-")
    ACCdurIndex = command.find("Ad")
    ACCspdIndex = command.find("As")
    DECdurIndex = command.find("Dd")
    DECspdIndex = command.find("Ds")
    WristConfIndex = command.find("$")
    CX = float(command[J1newIndex+3:J2newIndex-1])
    CY = float(command[J2newIndex+3:J3newIndex-1])
    CZ = float(command[J3newIndex+3:J4newIndex-1])
    CRx = float(command[J4newIndex+3:J5newIndex-1])
    CRy = float(command[J5newIndex+3:J6newIndex-1])
    CRz = float(command[J6newIndex+3:TRnewIndex-1])
    Track = float(command[TRnewIndex+3:SpeedIndex-1])
    newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
    ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
    ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
    DECdur = command[DECdurIndex+3:DECspdIndex-1]
    DECspd = command[DECspdIndex+3:WristConfIndex-1]
    WC = command[WristConfIndex+1:]
    TCX = 0
    TCY = 0 
    TCZ = 0
    TCRx = 0
    TCRy = 0
    TCRz = 0 
    CalcLinDist(CX,CY,CZ)
    CalcLinVect(CX,CY,CZ)
    numWayPts = 10
    #numWayPts = int(LineDist/2)
    Xstart = XcurPos
    Ystart = YcurPos
    Zstart = ZcurPos
    Rxstart = RxcurPos
    Rystart = RycurPos
    Rzstart = RzcurPos
    
    ## SPEEDS
    #ACCpts = numWayPts * (int(ACCdur)/100)
    #ACCpctInc = 100 / int(ACCpts)
    #numDECpts = (numWayPts * (int(DECdur)/100))
    #DECpts = numWayPts - numDECpts
    #DECpctInc = 100 / int(numDECpts)
    #minACC = int(newSpeed)*(int(ACCspd)/100)
    #minDEC = int(newSpeed)*(int(DECspd)/100)
    
    lACCspd = "100"
    lDECspd = "100"
    lACCdur = "1"
    lDECdur = "1"     
    
    ##GENERATE WAYPOINTS CMD	
    WayPtsCMD = "ML"+str(numWayPts)
    ser.write(WayPtsCMD.encode())
    ser.flushInput()
    time.sleep(.01)
    for i in range(numWayPts+1):
      curWayDis = (1 / numWayPts) * i
      lCX = Xstart + (Xv * curWayDis)
      lCY = Ystart + (Yv * curWayDis)
      lCZ = Zstart + (Zv * curWayDis)
      
      #if i < ACCpts:
      #  tempSpeed = str(round(((i * (ACCpctInc/100))*int(newSpeed)),2))
      #  if float(tempSpeed) < minACC:
      #    tempSpeed = str(round(minACC,2))
      #elif i > DECpts:
      #  tempSpeed = str(round((((numWayPts - i) * (DECpctInc/100))*int(newSpeed)),2))
      #  if float(tempSpeed) < minDEC:
      #    tempSpeed = str(round(minDEC,2))
      #else:
      #  tempSpeed = newSpeed



      Code = 2
        
      MoveXYZ(lCX,lCY,lCZ,CRx,CRy,CRz,newSpeed,lACCdur,lACCspd,lDECdur,lDECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
      ser.write(commandCalc.encode())  
      ser.flushInput()
      RobotCode = str(ser.readline())
      Pcode = RobotCode[2:4]
      if (Pcode == "01"):
        applyRobotCal(RobotCode) 
    blockEncPosCal = 0
    getRobotPosition()    
      
      
      
  ##Move A Command##  
  if (cmdType == "Move A"):
    subCmd=command[:10]
    if (subCmd == "Move A Mid" or subCmd == "Move A End"):
      almStatusLab.config(text="Move A must start with a Beg followed by Mid & End", bg = "red")
      almStatusLab2.config(text="Move A must start with a Beg followed by Mid & End", bg = "red")
    J1newIndex = command.find("X) ")
    J2newIndex = command.find("Y) ")
    J3newIndex = command.find("Z) ")
    J4newIndex = command.find("W) ")
    J5newIndex = command.find("P) ")
    J6newIndex = command.find("R) ")
    TRnewIndex = command.find("T) ")	
    SpeedIndex = command.find("Speed-")
    ACCdurIndex = command.find("Ad")
    ACCspdIndex = command.find("As")
    DECdurIndex = command.find("Dd")
    DECspdIndex = command.find("Ds")
    WristConfIndex = command.find("$")
    CXbeg = float(command[J1newIndex+3:J2newIndex-1])
    CYbeg = float(command[J2newIndex+3:J3newIndex-1])
    CZbeg = float(command[J3newIndex+3:J4newIndex-1])
    CRx = float(command[J4newIndex+3:J5newIndex-1])
    CRy = float(command[J5newIndex+3:J6newIndex-1])
    CRz = float(command[J6newIndex+3:TRnewIndex-1])
    Track = float(command[TRnewIndex+3:SpeedIndex-1])
    newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
    ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
    ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
    DECdur = command[DECdurIndex+3:DECspdIndex-1]
    DECspd = command[DECspdIndex+3:WristConfIndex-1]
    WC = command[WristConfIndex+1:]
    TCX = 0
    TCY = 0 
    TCZ = 0
    TCRx = 0
    TCRy = 0
    TCRz = 0
    ##read next row for Mid position	
    curRow = tab1.progView.curselection()[0]
    selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
      tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
    tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
    for row in range (selRow+1,last):
      tab1.progView.itemconfig(row, {'fg': 'black'})
    tab1.progView.selection_clear(0, END)
    selRow += 1
    tab1.progView.select_set(selRow)
    curRow += 1
    selRow = tab1.progView.curselection()[0]
    tab1.progView.see(selRow+2)
    data = list(map(int, tab1.progView.curselection()))
    command=tab1.progView.get(data[0])
    J1newIndex = command.find("X) ")
    J2newIndex = command.find("Y) ")
    J3newIndex = command.find("Z) ")
    CXmid = float(command[J1newIndex+3:J2newIndex-1])
    CYmid = float(command[J2newIndex+3:J3newIndex-1])
    CZmid = float(command[J3newIndex+3:J4newIndex-1])	
    ##read next row for End position	
    curRow = tab1.progView.curselection()[0]
    selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
      tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
    tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
    for row in range (selRow+1,last):
      tab1.progView.itemconfig(row, {'fg': 'black'})
    tab1.progView.selection_clear(0, END)
    selRow += 1
    tab1.progView.select_set(selRow)
    curRow += 1
    selRow = tab1.progView.curselection()[0]
    tab1.progView.see(selRow+2)
    data = list(map(int, tab1.progView.curselection()))
    command=tab1.progView.get(data[0])
    J1newIndex = command.find("X) ")
    J2newIndex = command.find("Y) ")
    J3newIndex = command.find("Z) ")
    CXend = float(command[J1newIndex+3:J2newIndex-1])
    CYend = float(command[J2newIndex+3:J3newIndex-1])
    CZend = float(command[J3newIndex+3:J4newIndex-1])
    ### FIND CENTER AND RADIUS OF CIRCLE
    A = np.array([CXbeg, CYbeg, CZbeg])
    B = np.array([CXmid, CYmid, CZmid])
    C = np.array([CXend, CYend, CZend])
    a = np.linalg.norm(C - B)
    b = np.linalg.norm(C - A)
    c = np.linalg.norm(B - A)
    s = (a + b + c) / 2
    R = a*b*c / 4 / np.sqrt(s * (s - a) * (s - b) * (s - c))
    b1 = a*a * (b*b + c*c - a*a)
    b2 = b*b * (a*a + c*c - b*b)
    b3 = c*c * (a*a + b*b - c*c)
    P = np.column_stack((A, B, C)).dot(np.hstack((b1, b2, b3)))
    P /= b1 + b2 + b3
    Px = P[0]
    Py = P[1]
    Pz = P[2]
	###SHIFT POINTS TO ORIGIN
    sCXbeg = CXbeg - Px
    sCYbeg = CYbeg - Py
    sCZbeg = CZbeg - Pz
    sCXmid = CXmid - Px
    sCYmid = CYmid - Py
    sCZmid = CZmid - Pz
    sCXend = CXend - Px
    sCYend = CYend - Py
    sCZend = CZend - Pz
	###FIND CROSS PRODUCT 
    a_vec = np.array([sCXbeg, sCYbeg, sCZbeg])/np.linalg.norm(np.array([sCXbeg, sCYbeg, sCZbeg]))
    b_vec = np.array([sCXend, sCYend, sCZend])/np.linalg.norm(np.array([sCXend, sCYend, sCZend]))
    axis = np.cross(a_vec, b_vec)
    ab_angle = np.arccos(np.dot(a_vec,b_vec))
    ab_angle_Deg = math.degrees(ab_angle)
	###FIND ANGLE & NUM WAYPOINTS
    numWayPts = int(ab_angle_Deg / 1)
    #numWayPts = 100
    theta_Deg = (ab_angle_Deg / (numWayPts+1))
    ###DEFINE START VECTOR
    v = [sCXbeg, sCYbeg, sCZbeg]  
    ###MOVE TO BEGINING OF ARC
    Code = 0
    MoveXYZ(CXbeg,CYbeg,CZbeg,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
    
    ## SPEEDS
    #ACCpts = numWayPts * (int(ACCdur)/100)
    #ACCpctInc = 100 / int(ACCpts)
    #numDECpts = (numWayPts * (int(DECdur)/100))
    #DECpts = numWayPts - numDECpts
    #DECpctInc = 100 / int(numDECpts)
    #minACC = int(newSpeed)*(int(ACCspd)/100)
    #minDEC = int(newSpeed)*(int(DECspd)/100)
    
    lACCspd = "100"
    lDECspd = "100"
    lACCdur = "1"
    lDECdur = "1"  
    
    ##GENERATE WAYPOINTS CMD	
    WayPtsCMD = "ML"+str(numWayPts)
    ser.write(WayPtsCMD.encode())
    ser.flushInput()

	###LOOP FIND ALL POINTS IN ARC
    cur_deg = theta_Deg
    ###START LOOP	
    for i in range(numWayPts+1):
      theta = math.radians(cur_deg) 
      new_pt = np.dot(rotation_matrix(axis, theta), v)
      lCX = round(new_pt[0] + Px,2)
      lCY = round(new_pt[1] + Py,2)
      lCZ = round(new_pt[2] + Pz,2)  
      cur_deg += theta_Deg
      
      #if i < ACCpts:
      #  tempSpeed = str(round(((i * (ACCpctInc/100))*int(newSpeed)),2))
      #  if float(tempSpeed) < minACC:
      #    tempSpeed = str(round(minACC,2))
      #elif i > DECpts:
      #  tempSpeed = str(round((((numWayPts - i) * (DECpctInc/100))*int(newSpeed)),2))
      #  if float(tempSpeed) < minDEC:
      #    tempSpeed = str(round(minDEC,2))
      #else:
      #tempSpeed = newSpeed
         
      if i >= numWayPts:  
        Code = 3
      else:
        Code = 2
        
      MoveXYZ(lCX,lCY,lCZ,CRx,CRy,CRz,newSpeed,lACCdur,lACCspd,lDECdur,lDECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
      ser.write(commandCalc.encode())	  
      ser.flushInput()
      time.sleep(.01)
      ser.read()
    ser.flushInput()
    ser.read()
    getRobotPosition()         
      
      
  ##Move C Command##  
  if (cmdType == "Move C"):
    blockEncPosCal = 1
    subCmd=command[:10]
    if (subCmd == "Move C Sta" or subCmd == "Move C Pla"):
      almStatusLab.config(text="Move C must start with a Center followed by Start & Plane", bg = "red")
      almStatusLab2.config(text="Move C must start with a Center followed by Start & Plane", bg = "red")
    J1newIndex = command.find("X) ")
    J2newIndex = command.find("Y) ")
    J3newIndex = command.find("Z) ")
    J4newIndex = command.find("W) ")
    J5newIndex = command.find("P) ")
    J6newIndex = command.find("R) ")
    TRnewIndex = command.find("T) ")	
    SpeedIndex = command.find("Speed-")
    ACCdurIndex = command.find("Ad")
    ACCspdIndex = command.find("As")
    DECdurIndex = command.find("Dd")
    DECspdIndex = command.find("Ds")
    WristConfIndex = command.find("$")
    CXbeg = float(command[J1newIndex+3:J2newIndex-1])
    CYbeg = float(command[J2newIndex+3:J3newIndex-1])
    CZbeg = float(command[J3newIndex+3:J4newIndex-1])
    CRx = float(command[J4newIndex+3:J5newIndex-1])
    CRy = float(command[J5newIndex+3:J6newIndex-1])
    CRz = float(command[J6newIndex+3:TRnewIndex-1])
    Track = float(command[TRnewIndex+3:SpeedIndex-1])
    newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
    ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
    ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
    DECdur = command[DECdurIndex+3:DECspdIndex-1]
    DECspd = command[DECspdIndex+3:WristConfIndex-1]
    WC = command[WristConfIndex+1:]
    TCX = 0
    TCY = 0 
    TCZ = 0
    TCRx = 0
    TCRy = 0
    TCRz = 0
    ##read next row for Mid position	
    curRow = tab1.progView.curselection()[0]
    selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
      tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
    tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
    for row in range (selRow+1,last):
      tab1.progView.itemconfig(row, {'fg': 'black'})
    tab1.progView.selection_clear(0, END)
    selRow += 1
    tab1.progView.select_set(selRow)
    curRow += 1
    selRow = tab1.progView.curselection()[0]
    tab1.progView.see(selRow+2)
    data = list(map(int, tab1.progView.curselection()))
    command=tab1.progView.get(data[0])
    J1newIndex = command.find("X) ")
    J2newIndex = command.find("Y) ")
    J3newIndex = command.find("Z) ")
    CXmid = float(command[J1newIndex+3:J2newIndex-1])
    CYmid = float(command[J2newIndex+3:J3newIndex-1])
    CZmid = float(command[J3newIndex+3:J4newIndex-1])	
    ##read next row for End position	
    curRow = tab1.progView.curselection()[0]
    selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
      tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
    tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
    for row in range (selRow+1,last):
      tab1.progView.itemconfig(row, {'fg': 'black'})
    tab1.progView.selection_clear(0, END)
    selRow += 1
    tab1.progView.select_set(selRow)
    curRow += 1
    selRow = tab1.progView.curselection()[0]
    tab1.progView.see(selRow+2)
    data = list(map(int, tab1.progView.curselection()))
    command=tab1.progView.get(data[0])
    J1newIndex = command.find("X) ")
    J2newIndex = command.find("Y) ")
    J3newIndex = command.find("Z) ")
    CXend = float(command[J1newIndex+3:J2newIndex-1])
    CYend = float(command[J2newIndex+3:J3newIndex-1])
    CZend = float(command[J3newIndex+3:J4newIndex-1])
	###SHIFT POINTS TO ORIGIN
    sCXmid = CXmid - CXbeg
    sCYmid = CYmid - CYbeg
    sCZmid = CZmid - CZbeg
    sCXend = CXend - CXbeg
    sCYend = CYend - CYbeg
    sCZend = CZend - CZbeg
	###FIND CROSS PRODUCT 
    a_vec = np.array([sCXmid, sCYmid, sCZmid])/np.linalg.norm(np.array([sCXmid, sCYmid, sCZmid]))
    b_vec = np.array([sCXend, sCYend, sCZend])/np.linalg.norm(np.array([sCXend, sCYend, sCZend]))
    axis = np.cross(a_vec, b_vec)
    ab_angle = np.arccos(np.dot(a_vec,b_vec))
    ab_angle_Deg = math.degrees(ab_angle)
	###FIND ANGLE & NUM WAYPOINTS
    #numWayPts = 220
    numWayPts = 120
    theta_Deg = (360 / (numWayPts))
    ###DEFINE START VECTOR
    v = [sCXmid, sCYmid, sCZmid]  
    ###MOVE TO BEGINING OF ARC
    Code = 0
    MoveXYZ(CXmid,CYmid,CZmid,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
    
    #removed 9-12-19
    ## SPEEDS
    ACCpts = numWayPts * (int(ACCdur)/100)
    ACCpctInc = 100 / int(ACCpts)
    numDECpts = (numWayPts * (int(DECdur)/100))
    DECpts = numWayPts - numDECpts
    DECpctInc = 100 / int(numDECpts)
    minACC = int(newSpeed)*(int(ACCspd)/100)
    minDEC = int(newSpeed)*(int(DECspd)/100)
    
    lACCspd = "100"
    lDECspd = "100"
    lACCdur = "1"
    lDECdur = "1"  
    
    ##GENERATE WAYPOINTS CMD	
    WayPtsCMD = "MC"+str(numWayPts)
    ser.write(WayPtsCMD.encode())
    ser.flushInput()
    time.sleep(.02)
    
	###LOOP FIND ALL POINTS IN ARC
    cur_deg = theta_Deg
    ###START LOOP
    i = 0	
    for i in range(numWayPts+1):
      theta = math.radians(cur_deg) 
      new_pt = np.dot(rotation_matrix(axis, theta), v)
      lCX = round(new_pt[0] + CXbeg,2)
      lCY = round(new_pt[1] + CYbeg,2)
      lCZ = round(new_pt[2] + CZbeg,2)  
      cur_deg += theta_Deg
      
      #removed 9-12-19
      if i < ACCpts:
        tempSpeed = str(round(((i * (ACCpctInc/100))*int(newSpeed)),2))
        if float(tempSpeed) < minACC:
          tempSpeed = str(round(minACC,2))
      elif i > DECpts:
        tempSpeed = str(round((((numWayPts - i) * (DECpctInc/100))*int(newSpeed)),2))
        if float(tempSpeed) < minDEC:
          tempSpeed = str(round(minDEC,2))
      else:
        tempSpeed = newSpeed
        
      if i >= numWayPts:  
        Code = 3
      else:
        Code = 2
      
      MoveXYZ(lCX,lCY,lCZ,CRx,CRy,CRz,newSpeed,lACCdur,lACCspd,lDECdur,lDECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
      ser.write(commandCalc.encode())
      ser.flushInput()
      RobotCode = str(ser.readline())
      Pcode = RobotCode[2:4]
      if (Pcode == "01"):
        applyRobotCal(RobotCode)   
    #ser.flushInput()
    #ser.read()
    blockEncPosCal = 0
    getRobotPosition() 
  	  
  rowinproc = 0  	  

  
def rotation_matrix(axis, theta):
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])  


  
##############################################################################################################################################################
### BUTTON JOGGING DEFS ############################################################################################################## BUTTON JOGGING DEFS ###
##############################################################################################################################################################  
 

def xbox():
  def threadxbox():
    from inputs import get_gamepad
    global xboxUse
    jogMode = 1
    if xboxUse == 0:
      xboxUse = 1
      mainMode = 1
      jogMode = 1
      grip = 0
      almStatusLab.config(text='JOGGING JOINTS 1 & 2', bg = "lightgreen")
      almStatusLab2.config(text='JOGGING JOINTS 1 & 2', bg = "lightgreen")
      xbcStatusLab.config(text='Xbox ON', bg = "lightgreen")
      ChgDis(2)
    else:
      xboxUse = 0
      almStatusLab.config(text='XBOX CONTROLLER OFF', bg = "salmon")
      almStatusLab2.config(text='XBOX CONTROLLER OFF', bg = "salmon")
      xbcStatusLab.config(text='Xbox OFF', bg = "salmon")
    while xboxUse == 1:
      try:
        events = get_gamepad()
        for event in events:
          ##DISTANCE
          if (event.code == 'ABS_RZ' and event.state >= 100):
            ChgDis(0)
          elif (event.code == 'ABS_Z' and event.state >= 100): 
            ChgDis(1)
          ##SPEED
          elif (event.code == 'BTN_TR' and event.state == 1): 
            ChgSpd(0)
          elif (event.code == 'BTN_TL' and event.state == 1): 
            ChgSpd(1)
          ##JOINT MODE
          elif (event.code == 'BTN_WEST' and event.state == 1): 
            if mainMode != 1:
              mainMode = 1
              jogMode = 1
              almStatusLab.config(text='JOGGING JOINTS 1 & 2', bg = "lightgreen")
              almStatusLab2.config(text='JOGGING JOINTS 1 & 2', bg = "lightgreen")
            else:                
              jogMode +=1        
            if jogMode == 2:
              almStatusLab.config(text='JOGGING JOINTS 3 & 4', bg = "lightgreen")
              almStatusLab2.config(text='JOGGING JOINTS 3 & 4', bg = "lightgreen")
            elif jogMode == 3:
              almStatusLab.config(text='JOGGING JOINTS 5 & 6', bg = "lightgreen")
              almStatusLab2.config(text='JOGGING JOINTS 5 & 6', bg = "lightgreen")
            elif jogMode == 4:
              jogMode = 1
              almStatusLab.config(text='JOGGING JOINTS 1 & 2', bg = "lightgreen")
              almStatusLab2.config(text='JOGGING JOINTS 1 & 2', bg = "lightgreen")
          ##JOINT JOG
          elif (mainMode == 1 and event.code == 'ABS_HAT0X' and event.state == 1 and jogMode == 1): 
            J1jogNeg()    
          elif (mainMode == 1 and event.code == 'ABS_HAT0X' and event.state == -1 and jogMode == 1): 
            J1jogPos()
          elif (mainMode == 1 and event.code == 'ABS_HAT0Y' and event.state == -1 and jogMode == 1): 
            J2jogNeg()    
          elif (mainMode == 1 and event.code == 'ABS_HAT0Y' and event.state == 1 and jogMode == 1): 
            J2jogPos()           
          elif (mainMode == 1 and event.code == 'ABS_HAT0Y' and event.state == -1 and jogMode == 2): 
            J3jogNeg()    
          elif (mainMode == 1 and event.code == 'ABS_HAT0Y' and event.state == 1 and jogMode == 2): 
            J3jogPos()
          elif (mainMode == 1 and event.code == 'ABS_HAT0X' and event.state == 1 and jogMode == 2): 
            J4jogNeg()    
          elif (mainMode == 1 and event.code == 'ABS_HAT0X' and event.state == -1 and jogMode == 2): 
            J4jogPos()           
          elif (mainMode == 1 and event.code == 'ABS_HAT0Y' and event.state == -1 and jogMode == 3): 
            J5jogNeg()    
          elif (mainMode == 1 and event.code == 'ABS_HAT0Y' and event.state == 1 and jogMode == 3): 
            J5jogPos()
          elif (mainMode == 1 and event.code == 'ABS_HAT0X' and event.state == 1 and jogMode == 3): 
           J6jogNeg()    
          elif (mainMode == 1 and event.code == 'ABS_HAT0X' and event.state == -1 and jogMode == 3): 
            J6jogPos()                      
         ##CARTESIAN DIR MODE
          elif (event.code == 'BTN_SOUTH' and event.state == 1): 
            if mainMode != 2:
              mainMode = 2
              jogMode = 1
              almStatusLab.config(text='JOGGING X & Y AXIS', bg = "lightgreen")
              almStatusLab2.config(text='JOGGING X & Y AXIS', bg = "lightgreen")
            else:                
              jogMode +=1        
            if jogMode == 2:
              almStatusLab.config(text='JOGGING Z AXIS', bg = "lightgreen")
              almStatusLab2.config(text='JOGGING Z AXIS', bg = "lightgreen")
            elif jogMode == 3:
              jogMode = 1
              almStatusLab.config(text='JOGGING X & Y AXIS', bg = "lightgreen")
              almStatusLab2.config(text='JOGGING X & Y AXIS', bg = "lightgreen")
          ##CARTESIAN DIR JOG
          elif (mainMode == 2 and event.code == 'ABS_HAT0Y' and event.state == -1 and jogMode == 1): 
            XjogNeg()    
          elif (mainMode == 2 and event.code == 'ABS_HAT0Y' and event.state == 1 and jogMode == 1): 
            XjogPos()
          elif (mainMode == 2 and event.code == 'ABS_HAT0X' and event.state == 1 and jogMode == 1): 
            YjogNeg()    
          elif (mainMode == 2 and event.code == 'ABS_HAT0X' and event.state == -1 and jogMode == 1): 
            YjogPos()           
          elif (mainMode == 2 and event.code == 'ABS_HAT0Y' and event.state == 1 and jogMode == 2): 
            ZjogNeg()    
          elif (mainMode == 2 and event.code == 'ABS_HAT0Y' and event.state == -1 and jogMode == 2): 
            ZjogPos()                          
         ##CARTESIAN ORIENTATION MODE
          elif (event.code == 'BTN_EAST' and event.state == 1): 
            if mainMode != 3:
              mainMode = 3
              jogMode = 1
              almStatusLab.config(text='JOGGING Rx & Ry AXIS', bg = "lightgreen")
              almStatusLab2.config(text='JOGGING Rx & Ry AXIS', bg = "lightgreen")
            else:                
              jogMode +=1        
            if jogMode == 2:
              almStatusLab.config(text='JOGGING Rz AXIS', bg = "lightgreen")
              almStatusLab2.config(text='JOGGING Rz AXIS', bg = "lightgreen")
            elif jogMode == 3:
              jogMode = 1
              almStatusLab.config(text='JOGGING Rx & Ry AXIS', bg = "lightgreen")
              almStatusLab2.config(text='JOGGING Rx & Ry AXIS', bg = "lightgreen")
          ##CARTESIAN ORIENTATION JOG
          elif (mainMode == 3 and event.code == 'ABS_HAT0X' and event.state == -1 and jogMode == 1): 
            RxjogNeg()    
          elif (mainMode == 3 and event.code == 'ABS_HAT0X' and event.state == 1 and jogMode == 1): 
            RxjogPos()
          elif (mainMode == 3 and event.code == 'ABS_HAT0Y' and event.state == 1 and jogMode == 1): 
            RyjogNeg()    
          elif (mainMode == 3 and event.code == 'ABS_HAT0Y' and event.state == -1 and jogMode == 1): 
            RyjogPos()           
          elif (mainMode == 3 and event.code == 'ABS_HAT0X' and event.state == 1 and jogMode == 2): 
            RzjogNeg()    
          elif (mainMode == 3 and event.code == 'ABS_HAT0X' and event.state == -1 and jogMode == 2): 
            RzjogPos()
          ##TRACK MODE
          elif (event.code == 'BTN_START' and event.state == 1): 
            mainMode = 4
            almStatusLab.config(text='JOGGING TRACK', bg = "lightgreen")
            almStatusLab2.config(text='JOGGING TRACK', bg = "lightgreen")
          ##TRACK JOG
          elif (mainMode == 4 and event.code == 'ABS_HAT0X' and event.state == 1): 
            TrackjogPos()    
          elif (mainMode == 4 and event.code == 'ABS_HAT0X' and event.state == -1): 
            TrackjogNeg()                   
          ##TEACH POS          
          elif (event.code == 'BTN_NORTH' and event.state == 1): 
            teachInsertBelSelected()
          ##GRIPPER         
          elif (event.code == 'BTN_SELECT' and event.state == 1): 
            if grip == 0:
              grip = 1
              outputNum = DO1offEntryField.get()
              command = "OFX"+outputNum+"\n"
              ser2.write(command.encode())
              ser2.flushInput()
              time.sleep(.2)
              ser2.read() 
            else:
              grip = 0
              outputNum = DO1onEntryField.get()
              command = "ONX"+outputNum+"\n"
              ser2.write(command.encode())
              ser2.flushInput()
              time.sleep(.2)
              ser2.read()     
              time.sleep(.1)
      except:
        almStatusLab.config(text='XBOX CONTROLLER NOT RESPONDING', bg = "red")
        almStatusLab2.config(text='XBOX CONTROLLER NOT RESPONDING', bg = "red")
        Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
        tab6.ElogView.insert(END, Curtime+" - "+"XBOX CONTROLLER NOT RESPONDING")
        value=tab6.ElogView.get(0,END)
        pickle.dump(value,open("ErrorLog","wb"))        
  t = threading.Thread(target=threadxbox)
  t.start()



  
def ChgDis(val):
  curSpd = int(J1jogDegsEntryField.get())
  if curSpd >=100 and val == 0:
    curSpd = 100 
  elif curSpd < 5 and val == 0:  
    curSpd += 1
  elif val == 0:
    curSpd += 5   
  if curSpd <=1 and val == 1:
    curSpd = 1 
  elif curSpd <= 5 and val == 1:  
    curSpd -= 1
  elif val == 1:
    curSpd -= 5
  elif val == 2:
    curSpd = 5  
  J1jogDegsEntryField.delete(0, 'end')
  J2jogDegsEntryField.delete(0, 'end')
  J3jogDegsEntryField.delete(0, 'end')
  J4jogDegsEntryField.delete(0, 'end')
  J5jogDegsEntryField.delete(0, 'end')
  J6jogDegsEntryField.delete(0, 'end')
  XjogEntryField.delete(0, 'end')
  YjogEntryField.delete(0, 'end')
  ZjogEntryField.delete(0, 'end')
  RxjogEntryField.delete(0, 'end')
  RyjogEntryField.delete(0, 'end')
  RzjogEntryField.delete(0, 'end')
  TXjogEntryField.delete(0, 'end')
  TYjogEntryField.delete(0, 'end')
  TZjogEntryField.delete(0, 'end')
  TRxjogEntryField.delete(0, 'end')
  TRyjogEntryField.delete(0, 'end')
  TRzjogEntryField.delete(0, 'end')
  J1jogDegsEntryField.insert(0,str(curSpd))
  J2jogDegsEntryField.insert(0,str(curSpd))
  J3jogDegsEntryField.insert(0,str(curSpd))
  J4jogDegsEntryField.insert(0,str(curSpd))
  J5jogDegsEntryField.insert(0,str(curSpd))
  J6jogDegsEntryField.insert(0,str(curSpd))
  XjogEntryField.insert(0,str(curSpd))
  YjogEntryField.insert(0,str(curSpd))
  ZjogEntryField.insert(0,str(curSpd))
  RxjogEntryField.insert(0,str(curSpd))
  RyjogEntryField.insert(0,str(curSpd))
  RzjogEntryField.insert(0,str(curSpd))
  TXjogEntryField.insert(0,str(curSpd))
  TYjogEntryField.insert(0,str(curSpd))
  TZjogEntryField.insert(0,str(curSpd))
  TRxjogEntryField.insert(0,str(curSpd))
  TRyjogEntryField.insert(0,str(curSpd))
  TRzjogEntryField.insert(0,str(curSpd))
  time.sleep(.3)  


def ChgSpd(val):
  curSpd = int(speedEntryField.get())
  if curSpd >=100 and val == 0:
    curSpd = 100 
  elif curSpd < 5 and val == 0:  
    curSpd += 1
  elif val == 0:
    curSpd += 5   
  if curSpd <=1 and val == 1:
    curSpd = 1 
  elif curSpd <= 5 and val == 1:  
    curSpd -= 1
  elif val == 1:
    curSpd -= 5
  elif val == 2:
    curSpd = 5  
  speedEntryField.delete(0, 'end')    
  speedEntryField.insert(0,str(curSpd))  
 
def J1jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J1AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1Degs = float(J1jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J1jogSteps = int(J1Degs/J1DegPerStep)
  else:
    #switch from degs to steps
    J1jogSteps = J1Degs
    J1Degs = J1Degs*J1DegPerStep
  if (J1Degs <= -(J1NegAngLim - J1AngCur)):   
    J1StepCur = J1StepCur - int(J1jogSteps)
    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJA"+J1motdir+str(J1jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode)         
  else:
    almStatusLab.config(text="J1 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J1 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J1 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()
    

def J1jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J1AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1Degs = float(J1jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J1jogSteps = int(J1Degs/J1DegPerStep)
  else:
    #switch from degs to steps
    J1jogSteps = J1Degs
    J1Degs = J1Degs*J1DegPerStep
  #calc pos dir output
  if (J1motdir == "0"):
    J1drivedir = "1"
  else:
    J1drivedir = "0"	
  if (J1Degs <= (J1PosAngLim - J1AngCur)):   
    J1StepCur = J1StepCur + int(J1jogSteps)
    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJA"+J1drivedir+str(J1jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode)  
  else:
    almStatusLab.config(text="J1 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J1 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J1 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J2jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J2AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J2Degs = float(J2jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J2jogSteps = int(J2Degs/J2DegPerStep)
  else:
    #switch from degs to steps
    J2jogSteps = J2Degs
    J2Degs = J2Degs*J2DegPerStep
  if (J2Degs <= -(J2NegAngLim - J2AngCur)):  
    J2StepCur = J2StepCur - int(J2jogSteps)
    J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJB"+J2motdir+str(J2jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J2 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J2 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J2 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J2jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J2AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J2Degs = float(J2jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J2jogSteps = int(J2Degs/J2DegPerStep)
  else:
    #switch from degs to steps
    J2jogSteps = J2Degs
    J2Degs = J2Degs*J2DegPerStep
  #calc pos dir output
  if (J2motdir == "0"):
    J2drivedir = "1"
  else:
    J2drivedir = "0"	
  if (J2Degs <= (J2PosAngLim - J2AngCur)):  
    J2StepCur = J2StepCur + int(J2jogSteps)
    J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJB"+J2drivedir+str(J2jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J2 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J2 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J2 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()
   
def J3jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J3AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J3Degs = float(J3jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J3jogSteps = int(J3Degs/J3DegPerStep)
  else:
    #switch from degs to steps
    J3jogSteps = J3Degs
    J3Degs = J3Degs*J3DegPerStep
  if (J3Degs <= -(J3NegAngLim - J3AngCur)): 
    J3StepCur = J3StepCur - int(J3jogSteps)
    J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJC"+J3motdir+str(J3jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J3 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J3 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J3 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J3jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J3AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J3Degs = float(J3jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J3jogSteps = int(J3Degs/J3DegPerStep)
  else:
    #switch from degs to steps
    J3jogSteps = J3Degs
    J3Degs = J3Degs*J3DegPerStep
  #calc pos dir output
  if (J3motdir == "0"):
    J3drivedir = "1"
  else:
    J3drivedir = "0"	
  if (J3Degs <= (J3PosAngLim - J3AngCur)):  
    J3StepCur = J3StepCur + int(J3jogSteps)
    J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJC"+J3drivedir+str(J3jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J3 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J3 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J3 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J4jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J4AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J4Degs = float(J4jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J4jogSteps = int(J4Degs/J4DegPerStep)
  else:
    #switch from degs to steps
    J4jogSteps = J4Degs
    J4Degs = J4Degs*J4DegPerStep
  if (J4Degs <= -(J4NegAngLim - J4AngCur)):  
    J4StepCur = J4StepCur - int(J4jogSteps)
    J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJD"+J4motdir+str(J4jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())	
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J4 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J4 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J4 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J4jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J4AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J4Degs = float(J4jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J4jogSteps = int(J4Degs/J4DegPerStep)
  else:
    #switch from degs to steps
    J4jogSteps = J4Degs
    J4Degs = J4Degs*J4DegPerStep
  #calc pos dir output
  if (J4motdir == "0"):
    J4drivedir = "1"
  else:
    J4drivedir = "0"	
  if (J4Degs <= (J4PosAngLim - J4AngCur)):  
    J4StepCur = J4StepCur + int(J4jogSteps)
    J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJD"+J4drivedir+str(J4jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J4 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J4 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J4 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()  
   
def J5jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J5AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J5Degs = float(J5jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J5jogSteps = int(J5Degs/J5DegPerStep)
  else:
    #switch from degs to steps
    J5jogSteps = J5Degs
    J5Degs = J5Degs*J5DegPerStep
  if (J5Degs <= -(J5NegAngLim - J5AngCur)):  
    J5StepCur = J5StepCur - int(J5jogSteps)
    J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJE"+J5motdir+str(J5jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J5 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J5 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J5 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J5jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J5AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J5Degs = float(J5jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J5jogSteps = int(J5Degs/J5DegPerStep)
  else:
    #switch from degs to steps
    J5jogSteps = J5Degs
    J5Degs = J5Degs*J5DegPerStep
  #calc pos dir output
  if (J5motdir == "0"):
    J5drivedir = "1"
  else:
    J5drivedir = "0"	
  if (J5Degs <= (J5PosAngLim - J5AngCur)):  
    J5StepCur = J5StepCur + int(J5jogSteps)
    J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJE"+J5drivedir+str(J5jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J5 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J5 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J5 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()
   
def J6jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J6AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J6Degs = float(J6jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J6jogSteps = int(J6Degs/J6DegPerStep)
  else:
    #switch from degs to steps
    J6jogSteps = J6Degs
    J6Degs = J6Degs*J6DegPerStep
  if (J6Degs <= -(J6NegAngLim - J6AngCur)):  
    J6StepCur = J6StepCur - int(J6jogSteps)
    J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJF"+J6motdir+str(J6jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())	
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J6 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J6 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J6 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J6jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J6AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J6Degs = float(J6jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J6jogSteps = int(J6Degs/J6DegPerStep)
  else:
    #switch from degs to steps
    J6jogSteps = J6Degs
    J6Degs = J6Degs*J6DegPerStep
  #calc pos dir output
  if (J6motdir == "0"):
    J6drivedir = "1"
  else:
    J6drivedir = "0"	
  if (J6Degs <= (J6PosAngLim - J6AngCur)): 
    J6StepCur = J6StepCur + int(J6jogSteps)
    J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJF"+J6drivedir+str(J6jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())	
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J6 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J6 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J6 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def XjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos - float(XjogEntryField.get())
  CY = YcurPos 
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0 
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def YjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos - float(YjogEntryField.get())
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0 
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def ZjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos - float(ZjogEntryField.get())
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RxjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos - float(RxjogEntryField.get())
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RyjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos - float(RyjogEntryField.get())
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RzjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos - float(RzjogEntryField.get())
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def XjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos + float(XjogEntryField.get())
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def YjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos + float(YjogEntryField.get())
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def ZjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos + float(ZjogEntryField.get())
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RxjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos + float(RxjogEntryField.get())
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RyjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos + float(RyjogEntryField.get())
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RzjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos + float(RzjogEntryField.get())
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TrackjogNeg():
  global TrackcurPos
  global TrackLength
  global TrackStepLim
  if xboxUse != 1:  
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CT = float(TrackjogEntryField.get())
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  if JogStepsStat.get() == 1:
    TrackSteps = TrackjogEntryField.get()
  else:
    TrackSteps = str(int((TrackStepLim/TrackLength)*CT))
  if (TrackcurPos - (float(TrackSteps) * (TrackLength/TrackStepLim)) >= 0):
    command = "MJT0"+TrackSteps+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  	
    TrackcurPos = TrackcurPos - (float(TrackSteps) * (TrackLength/TrackStepLim))
    TrackcurEntryField.delete(0, 'end')  
    TrackcurEntryField.insert(0,str(TrackcurPos))
    savePosData()
  else:
    almStatusLab.config(text="TRACK NEG TRAVEL LIMIT", bg = "red")
    almStatusLab2.config(text="TRACK NEG TRAVEL LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"TRACK NEG TRAVEL LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))

def TrackjogPos():
  global TrackcurPos
  global TrackLength
  global TrackStepLim
  if xboxUse != 1:  
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CT = float(TrackjogEntryField.get())
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  if JogStepsStat.get() == 1:
    TrackSteps = TrackjogEntryField.get()
  else:
    TrackSteps = str(int((TrackStepLim/TrackLength)*CT))
  if (TrackcurPos + (float(TrackSteps) * (TrackLength/TrackStepLim)) <= TrackLength):
    command = "MJT1"+TrackSteps+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()
    TrackcurPos = TrackcurPos + (float(TrackSteps) * (TrackLength/TrackStepLim))
    TrackcurEntryField.delete(0, 'end')  
    TrackcurEntryField.insert(0,str(TrackcurPos))
    savePosData()
  else:
    almStatusLab.config(text="TRACK POS TRAVEL LIMIT", bg = "red")
    almStatusLab2.config(text="TRACK POS TRAVEL LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"TRACK POS TRAVEL LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))    
  
def TXjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos 
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0 - float(TXjogEntryField.get())
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TYjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 - float(TYjogEntryField.get()) 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TZjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0 - float(TZjogEntryField.get())
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRxjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0 - float(TRxjogEntryField.get())
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRyjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0 - float(TRyjogEntryField.get())
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRzjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0 - float(TRzjogEntryField.get())
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TXjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0 + float(TXjogEntryField.get())
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TYjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 + float(TYjogEntryField.get()) 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TZjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0 + float(TZjogEntryField.get())
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRxjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0 + float(TRxjogEntryField.get())
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRyjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0 + float(TRyjogEntryField.get())
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRzjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0 + float(TRzjogEntryField.get())
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
  
  
##############################################################################################################################################################  
### TEACH DEFS ################################################################################################################################ TEACH DEFS ###
##############################################################################################################################################################  

def teachInsertBelSelected():
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global WC
  global TrackcurPos
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1AngWrite = str(round(XcurPos,3))
  J2AngWrite = str(round(YcurPos,3))
  J3AngWrite = str(round(ZcurPos,3))
  J4AngWrite = str(round(RxcurPos,3))
  J5AngWrite = str(round(RycurPos,3))
  J6AngWrite = str(round(RzcurPos,3))
  TrackPosWrite = str(round(TrackcurPos,3))
  movetype = options.get()
  if(movetype == "OFFS J"):
    movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"]"
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move SP"):
    movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"]"
    newPos = movetype + " [*]  T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "OFFS SP"):
    movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"] offs [*SP:"+str(int(SavePosEntryField.get())+1)+"] "
    newPos = movetype + " [*]  T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move J"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move L"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move A Beg"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move A Mid"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite                 
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))	
  elif(movetype == "Move A End"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))	
  elif(movetype == "Move C Center"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move C Start"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite                 
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))	
  elif(movetype == "Move C Plane"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Teach SP"):
    SP = str(SavePosEntryField.get())
    SPE6 = "Store Position "+SP+" Element 6 = "+str(round(RzcurPos,3))         
    tab1.progView.insert(selRow, SPE6)	
    SPE5 = "Store Position "+SP+" Element 5 = "+str(round(RycurPos,3))            
    tab1.progView.insert(selRow, SPE5)
    SPE4 = "Store Position "+SP+" Element 4 = "+str(round(RxcurPos,3))           
    tab1.progView.insert(selRow, SPE4)	
    SPE3 = "Store Position "+SP+" Element 3 = "+str(round(ZcurPos,3))        
    tab1.progView.insert(selRow, SPE3)	
    SPE2 = "Store Position "+SP+" Element 2 = "+str(round(YcurPos,3))            
    tab1.progView.insert(selRow, SPE2)	
    SPE1 = "Store Position "+SP+" Element 1 = "+str(round(XcurPos,3))         
    tab1.progView.insert(selRow, SPE1)   	
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))

def teachReplaceSelected():
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global WC
  global TrackcurPos  
  selRow = tab1.progView.curselection()[0]
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1AngWrite = str(round(XcurPos,3))
  J2AngWrite = str(round(YcurPos,3))
  J3AngWrite = str(round(ZcurPos,3))
  J4AngWrite = str(round(RxcurPos,3))
  J5AngWrite = str(round(RycurPos,3))
  J6AngWrite = str(round(RzcurPos,3))
  TrackPosWrite = str(round(TrackcurPos,3))
  movetype = options.get()
  if(movetype[:-2]== "OFFS"):
    movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"]"
  newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
  tab1.progView.insert(selRow, newPos)
  selection = tab1.progView.curselection()
  tab1.progView.delete(selection[0]) 
  tab1.progView.select_set(selRow)
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def teachFineCal():
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global WC
  global TrackcurPos
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1AngWrite = str(round(XcurPos,3))
  J2AngWrite = str(round(YcurPos,3))
  J3AngWrite = str(round(ZcurPos,3))
  J4AngWrite = str(round(RxcurPos,3))
  J5AngWrite = str(round(RycurPos,3))
  J6AngWrite = str(round(RzcurPos,3))
  TrackPosWrite = str(round(TrackcurPos,3))
  newPos = "Move J [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
  fineCalEntryField.delete(0, 'end')   
  fineCalEntryField.insert(0,str(newPos))
  savePosData()
  almStatusLab.config(text="NEW FINE CALIBRATION POSITION TAUGHT", bg = "blue")
  almStatusLab2.config(text="NEW FINE CALIBRATION POSITION TAUGHT", bg = "blue")
  Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
  tab6.ElogView.insert(END, Curtime+" - "+"NEW FINE CALIBRATION POSITION TAUGHT")
  value=tab6.ElogView.get(0,END)
  pickle.dump(value,open("ErrorLog","wb"))
 

############################################################################################################################################################## 
### PROGRAM FUNCTION DEFS ########################################################################################################## PROGRAM FUNCTION DEFS ###
############################################################################################################################################################## 
  
def deleteitem():
  selRow = tab1.progView.curselection()[0]
  selection = tab1.progView.curselection()  
  tab1.progView.delete(selection[0])
  tab1.progView.select_set(selRow)  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))  
  
def manInsItem():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow) 
  tab1.progView.insert(selRow, manEntryField.get())
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow) 
  selRow = tab1.progView.curselection()[0]
  curRowEntryField.delete(0, 'end')
  curRowEntryField.insert(0,selRow)
  tab1.progView.itemconfig(selRow, {'fg': 'darkgreen'})
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  
def manReplItem():
  #selRow = curRowEntryField.get()
  selRow = tab1.progView.curselection()[0]
  tab1.progView.delete(selRow) 
  tab1.progView.insert(selRow, manEntryField.get())
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow)
  tab1.progView.itemconfig(selRow, {'fg': 'darkgreen'})  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  
def waitTime():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  seconds = waitTimeEntryField.get()
  newTime = "Wait Time = "+seconds               
  tab1.progView.insert(selRow, newTime)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))


def waitInputOn():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  input = waitInputEntryField.get()
  newInput = "Wait Input On = "+input              
  tab1.progView.insert(selRow, newInput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def waitInputOff():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  input = waitInputOffEntryField.get()
  newInput = "Wait Off Input = "+input              
  tab1.progView.insert(selRow, newInput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def setOutputOn():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  output = outputOnEntryField.get()
  newOutput = "Out On = "+output              
  tab1.progView.insert(selRow, newOutput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def setOutputOff():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  output = outputOffEntryField.get()
  newOutput = "Out Off = "+output              
  tab1.progView.insert(selRow, newOutput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def tabNumber():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  tabNum = tabNumEntryField.get()
  tabins = "Tab Number "+tabNum              
  tab1.progView.insert(selRow, tabins) 
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def jumpTab():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  tabNum = jumpTabEntryField.get()
  tabjmp = "Jump Tab-"+tabNum              
  tab1.progView.insert(selRow, tabjmp) 
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')
 
def getvision():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  value = "Get Vision"
  tab1.progView.insert(selRow, value) 
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  
def IfOnjumpTab():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  inpNum = IfOnjumpInputTabEntryField.get()
  tabNum = IfOnjumpNumberTabEntryField.get()
  tabjmp = "If On Jump - Input-"+inpNum+" Jump to Tab-"+tabNum             
  tab1.progView.insert(selRow, tabjmp)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def IfOffjumpTab():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  inpNum = IfOffjumpInputTabEntryField.get()
  tabNum = IfOffjumpNumberTabEntryField.get()
  tabjmp = "If Off Jump - Input-"+inpNum+" Jump to Tab-"+tabNum             
  tab1.progView.insert(selRow, tabjmp) 
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def Servo():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  servoNum = servoNumEntryField.get()
  servoPos = servoPosEntryField.get()
  servoins = "Servo number "+servoNum+" to position: "+servoPos              
  tab1.progView.insert(selRow, servoins)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def loadProg():
  progframe=Frame(tab1)
  progframe.place(x=7,y=174)
  #progframe.pack(side=RIGHT, fill=Y)
  scrollbar = Scrollbar(progframe) 
  scrollbar.pack(side=RIGHT, fill=Y)
  tab1.progView = Listbox(progframe,width=84,height=31, yscrollcommand=scrollbar.set)
  tab1.progView.bind('<<ListboxSelect>>', progViewselect)
  try:
    Prog = pickle.load(open(ProgEntryField.get(),"rb"))
  except:
    try:
      Prog = ['##BEGINNING OF PROGRAM##','Tab Number 1']
      pickle.dump(Prog,open(ProgEntryField.get(),"wb"))    
    except:
      Prog = ['##BEGINNING OF PROGRAM##','Tab Number 1']
      pickle.dump(Prog,open("new","wb"))
      ProgEntryField.insert(0,"new")
  time.sleep(.2)
  for item in Prog:
    tab1.progView.insert(END,item) 
  tab1.progView.pack()
  scrollbar.config(command=tab1.progView.yview)
  savePosData()

def insertCallProg():  
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  newProg = changeProgEntryField.get()
  changeProg = "Call Program - "+newProg            
  tab1.progView.insert(selRow, changeProg)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def insertReturn():  
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  value = "Return"           
  tab1.progView.insert(selRow, value)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def IfRegjumpTab():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  regNum = regNumJmpEntryField.get()
  regEqNum = regEqJmpEntryField.get()
  tabNum = regTabJmpEntryField.get()
  tabjmp = "If Register "+regNum+" = "+regEqNum+" Jump to Tab "+ tabNum            
  tab1.progView.insert(selRow, tabjmp)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def insertRegister():  
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  regNum = regNumEntryField.get()
  regCmd = regEqEntryField.get()
  regIns = "Register "+regNum+" = "+regCmd             
  tab1.progView.insert(selRow, regIns)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')
  
def storPos():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  regNum = storPosNumEntryField.get()
  regElmnt = storPosElEntryField.get()
  regCmd = storPosValEntryField.get()
  regIns = "Store Position "+regNum+" Element "+regElmnt+" = "+regCmd             
  tab1.progView.insert(selRow, regIns)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')
  
def insCalibrate():  
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  insCal = "Calibrate Robot"          
  tab1.progView.insert(selRow, insCal)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def progViewselect(e):
  selRow = tab1.progView.curselection()[0]
  curRowEntryField.delete(0, 'end')
  curRowEntryField.insert(0,selRow)
  

def getSel():
  selRow = tab1.progView.curselection()[0]
  tab1.progView.see(selRow+2)
  data = list(map(int, tab1.progView.curselection()))
  command=tab1.progView.get(data[0])
  manEntryField.delete(0, 'end')
  manEntryField.insert(0, command)  
  
def Servo0on():
  savePosData() 
  servoPos = servo0onEntryField.get()
  command = "SV0P"+servoPos+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read()


def Servo0off():
  savePosData() 
  servoPos = servo0offEntryField.get()
  command = "SV0P"+servoPos+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read()


def Servo1on():
  savePosData() 
  servoPos = servo1onEntryField.get()
  command = "SV1P"+servoPos+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 


def Servo1off():
  savePosData() 
  servoPos = servo1offEntryField.get()
  command = "SV1P"+servoPos+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read()
 

def Servo2on():
  savePosData() 
  servoPos = servo2onEntryField.get()
  command = "SV2P"+servoPos+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 


def Servo2off():
  savePosData() 
  servoPos = servo2offEntryField.get()
  command = "SV2P"+servoPos+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read()

def Servo3on():
  savePosData() 
  servoPos = servo3onEntryField.get()
  command = "SV3P"+servoPos+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser.read() 

def Servo3off():
  savePosData() 
  servoPos = servo3offEntryField.get()
  command = "SV3P"+servoPos+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser.read()

def DO1on():
  outputNum = DO1onEntryField.get()
  command = "ONX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 


def DO1off():
  outputNum = DO1offEntryField.get()
  command = "OFX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 
 

def DO2on():
  outputNum = DO2onEntryField.get()
  command = "ONX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read()
 

def DO2off():
  outputNum = DO2offEntryField.get()
  command = "OFX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 


def DO3on():
  outputNum = DO3onEntryField.get()
  command = "ONX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 


def DO3off():
  outputNum = DO3offEntryField.get()
  command = "OFX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 
 

def DO4on():
  outputNum = DO4onEntryField.get()
  command = "ONX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read()
 

def DO4off():
  outputNum = DO4offEntryField.get()
  command = "OFX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 


def DO5on():
  outputNum = DO5onEntryField.get()
  command = "ONX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 


def DO5off():
  outputNum = DO5offEntryField.get()
  command = "OFX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 
 

def DO6on():
  outputNum = DO6onEntryField.get()
  command = "ONX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read()
 

def DO6off():
  outputNum = DO6offEntryField.get()
  command = "OFX"+outputNum+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(.2)
  ser2.read() 
  
def TestString():
  message = testSendEntryField.get()
  command = "TM"+message+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(0)
  echo = ser2.readline()
  testRecEntryField.delete(0, 'end')
  testRecEntryField.insert(0,echo)  

def ClearTestString():
  testRecEntryField.delete(0, 'end')
  
def CalcLinDist(X2,Y2,Z2):
  global XcurPos
  global YcurPos
  global ZcurPos
  global LineDist
  X1 = XcurPos
  Y1 = YcurPos
  Z1 = ZcurPos
  LineDist = (((X2-X1)**2)+((Y2-Y1)**2)+((Z2-Z1)**2))**.5
  return (LineDist)

def CalcLinVect(X2,Y2,Z2):
  global XcurPos
  global YcurPos
  global ZcurPos
  global Xv
  global Yv
  global Zv
  X1 = XcurPos
  Y1 = YcurPos
  Z1 = ZcurPos
  Xv = X2-X1
  Yv = Y2-Y1
  Zv = Z2-Z1
  return (Xv,Yv,Zv)  

def CalcLinWayPt(CX,CY,CZ,curWayPt,):
  global XcurPos
  global YcurPos
  global ZcurPos

 

##############################################################################################################################################################
### KINEMATIC DEFS ######################################################################################################################## KINEMATIC DEFS ###
##############################################################################################################################################################

def CalcFwdKin(): 
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  global WC
  if (J1AngCur == 0):
    J1AngCur = .0001
  if (J2AngCur == 0):
    J2AngCur = .0001
  if (J3AngCur == 0):
    J3AngCur = .0001
  if (J4AngCur == 0):
    J4AngCur = .0001
  if (J5AngCur == 0):
    J5AngCur = .0001
  if (J6AngCur == 0):
    J6AngCur = .0001  
  ## Set Wrist Config
  if (J5AngCur > 0):
    WC = "F"
  else:
    WC = "N"
  ## CONVERT TO RADIANS
  C4 = math.radians(float(J1AngCur)+DHt1)
  C5 = math.radians(float(J2AngCur)+DHt2)
  C6 = math.radians(float(J3AngCur)+DHt3)
  C7 = math.radians(float(J4AngCur)+DHt4)
  C8 = math.radians(float(J5AngCur)+DHt5)
  C9 = math.radians(float(J6AngCur)+DHt6)
  ## DH TABLE
  C13 = C4
  C14 = C5
  C15 = C6
  C16 = C7
  C17 = C8
  C18 = C9
  D13 = math.radians(DHr1)
  D14 = math.radians(DHr2)
  D15 = math.radians(DHr3)
  D16 = math.radians(DHr4)
  D17 = math.radians(DHr5)
  D18 = math.radians(DHr6)
  E13 = DHd1
  E14 = DHd2
  E15 = DHd3
  E16 = DHd4
  E17 = DHd5
  E18 = DHd6
  F13 = DHa1
  F14 = DHa2
  F15 = DHa3
  F16 = DHa4
  F17 = DHa5
  F18 = DHa6
  ## WORK FRAME INPUT
  H13 = float(UFxEntryField.get()) 
  H14 = float(UFyEntryField.get())  
  H15 = float(UFzEntryField.get())
  H16 = float(UFrxEntryField.get()) 
  H17 = float(UFryEntryField.get()) 
  H18 = float(UFrzEntryField.get()) 
  ## TOOL FRAME INPUT
  J13 = float(TFxEntryField.get()) 
  J14 = float(TFyEntryField.get())  
  J15 = float(TFzEntryField.get())
  J16 = float(TFrxEntryField.get()) 
  J17 = float(TFryEntryField.get()) 
  J18 = float(TFrzEntryField.get())
  ## WORK FRAME TABLE
  B21 = math.cos(math.radians(H18))*math.cos(math.radians(H17))
  B22 = math.sin(math.radians(H18))*math.cos(math.radians(H17))
  B23 = -math.sin(math.radians(H18))
  B24 = 0
  C21 = -math.sin(math.radians(H18))*math.cos(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  C22 = math.cos(math.radians(H18))*math.cos(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  C23 = math.cos(math.radians(H17))*math.sin(math.radians(H16))
  C24 = 0
  D21 = math.sin(math.radians(H18))*math.sin(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  D22 = -math.cos(math.radians(H18))*math.sin(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  D23 = math.cos(math.radians(H17))*math.cos(math.radians(H16))
  D24 = 0
  E21 = H13
  E22 = H14
  E23 = H15
  E24 = 1 
  ## J1 FRAME
  B27 = math.cos(C13)
  B28 = math.sin(C13)
  B29 = 0
  B30 = 0
  C27 = -math.sin(C13)*math.cos(D13)
  C28 = math.cos(C13)*math.cos(D13)
  C29 = math.sin(D13)
  C30 = 0  
  D27 = math.sin(C13)*math.sin(D13)
  D28 = -math.cos(C13)*math.sin(D13)
  D29 = math.cos(D13)
  D30 = 0 
  E27 = F13*math.cos(C13)
  E28 = F13*math.sin(C13)
  E29 = E13
  E30 = 1
  ## J2 FRAME
  B33 = math.cos(C14)
  B34 = math.sin(C14)
  B35 = 0
  B36 = 0
  C33 = -math.sin(C14)*math.cos(D14)
  C34 = math.cos(C14)*math.cos(D14)
  C35 = math.sin(D14)
  C36 = 0
  D33 = math.sin(C14)*math.sin(D14)
  D34 = -math.cos(C14)*math.sin(D14)
  D35 = math.cos(D14)
  D36 = 0
  E33 = F14*math.cos(C14)
  E34 = F14*math.sin(C14)
  E35 = E14
  E36 = 1
  ## J3 FRAME 
  B39 = math.cos(C15)
  B40 = math.sin(C15)
  B41 = 0
  B42 = 0
  C39 = -math.sin(C15)*math.cos(D15)
  C40 = math.cos(C15)*math.cos(D15)
  C41 = math.sin(D15)
  C42 = 0
  D39 = math.sin(C15)*math.sin(D15)
  D40 = -math.cos(C15)*math.sin(D15)
  D41 = math.cos(D15)
  D42 = 0
  E39 = F15*math.cos(C15)
  E40 = F15*math.sin(C15)
  E41 = 0
  E42 = 1
  ## J4 FRAME 
  B45 = math.cos(C16)
  B46 = math.sin(C16)
  B47 = 0
  B48 = 0
  C45 = -math.sin(C16)*math.cos(D16)
  C46 = math.cos(C16)*math.cos(D16)
  C47 = math.sin(D16)
  C48 = 0
  D45 = math.sin(C16)*math.sin(D16)
  D46 = -math.cos(C16)*math.sin(D16)
  D47 = math.cos(D16)
  D48 = 0
  E45 = F16*math.cos(C16)
  E46 = F16*math.sin(C16)
  E47 = E16
  E48 = 1
  ## J5 FRAME 
  B51 = math.cos(C17)
  B52 = math.sin(C17)
  B53 = 0
  B54 = 0
  C51 = -math.sin(C17)*math.cos(D17)
  C52 = math.cos(C17)*math.cos(D17)
  C53 = math.sin(D17)
  C54 = 0 
  D51 = math.sin(C17)*math.sin(D17)
  D52 = -math.cos(C17)*math.sin(D17)
  D53 = math.cos(D17)
  D54 = 0
  E51 = F17*math.cos(C17)
  E52 = F17*math.sin(C17)
  E53 = E17
  E54 = 1
  ## J6 FRAME
  B57 = math.cos(C18)
  B58 = math.sin(C18)
  B59 = 0
  B60 = 0
  C57 = -math.sin(C18)*math.cos(D18)
  C58 = math.cos(C18)*math.cos(D18)
  C59 = math.sin(D18)
  C60 = 0
  D57 = math.sin(C18)*math.sin(D18)
  D58 = -math.cos(C18)*math.sin(D18)
  D59 = math.cos(D18)
  D60 = 0
  E57 = F18*math.cos(C18)
  E58 = F18*math.sin(C18)
  E59 = E18
  E60 = 1
  ## TOOL FRAME
  B63 = math.cos(math.radians(J18))*math.cos(math.radians(J17))
  B64 = math.sin(math.radians(J18))*math.cos(math.radians(J17))
  B65 = -math.sin(math.radians(J18))
  B66 = 0
  C63 = -math.sin(math.radians(J18))*math.cos(math.radians(J16))+math.cos(math.radians(J18))*math.sin(math.radians(J17))*math.sin(math.radians(J16))
  C64 = math.cos(math.radians(J18))*math.cos(math.radians(J16))+math.sin(math.radians(J18))*math.sin(math.radians(J17))*math.sin(math.radians(J16))
  C65 = math.cos(math.radians(J17))*math.sin(math.radians(J16))
  C66 = 0
  D63 = math.sin(math.radians(J18))*math.sin(math.radians(J16))+math.cos(math.radians(J18))*math.sin(math.radians(J17))*math.cos(math.radians(J16))
  D64 = -math.cos(math.radians(J18))*math.sin(math.radians(J16))+math.sin(math.radians(J18))*math.sin(math.radians(J17))*math.cos(math.radians(J16))
  D65 = math.cos(math.radians(J17))*math.cos(math.radians(J16))
  D66 = 0
  E63 = J13
  E64 = J14
  E65 = J15
  E66 = 1
  ## WF*J1
  G24 = (B21*B27)+(C21*B28)+(D21*B29)+(E21*B30)
  G25 = (B22*B27)+(C22*B28)+(D22*B29)+(E22*B30)
  G26 = (B23*B27)+(C23*B28)+(D23*B29)+(E23*B30)
  G27 = (B24*B27)+(C24*B28)+(D24*B29)+(E24*B30)
  H24 = (B21*C27)+(C21*C28)+(D21*C29)+(E21*C30)
  H25 = (B22*C27)+(C22*C28)+(D22*C29)+(E22*C30)
  H26 = (B23*C27)+(C23*C28)+(D23*C29)+(E23*C30)
  H27 = (B24*C27)+(C24*C28)+(D24*C29)+(E24*C30)
  I24 = (B21*D27)+(C21*D28)+(D21*D29)+(E21*D30)
  I25 = (B22*D27)+(C22*D28)+(D22*D29)+(E22*D30)
  I26 = (B23*D27)+(C23*D28)+(D23*D29)+(E23*D30)
  I27 = (B24*D27)+(C24*D28)+(D24*D29)+(E24*D30)
  J24 = (B21*E27)+(C21*E28)+(D21*E29)+(E21*E30)
  J25 = (B22*E27)+(C22*E28)+(D22*E29)+(E22*E30)
  J26 = (B23*E27)+(C23*E28)+(D23*E29)+(E23*E30)
  J27 = (B24*E27)+(C24*E28)+(D24*E29)+(E24*E30)
  ## (WF*J1)*J2
  G30 = (G24*B33)+(H24*B34)+(I24*B35)+(J24*B36)
  G31 = (G25*B33)+(H25*B34)+(I25*B35)+(J25*B36)
  G32 = (G26*B33)+(H26*B34)+(I26*B35)+(J26*B36)
  G33 = (G27*B33)+(H27*B34)+(I27*B35)+(J27*B36)
  H30 = (G24*C33)+(H24*C34)+(I24*C35)+(J24*C36)
  H31 = (G25*C33)+(H25*C34)+(I25*C35)+(J25*C36)
  H32 = (G26*C33)+(H26*C34)+(I26*C35)+(J26*C36)
  H33 = (G27*C33)+(H27*C34)+(I27*C35)+(J27*C36)
  I30 = (G24*D33)+(H24*D34)+(I24*D35)+(J24*D36)
  I31 = (G25*D33)+(H25*D34)+(I25*D35)+(J25*D36)
  I32 = (G26*D33)+(H26*D34)+(I26*D35)+(J26*D36)
  I33 = (G27*D33)+(H27*D34)+(I27*D35)+(J27*D36)
  J30 = (G24*E33)+(H24*E34)+(I24*E35)+(J24*E36)
  J31 = (G25*E33)+(H25*E34)+(I25*E35)+(J25*E36)
  J32 = (G26*E33)+(H26*E34)+(I26*E35)+(J26*E36)
  J33 = (G27*E33)+(H27*E34)+(I27*E35)+(J27*E36)
  ## (WF*J1*J2)*J3
  G36 = (G30*B39)+(H30*B40)+(I30*B41)+(J30*B42) 
  G37 = (G31*B39)+(H31*B40)+(I31*B41)+(J31*B42)  
  G38 = (G32*B39)+(H32*B40)+(I32*B41)+(J32*B42)  
  G39 = (G33*B39)+(H33*B40)+(I33*B41)+(J33*B42)  
  H36 = (G30*C39)+(H30*C40)+(I30*C41)+(J30*C42)  
  H37 = (G31*C39)+(H31*C40)+(I31*C41)+(J31*C42)  
  H38 = (G32*C39)+(H32*C40)+(I32*C41)+(J32*C42)  
  H39 = (G33*C39)+(H33*C40)+(I33*C41)+(J33*C42)  
  I36 = (G30*D39)+(H30*D40)+(I30*D41)+(J30*D42)  
  I37 = (G31*D39)+(H31*D40)+(I31*D41)+(J31*D42)  
  I38 = (G32*D39)+(H32*D40)+(I32*D41)+(J32*D42)  
  I39 = (G33*D39)+(H33*D40)+(I33*D41)+(J33*D42)  
  J36 = (G30*E39)+(H30*E40)+(I30*E41)+(J30*E42)  
  J37 = (G31*E39)+(H31*E40)+(I31*E41)+(J31*E42)  
  J38 = (G32*E39)+(H32*E40)+(I32*E41)+(J32*E42)  
  J39 = (G33*E39)+(H33*E40)+(I33*E41)+(J33*E42)
  ## (WF*J1*J2*J3)*J4
  G42 = (G36*B45)+(H36*B46)+(I36*B47)+(J36*B48)  
  G43 = (G37*B45)+(H37*B46)+(I37*B47)+(J37*B48) 
  G44 = (G38*B45)+(H38*B46)+(I38*B47)+(J38*B48) 
  G45 = (G39*B45)+(H39*B46)+(I39*B47)+(J39*B48) 
  H42 = (G36*C45)+(H36*C46)+(I36*C47)+(J36*C48)  
  H43 = (G37*C45)+(H37*C46)+(I37*C47)+(J37*C48) 
  H44 = (G38*C45)+(H38*C46)+(I38*C47)+(J38*C48) 
  H45 = (G39*C45)+(H39*C46)+(I39*C47)+(J39*C48) 
  I42 = (G36*D45)+(H36*D46)+(I36*D47)+(J36*D48)  
  I43 = (G37*D45)+(H37*D46)+(I37*D47)+(J37*D48) 
  I44 = (G38*D45)+(H38*D46)+(I38*D47)+(J38*D48) 
  I45 = (G39*D45)+(H39*D46)+(I39*D47)+(J39*D48) 
  J42 = (G36*E45)+(H36*E46)+(I36*E47)+(J36*E48)  
  J43 = (G37*E45)+(H37*E46)+(I37*E47)+(J37*E48) 
  J44 = (G38*E45)+(H38*E46)+(I38*E47)+(J38*E48) 
  J45 = (G39*E45)+(H39*E46)+(I39*E47)+(J39*E48)
  ## (WF*J1*J2*J3*J4)*J5
  G48 = (G42*B51)+(H42*B52)+(I42*B53)+(J42*B54)
  G49 = (G43*B51)+(H43*B52)+(I43*B53)+(J43*B54)
  G50 = (G44*B51)+(H44*B52)+(I44*B53)+(J44*B54)
  G51 = (G45*B51)+(H45*B52)+(I45*B53)+(J45*B54)
  H48 = (G42*C51)+(H42*C52)+(I42*C53)+(J42*C54)
  H49 = (G43*C51)+(H43*C52)+(I43*C53)+(J43*C54)
  H50 = (G44*C51)+(H44*C52)+(I44*C53)+(J44*C54)
  H51 = (G45*C51)+(H45*C52)+(I45*C53)+(J45*C54)
  I48 = (G42*D51)+(H42*D52)+(I42*D53)+(J42*D54)
  I49 = (G43*D51)+(H43*D52)+(I43*D53)+(J43*D54)
  I50 = (G44*D51)+(H44*D52)+(I44*D53)+(J44*D54)
  I51 = (G45*D51)+(H45*D52)+(I45*D53)+(J45*D54)
  J48 = (G42*E51)+(H42*E52)+(I42*E53)+(J42*E54)
  J49 = (G43*E51)+(H43*E52)+(I43*E53)+(J43*E54)
  J50 = (G44*E51)+(H44*E52)+(I44*E53)+(J44*E54)
  J51 = (G45*E51)+(H45*E52)+(I45*E53)+(J45*E54)
  ## (WF*J1*J2*J3*J4*J5)*J6 
  G54 = (G48*B57)+(H48*B58)+(I48*B59)+(J48*B60)
  G55 = (G49*B57)+(H49*B58)+(I49*B59)+(J49*B60)
  G56 = (G50*B57)+(H50*B58)+(I50*B59)+(J50*B60)
  G57 = (G51*B57)+(H51*B58)+(I51*B59)+(J51*B60)
  H54 = (G48*C57)+(H48*C58)+(I48*C59)+(J48*C60)
  H55 = (G49*C57)+(H49*C58)+(I49*C59)+(J49*C60)
  H56 = (G50*C57)+(H50*C58)+(I50*C59)+(J50*C60)
  H57 = (G51*C57)+(H51*C58)+(I51*C59)+(J51*C60)
  I54 = (G48*D57)+(H48*D58)+(I48*D59)+(J48*D60)
  I55 = (G49*D57)+(H49*D58)+(I49*D59)+(J49*D60)
  I56 = (G50*D57)+(H50*D58)+(I50*D59)+(J50*D60)
  I57 = (G51*D57)+(H51*D58)+(I51*D59)+(J51*D60)
  J54 = (G48*E57)+(H48*E58)+(I48*E59)+(J48*E60)
  J55 = (G49*E57)+(H49*E58)+(I49*E59)+(J49*E60)
  J56 = (G50*E57)+(H50*E58)+(I50*E59)+(J50*E60)
  J57 = (G51*E57)+(H51*E58)+(I51*E59)+(J51*E60)
  ## (WF*J1*J2*J3*J4*J5*J6)*TF
  G60 = (G54*B63)+(H54*B64)+(I54*B65)+(J54*B66)
  G61 = (G55*B63)+(H55*B64)+(I55*B65)+(J55*B66)
  G62 = (G56*B63)+(H56*B64)+(I56*B65)+(J56*B66)
  G63 = (G57*B63)+(H57*B64)+(I57*B65)+(J57*B66)
  H60 = (G54*C63)+(H54*C64)+(I54*C65)+(J54*C66)
  H61 = (G55*C63)+(H55*C64)+(I55*C65)+(J55*C66)
  H62 = (G56*C63)+(H56*C64)+(I56*C65)+(J56*C66)
  H63 = (G57*C63)+(H57*C64)+(I57*C65)+(J57*C66)
  I60 = (G54*D63)+(H54*D64)+(I54*D65)+(J54*D66)
  I61 = (G55*D63)+(H55*D64)+(I55*D65)+(J55*D66)
  I62 = (G56*D63)+(H56*D64)+(I56*D65)+(J56*D66)
  I63 = (G57*D63)+(H57*D64)+(I57*D65)+(J57*D66)
  J60 = (G54*E63)+(H54*E64)+(I54*E65)+(J54*E66)
  J61 = (G55*E63)+(H55*E64)+(I55*E65)+(J55*E66)
  J62 = (G56*E63)+(H56*E64)+(I56*E65)+(J56*E66)
  J63 = (G57*E63)+(H57*E64)+(I57*E65)+(J57*E66)
  ## GET YPR
  I8 = math.atan2(math.sqrt((I60**2)+(I61**2)),-I62)  
  I7 = math.atan2((G62/I8),(H62/I8))  
  I9 = math.atan2((I60/I8),(I61/I8))
  H4 = J60
  H5 = J61
  H6 = J62
  H7 = math.degrees(I7)
  H8 = math.degrees(I8)
  H9 = math.degrees(I9)  
  XcurPos = J60
  YcurPos = J61
  ZcurPos = J62
  RxcurPos = H9
  RycurPos = H8
  RzcurPos = H7
  XcurEntryField.delete(0, 'end')
  XcurEntryField.insert(0,str(XcurPos))
  YcurEntryField.delete(0, 'end')
  YcurEntryField.insert(0,str(YcurPos))
  ZcurEntryField.delete(0, 'end')
  ZcurEntryField.insert(0,str(ZcurPos))
  RxcurEntryField.delete(0, 'end')
  RxcurEntryField.insert(0,str(RxcurPos))
  RycurEntryField.delete(0, 'end')
  RycurEntryField.insert(0,str(RycurPos))
  RzcurEntryField.delete(0, 'end')
  RzcurEntryField.insert(0,str(RzcurPos))

def CalcRevKin(CX,CY,CZ,CRx,CRy,CRz,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz):
  global J1out
  global J2out
  global J3out
  global J4out
  global J5out
  global J6out
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  if (J1AngCur == 0):
    J1AngCur = .0001
  if (J2AngCur == 0):
    J2AngCur = .0001
  if (J3AngCur == 0):
    J3AngCur = .0001
  if (J4AngCur == 0):
    J4AngCur = .0001
  if (J5AngCur == 0):
    J5AngCur = .0001
  if (J6AngCur == 0):
    J6AngCur = .0001  
  #input
  O4 = CX
  O5 = CY 
  O6 = CZ 
  O9 = CRx
  O8 = CRy
  O7 = CRz
  V8 = WC
  if (O4 == 0):
    O4 = .0001
  if (O5 == 0):
    O5 = .0001
  if (O6 == 0):
    O6 = .0001
  if (O7 == 0):
    O7 = .0001
  if (O8 == 0):
    O8 = .0001
  if (O9 == 0):
    O9 = .0001  
  #quadrant
  if (O4>0 and O5>0):
    V9 = 1
  elif (O4>0 and O5<0):
    V9 = 2
  elif (O4<0 and O5<0):
    V9 = 3
  elif (O4<0 and O5>0):
    V9 = 4	
  ## DH TABLE
  D13 = math.radians(DHr1)
  D14 = math.radians(DHr2)
  D15 = math.radians(DHr3)
  D16 = math.radians(DHr4)
  D17 = math.radians(DHr5)
  D18 = math.radians(DHr6)
  E13 = DHd1
  E14 = DHd2
  E15 = DHd3
  E16 = DHd4
  E17 = DHd5
  E18 = DHd6
  F13 = DHa1
  F14 = DHa2
  F15 = DHa3
  F16 = DHa4
  F17 = DHa5
  F18 = DHa6	
  ## WORK FRAME INPUT
  H13 = -float(UFxEntryField.get()) 
  H14 = -float(UFyEntryField.get())  
  H15 = -float(UFzEntryField.get())
  H16 = -float(UFrxEntryField.get()) 
  H17 = -float(UFryEntryField.get()) 
  H18 = -float(UFrzEntryField.get()) 
  ## TOOL FRAME INPUT
  J13 = -float(TFxEntryField.get()) + TCX
  J14 = -float(TFyEntryField.get()) + TCY
  J15 = -float(TFzEntryField.get()) + TCZ
  J16 = -float(TFrxEntryField.get()) + TCRx
  J17 = -float(TFryEntryField.get()) + TCRy
  J18 = -float(TFrzEntryField.get()) + TCRz
  ## WORK FRAME TABLE
  N30 = math.cos(math.radians(H18))*math.cos(math.radians(H17))
  O30 = -math.sin(math.radians(H18))*math.cos(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  P30 = math.sin(math.radians(H18))*math.sin(math.radians(H16))+math.cos(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  Q30 = H13
  N31 = math.sin(math.radians(H18))*math.cos(math.radians(H17))
  O31 = math.cos(math.radians(H18))*math.cos(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.sin(math.radians(H16))
  P31 = -math.cos(math.radians(H18))*math.sin(math.radians(H16))+math.sin(math.radians(H18))*math.sin(math.radians(H17))*math.cos(math.radians(H16))
  Q31 = H14
  N32 = -math.sin(math.radians(H18))
  O32 = math.cos(math.radians(H17))*math.sin(math.radians(H16))
  P32 = math.cos(math.radians(H17))*math.cos(math.radians(H16))
  Q32 = H15
  N33 = 0
  O33 = 0
  P33 = 0
  Q33 = 1   
  ## R 0-T
  X30 = math.cos(math.radians(O7))*math.cos(math.radians(O9))-math.cos(math.radians(O8))*math.sin(math.radians(O7))*math.sin(math.radians(O9)) 
  Y30 = math.cos(math.radians(O9))*math.sin(math.radians(O7))+math.cos(math.radians(O7))*math.cos(math.radians(O8))*math.sin(math.radians(O9))
  Z30 = math.sin(math.radians(O8))*math.sin(math.radians(O9))
  AA30 = O4  
  X31 = math.cos(math.radians(O8))*math.cos(math.radians(O9))*math.sin(math.radians(O7))+math.cos(math.radians(O7))*math.sin(math.radians(O9))
  Y31 = math.cos(math.radians(O7))*math.cos(math.radians(O8))*math.cos(math.radians(O9))-math.sin(math.radians(O7))*math.sin(math.radians(O9))
  Z31 = math.cos(math.radians(O9))*math.sin(math.radians(O8))
  AA31 = O5   	
  X32 = math.sin(math.radians(O7))*math.sin(math.radians(O8))
  Y32 = math.cos(math.radians(O7))*math.sin(math.radians(O8))
  Z32 = -math.cos(math.radians(O8))
  AA32 = O6 
  X33 = 0
  Y33 = 0
  Z33 = 0
  AA33 = 1     
  ## R 0-T   offset by work frame
  X36 = ((N30*X30)+(O30*X31)+(P30*X32)+(Q30*X33))*-1
  Y36 = (N30*Y30)+(O30*Y31)+(P30*Y32)+(Q30*Y33)
  Z36 = (N30*Z30)+(O30*Z31)+(P30*Z32)+(Q30*Z33)
  AA36 = (N30*AA30)+(O30*AA31)+(P30*AA32)+(Q30*AA33)
  X37 = (N31*X30)+(O31*X31)+(P31*X32)+(Q31*X33)
  Y37 = (N31*Y30)+(O31*Y31)+(P31*Y32)+(Q31*Y33)
  Z37 = (N31*Z30)+(O31*Z31)+(P31*Z32)+(Q31*Z33)
  AA37 = (N31*AA30)+(O31*AA31)+(P31*AA32)+(Q31*AA33) 
  X38 = (N32*X30)+(O32*X31)+(P32*X32)+(Q32*X33)
  Y38 = (N32*Y30)+(O32*Y31)+(P32*Y32)+(Q32*Y33)
  Z38 = (N32*Z30)+(O32*Z31)+(P32*Z32)+(Q32*Z33)
  AA38 = (N32*AA30)+(O32*AA31)+(P32*AA32)+(Q32*AA33) 
  X39 = (N33*X30)+(O33*X31)+(P33*X32)+(Q33*X33)
  Y39 = (N33*Y30)+(O33*Y31)+(P33*Y32)+(Q33*Y33)
  Z39 = (N33*Z30)+(O33*Z31)+(P33*Z32)+(Q33*Z33)
  AA39 = (N33*AA30)+(O33*AA31)+(P33*AA32)+(Q33*AA33)
  ## TOOL FRAME
  X42 = math.cos(math.radians(J18))*math.cos(math.radians(J17))
  Y42 = -math.sin(math.radians(J18))*math.cos(math.radians(J16))+math.cos(math.radians(J18))*math.sin(math.radians(J17))*math.sin(math.radians(J16)) 
  Z42 = math.sin(math.radians(J18))*math.sin(math.radians(J16))+math.cos(math.radians(J18))*math.sin(math.radians(J17))*math.cos(math.radians(J16)) 
  AA42 = (J13)
  X43 = math.sin(math.radians(J18))*math.cos(math.radians(J17))
  Y43 = math.cos(math.radians(J18))*math.cos(math.radians(J16))+math.sin(math.radians(J18))*math.sin(math.radians(J17))*math.sin(math.radians(J16)) 
  Z43 = -math.cos(math.radians(J18))*math.sin(math.radians(J16))+math.sin(math.radians(J18))*math.sin(math.radians(J17))*math.cos(math.radians(J16)) 
  AA43 = (J14)  
  X44 = -math.sin(math.radians(J18))
  Y44 = math.cos(math.radians(J17))*math.sin(math.radians(J16)) 
  Z44 = math.cos(math.radians(J17))*math.cos(math.radians(J16)) 
  AA44 = (J15)  
  X45 = 0
  Y45 = 0 
  Z45 = 0 
  AA45 = 1    
  ## INVERT TOOL FRAME
  X48 = X42
  Y48 = X43
  Z48 = X44
  AA48 = (X48*AA42)+(Y48*AA43)+(Z48*AA44)
  X49 = Y42
  Y49 = Y43
  Z49 = Y44
  AA49 = (X49*AA42)+(Y49*AA43)+(Z49*AA44)
  X50 = Z42
  Y50 = Z43
  Z50 = Z44
  AA50 = (X50*AA42)+(Y50*AA43)+(Z50*AA44)
  X51 = 0
  Y51 = 0
  Z51 = 0
  AA51 = 1
  ## R 0-6
  X54 =(X36*X48)+(Y36*X49)+(Z36*X50)+(AA36*X51)
  Y54 =(X36*Y48)+(Y36*Y49)+(Z36*Y50)+(AA36*Y51)
  Z54 =(X36*Z48)+(Y36*Z49)+(Z36*Z50)+(AA36*Z51)
  AA54 =(X36*AA48)+(Y36*AA49)+(Z36*AA50)+(AA36*AA51)
  X55 =(X37*X48)+(Y37*X49)+(Z37*X50)+(AA37*X51)
  Y55 =(X37*Y48)+(Y37*Y49)+(Z37*Y50)+(AA37*Y51)
  Z55 =(X37*Z48)+(Y37*Z49)+(Z37*Z50)+(AA37*Z51)
  AA55 =(X37*AA48)+(Y37*AA49)+(Z37*AA50)+(AA37*AA51)
  X56 =(X38*X48)+(Y38*X49)+(Z38*X50)+(AA38*X51)
  Y56 =(X38*Y48)+(Y38*Y49)+(Z38*Y50)+(AA38*Y51)
  Z56 =(X38*Z48)+(Y38*Z49)+(Z38*Z50)+(AA38*Z51)
  AA56 =(X38*AA48)+(Y38*AA49)+(Z38*AA50)+(AA38*AA51)
  X57 =(X39*X48)+(Y39*X49)+(Z39*X50)+(AA39*X51)
  Y57 =(X39*Y48)+(Y39*Y49)+(Z39*Y50)+(AA39*Y51)
  Z57 =(X39*Z48)+(Y39*Z49)+(Z39*Z50)+(AA39*Z51)
  AA57 =(X39*AA48)+(Y39*AA49)+(Z39*AA50)+(AA39*AA51)
  ## REMOVE R 0-6
  X60 =math.cos(math.radians(180))
  Y60 =math.sin(math.radians(180))
  Z60 = 0
  AA60 = 0
  X61 =-math.sin(math.radians(180))*math.cos(D18)
  Y61 =math.cos(math.radians(180))*math.cos(D18)
  Z61 =math.sin(D18)
  AA61 = 0
  X62 =math.sin(math.radians(180))*math.sin(D18)
  Y62 =-math.cos(math.radians(180))*math.sin(D18)
  Z62 =math.cos(D18)
  AA62 = -E18
  X63 = 0
  Y63 = 0
  Z63 = 0
  AA63 = 1
  ## R 0-5 (center spherica wrist)
  X66 =(X54*X60)+(Y54*X61)+(Z54*X62)+(AA54*X63)
  Y66 =(X54*Y60)+(Y54*Y61)+(Z54*Y62)+(AA54*Y63)
  Z66 =(X54*Z60)+(Y54*Z61)+(Z54*Z62)+(AA54*Z63)
  AA66 =(X54*AA60)+(Y54*AA61)+(Z54*AA62)+(AA54*AA63)
  X67 =(X55*X60)+(Y55*X61)+(Z55*X62)+(AA55*X63)
  Y67 =(X55*Y60)+(Y55*Y61)+(Z55*Y62)+(AA55*Y63)
  Z67 =(X55*Z60)+(Y55*Z61)+(Z55*Z62)+(AA55*Z63)
  AA67 =(X55*AA60)+(Y55*AA61)+(Z55*AA62)+(AA55*AA63)
  X68 =(X56*X60)+(Y56*X61)+(Z56*X62)+(AA56*X63)
  Y68 =(X56*Y60)+(Y56*Y61)+(Z56*Y62)+(AA56*Y63)
  Z68 =(X56*Z60)+(Y56*Z61)+(Z56*Z62)+(AA56*Z63)
  AA68 =(X56*AA60)+(Y56*AA61)+(Z56*AA62)+(AA56*AA63)
  X69 =(X57*X60)+(Y57*X61)+(Z57*X62)+(AA57*X63)
  Y69 =(X57*Y60)+(Y57*Y61)+(Z57*Y62)+(AA57*Y63)
  Z69 =(X57*Z60)+(Y57*Z61)+(Z57*Z62)+(AA57*Z63)
  AA69 =(X57*AA60)+(Y57*AA61)+(Z57*AA62)+(AA57*AA63)
  ## CALCULATE J1 ANGLE
  O13 = math.atan((AA67)/(AA66))
  if (V9 == 1):
    P13 = math.degrees(O13)
  if (V9 == 2):
    P13 = math.degrees(O13)
  if (V9 == 3):
    P13 = -180 + math.degrees(O13)
  if (V9 == 4):
    P13 = 180 + math.degrees(O13)
  ## CALCULATE J2 ANGLE	FWD

  O16 = math.sqrt(((abs(AA67))**2)+((abs(AA66))**2))
  O17 = AA68-E13
  O18 = O16-F13
  O19 = math.sqrt((O17**2)+(O18**2))
  O20 = math.sqrt((E16**2)+(F15**2))
  O21 = math.degrees(math.atan(O17/O18))
  O22 = math.degrees(math.acos(((F14**2)+(O19**2)-(abs(O20)**2))/(2*F14*O19)))
  try:
    O25 = math.degrees(math.atan(abs(E16)/F15))
  except:
    O25 = 90
  O23 = 180-math.degrees(math.acos(((abs(O20)**2)+(F14**2)-(O19**2))/(2*abs(O20)*F14)))+(90-O25)
  O26 = -(O21+O22)
  O27 = O23
  ## CALCULATE J2 ANGLE	MID
  P18 = -O18
  P19 = math.sqrt((O17**2)+(P18**2))   
  P21 = math.degrees(math.acos(((F14**2)+(P19**2)-(abs(O20)**2))/(2*F14*P19)))
  P22 = math.degrees(math.atan(P18/O17))
  P23 = 180-math.degrees(math.acos(((abs(O20)**2)+(F14**2)-(P19**2))/(2*abs(O20)*F14)))+(90-O25)
  P24 = 90-(P21+P22)
  P26 = -180+P24
  P27 = P23
  ## J1,J2,J3
  Q4 = P13
  if (O18<0):
    Q5 = P26
    Q6 = P27
  else:
    Q5 = O26
    Q6 = O27
  ## J1
  N36 =math.cos(math.radians(Q4))
  O36 =-math.sin(math.radians(Q4))*math.cos(D13)
  P36 =math.sin(math.radians(Q4))*math.sin(D13)
  Q36 =F13*math.cos(math.radians(Q4))
  N37 =math.sin(math.radians(Q4))
  O37 =math.cos(math.radians(Q4))*math.cos(D13)
  P37 =-math.cos(math.radians(Q4))*math.sin(D13)
  Q37 =F13*math.sin(math.radians(Q4)) 
  N38 = 0
  O38 =math.sin(D13)
  P38 =math.cos(D13)
  Q38 =E13  
  N39 = 0
  O39 = 0
  P39 = 0
  Q39 = 1
  ## J2
  N42 =math.cos(math.radians(Q5))
  O42 =-math.sin(math.radians(Q5))*math.cos(D14)
  P42 =math.sin(math.radians(Q5))*math.sin(D14)
  Q42 =F14*math.cos(math.radians(Q5))  
  N43 =math.sin(math.radians(Q5))
  O43 =math.cos(math.radians(Q5))*math.cos(D14)
  P43 =-math.cos(math.radians(Q5))*math.sin(D14)
  Q43 =F14*math.sin(math.radians(Q5))  
  N44 = 0
  O44 =math.sin(D14)
  P44 =math.cos(D14)
  Q44 =E14  
  N45 = 0
  O45 = 0
  P45 = 0
  Q45 = 1
  ## J3  
  N48 =math.cos(math.radians((Q6)-90))
  O48 =-math.sin(math.radians((Q6)-90))*math.cos(D15)
  P48 =math.sin(math.radians((Q6)-90))*math.sin(D15)
  Q48 =F15*math.cos(math.radians((Q6)-90))
  N49 =math.sin(math.radians((Q6)-90))
  O49 =math.cos(math.radians((Q6)-90))*math.cos(D15)
  P49 =-math.cos(math.radians((Q6)-90))*math.sin(D15)
  Q49 =F15*math.sin(math.radians((Q6)-90))
  N50 =0
  O50 =math.sin(D15)
  P50 =math.cos(D15)
  Q50 =E15
  N51 =0
  O51 =0
  P51 =0
  Q51 =0 
  ## R 0-1
  S33 =(N30*N36)+(O30*N37)+(P30*N38)+(Q30*N39)
  T33 =(N30*O36)+(O30*O37)+(P30*O38)+(Q30*O39)
  U33 =(N30*P36)+(O30*P37)+(P30*P38)+(Q30*P39)
  V33 =(N30*Q36)+(O30*Q37)+(P30*Q38)+(Q30*Q39) 
  S34 =(N31*N36)+(O31*N37)+(P31*N38)+(Q31*N39)
  T34 =(N31*O36)+(O31*O37)+(P31*O38)+(Q31*O39)
  U34 =(N31*P36)+(O31*P37)+(P31*P38)+(Q31*P39)
  V34 =(N31*Q36)+(O31*Q37)+(P31*Q38)+(Q31*Q39)
  S35 =(N32*N36)+(O32*N37)+(P32*N38)+(Q32*N39)
  T35 =(N32*O36)+(O32*O37)+(P32*O38)+(Q32*O39)
  U35 =(N32*P36)+(O32*P37)+(P32*P38)+(Q32*P39)
  V35 =(N32*Q36)+(O32*Q37)+(P32*Q38)+(Q32*Q39)
  S36 =(N33*N36)+(O33*N37)+(P33*N38)+(Q33*N39)
  T36 =(N33*O36)+(O33*O37)+(P33*O38)+(Q33*O39)
  U36 =(N33*P36)+(O33*P37)+(P33*P38)+(Q33*P39)
  V36 =(N33*Q36)+(O33*Q37)+(P33*Q38)+(Q33*Q39)
  ## R 0-2  
  S39 =(S33*N42)+(T33*N43)+(U33*N44)+(V33*N45)
  T39 =(S33*O42)+(T33*O43)+(U33*O44)+(V33*O45)
  U39 =(S33*P42)+(T33*P43)+(U33*P44)+(V33*P45)
  V39 =(S33*Q42)+(T33*Q43)+(U33*Q44)+(V33*Q45)  
  S40 =(S34*N42)+(T34*N43)+(U34*N44)+(V34*N45)
  T40 =(S34*O42)+(T34*O43)+(U34*O44)+(V34*O45)
  U40 =(S34*P42)+(T34*P43)+(U34*P44)+(V34*P45)
  V40 =(S34*Q42)+(T34*Q43)+(U34*Q44)+(V34*Q45)
  S41 =(S35*N42)+(T35*N43)+(U35*N44)+(V35*N45)
  T41 =(S35*O42)+(T35*O43)+(U35*O44)+(V35*O45)
  U41 =(S35*P42)+(T35*P43)+(U35*P44)+(V35*P45)
  V41 =(S35*Q42)+(T35*Q43)+(U35*Q44)+(V35*Q45)
  S42 =(S36*N42)+(T36*N43)+(U36*N44)+(V36*N45)
  T42 =(S36*O42)+(T36*O43)+(U36*O44)+(V36*O45)
  U42 =(S36*P42)+(T36*P43)+(U36*P44)+(V36*P45)
  V42 =(S36*Q42)+(T36*Q43)+(U36*Q44)+(V36*Q45)
  ## R 0-3 
  S45 =(S39*N48)+(T39*N49)+(U39*N50)+(V39*N51)
  T45 =(S39*O48)+(T39*O49)+(U39*O50)+(V39*O51)
  U45 =(S39*P48)+(T39*P49)+(U39*P50)+(V39*P51)
  V45 =(S39*Q48)+(T39*Q49)+(U39*Q50)+(V39*Q51) 
  S46 =(S40*N48)+(T40*N49)+(U40*N50)+(V40*N51)
  T46 =(S40*O48)+(T40*O49)+(U40*O50)+(V40*O51)
  U46 =(S40*P48)+(T40*P49)+(U40*P50)+(V40*P51)
  V46 =(S40*Q48)+(T40*Q49)+(U40*Q50)+(V40*Q51)
  S47 =(S41*N48)+(T41*N49)+(U41*N50)+(V41*N51)
  T47 =(S41*O48)+(T41*O49)+(U41*O50)+(V41*O51)
  U47 =(S41*P48)+(T41*P49)+(U41*P50)+(V41*P51)
  V47 =(S41*Q48)+(T41*Q49)+(U41*Q50)+(V41*Q51)
  S48 =(S42*N48)+(T42*N49)+(U42*N50)+(V42*N51)
  T48 =(S42*O48)+(T42*O49)+(U42*O50)+(V42*O51)
  U48 =(S42*P48)+(T42*P49)+(U42*P50)+(V42*P51)
  V48 =(S42*Q48)+(T42*Q49)+(U42*Q50)+(V42*Q51)
  ## R 0-3 transposed
  S51 =S45
  T51 =S46
  U51 =S47
  S52 =T45
  T52 =T46
  U52 =T47
  S53 =U45
  T53 =U46
  U53 =U47
  ## R 3-6 (spherical wrist  orietation)
  X72 =(S51*X66)+(T51*X67)+(U51*X68) 
  Y72 =(S51*Y66)+(T51*Y67)+(U51*Y68)
  Z72 =(S51*Z66)+(T51*Z67)+(U51*Z68)
  X73 =(S52*X66)+(T52*X67)+(U52*X68)
  Y73 =(S52*Y66)+(T52*Y67)+(U52*Y68)
  Z73 =(S52*Z66)+(T52*Z67)+(U52*Z68)
  X74 =(S53*X66)+(T53*X67)+(U53*X68)
  Y74 =(S53*Y66)+(T53*Y67)+(U53*Y68)
  Z74 =(S53*Z66)+(T53*Z67)+(U53*Z68)
  ## WRIST ORENTATION
  R7 = math.degrees(math.atan2(Z73,Z72))
  R8 = math.degrees(math.atan2(+math.sqrt(1-Z74**2),Z74))
  if (Y74 < 0):
    R9 = math.degrees(math.atan2(-Y74,X74))-180
  else:
    R9 = math.degrees(math.atan2(-Y74,X74))+180  	
  S7 = math.degrees(math.atan2(-Z73,-Z72))
  S8 = math.degrees(math.atan2(-math.sqrt(1-Z74**2),Z74))
  if (Y74 < 0):
    S9 = math.degrees(math.atan2(Y74,-X74))+180
  else:
    S9 = math.degrees(math.atan2(Y74,-X74))-180
  if (V8 == "F"):
    Q8 = R8
  else:
    Q8 = S8
  if(Q8>0):
    Q7 = R7 
  else:
    Q7 = S7
  if(Q8<0):
    Q9 = S9
  else:
    Q9 = R9
  ## FINAL OUTPUT
  J1out = Q4
  J2out = Q5
  J3out = Q6
  J4out = Q7
  J5out = Q8
  J6out = Q9
  return (J1out,J2out,J3out,J4out,J5out,J6out)

  
  
##############################################################################################################################################################  
### MOVE DEFS ################################################################################################################################## MOVE DEFS ###  
##############################################################################################################################################################  
  
def MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code):
  global commandCalc
  global blockEncPosMove
  blockEncPosMove = 1
  CalcRevKin(CX,CY,CZ,CRx,CRy,CRz,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz)
  MoveNew(J1out,J2out,J3out,J4out,J5out,J6out,newSpeed,ACCdur,ACCspd,DECdur,DECspd,Track,Code)
  blockEncPosMove = 0
  if Code == 2 or Code == 3:
    return(commandCalc)

def MoveNew(J1out,J2out,J3out,J4out,J5out,J6out,newSpeed,ACCdur,ACCspd,DECdur,DECspd,Track,Code):
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  global J1AngCur
  global J2AngCur
  global J3AngCur
  global J4AngCur
  global J5AngCur
  global J6AngCur
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global TrackcurPos
  global TrackLength
  global TrackStepLim
  global commandCalc  
  J1newAng = J1out
  J2newAng = J2out
  J3newAng = J3out
  J4newAng = J4out
  J5newAng = J5out
  J6newAng = J6out
  TrackNew = Track
  ###CHECK WITHIN ANGLE LIMITS
  #if (J1newAng < J1NegAngLim or J1newAng > J1PosAngLim) or (J2newAng < J2NegAngLim or J2newAng > J2PosAngLim) or (J3newAng < J3NegAngLim or J3newAng > J3PosAngLim) or (J4newAng < J4NegAngLim or J4newAng > J4PosAngLim) or (J5newAng < J5NegAngLim or J5newAng > J5PosAngLim) or (J6newAng < J6NegAngLim or J6newAng > J6PosAngLim or TrackNew < 0 or TrackNew > TrackLength):
    #almStatusLab.config(text="AXIS LIMIT", bg = "red")
    #almStatusLab2.config(text="AXIS LIMIT", bg = "red")
    #tab1.runTrue = 0
  if (J1newAng < J1NegAngLim or J1newAng > J1PosAngLim): 
    almStatusLab.config(text="J1 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J1 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J1 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
    tab1.runTrue = 0
  elif (J2newAng < J2NegAngLim or J2newAng > J2PosAngLim): 
    almStatusLab.config(text="J2 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J2 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J2 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
    tab1.runTrue = 0
  elif (J3newAng < J3NegAngLim or J3newAng > J3PosAngLim): 
    almStatusLab.config(text="J3 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J3 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J3 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
    tab1.runTrue = 0
  elif (J4newAng < J4NegAngLim or J4newAng > J4PosAngLim): 
    almStatusLab.config(text="J4 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J4 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J4 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
    tab1.runTrue = 0
  elif (J5newAng < J5NegAngLim or J5newAng > J5PosAngLim): 
    almStatusLab.config(text="J5 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J5 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J5 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
    tab1.runTrue = 0
  elif (J6newAng < J6NegAngLim or J6newAng > J6PosAngLim): 
    almStatusLab.config(text="J6 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J6 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J6 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
    tab1.runTrue = 0    
  else:  
    ##J1 calc##
    if (float(J1newAng) >= float(J1AngCur)):   
      #calc pos dir output
      if (J1motdir == "0"):
        J1drivedir = "1"
      else:
        J1drivedir = "0"
      J1dir = J1drivedir
      J1calcAng = float(J1newAng) - float(J1AngCur)
      J1steps = int(J1calcAng / J1DegPerStep)
      if Code != 3:
        J1StepCur = J1StepCur + J1steps #Invert       
        J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
      J1steps = str(J1steps) 
    elif (float(J1newAng) < float(J1AngCur)):
      J1dir = J1motdir
      J1calcAng = float(J1AngCur) - float(J1newAng)
      J1steps = int(J1calcAng / J1DegPerStep)
      if Code != 3:
        J1StepCur = J1StepCur - J1steps #Invert       
        J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
      J1steps = str(J1steps) 
    ##J2 calc##
    if (float(J2newAng) >= float(J2AngCur)):   
      #calc pos dir output
      if (J2motdir == "0"):
        J2drivedir = "1"
      else:
        J2drivedir = "0"
      J2dir = J2drivedir
      J2calcAng = float(J2newAng) - float(J2AngCur)
      J2steps = int(J2calcAng / J2DegPerStep)
      if Code != 3:
        J2StepCur = J2StepCur + J2steps #Invert       
        J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
      J2steps = str(J2steps) 
    elif (float(J2newAng) < float(J2AngCur)):
      J2dir = J2motdir
      J2calcAng = float(J2AngCur) - float(J2newAng)
      J2steps = int(J2calcAng / J2DegPerStep)
      if Code != 3:
        J2StepCur = J2StepCur - J2steps #Invert       
        J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
      J2steps = str(J2steps) 
    ##J3 calc##
    if (float(J3newAng) >= float(J3AngCur)):   
      #calc pos dir output
      if (J3motdir == "0"):
        J3drivedir = "1"
      else:
        J3drivedir = "0"
      J3dir = J3drivedir
      J3calcAng = float(J3newAng) - float(J3AngCur)
      J3steps = int(J3calcAng / J3DegPerStep)
      if Code != 3:
        J3StepCur = J3StepCur + J3steps #Invert       
        J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
      J3steps = str(J3steps) 
    elif (float(J3newAng) < float(J3AngCur)):
      J3dir = J3motdir
      J3calcAng = float(J3AngCur) - float(J3newAng)
      J3steps = int(J3calcAng / J3DegPerStep)
      if Code != 3:
        J3StepCur = J3StepCur - J3steps #Invert       
        J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
      J3steps = str(J3steps) 
    ##J4 calc##
    if (float(J4newAng) >= float(J4AngCur)):   
      #calc pos dir output
      if (J4motdir == "0"):
        J4drivedir = "1"
      else:
        J4drivedir = "0"
      J4dir = J4drivedir
      J4calcAng = float(J4newAng) - float(J4AngCur)
      J4steps = int(J4calcAng / J4DegPerStep)
      if Code != 3:
        J4StepCur = J4StepCur + J4steps #Invert       
        J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
      J4steps = str(J4steps) 
    elif (float(J4newAng) < float(J4AngCur)):
      J4dir = J4motdir
      J4calcAng = float(J4AngCur) - float(J4newAng)
      J4steps = int(J4calcAng / J4DegPerStep)
      if Code != 3:
        J4StepCur = J4StepCur - J4steps #Invert       
        J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
      J4steps = str(J4steps) 
    ##J5 calc##
    if (float(J5newAng) >= float(J5AngCur)):   
      #calc pos dir output
      if (J5motdir == "0"):
        J5drivedir = "1"
      else:
        J5drivedir = "0"
      J5dir = J5drivedir
      J5calcAng = float(J5newAng) - float(J5AngCur)
      J5steps = int(J5calcAng / J5DegPerStep)
      if Code != 3:
        J5StepCur = J5StepCur + J5steps #Invert       
        J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
      J5steps = str(J5steps) 
    elif (float(J5newAng) < float(J5AngCur)):
      J5dir = J5motdir
      J5calcAng = float(J5AngCur) - float(J5newAng)
      J5steps = int(J5calcAng / J5DegPerStep)
      if Code != 3:
        J5StepCur = J5StepCur - J5steps #Invert       
        J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
      J5steps = str(J5steps) 
    ##J6 calc##
    if (float(J6newAng) >= float(J6AngCur)):   
      #calc pos dir output
      if (J6motdir == "0"):
        J6drivedir = "1"
      else:
        J6drivedir = "0"
      J6dir = J6drivedir
      J6calcAng = float(J6newAng) - float(J6AngCur)
      J6steps = int(J6calcAng / J6DegPerStep)
      if Code != 3:
        J6StepCur = J6StepCur + J6steps #Invert       
        J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
      J6steps = str(J6steps) 
    elif (float(J6newAng) < float(J6AngCur)):
      J6dir = J6motdir
      J6calcAng = float(J6AngCur) - float(J6newAng)
      J6steps = int(J6calcAng / J6DegPerStep)
      if Code != 3:
        J6StepCur = J6StepCur - J6steps #Invert       
        J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
      J6steps = str(J6steps)
    ##Track calc##
    if (TrackNew >= TrackcurPos):
      TRdir = "1"
      TRdist = TrackNew - TrackcurPos
      TRstep = str(int((TrackStepLim/TrackLength)*TRdist))
    else:
      TRdir = "0"
      TRdist = TrackcurPos - TrackNew	
      TRstep = str(int((TrackStepLim/TrackLength)*TRdist))
    TrackcurPos = TrackNew
    TrackcurEntryField.delete(0, 'end')  
    TrackcurEntryField.insert(0,str(TrackcurPos))
    commandCalc = "MJA"+J1dir+J1steps+"B"+J2dir+J2steps+"C"+J3dir+J3steps+"D"+J4dir+J4steps+"E"+J5dir+J5steps+"F"+J6dir+J6steps+"T"+TRdir+TRstep+"S"+newSpeed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    if Code == 0:
      ser.write(commandCalc.encode())
      ser.flushInput()
      time.sleep(.01)
      #ser.read() 
      RobotCode = str(ser.readline())
      Pcode = RobotCode[2:4]
      if (Pcode == "01"):
        applyRobotCal(RobotCode)       
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur))
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2AngCur))
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3AngCur))
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4AngCur))
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5AngCur))
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6AngCur))
    CalcFwdKin()
    DisplaySteps()
    savePosData() 
    if Code == 2 or Code == 3 :
      return(commandCalc)	

	
	
##############################################################################################################################################################	
### CALIBRATION & SAVE DEFS ###################################################################################################### CALIBRATION & SAVE DEFS ###
##############################################################################################################################################################	



def getRobotPosition():
  commandCalc = "GP"+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
  ser.write(commandCalc.encode())
  RobotCode = str(ser.readline())
  Pcode = RobotCode[2:4]
  if (Pcode == "01"):
    applyRobotCal(RobotCode)

def applyRobotCal(RobotCode):
  global J1NegAngLim
  global J1PosAngLim
  global J1StepLim
  global J1DegPerStep
  global J1StepCur
  global J1AngCur
  global J2NegAngLim
  global J2PosAngLim
  global J2StepLim
  global J2DegPerStep
  global J2StepCur
  global J2AngCur
  global J3NegAngLim
  global J3PosAngLim
  global J3StepLim
  global J3DegPerStep
  global J3StepCur
  global J3AngCur
  global J4NegAngLim
  global J4PosAngLim
  global J4StepLim
  global J4DegPerStep
  global J4StepCur
  global J4AngCur
  global J5NegAngLim
  global J5PosAngLim
  global J5StepLim
  global J5DegPerStep
  global J5StepCur
  global J5AngCur
  global J6NegAngLim
  global J6PosAngLim
  global J6StepLim
  global J6DegPerStep
  global J6StepCur
  global J6AngCur
  Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
  J1fault = RobotCode[4:5]
  J2fault = RobotCode[5:6]
  J3fault = RobotCode[6:7]
  J4fault = RobotCode[7:8]
  J5fault = RobotCode[8:9]
  J6fault = RobotCode[9:10]
  J1index = RobotCode.find('A')
  J2index = RobotCode.find('B')
  J3index = RobotCode.find('C')
  J4index = RobotCode.find('D')
  J5index = RobotCode.find('E')
  J6index = RobotCode.find('F')
  if (J1OpenLoopStat.get() == 0):
    if (J1fault == "1"):
      almStatusLab.config(text="J1 COLLISION OR OUT OF CALIBRATION", bg = "red")
      almStatusLab2.config(text="J1 COLLISION OR OUT OF CALIBRATION", bg = "red")
      tab6.ElogView.insert(END, Curtime+" - "+"J1 COLLISION OR OUT OF CALIBRATION")
      J1StepCur = int(RobotCode[J1index+1:J2index])
      J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
      J1curAngEntryField.delete(0, 'end')
      J1curAngEntryField.insert(0,str(J1AngCur))
      stopProg()
  if (J2OpenLoopStat.get() == 0):    
    if (J2fault == "1"):
      almStatusLab.config(text="J2 COLLISION OR OUT OF CALIBRATION", bg = "red")
      almStatusLab2.config(text="J2 COLLISION OR OUT OF CALIBRATION", bg = "red")
      tab6.ElogView.insert(END, Curtime+" - "+"J2 COLLISION OR OUT OF CALIBRATION")
      J2StepCur = int(RobotCode[J2index+1:J3index])
      J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
      J2curAngEntryField.delete(0, 'end')
      J2curAngEntryField.insert(0,str(J2AngCur))
      stopProg()
  if (J3OpenLoopStat.get() == 0):    
    if (J3fault == "1"):
      almStatusLab.config(text="J3 COLLISION OR OUT OF CALIBRATION", bg = "red")
      almStatusLab2.config(text="J3 COLLISION OR OUT OF CALIBRATION", bg = "red")
      tab6.ElogView.insert(END, Curtime+" - "+"J3 COLLISION OR OUT OF CALIBRATION")
      J3StepCur = int(RobotCode[J3index+1:J4index])
      J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
      J3curAngEntryField.delete(0, 'end')
      J3curAngEntryField.insert(0,str(J3AngCur))
      stopProg()
  if (J4OpenLoopStat.get() == 0):    
    if (J4fault == "1"):
      almStatusLab.config(text="J4 COLLISION OR OUT OF CALIBRATION", bg = "red")
      almStatusLab2.config(text="J4 COLLISION OR OUT OF CALIBRATION", bg = "red")
      tab6.ElogView.insert(END, Curtime+" - "+"J4 COLLISION OR OUT OF CALIBRATION")
      J4StepCur = int(RobotCode[J4index+1:J5index])
      J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
      J4curAngEntryField.delete(0, 'end')
      J4curAngEntryField.insert(0,str(J4AngCur))
      stopProg()
  if (J5OpenLoopStat.get() == 0):    
    if (J5fault == "1"):
      almStatusLab.config(text="J5 COLLISION OR OUT OF CALIBRATION", bg = "red")
      almStatusLab2.config(text="J5 COLLISION OR OUT OF CALIBRATION", bg = "red")
      tab6.ElogView.insert(END, Curtime+" - "+"J5 COLLISION OR OUT OF CALIBRATION")
      J5StepCur = int(RobotCode[J5index+1:J6index])
      J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
      J5curAngEntryField.delete(0, 'end')
      J5curAngEntryField.insert(0,str(J5AngCur))
      stopProg()      
  if (J6OpenLoopStat.get() == 0):    
    if (J6fault == "1"):
      almStatusLab.config(text="J6 COLLISION OR OUT OF CALIBRATION", bg = "red")
      almStatusLab2.config(text="J6 COLLISION OR OUT OF CALIBRATION", bg = "red")
      tab6.ElogView.insert(END, Curtime+" - "+"J6 COLLISION OR OUT OF CALIBRATION")
      J6StepCur = int(RobotCode[J6index+1:-5])
      J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
      J6curAngEntryField.delete(0, 'end')
      J6curAngEntryField.insert(0,str(J6AngCur))
      stopProg()
  CalcFwdKin()
  DisplaySteps()
  savePosData()
  value=tab6.ElogView.get(0,END)
  pickle.dump(value,open("ErrorLog","wb"))



def calRobotAll():
  global blockEncPosCal
  blockEncPosCal = 1
  calaxis = "111110"
  speed = "50"
  calRobot(calaxis,speed)
  ### calc correct calibration direction
  if(J1caldir == J1motdir):
    J1caldrive = "1"
  else:
    J1caldrive = "0"      
  if(J2caldir == J2motdir):
    J2caldrive = "1"
  else:
    J2caldrive = "0" 
  if(J3caldir == J3motdir):
    J3caldrive = "1"
  else:
    J3caldrive = "0" 
  if(J4caldir == J4motdir):
    J4caldrive = "1"
  else:
    J4caldrive = "0" 	
  if(J5caldir == J5motdir):
    J5caldrive = "1"
  else:
    J5caldrive = "0" 	
  if(J6caldir == J6motdir):
    J6caldrive = "1"
  else:
    J6caldrive = "0"        
  command = "MJA"+J1caldrive+"500"+"B"+J2caldrive+"500"+"C"+J3caldrive+"500"+"D"+J4caldrive+"500"+"E"+J5caldrive+"500"+"F"+J6caldrive+"0"+"S15G10H10I10K10"+"\n"
  ser.write(command.encode())
  ser.flushInput()
  speed = "8"
  time.sleep(2.5)
  calRobot(calaxis,speed)
  gotoRestPos()
  calaxis = "000001"
  speed = "50"
  calRobot(calaxis,speed)
  command = "MJA"+J1caldrive+"0"+"B"+J2caldrive+"0"+"C"+J3caldrive+"0"+"D"+J4caldrive+"0"+"E"+J5caldrive+"0"+"F"+J6caldrive+"500"+"S15G10H10I10K10"+"\n"
  ser.write(command.encode())
  ser.flushInput()
  calaxis = "000001"
  speed = "8"
  time.sleep(1)
  calRobot(calaxis,speed)
  gotoRestPos()
  almStatusLab.config(text='CALIBRATION SUCCESSFUL', bg = "cornflowerblue")
  almStatusLab2.config(text='CALIBRATION SUCCESSFUL', bg = "cornflowerblue")	
  blockEncPosCal = 0 

def calRobotJ1():
  global blockEncPosCal
  blockEncPosCal = 1
  calaxis = "100000"
  speed = "20"
  calRobot(calaxis,speed)
  ### calc correct calibration direction
  if(J1caldir == J1motdir):
    J1caldrive = "1"
  else:
    J1caldrive = "0"            
  command = "MJA"+J1caldrive+"500"+"S15G10H10I10K10"+"\n"
  ser.write(command.encode())
  ser.flushInput()
  speed = "8"
  time.sleep(2.5)
  calRobot(calaxis,speed)
  blockEncPosCal = 0 

def calRobotJ2():
  global blockEncPosCal
  blockEncPosCal = 1
  calaxis = "010000"
  speed = "40"
  calRobot(calaxis,speed)
  ### calc correct calibration direction    
  if(J2caldir == J2motdir):
    J2caldrive = "1"
  else:
    J2caldrive = "0"     
  command = "MJB"+J2caldrive+"500"+"S15G10H10I10K10"+"\n"
  ser.write(command.encode())
  ser.flushInput()
  speed = "8"
  time.sleep(2.5)
  calRobot(calaxis,speed)  
  blockEncPosCal = 0 

def calRobotJ3():
  global blockEncPosCal
  blockEncPosCal = 1
  calaxis = "001000"
  speed = "40"
  calRobot(calaxis,speed)
  ### calc correct calibration direction
  if(J3caldir == J3motdir):
    J3caldrive = "1"
  else:
    J3caldrive = "0"        
  command = "MJC"+J3caldrive+"500"+"S15G10H10I10K10"+"\n"
  ser.write(command.encode())
  ser.flushInput()
  speed = "8"
  time.sleep(2.5)
  calRobot(calaxis,speed)  
  blockEncPosCal = 0 

def calRobotJ4():
  global blockEncPosCal
  blockEncPosCal = 1
  calaxis = "000100"
  speed = "40"
  calRobot(calaxis,speed)
  ### calc correct calibration direction
  if(J4caldir == J4motdir):
    J4caldrive = "1"
  else:
    J4caldrive = "0" 	   
  command = "MJD"+J4caldrive+"500"+"S15G10H10I10K10"+"\n"
  ser.write(command.encode())
  ser.flushInput()
  speed = "8"
  time.sleep(2.5)
  calRobot(calaxis,speed)
  blockEncPosCal = 0   

def calRobotJ5():
  global blockEncPosCal
  blockEncPosCal = 1
  calaxis = "000010"
  speed = "40"
  calRobot(calaxis,speed)
  ### calc correct calibration direction
  if(J5caldir == J5motdir):
    J5caldrive = "1"
  else:
    J5caldrive = "0" 	       
  command = "MJE"+J5caldrive+"500"+"S15G10H10I10K10"+"\n"
  ser.write(command.encode())
  ser.flushInput()
  speed = "8"
  time.sleep(2.5)
  calRobot(calaxis,speed)
  blockEncPosCal = 0   

def calRobotJ6():
  global blockEncPosCal
  blockEncPosCal = 1
  calaxis = "000001"
  speed = "40"
  calRobot(calaxis,speed)
  ### calc correct calibration direction
  if(J6caldir == J6motdir):
    J6caldrive = "1"
  else:
    J6caldrive = "0"        
  command = "MJF"+J6caldrive+"500"+"S15G10H10I10K10"+"\n"
  ser.write(command.encode())
  ser.flushInput()
  speed = "8"
  time.sleep(2.5)
  calRobot(calaxis,speed)
  blockEncPosCal = 0  
	
	

def calRobot(calaxis,speed):
  J1axis = calaxis[:-5]
  J2axis = calaxis[1:-4]
  J3axis = calaxis[2:-3]
  J4axis = calaxis[3:-2]
  J5axis = calaxis[4:-1]
  J6axis = calaxis[5:]
  ###
  if (J1axis == "1"):
    J1step = str(J1StepLim)
  else:
    J1step = "0"
  if (J2axis == "1"):
    J2step = str(J2StepLim)
  else:
    J2step = "0" 	
  if (J3axis == "1"):
    J3step = str(J3StepLim)
  else:
    J3step = "0" 	
  if (J4axis == "1"):
    J4step = str(J4StepLim)
  else:
    J4step = "0" 
  if (J5axis == "1"):
    J5step = str(J5StepLim)
  else:
    J5step = "0" 
  if (J6axis == "1"):
    J6step = str(J6StepLim)
  else:
    J6step = "0" 	
  ### calc correct calibration direction
  if(J1caldir == J1motdir):
    J1caldrive = "0"
  else:
    J1caldrive = "1"      
  if(J2caldir == J2motdir):
    J2caldrive = "0"
  else:
    J2caldrive = "1" 
  if(J3caldir == J3motdir):
    J3caldrive = "0"
  else:
    J3caldrive = "1" 
  if(J4caldir == J4motdir):
    J4caldrive = "0"
  else:
    J4caldrive = "1" 	
  if(J5caldir == J5motdir):
    J5caldrive = "0"
  else:
    J5caldrive = "1" 	
  if(J6caldir == J6motdir):
    J6caldrive = "0"
  else:
    J6caldrive = "1"    
  command = "LL"+"A"+J1caldrive+J1step+"B"+J2caldrive+J2step+"C"+J3caldrive+J3step+"D"+J4caldrive+J4step+"E"+J5caldrive+J5step+"F"+J6caldrive+J6step+"S"+str(speed)+"\n"  
  ser.write(command.encode())
  ser.flushInput()
  calvalue = ser.read()
  global calStat
  if (calvalue == b'P'):
    calStat = 1
    calibration.delete(0, END)
    ##J1##
    global J1StepCur
    global J1AngCur
    if (J1axis == "1"):
      if (J1caldir == "0"):
        J1StepCur = 0
        J1AngCur = J1NegAngLim
      else:
        J1StepCur = J1StepLim
        J1AngCur = J1PosAngLim
      J1curAngEntryField.delete(0, 'end')
      J1curAngEntryField.insert(0,str(J1AngCur))
    ###########
    ##J2##
    global J2StepCur
    global J2AngCur
    if (J2axis == "1"):
      if (J2caldir == "0"):
        J2StepCur = 0
        J2AngCur = J2NegAngLim
      else:
        J2StepCur = J2StepLim
        J2AngCur = J2PosAngLim
      J2curAngEntryField.delete(0, 'end')
      J2curAngEntryField.insert(0,str(J2AngCur))
    ###########
    ##J3##
    global J3StepCur
    global J3AngCur
    if (J3axis == "1"):
      if (J3caldir == "0"):
        J3StepCur = 0
        J3AngCur = J3NegAngLim
      else:
        J3StepCur = J3StepLim
        J3AngCur = J3PosAngLim
      J3curAngEntryField.delete(0, 'end')
      J3curAngEntryField.insert(0,str(J3AngCur))
    ###########
    ##J4##
    global J4StepCur
    global J4AngCur
    if (J4axis == "1"):
      if (J4caldir == "0"):
        J4StepCur = 0
        J4AngCur = J4NegAngLim
      else:
        J4StepCur = J4StepLim
        J4AngCur = J4PosAngLim
      J4curAngEntryField.delete(0, 'end')
      J4curAngEntryField.insert(0,str(J4AngCur))
    ###########	
    ##J5##
    global J5StepCur
    global J5AngCur
    if (J5axis == "1"):
      if (J5caldir == "0"):
        J5StepCur = 0
        J5AngCur = J5NegAngLim
      else:
        J5StepCur = J5StepLim
        J5AngCur = J5PosAngLim
      J5curAngEntryField.delete(0, 'end')
      J5curAngEntryField.insert(0,str(J5AngCur))
    ###########	
    ##J6##
    global J6StepCur
    global J6AngCur
    if (J6axis == "1"):
      if (J6caldir == "0"):
        J6StepCur = 0
        J6AngCur = J6NegAngLim
      else:
        J6StepCur = J6StepLim
        J6AngCur = J6PosAngLim
      J6curAngEntryField.delete(0, 'end')
      J6curAngEntryField.insert(0,str(J6AngCur))
    ###########		
    value=calibration.get(0,END)
    pickle.dump(value,open("ARbot.cal","wb"))
    almStatusLab.config(text='CALIBRATION SUCCESSFUL', bg = "cornflowerblue")
    almStatusLab2.config(text='CALIBRATION SUCCESSFUL', bg = "cornflowerblue")	
    DisplaySteps()
  else:
    if (calvalue == b'F'):
      calStat = 0
      almStatusLab.config(text="CALIBRATION FAILED", bg = "red")
      almStatusLab2.config(text="CALIBRATION FAILED", bg = "red")
    else:
      almStatusLab.config(text="NO CAL FEEDBACK FROM ARDUINO", bg = "red")
      almStatusLab2.config(text="NO CAL FEEDBACK FROM ARDUINO", bg = "red")	  
  CalcFwdKin()	  
  savePosData()
  command = "LM"+"A"+str(J1StepCur)+"B"+str(J2StepCur)+"C"+str(J3StepCur)+"D"+str(J4StepCur)+"E"+str(J5StepCur)+"F"+str(J6StepCur)+"\n"  
  ser.write(command.encode())
  ser.flushInput()


def calRobotMid():
  Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
  calibration.delete(0, END)
  ##J1##
  global J1StepCur
  global J1AngCur
  J1StepCur = J1StepLim/2
  J1AngCur = 0
  J1curAngEntryField.delete(0, 'end')
  J1curAngEntryField.insert(0,str(J1AngCur))
  ###########
  ##J2## j2 goes to -90 given axis not centered
  global J2StepCur
  global J2AngCur
  J2StepCur = (J2StepLim/abs(J2NegAngLim))*(abs(J2NegAngLim)-90)
  J2AngCur = -90
  J2curAngEntryField.delete(0, 'end')
  J2curAngEntryField.insert(0,str(J2AngCur))
  ###########
  ##J3##  j3 goes to 1 given axis not centered
  global J3StepCur
  global J3AngCur
  J3StepCur = 0
  J3AngCur = 1.05
  J3curAngEntryField.delete(0, 'end')
  J3curAngEntryField.insert(0,str(J3AngCur))
  ###########
  ##J4##
  global J4StepCur
  global J4AngCur
  J4StepCur = J4StepLim/2
  J4AngCur = 0
  J4curAngEntryField.delete(0, 'end')
  J4curAngEntryField.insert(0,str(J4AngCur))
  ###########
  ##J5##
  global J5StepCur
  global J5AngCur
  J5StepCur = J5StepLim/2
  J5AngCur = 0
  J5curAngEntryField.delete(0, 'end')
  J5curAngEntryField.insert(0,str(J5AngCur))
  ###########
  ##J6##
  global J6StepCur
  global J6AngCur
  J6StepCur = J6StepLim/2
  J6AngCur = 0
  J6curAngEntryField.delete(0, 'end')
  J6curAngEntryField.insert(0,str(J6AngCur))
  ###########
  ##J7##
  global TrackStepLim
  global TrackcurPos
  global TrackLength
  TrackStepLim = TrackStepLim/2
  TrackcurPos = TrackLength/2
  TrackcurEntryField.delete(0, 'end')
  TrackcurEntryField.insert(0,str(TrackcurPos))
  ###########  
  value=calibration.get(0,END)
  pickle.dump(value,open("ARbot.cal","wb"))
  almStatusLab.config(text="CALIBRATED TO REST POSITION", bg = "orange")
  almStatusLab2.config(text="CALIBRATED TO REST POSITION", bg = "orange")
  tab6.ElogView.insert(END, Curtime+" - "+"CALIBRATED TO REST POSITION")
  CalcFwdKin()
  DisplaySteps()
  savePosData()
  command = "LM"+"A"+str(J1StepCur)+"B"+str(J2StepCur)+"C"+str(J3StepCur)+"D"+str(J4StepCur)+"E"+str(J5StepCur)+"F"+str(J6StepCur)+"\n"  
  ser.write(command.encode())
  ser.flushInput()

def savePosData():
  calibration.delete(0, END)
  calibration.insert(END, J1StepCur)
  calibration.insert(END, J1AngCur)
  calibration.insert(END, J2StepCur)
  calibration.insert(END, J2AngCur)
  calibration.insert(END, J3StepCur)
  calibration.insert(END, J3AngCur)
  calibration.insert(END, J4StepCur)
  calibration.insert(END, J4AngCur)
  calibration.insert(END, J5StepCur)
  calibration.insert(END, J5AngCur)
  calibration.insert(END, J6StepCur)
  calibration.insert(END, J6AngCur)
  calibration.insert(END, comPortEntryField.get())  
  calibration.insert(END, ProgEntryField.get())
  calibration.insert(END, servo0onEntryField.get())
  calibration.insert(END, servo0offEntryField.get())
  calibration.insert(END, servo1onEntryField.get())
  calibration.insert(END, servo1offEntryField.get())
  calibration.insert(END, DO1onEntryField.get())
  calibration.insert(END, DO1offEntryField.get())
  calibration.insert(END, DO2onEntryField.get())
  calibration.insert(END, DO2offEntryField.get())
  calibration.insert(END, UFxEntryField.get())
  calibration.insert(END, UFyEntryField.get())
  calibration.insert(END, UFzEntryField.get())
  calibration.insert(END, UFrxEntryField.get())
  calibration.insert(END, UFryEntryField.get())
  calibration.insert(END, UFrzEntryField.get())
  calibration.insert(END, TFxEntryField.get())
  calibration.insert(END, TFyEntryField.get())
  calibration.insert(END, TFzEntryField.get())
  calibration.insert(END, TFrxEntryField.get())
  calibration.insert(END, TFryEntryField.get())
  calibration.insert(END, TFrzEntryField.get())
  calibration.insert(END, fineCalEntryField.get())
  calibration.insert(END, J1NegAngLimEntryField.get())
  calibration.insert(END, J1PosAngLimEntryField.get())
  calibration.insert(END, J1StepLimEntryField.get())
  calibration.insert(END, J2NegAngLimEntryField.get())
  calibration.insert(END, J2PosAngLimEntryField.get())
  calibration.insert(END, J2StepLimEntryField.get())
  calibration.insert(END, J3NegAngLimEntryField.get())
  calibration.insert(END, J3PosAngLimEntryField.get())
  calibration.insert(END, J3StepLimEntryField.get())
  calibration.insert(END, J4NegAngLimEntryField.get())
  calibration.insert(END, J4PosAngLimEntryField.get())
  calibration.insert(END, J4StepLimEntryField.get())
  calibration.insert(END, J5NegAngLimEntryField.get())
  calibration.insert(END, J5PosAngLimEntryField.get())
  calibration.insert(END, J5StepLimEntryField.get())
  calibration.insert(END, J6NegAngLimEntryField.get())
  calibration.insert(END, J6PosAngLimEntryField.get())
  calibration.insert(END, J6StepLimEntryField.get())
  calibration.insert(END, DHr1EntryField.get())
  calibration.insert(END, DHr2EntryField.get())
  calibration.insert(END, DHr3EntryField.get())
  calibration.insert(END, DHr4EntryField.get())
  calibration.insert(END, DHr5EntryField.get())
  calibration.insert(END, DHr6EntryField.get())
  calibration.insert(END, DHa1EntryField.get())
  calibration.insert(END, DHa2EntryField.get())
  calibration.insert(END, DHa3EntryField.get())
  calibration.insert(END, DHa4EntryField.get())
  calibration.insert(END, DHa5EntryField.get())
  calibration.insert(END, DHa6EntryField.get())
  calibration.insert(END, DHd1EntryField.get())
  calibration.insert(END, DHd2EntryField.get())
  calibration.insert(END, DHd3EntryField.get())
  calibration.insert(END, DHd4EntryField.get())
  calibration.insert(END, DHd5EntryField.get())
  calibration.insert(END, DHd6EntryField.get())
  calibration.insert(END, DHt1EntryField.get())
  calibration.insert(END, DHt2EntryField.get())
  calibration.insert(END, DHt3EntryField.get())
  calibration.insert(END, DHt4EntryField.get())
  calibration.insert(END, DHt5EntryField.get())
  calibration.insert(END, DHt6EntryField.get())
  calibration.insert(END, CalDirEntryField.get())
  calibration.insert(END, MotDirEntryField.get())
  calibration.insert(END, TrackcurEntryField.get())
  calibration.insert(END, TrackLengthEntryField.get())
  calibration.insert(END, TrackStepLimEntryField.get())
  calibration.insert(END, VisFileLocEntryField.get())
  calibration.insert(END, visoptions.get())
  calibration.insert(END, VisPicOxPEntryField.get())
  calibration.insert(END, VisPicOxMEntryField.get())
  calibration.insert(END, VisPicOyPEntryField.get())
  calibration.insert(END, VisPicOyMEntryField.get())
  calibration.insert(END, VisPicXPEntryField.get())
  calibration.insert(END, VisPicXMEntryField.get())
  calibration.insert(END, VisPicYPEntryField.get())
  calibration.insert(END, VisPicYMEntryField.get())
  calibration.insert(END, com2PortEntryField.get())
  calibration.insert(END, J1OpenLoopVal)
  calibration.insert(END, J2OpenLoopVal)
  calibration.insert(END, J3OpenLoopVal)
  calibration.insert(END, J4OpenLoopVal)
  calibration.insert(END, J5OpenLoopVal)
  calibration.insert(END, J6OpenLoopVal)
  ###########
  value=calibration.get(0,END)
  pickle.dump(value,open("ARbot.cal","wb"))

def SaveAndApplyCalibration():
  global J1NegAngLim
  global J1PosAngLim
  global J1StepLim
  global J1DegPerStep
  global J1StepCur
  global J1AngCur
  global J2NegAngLim
  global J2PosAngLim
  global J2StepLim
  global J2DegPerStep
  global J2StepCur
  global J2AngCur
  global J2NegAngLim
  global J2PosAngLim
  global J2StepLim
  global J2DegPerStep
  global J2StepCur
  global J2AngCur
  global J3NegAngLim
  global J3PosAngLim
  global J3StepLim
  global J3DegPerStep
  global J3StepCur
  global J3AngCur
  global J4NegAngLim
  global J4PosAngLim
  global J4StepLim
  global J4DegPerStep
  global J4StepCur
  global J4AngCur
  global J5NegAngLim
  global J5PosAngLim
  global J5StepLim
  global J5DegPerStep
  global J5StepCur
  global J5AngCur
  global J6NegAngLim
  global J6PosAngLim
  global J6StepLim
  global J6DegPerStep
  global J6StepCur
  global J6AngCur
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global DHr1
  global DHr2
  global DHr3
  global DHr4
  global DHr5
  global DHr6
  global DHa1
  global DHa2
  global DHa3
  global DHa4
  global DHa5
  global DHa6
  global DHd1
  global DHd2
  global DHd3
  global DHd4
  global DHd5
  global DHd6
  global DHt1
  global DHt2
  global DHt3
  global DHt4
  global DHt5
  global DHt6
  global CalDir
  global J1caldir
  global J2caldir
  global J3caldir
  global J4caldir
  global J5caldir
  global J6caldir 
  global MotDir
  global J1motdir
  global J2motdir
  global J3motdir
  global J4motdir
  global J5motdir
  global J6motdir
  global TrackcurPos
  global TrackLength
  global TrackStepLim
  global VisFileLoc
  global VisProg
  global VisOrigXpix
  global VisOrigXmm
  global VisOrigYpix
  global VisOrigYmm
  global VisEndXpix
  global VisEndXmm
  global VisEndYpix
  global VisEndYmm 
  global J1OpenLoopVal
  global J2OpenLoopVal
  global J3OpenLoopVal
  global J4OpenLoopVal
  global J5OpenLoopVal
  global J6OpenLoopVal 
  ###joint variables
  J1NegAngLim = float(J1NegAngLimEntryField.get())
  J1PosAngLim = float(J1PosAngLimEntryField.get())
  J1StepLim = int(J1StepLimEntryField.get())
  J1DegPerStep = float((J1PosAngLim - J1NegAngLim)/float(J1StepLim))
  J2NegAngLim = float(J2NegAngLimEntryField.get())
  J2PosAngLim = float(J2PosAngLimEntryField.get())
  J2StepLim = int(J2StepLimEntryField.get())
  J2DegPerStep = float((J2PosAngLim - J2NegAngLim)/float(J2StepLim))
  J3NegAngLim = float(J3NegAngLimEntryField.get())
  J3PosAngLim = float(J3PosAngLimEntryField.get())
  J3StepLim = int(J3StepLimEntryField.get())
  J3DegPerStep = float((J3PosAngLim - J3NegAngLim)/float(J3StepLim))
  J4NegAngLim = float(J4NegAngLimEntryField.get())
  J4PosAngLim = float(J4PosAngLimEntryField.get())
  J4StepLim = int(J4StepLimEntryField.get())
  J4DegPerStep = float((J4PosAngLim - J4NegAngLim)/float(J4StepLim))
  J5NegAngLim = float(J5NegAngLimEntryField.get())
  J5PosAngLim = float(J5PosAngLimEntryField.get())
  J5StepLim = int(J5StepLimEntryField.get())
  J5DegPerStep = float((J5PosAngLim - J5NegAngLim)/float(J5StepLim))
  J6NegAngLim = float(J6NegAngLimEntryField.get())
  J6PosAngLim = float(J6PosAngLimEntryField.get())
  J6StepLim = int(J6StepLimEntryField.get())
  J6DegPerStep = float((J6PosAngLim - J6NegAngLim)/float(J6StepLim))
  ####AXIS LIMITS LABELS GREEN######
  AxLimCol = "OliveDrab4"
  J1PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J1PosAngLim)))
  J1PlimLab.place(x=685, y=10)
  J1NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J1NegAngLim)))
  J1NlimLab.place(x=635, y=10)
  J2PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J2PosAngLim)))
  J2PlimLab.place(x=780, y=10)
  J2NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J2NegAngLim)))
  J2NlimLab.place(x=725, y=10)
  J3PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J3PosAngLim)))
  J3PlimLab.place(x=868, y=10)
  J3NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J3NegAngLim)))
  J3NlimLab.place(x=825, y=10)
  J4PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J4PosAngLim)))
  J4PlimLab.place(x=960, y=10)
  J4NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J4NegAngLim)))
  J4NlimLab.place(x=905, y=10)
  J5PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J5PosAngLim)))
  J5PlimLab.place(x=1050, y=10)
  J5NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J5NegAngLim)))
  J5NlimLab.place(x=995, y=10)
  J6PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J6PosAngLim)))
  J6PlimLab.place(x=1140, y=10)
  J6NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J6NegAngLim)))
  J6NlimLab.place(x=1085, y=10)
  DHr1 = float(DHr1EntryField.get())
  DHr2 = float(DHr2EntryField.get())
  DHr3 = float(DHr3EntryField.get())
  DHr4 = float(DHr4EntryField.get())
  DHr5 = float(DHr5EntryField.get())
  DHr6 = float(DHr6EntryField.get())
  DHa1 = float(DHa1EntryField.get())
  DHa2 = float(DHa2EntryField.get())
  DHa3 = float(DHa3EntryField.get())
  DHa4 = float(DHa4EntryField.get())
  DHa5 = float(DHa5EntryField.get())
  DHa6 = float(DHa6EntryField.get())
  DHd1 = float(DHd1EntryField.get())
  DHd2 = float(DHd2EntryField.get())
  DHd3 = float(DHd3EntryField.get())
  DHd4 = float(DHd4EntryField.get())
  DHd5 = float(DHd5EntryField.get())
  DHd6 = float(DHd6EntryField.get())
  DHt1 = float(DHt1EntryField.get())
  DHt2 = float(DHt2EntryField.get())
  DHt3 = float(DHt3EntryField.get())
  DHt4 = float(DHt4EntryField.get())
  DHt5 = float(DHt5EntryField.get())
  DHt6 = float(DHt6EntryField.get())
  CalDir = CalDirEntryField.get()
  J1caldir = CalDir[:-5]
  J2caldir = CalDir[1:-4]
  J3caldir = CalDir[2:-3]
  J4caldir = CalDir[3:-2]
  J5caldir = CalDir[4:-1]
  J6caldir = CalDir[5:] 
  MotDir = MotDirEntryField.get()
  J1motdir = MotDir[:-5]
  J2motdir = MotDir[1:-4]
  J3motdir = MotDir[2:-3]
  J4motdir = MotDir[3:-2]
  J5motdir = MotDir[4:-1]
  J6motdir = MotDir[5:]
  TrackcurPos = float(TrackcurEntryField.get())
  TrackLength = float(TrackLengthEntryField.get())
  TrackStepLim = float(TrackStepLimEntryField.get())
  VisFileLoc = VisFileLocEntryField.get()
  VisProg = visoptions.get()
  VisOrigXpix = float(VisPicOxPEntryField.get())
  VisOrigXmm  = float(VisPicOxMEntryField.get())
  VisOrigYpix = float(VisPicOyPEntryField.get())
  VisOrigYmm  = float(VisPicOyMEntryField.get())
  VisEndXpix  = float(VisPicXPEntryField.get())
  VisEndXmm   = float(VisPicXMEntryField.get())
  VisEndYpix  = float(VisPicYPEntryField.get())
  VisEndYmm   = float(VisPicYMEntryField.get())
  J1OpenLoopVal = int(J1OpenLoopStat.get())
  J2OpenLoopVal = int(J2OpenLoopStat.get())
  J3OpenLoopVal = int(J3OpenLoopStat.get())
  J4OpenLoopVal = int(J4OpenLoopStat.get())
  J5OpenLoopVal = int(J5OpenLoopStat.get())
  J6OpenLoopVal = int(J6OpenLoopStat.get())

  savePosData()

def DisplaySteps():
  J1stepsLab['text'] = str(int(J1StepCur))
  J2stepsLab['text'] = str(int(J2StepCur))
  J3stepsLab['text'] = str(int(J3StepCur))
  J4stepsLab['text'] = str(int(J4StepCur))
  J5stepsLab['text'] = str(int(J5StepCur))
  J6stepsLab['text'] = str(int(J6StepCur))



  

def gotoFineCalPos():
  command = fineCalEntryField.get() 
  J1newIndex = command.find("X) ")
  J2newIndex = command.find("Y) ")
  J3newIndex = command.find("Z) ")
  J4newIndex = command.find("W) ")
  J5newIndex = command.find("P) ")
  J6newIndex = command.find("R) ")
  TRnewIndex = command.find("T) ")	
  SpeedIndex = command.find("Speed-")
  ACCdurIndex = command.find("Ad")
  ACCspdIndex = command.find("As")
  DECdurIndex = command.find("Dd")
  DECspdIndex = command.find("Ds")
  WristConfIndex = command.find("$")
  CX = float(command[J1newIndex+3:J2newIndex-1])
  CY = float(command[J2newIndex+3:J3newIndex-1])
  CZ = float(command[J3newIndex+3:J4newIndex-1])
  CRx = float(command[J4newIndex+3:J5newIndex-1])
  CRy = float(command[J5newIndex+3:J6newIndex-1])
  CRz = float(command[J6newIndex+3:TRnewIndex-1])
  Track = float(command[TRnewIndex+3:SpeedIndex-1])
  newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
  ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
  ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
  DECdur = command[DECdurIndex+3:DECspdIndex-1]
  DECspd = command[DECspdIndex+3:WristConfIndex-1]
  WC = command[WristConfIndex+1:]
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Code = 0  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
  almStatusLab.config(text="MOVED TO FINE CALIBRATION POSITION", bg = "yellow")
  almStatusLab2.config(text="MOVED TO FINE CALIBRATION POSITION", bg = "yellow")
  
  
def gotoRestPos():
  command = "Move J [*]  X) 68.944   Y) 0.0   Z) 733.607   W) -90.0   P) 1.05   R) -90.0   T) 201.5   Speed-50 Ad 15 As 10 Dd 20 Ds 5 $F" 
  J1newIndex = command.find("X) ")
  J2newIndex = command.find("Y) ")
  J3newIndex = command.find("Z) ")
  J4newIndex = command.find("W) ")
  J5newIndex = command.find("P) ")
  J6newIndex = command.find("R) ")
  TRnewIndex = command.find("T) ")	
  SpeedIndex = command.find("Speed-")
  ACCdurIndex = command.find("Ad")
  ACCspdIndex = command.find("As")
  DECdurIndex = command.find("Dd")
  DECspdIndex = command.find("Ds")
  WristConfIndex = command.find("$")
  CX = float(command[J1newIndex+3:J2newIndex-1])
  CY = float(command[J2newIndex+3:J3newIndex-1])
  CZ = float(command[J3newIndex+3:J4newIndex-1])
  CRx = float(command[J4newIndex+3:J5newIndex-1])
  CRy = float(command[J5newIndex+3:J6newIndex-1])
  CRz = float(command[J6newIndex+3:TRnewIndex-1])
  Track = float(command[TRnewIndex+3:SpeedIndex-1])
  newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
  ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
  ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
  DECdur = command[DECdurIndex+3:DECspdIndex-1]
  DECspd = command[DECspdIndex+3:WristConfIndex-1]
  WC = command[WristConfIndex+1:]
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Code = 0  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

  
def exeFineCalPos():
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  command = fineCalEntryField.get() 
  J1newIndex = command.find("X) ")
  J2newIndex = command.find("Y) ")
  J3newIndex = command.find("Z) ")
  J4newIndex = command.find("W) ")
  J5newIndex = command.find("P) ")
  J6newIndex = command.find("R) ")
  TRnewIndex = command.find("T) ")	
  SpeedIndex = command.find("Speed-")
  ACCdurIndex = command.find("Ad")
  ACCspdIndex = command.find("As")
  DECdurIndex = command.find("Dd")
  DECspdIndex = command.find("Ds")
  WristConfIndex = command.find("$")
  CX = float(command[J1newIndex+3:J2newIndex-1])
  CY = float(command[J2newIndex+3:J3newIndex-1])
  CZ = float(command[J3newIndex+3:J4newIndex-1])
  CRx = float(command[J4newIndex+3:J5newIndex-1])
  CRy = float(command[J5newIndex+3:J6newIndex-1])
  CRz = float(command[J6newIndex+3:TRnewIndex-1])
  Track = float(command[TRnewIndex+3:SpeedIndex-1])
  newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
  ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
  ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
  DECdur = command[DECdurIndex+3:DECspdIndex-1]
  DECspd = command[DECspdIndex+3:WristConfIndex-1]
  WC = command[WristConfIndex+1:]
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Code = 1  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
  almStatusLab.config(text="CALIBRATED TO FINE CALIBRATE POSITION", bg = "orange")
  almStatusLab2.config(text="CALIBRATED TO FINE CALIBRATE POSITION", bg = "orange")  
  CalcFwdKin()
  DisplaySteps()
  savePosData()
  command = "LM"+"A"+str(J1StepCur)+"B"+str(J2StepCur)+"C"+str(J3StepCur)+"D"+str(J4StepCur)+"E"+str(J5StepCur)+"F"+str(J6StepCur)+"\n"  
  ser.write(command.encode())
  ser.flushInput()

def CalTrackPos():
  global TrackcurPos  
  TrackcurPos = 0 
  TrackcurEntryField.delete(0, 'end')  
  TrackcurEntryField.insert(0,str(TrackcurPos))
  savePosData()   
  
  
def monitorEnc():
  global blockEncPosMove
  global blockEncPosCal
  while True:
    if blockEncPosMove == 0 and blockEncPosCal == 0:
      getRobotPosition()
    time.sleep(2)  
	
	

###VISION DEFS###################################################################
#################################################################################	
 
def testvis():  
  visprog = visoptions.get()
  if(visprog[:]== "Openvision"):
    openvision()
  if(visprog[:]== "Roborealm 1.7.5"):
    roborealm175()
  if(visprog[:]== "x,y,r"):
    xyr()	
	
	

def openvision():
  global Xpos
  global Ypos
  global VisEndYmm
  visfail = 1
  while (visfail == 1):
    value = 0
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
    while (value == 0): 
      try:
        with  open(VisFileLoc,"r") as file:
          value = file.readlines()[-1]#.decode()
      except:
        value = 0  
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
    x = int(value[110:122])
    y = int(value[130:142])
    viscalc(x,y)
    if (Ypos > VisEndYmm):
      visfail = 1
      time.sleep(.1)
    else:
      visfail = 0
  open(VisFileLoc,"w").close()	  
  VisXfindEntryField.delete(0, 'end')
  VisXfindEntryField.insert(0,Xpos) 
  VisYfindEntryField.delete(0, 'end')
  VisYfindEntryField.insert(0,Ypos) 
  VisRZfindEntryField.delete(0, 'end')
  VisRZfindEntryField.insert(0,0)
  ##
  VisXpixfindEntryField.delete(0, 'end')
  VisXpixfindEntryField.insert(0,x) 
  VisYpixfindEntryField.delete(0, 'end')
  VisYpixfindEntryField.insert(0,y) 
  ##
  SP_1_E1_EntryField.delete(0, 'end')
  SP_1_E1_EntryField.insert(0,Xpos) 
  SP_1_E2_EntryField.delete(0, 'end')
  SP_1_E2_EntryField.insert(0,Ypos) 
 


  
def roborealm175():
  global Xpos
  global Ypos
  global VisEndYmm
  visfail = 1
  while (visfail == 1):
    value = 0
    almStatusLab.config(text="WAITING FOR CAMERA", bg = "yellow")
    almStatusLab2.config(text="WAITING FOR CAMERA", bg = "yellow")
    while (value == 0): 
      try:
        with  open(VisFileLoc,"r") as file:
          value = file.readlines()[-1]#.decode()
      except:
        value = 0 
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
    Index = value.find(",")
    x = float(value[:Index])
    y = float(value[Index+1:])
    viscalc(x,y)
    if (Ypos > VisEndYmm):
      visfail = 1
      time.sleep(.1)
    else:
      visfail = 0    
  open(VisFileLoc,"w").close() 
  VisXfindEntryField.delete(0, 'end')
  VisXfindEntryField.insert(0,Xpos) 
  VisYfindEntryField.delete(0, 'end')
  VisYfindEntryField.insert(0,Ypos) 
  VisRZfindEntryField.delete(0, 'end')
  VisRZfindEntryField.insert(0,0)
  ##
  VisXpixfindEntryField.delete(0, 'end')
  VisXpixfindEntryField.insert(0,x) 
  VisYpixfindEntryField.delete(0, 'end')
  VisYpixfindEntryField.insert(0,y) 
  ##
  SP_1_E1_EntryField.delete(0, 'end')
  SP_1_E1_EntryField.insert(0,Xpos) 
  SP_1_E2_EntryField.delete(0, 'end')
  SP_1_E2_EntryField.insert(0,Ypos) 
 


def xyr():
  global Xpos
  global Ypos
  global VisEndYmm
  visfail = 1
  while (visfail == 1):
    value = 0
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
    while (value == 0): 
      try:
        with  open(VisFileLoc,"r") as file:
          value = file.readlines()[-1]#.decode()
      except:
        value = 0 
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
    Index = value.find(",")
    x = float(value[:Index])
    value2 = value[Index+1:]
    Index2 = value2.find(",")
    y = float(value2[:Index2])
    r = float(value2[Index2+1:])
    viscalc(x,y)
    if (Ypos > VisEndYmm):
      visfail = 1
      time.sleep(.1)
    else:
      visfail = 0
  open(VisFileLoc,"w").close() 
  VisXfindEntryField.delete(0, 'end')
  VisXfindEntryField.insert(0,Xpos) 
  VisYfindEntryField.delete(0, 'end')
  VisYfindEntryField.insert(0,Ypos) 
  VisRZfindEntryField.delete(0, 'end')
  VisRZfindEntryField.insert(0,r)
  ##
  VisXpixfindEntryField.delete(0, 'end')
  VisXpixfindEntryField.insert(0,x) 
  VisYpixfindEntryField.delete(0, 'end')
  VisYpixfindEntryField.insert(0,y) 
  ##
  SP_1_E1_EntryField.delete(0, 'end')
  SP_1_E1_EntryField.insert(0,str(Xpos)) 
  SP_1_E2_EntryField.delete(0, 'end')
  SP_1_E2_EntryField.insert(0,str(Ypos)) 
  SP_1_E3_EntryField.delete(0, 'end')
  SP_1_E3_EntryField.insert(0,r)
    
  

def viscalc(x,y):
  global VisOrigXpix
  global VisOrigXmm
  global VisOrigYpix
  global VisOrigYmm
  global VisEndXpix
  global VisEndXmm
  global VisEndYpix
  global VisEndYmm
  global Xpos
  global Ypos
  XPrange = float(VisEndXpix - VisOrigXpix)
  XPratio = float((x-VisOrigXpix)/XPrange)
  XMrange = float(VisEndXmm - VisOrigXmm)
  XMpos = float(XMrange * XPratio)
  Xpos = float(VisOrigXmm + XMpos)
  ##
  YPrange = float(VisEndYpix - VisOrigYpix)
  YPratio = float((y-VisOrigYpix)/YPrange)
  YMrange = float(VisEndYmm - VisOrigYmm)
  YMpos = float(YMrange * YPratio)
  Ypos = float(VisOrigYmm + YMpos)
  return (Xpos,Ypos)

 
 
  
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
#####TAB 1



  

###LABELS#################################################################
##########################################################################

curRowLab = Label(tab1, text = "Current Row  = ")
curRowLab.place(x=220, y=150)

almStatusLab = Label(tab1, text = "SYSTEM READY - NO ACTIVE ALARMS", bg = "cornflowerblue")
almStatusLab.place(x=10, y=10)

xbcStatusLab = Label(tab1, text = "Xbox OFF", bg = "salmon")
xbcStatusLab.place(x=1335, y=200)

runStatusLab = Label(tab1, text = "PROGRAM STOPPED", bg = "red")
runStatusLab.place(x=20, y=150)



manEntLab = Label(tab1, font=("Arial", 6), text = "Manual Program Entry")
manEntLab.place(x=630, y=630)

ifOnLab = Label(tab1,font=("Arial", 6), text = "Input           Tab")
ifOnLab.place(x=1092, y=348)

ifOffLab = Label(tab1,font=("Arial", 6), text = "Input           Tab")
ifOffLab.place(x=1092, y=388)

regEqLab = Label(tab1,font=("Arial", 6), text = "Register         Num (++/- -)")
regEqLab.place(x=1077, y=467)

ifregTabJmpLab = Label(tab1,font=("Arial", 6), text = "Register             Num              Jump to Tab")
ifregTabJmpLab.place(x=1077, y=507)

servoLab = Label(tab1,font=("Arial", 6), text = "Number      Position")
servoLab.place(x=1092, y=428)

ComPortLab = Label(tab1, text = "TEENSY-3.5 COM PORT:")
ComPortLab.place(x=310, y=40)

Com2PortLab = Label(tab1, text = "MEGA-2560 COM PORT:")
Com2PortLab.place(x=310, y=65)


ProgLab = Label(tab1, text = "Program:")
ProgLab.place(x=10, y=45)

speedLab = Label(tab1, text = "Robot Speed    (%)")
speedLab.place(x=356, y=100)

ACCLab = Label(tab1, text = "ACC(dur/speed %)")
ACCLab.place(x=356, y=125)

DECLab = Label(tab1, text = "DEC(dur/speed %)")
DECLab.place(x=356, y=150)


J1Lab = Label(tab1, font=("Arial", 18), text = "J1")
J1Lab.place(x=660, y=5)

J2Lab = Label(tab1, font=("Arial",18), text = "J2")
J2Lab.place(x=750, y=5)

J3Lab = Label(tab1, font=("Arial", 18), text = "J3")
J3Lab.place(x=840, y=5)

J4Lab = Label(tab1, font=("Arial", 18), text = "J4")
J4Lab.place(x=930, y=5)

J5Lab = Label(tab1, font=("Arial", 18), text = "J5")
J5Lab.place(x=1020, y=5)

J6Lab = Label(tab1, font=("Arial", 18), text = "J6")
J6Lab.place(x=1110, y=5)


####STEPS LABELS BLUE######
stepCol = "SteelBlue4"

StepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "/step")
StepsLab.place(x=620, y=40)

J1stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J1stepsLab.place(x=695, y=40)

J2stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J2stepsLab.place(x=785, y=40)

J3stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J3stepsLab.place(x=875, y=40)

J4stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J4stepsLab.place(x=965, y=40)

J5stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J5stepsLab.place(x=1055, y=40)

J6stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J6stepsLab.place(x=1145, y=40)



XLab = Label(tab1, font=("Arial", 18), text = " X")
XLab.place(x=660, y=125)

YLab = Label(tab1, font=("Arial",18), text = " Y")
YLab.place(x=750, y=125)

ZLab = Label(tab1, font=("Arial", 18), text = " Z")
ZLab.place(x=840, y=125)

yLab = Label(tab1, font=("Arial", 18), text = " W")
yLab.place(x=930, y=125)

pLab = Label(tab1, font=("Arial", 18), text = " P")
pLab.place(x=1020, y=125)

rLab = Label(tab1, font=("Arial", 18), text = " R")
rLab.place(x=1110, y=125)



TrackLab = Label(tab1, font=("Arial", 18), text = "Track")
TrackLab.place(x=1217, y=125)




TXLab = Label(tab1, font=("Arial", 18), text = "Tx")
TXLab.place(x=660, y=250)

TYLab = Label(tab1, font=("Arial",18), text = "Ty")
TYLab.place(x=750, y=250)

TZLab = Label(tab1, font=("Arial", 18), text = "Tz")
TZLab.place(x=840, y=250)

TyLab = Label(tab1, font=("Arial", 18), text = "Tw")
TyLab.place(x=930, y=250)

TpLab = Label(tab1, font=("Arial", 18), text = "Tp")
TpLab.place(x=1020, y=250)

TrLab = Label(tab1, font=("Arial", 18), text = "Tr")
TrLab.place(x=1110, y=250)






J1curAngLab = Label(tab1, text = "Current Angle:")
J1curAngLab.place(x=540, y=40)

XYZcurPoLab = Label(tab1, text = "Current Position:")
XYZcurPoLab.place(x=540, y=160)

J1jogDegsLab = Label(tab1, text = "Degrees to Jog:")
J1jogDegsLab.place(x=540, y=65)

XYZjogMMLab = Label(tab1, text = "Millimeters to Jog:")
XYZjogMMLab.place(x=540, y=185)

J1jogRobotLab = Label(tab1, text = "JOG ROBOT")
J1jogRobotLab.place(x=540, y=92)

XYZjogRobotLab = Label(tab1, text = "JOG ROBOT")
XYZjogRobotLab.place(x=540, y=212)

TXYZjogMMLab = Label(tab1, text = "Millimeters to Jog:")
TXYZjogMMLab.place(x=540, y=285)

TXYZjogRobotLab = Label(tab1, text = "JOG ROBOT")
TXYZjogRobotLab.place(x=540, y=310)



waitTequalsLab = Label(tab1, text = "=")
waitTequalsLab.place(x=855, y=360)

waitIequalsLab = Label(tab1, text = "=")
waitIequalsLab.place(x=855, y=400)

waitIoffequalsLab = Label(tab1, text = "=")
waitIoffequalsLab.place(x=855, y=440)

outputOnequalsLab = Label(tab1, text = "=")
outputOnequalsLab.place(x=855, y=480)

outputOffequalsLab = Label(tab1, text = "=")
outputOffequalsLab.place(x=855, y=520)

tabequalsLab = Label(tab1, text = "=")
tabequalsLab.place(x=1355, y=360)

jumpequalsLab = Label(tab1, text = "=")
jumpequalsLab.place(x=1355, y=400)

jumpIfOnequalsLab = Label(tab1, text = "=")
jumpIfOnequalsLab.place(x=1075, y=360)

jumpIfOffequalsLab = Label(tab1, text = "=")
jumpIfOffequalsLab.place(x=1075, y=400)

servoequalsLab = Label(tab1, text = "=")
servoequalsLab.place(x=1075, y=440)

changeProgequalsLab = Label(tab1, text = "=")
changeProgequalsLab.place(x=695, y=560)

regequalsLab = Label(tab1, text = "=")
regequalsLab.place(x=1117, y=481)

regJmpequalsLab = Label(tab1, text = "=")
regJmpequalsLab.place(x=1117, y=521)

savePositionLab = Label(tab1, text = "Stored Position  = ")
savePositionLab.place(x=542, y=400)




storPosEqLab = Label(tab1,font=("Arial", 6), text = " StorPos            Element          Num (++/- -)")
storPosEqLab.place(x=1077, y=547)

storPosequalsLab = Label(tab1, text = "=")
storPosequalsLab.place(x=1117, y=561)


###BUTTONS################################################################
##########################################################################



manInsBut = Button(tab1, borderwidth=3, text="Insert", height=1, width=6, relief=RAISED, command = manInsItem)
manInsBut.place(x=1220, y=641)

manRepBut = Button(tab1, borderwidth=3, text="Replace", height=1, width=6, command = manReplItem)
manRepBut.place(x=1280, y=641)

getSelBut = Button(tab1, borderwidth=3, text="Get Selected", height=1, width=10, command = getSel)
getSelBut.place(x=540, y=641)

options=StringVar(tab1)
options.set("Move J")
menu=OptionMenu(tab1, options, "Move J", "OFFS J", "Move L", "Move A Beg", "Move A Mid", "Move A End", "Move C Center", "Move C Start", "Move C Plane", "Move SP", "OFFS SP", "Teach SP")
menu.grid(row=2,column=2)
menu.place(x=540, y=360)


teachInsBut = Button(tab1, borderwidth=3,  text="Teach New Position", height=1, width=20, command = teachInsertBelSelected)
teachInsBut.place(x=540, y=440)

teachReplaceBut = Button(tab1, borderwidth=3, text="Modify Position", height=1, width=20, command = teachReplaceSelected)
teachReplaceBut.place(x=540, y=480)

waitTimeBut = Button(tab1, borderwidth=3, text="Wait Time (seconds)", height=1, width=20, command = waitTime)
waitTimeBut.place(x=700, y=360)

waitInputOnBut = Button(tab1, borderwidth=3, text="Wait Input ON", height=1, width=20, command = waitInputOn)
waitInputOnBut.place(x=700, y=400)

waitInputOffBut = Button(tab1, borderwidth=3, text="Wait Input OFF", height=1, width=20, command = waitInputOff)
waitInputOffBut.place(x=700, y=440)

setOutputOnBut = Button(tab1, borderwidth=3, text="Set Output On", height=1, width=20, command = setOutputOn)
setOutputOnBut.place(x=700, y=480)

setOutputOffBut = Button(tab1, borderwidth=3, text="Set Output OFF", height=1, width=20, command = setOutputOff)
setOutputOffBut.place(x=700, y=520)

tabNumBut = Button(tab1, borderwidth=3, text="Create Tab", height=1, width=14, command = tabNumber)
tabNumBut.place(x=1240, y=360)

jumpTabBut = Button(tab1, borderwidth=3, text="Jump to Tab", height=1, width=14, command = jumpTab)
jumpTabBut.place(x=1240, y=400)

getVisBut = Button(tab1, borderwidth=3, text="Get Vision", height=1, width=14, command = getvision)
getVisBut.place(x=1240, y=440)

IfOnjumpTabBut = Button(tab1, borderwidth=3, text="If On Jump", height=1, width=20, command = IfOnjumpTab)
IfOnjumpTabBut.place(x=920, y=360)

IfOffjumpTabBut = Button(tab1, borderwidth=3, text="If Off Jump", height=1, width=20, command = IfOffjumpTab)
IfOffjumpTabBut.place(x=920, y=400)

servoBut = Button(tab1, borderwidth=3, text="Servo", height=1, width=20, command = Servo)
servoBut.place(x=920, y=440)

callBut = Button(tab1, borderwidth=3, text="Call Program", height=1, width=20, command = insertCallProg)
callBut.place(x=540, y=560)

returnBut = Button(tab1, borderwidth=3, text="Return", height=1, width=20, command = insertReturn)
returnBut.place(x=540, y=600)

comPortBut = Button(tab1, borderwidth=3, text="Set Com", font = ("Arial", 7), height=0, width=7, command = setCom)
comPortBut.place(x=473, y=35)

comPortBut2 = Button(tab1, borderwidth=3, text="Set Com", font = ("Arial", 7),height=0, width=7, command = setCom2)
comPortBut2.place(x=473, y=65)



ProgBut = Button(tab1, borderwidth=3, text="Load Program", height=0, width=12, command = loadProg)
ProgBut.place(x=202, y=42)

deleteBut = Button(tab1, borderwidth=3, text="Delete", height=1, width=20, command = deleteitem)
deleteBut.place(x=540, y=520)

runProgBut = Button(tab1, borderwidth=3, height=60, width=60, command = runProg)
playPhoto=PhotoImage(file="play-icon.gif")
runProgBut.config(image=playPhoto,width="60",height="60")
runProgBut.place(x=20, y=80)

xboxBut = Button(tab1, borderwidth=3, height=43, width=60, command = xbox)
xboxPhoto=PhotoImage(file="xbox.gif")
xboxBut.config(image=xboxPhoto,width="60",height="43")
xboxBut.place(x=1330, y=140)

stopProgBut = Button(tab1, borderwidth=3, height=60, width=60, command = stopProg)
stopPhoto=PhotoImage(file="stop-icon.gif")
stopProgBut.config(image=stopPhoto,width="60",height="60")
stopProgBut.place(x=200, y=80)

fwdBut = Button(tab1, borderwidth=3, text="FWD", height=3, width=4, command = stepFwd)
fwdBut.place(x=100, y=80)

revBut = Button(tab1, borderwidth=3, text="REV", height=3, width=4, command = stepRev)
revBut.place(x=150, y=80)

RegNumBut = Button(tab1, borderwidth=3, text="Register", height=1, width=20, command = insertRegister)
RegNumBut.place(x=920, y=480)

RegJmpBut = Button(tab1, borderwidth=3, text="If Register Jump", height=1, width=20, command = IfRegjumpTab)
RegJmpBut.place(x=920, y=520)

CalibrateBut = Button(tab1, borderwidth=3, text="Auto Calibrate CMD", height=1, width=20, command = insCalibrate)
CalibrateBut.place(x=700, y=600)

J1jogNegBut = Button(tab1, borderwidth=3, text="-", height=1, width=3, command = J1jogNeg)
J1jogNegBut.place(x=642, y=90)

J1jogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = J1jogPos)
J1jogPosBut.place(x=680, y=90)

J2jogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = J2jogNeg)
J2jogNegBut.place(x=732, y=90)

J2jogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = J2jogPos)
J2jogPosBut.place(x=770, y=90)

J3jogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = J3jogNeg)
J3jogNegBut.place(x=822, y=90)

J3jogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = J3jogPos)
J3jogPosBut.place(x=860, y=90)

J4jogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = J4jogNeg)
J4jogNegBut.place(x=912, y=90)

J4jogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = J4jogPos)
J4jogPosBut.place(x=950, y=90)

J5jogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = J5jogNeg)
J5jogNegBut.place(x=1002, y=90)

J5jogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = J5jogPos)
J5jogPosBut.place(x=1040, y=90)

J6jogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = J6jogNeg)
J6jogNegBut.place(x=1092, y=90)

J6jogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = J6jogPos)
J6jogPosBut.place(x=1130, y=90)

XjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = XjogNeg)
XjogNegBut.place(x=642, y=210)

XjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = XjogPos)
XjogPosBut.place(x=680, y=210)

YjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = YjogNeg)
YjogNegBut.place(x=732, y=210)

YjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = YjogPos)
YjogPosBut.place(x=770, y=210)

ZjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = ZjogNeg)
ZjogNegBut.place(x=822, y=210)

ZjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = ZjogPos)
ZjogPosBut.place(x=860, y=210)

RxjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = RxjogNeg)
RxjogNegBut.place(x=912, y=210)

RxjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = RxjogPos)
RxjogPosBut.place(x=950, y=210)

RyjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = RyjogNeg)
RyjogNegBut.place(x=1002, y=210)

RyjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = RyjogPos)
RyjogPosBut.place(x=1040, y=210)

RzjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = RzjogNeg)
RzjogNegBut.place(x=1092, y=210)

RzjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = RzjogPos)
RzjogPosBut.place(x=1130, y=210)



TrackjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = TrackjogNeg)
TrackjogNegBut.place(x=1212, y=210)

TrackjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = TrackjogPos)
TrackjogPosBut.place(x=1250, y=210)






TXjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = TXjogNeg)
TXjogNegBut.place(x=642, y=310)

TXjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = TXjogPos)
TXjogPosBut.place(x=680, y=310)

TYjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = TYjogNeg)
TYjogNegBut.place(x=732, y=310)

TYjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = TYjogPos)
TYjogPosBut.place(x=770, y=310)

TZjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = TZjogNeg)
TZjogNegBut.place(x=822, y=310)

TZjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = TZjogPos)
TZjogPosBut.place(x=860, y=310)

TRxjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = TRxjogNeg)
TRxjogNegBut.place(x=912, y=310)

TRxjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = TRxjogPos)
TRxjogPosBut.place(x=950, y=310)

TRyjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = TRyjogNeg)
TRyjogNegBut.place(x=1002, y=310)

TRyjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = TRyjogPos)
TRyjogPosBut.place(x=1040, y=310)

TRzjogNegBut = Button(tab1, borderwidth=3,text="-", height=1, width=3, command = TRzjogNeg)
TRzjogNegBut.place(x=1092, y=310)

TRzjogPosBut = Button(tab1, borderwidth=3,text="+", height=1, width=3, command = TRzjogPos)
TRzjogPosBut.place(x=1130, y=310)


JogStepsCbut = Checkbutton(tab1, text="Jog joints in steps",variable = JogStepsStat)
JogStepsCbut.place(x=1230, y=15)


CheckRobotPosbut = Button(tab1, borderwidth=3, text="Check Robot Position", height=1, width=20, command = getRobotPosition)
#CheckRobotPosbut.place(x=1230, y=45)


StorPosBut = Button(tab1, borderwidth=3, text="Stored Position", height=1, width=20, command = storPos)
StorPosBut.place(x=920, y=560)






####ENTRY FIELDS##########################################################
##########################################################################



curRowEntryField = Entry(tab1,width=5)
curRowEntryField.place(x=310, y=150)

manEntryField = Entry(tab1,width=95)
manEntryField.place(x=630, y=645)

ProgEntryField = Entry(tab1,width=20)
ProgEntryField.place(x=70, y=45)

comPortEntryField = Entry(tab1,width=2)
comPortEntryField.place(x=450, y=40)

com2PortEntryField = Entry(tab1,width=2)
com2PortEntryField.place(x=450, y=65)

speedEntryField = Entry(tab1,width=3)
speedEntryField.place(x=465, y=100)

ACCdurField = Entry(tab1,width=3)
ACCdurField.place(x=465, y=125)

DECdurField = Entry(tab1,width=3)
DECdurField.place(x=465, y=150)

ACCspeedField = Entry(tab1,width=3)
ACCspeedField.place(x=490, y=125)

DECspeedField = Entry(tab1,width=3)
DECspeedField.place(x=490, y=150)

waitTimeEntryField = Entry(tab1,width=5)
waitTimeEntryField.place(x=872, y=363)

SavePosEntryField = Entry(tab1,width=5)
SavePosEntryField.place(x=650, y=402)



waitInputEntryField = Entry(tab1,width=5)
waitInputEntryField.place(x=872, y=403)

waitInputOffEntryField = Entry(tab1,width=5)
waitInputOffEntryField.place(x=872, y=443)

outputOnEntryField = Entry(tab1,width=5)
outputOnEntryField.place(x=872, y=483)

outputOffEntryField = Entry(tab1,width=5)
outputOffEntryField.place(x=872, y=523)

tabNumEntryField = Entry(tab1,width=5)
tabNumEntryField.place(x=1375, y=363)

jumpTabEntryField = Entry(tab1,width=5)
jumpTabEntryField.place(x=1375, y=403)

IfOnjumpInputTabEntryField = Entry(tab1,width=5)
IfOnjumpInputTabEntryField.place(x=1092, y=363)

IfOnjumpNumberTabEntryField = Entry(tab1,width=5)
IfOnjumpNumberTabEntryField.place(x=1132, y=363)

IfOffjumpInputTabEntryField = Entry(tab1,width=5)
IfOffjumpInputTabEntryField.place(x=1092, y=403)

IfOffjumpNumberTabEntryField = Entry(tab1,width=5)
IfOffjumpNumberTabEntryField.place(x=1132, y=403)

servoNumEntryField = Entry(tab1,width=5)
servoNumEntryField.place(x=1092, y=443)

servoPosEntryField = Entry(tab1,width=5)
servoPosEntryField.place(x=1132, y=443)

changeProgEntryField = Entry(tab1,width=22)
changeProgEntryField.place(x=712, y=563)



regNumEntryField = Entry(tab1,width=5)
regNumEntryField.place(x=1080, y=483)

regEqEntryField = Entry(tab1,width=5)
regEqEntryField.place(x=1132, y=483)

regNumJmpEntryField = Entry(tab1,width=5)
regNumJmpEntryField.place(x=1080, y=523)

regEqJmpEntryField = Entry(tab1,width=5)
regEqJmpEntryField.place(x=1132, y=523)

regTabJmpEntryField = Entry(tab1,width=5)
regTabJmpEntryField.place(x=1184, y=523)

storPosNumEntryField = Entry(tab1,width=5)
storPosNumEntryField.place(x=1080, y=563)

storPosElEntryField = Entry(tab1,width=5)
storPosElEntryField.place(x=1132, y=563)

storPosValEntryField = Entry(tab1,width=5)
storPosValEntryField.place(x=1184, y=563)


  ### J1 ###

J1curAngEntryField = Entry(tab1,width=5)
J1curAngEntryField.place(x=660, y=40)

J1jogDegsEntryField = Entry(tab1,width=5)
J1jogDegsEntryField.place(x=660, y=65)


   ### J2 ###

J2curAngEntryField = Entry(tab1,width=5)
J2curAngEntryField.place(x=750, y=40)

J2jogDegsEntryField = Entry(tab1,width=5)
J2jogDegsEntryField.place(x=750, y=65)


   ### J3 ###

J3curAngEntryField = Entry(tab1,width=5)
J3curAngEntryField.place(x=840, y=40)

J3jogDegsEntryField = Entry(tab1,width=5)
J3jogDegsEntryField.place(x=840, y=65)


   ### J4 ###

J4curAngEntryField = Entry(tab1,width=5)
J4curAngEntryField.place(x=930, y=40)

J4jogDegsEntryField = Entry(tab1,width=5)
J4jogDegsEntryField.place(x=930, y=65)


   ### J5 ###

J5curAngEntryField = Entry(tab1,width=5)
J5curAngEntryField.place(x=1020, y=40)

J5jogDegsEntryField = Entry(tab1,width=5)
J5jogDegsEntryField.place(x=1020, y=65)


   ### J6 ###

J6curAngEntryField = Entry(tab1,width=5)
J6curAngEntryField.place(x=1110, y=40)

J6jogDegsEntryField = Entry(tab1,width=5)
J6jogDegsEntryField.place(x=1110, y=65)







  ### X ###

XcurEntryField = Entry(tab1,width=5)
XcurEntryField.place(x=660, y=160)

XjogEntryField = Entry(tab1,width=5)
XjogEntryField.place(x=660, y=185)


   ### Y ###

YcurEntryField = Entry(tab1,width=5)
YcurEntryField.place(x=750, y=160)

YjogEntryField = Entry(tab1,width=5)
YjogEntryField.place(x=750, y=185)


   ### Z ###

ZcurEntryField = Entry(tab1,width=5)
ZcurEntryField.place(x=840, y=160)

ZjogEntryField = Entry(tab1,width=5)
ZjogEntryField.place(x=840, y=185)


   ### Rx ###

RxcurEntryField = Entry(tab1,width=5)
RxcurEntryField.place(x=930, y=160)

RxjogEntryField = Entry(tab1,width=5)
RxjogEntryField.place(x=930, y=185)


   ### Ry ###

RycurEntryField = Entry(tab1,width=5)
RycurEntryField.place(x=1020, y=160)

RyjogEntryField = Entry(tab1,width=5)
RyjogEntryField.place(x=1020, y=185)


   ### Rz ###

RzcurEntryField = Entry(tab1,width=5)
RzcurEntryField.place(x=1110, y=160)

RzjogEntryField = Entry(tab1,width=5)
RzjogEntryField.place(x=1110, y=185)



   ### Track ###

TrackcurEntryField = Entry(tab1,width=5)
TrackcurEntryField.place(x=1230, y=160)

TrackjogEntryField = Entry(tab1,width=5)
TrackjogEntryField.place(x=1230, y=185)








TXjogEntryField = Entry(tab1,width=5)
TXjogEntryField.place(x=660, y=285)

TYjogEntryField = Entry(tab1,width=5)
TYjogEntryField.place(x=750, y=285)

TZjogEntryField = Entry(tab1,width=5)
TZjogEntryField.place(x=840, y=285)

TRxjogEntryField = Entry(tab1,width=5)
TRxjogEntryField.place(x=930, y=285)

TRyjogEntryField = Entry(tab1,width=5)
TRyjogEntryField.place(x=1020, y=285)

TRzjogEntryField = Entry(tab1,width=5)
TRzjogEntryField.place(x=1110, y=285)











####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 2




### 2 LABELS#################################################################
#############################################################################

almStatusLab2 = Label(tab2, text = "SYSTEM READY - NO ACTIVE ALARMS", bg = "cornflowerblue")
almStatusLab2.place(x=10, y=20)

WorkFrameLab = Label(tab2, text = "Work Frame:")
WorkFrameLab.place(x=990, y=40)

ToolFrameLab = Label(tab2, text = "Tool Frame:")
ToolFrameLab.place(x=990, y=65)

UFxLab = Label(tab2, font=("Arial", 11), text = "X")
UFxLab.place(x=1088, y=17)

UFyLab = Label(tab2, font=("Arial", 11), text = "Y")
UFyLab.place(x=1128, y=17)

UFzLab = Label(tab2, font=("Arial", 11), text = "Z")
UFzLab.place(x=1168, y=17)

UFRxLab = Label(tab2, font=("Arial", 11), text = "Rx")
UFRxLab.place(x=1204, y=17)

UFRyLab = Label(tab2, font=("Arial", 11), text = "Ry")
UFRyLab.place(x=1244, y=17)

UFRzLab = Label(tab2, font=("Arial", 11), text = "Rz")
UFRzLab.place(x=1284, y=17)

fineCalLab = Label(tab2, fg = "orange4", text = "Fine Calibration Position:")
fineCalLab.place(x=10, y=133)


CalibrationValuesLab = Label(tab2, text = "Robot Calibration Values:")
CalibrationValuesLab.place(x=380, y=8)

DHValuesLab = Label(tab2, text = "DH Parameters:")
DHValuesLab.place(x=650, y=8)


J1NegAngLimLab = Label(tab2, text = "J1 Neg Ang Lim")
J1PosAngLimLab = Label(tab2, text = "J1 Pos Ang Lim")
J1StepLimLab = Label(tab2, text = "J1 Step Lim")

J2NegAngLimLab = Label(tab2, text = "J2 Neg Ang Lim")
J2PosAngLimLab = Label(tab2, text = "J2 Pos Ang Lim")
J2StepLimLab = Label(tab2, text = "J2 Step Lim")

J3NegAngLimLab = Label(tab2, text = "J3 Neg Ang Lim")
J3PosAngLimLab = Label(tab2, text = "J3 Pos Ang Lim")
J3StepLimLab = Label(tab2, text = "J3 Step Lim")

J4NegAngLimLab = Label(tab2, text = "J4 Neg Ang Lim")
J4PosAngLimLab = Label(tab2, text = "J4 Pos Ang Lim")
J4StepLimLab = Label(tab2, text = "J4 Step Lim")

J5NegAngLimLab = Label(tab2, text = "J5 Neg Ang Lim")
J5PosAngLimLab = Label(tab2, text = "J5 Pos Ang Lim")
J5StepLimLab = Label(tab2, text = "J5 Step Lim")

J6NegAngLimLab = Label(tab2, text = "J6 Neg Ang Lim")
J6PosAngLimLab = Label(tab2, text = "J6 Pos Ang Lim")
J6StepLimLab = Label(tab2, text = "J6 Step Lim")



J1NegAngLimLab.place(x=440, y=30)
J1PosAngLimLab.place(x=440, y=55)
J1StepLimLab.place(x=440, y=80)

J2NegAngLimLab.place(x=440, y=130)
J2PosAngLimLab.place(x=440, y=155)
J2StepLimLab.place(x=440, y=180)

J3NegAngLimLab.place(x=440, y=230)
J3PosAngLimLab.place(x=440, y=255)
J3StepLimLab.place(x=440, y=280)

J4NegAngLimLab.place(x=440, y=330)
J4PosAngLimLab.place(x=440, y=355)
J4StepLimLab.place(x=440, y=380)

J5NegAngLimLab.place(x=440, y=430)
J5PosAngLimLab.place(x=440, y=455)
J5StepLimLab.place(x=440, y=480)

J6NegAngLimLab.place(x=440, y=530)
J6PosAngLimLab.place(x=440, y=555)
J6StepLimLab.place(x=440, y=580)




TrackLengthLab = Label(tab2, text = "Track Length")
TrackStepLimLab = Label(tab2, text = "Track Step Lim")

TrackLengthLab.place(x=440, y=630)
TrackStepLimLab.place(x=440, y=655)



DHr1Lab = Label(tab2, text = "DH alpha-1 (link twist)")
DHr2Lab = Label(tab2, text = "DH alpha-2 (link twist)")
DHr3Lab = Label(tab2, text = "DH alpha-3 (link twist)")
DHr4Lab = Label(tab2, text = "DH alpha-4 (link twist)")
DHr5Lab = Label(tab2, text = "DH alpha-5 (link twist)")
DHr6Lab = Label(tab2, text = "DH alpha-6 (link twist)")

DHa1Lab = Label(tab2, text = "DH a-1 (link length)")
DHa2Lab = Label(tab2, text = "DH a-2 (link length)")
DHa3Lab = Label(tab2, text = "DH a-3 (link length)")
DHa4Lab = Label(tab2, text = "DH a-4 (link length)")
DHa5Lab = Label(tab2, text = "DH a-5 (link length)")
DHa6Lab = Label(tab2, text = "DH a-6 (link length)")

DHd1Lab = Label(tab2, text = "DH d-1 (link offset)")
DHd2Lab = Label(tab2, text = "DH d-2 (link offset)")
DHd3Lab = Label(tab2, text = "DH d-3 (link offset)")
DHd4Lab = Label(tab2, text = "DH d-4 (link offset)")
DHd5Lab = Label(tab2, text = "DH d-5 (link offset)")
DHd6Lab = Label(tab2, text = "DH d-6 (link offset)")

DHt1Lab = Label(tab2, text = "DH theta-1 (joint angle)")
DHt2Lab = Label(tab2, text = "DH theta-2 (joint angle)")
DHt3Lab = Label(tab2, text = "DH theta-3 (joint angle)")
DHt4Lab = Label(tab2, text = "DH theta-4 (joint angle)")
DHt5Lab = Label(tab2, text = "DH theta-5 (joint angle)")
DHt6Lab = Label(tab2, text = "DH theta-6 (joint angle)")



CalDirLab = Label(tab2, text = "Calibration Directions (default = 001001)")
CalDirLab.place(x=70, y=390)

MotDirLab = Label(tab2, text = "Motor Direction Output (default = 000000)")
MotDirLab.place(x=70, y=420)

### 2 BUTTONS################################################################
#############################################################################


manCalBut = Button(tab2, bg="lightskyblue3", text="Auto Calibrate", height=1, width=20, command = calRobotAll)
manCalBut.place(x=10, y=60)

ForcCalBut = Button(tab2, bg="lightskyblue3", text="Calibrate @ Rest Position", height=1, width=26, command = calRobotMid)
ForcCalBut.place(x=170, y=60)

fineCalBut = Button(tab2, bg="khaki2", text="Execute Fine Calibratation", height=1, width=20, command = exeFineCalPos)
fineCalBut.place(x=10, y=90)

teachfineCalBut = Button(tab2, bg="khaki2", text="Teach Fine Calibration Position", height=1, width=26, command = teachFineCal)
teachfineCalBut.place(x=170, y=90)

gotofineCalBut = Button(tab2, bg="khaki2", text="Go To Fine Calibration Position", height=1, width=26, command = gotoFineCalPos)
gotofineCalBut.place(x=170, y=120)

saveCalBut = Button(tab2, borderwidth=3, text="SAVE CALIBRATION DATA", height=1, width=26, command = SaveAndApplyCalibration)
saveCalBut.place(x=1150, y=630)


CalJ1But = Button(tab2,  borderwidth=3, text="Calibrate J1 Only", height=1, width=20, command = calRobotJ1)
CalJ1But.place(x=10, y=190)

CalJ2But = Button(tab2,  borderwidth=3, text="Calibrate J2 Only", height=1, width=20, command = calRobotJ2)
CalJ2But.place(x=10, y=220)

CalJ3But = Button(tab2,  borderwidth=3, text="Calibrate J3 Only", height=1, width=20, command = calRobotJ3)
CalJ3But.place(x=10, y=250)

CalJ4But = Button(tab2,  borderwidth=3, text="Calibrate J4 Only", height=1, width=20, command = calRobotJ4)
CalJ4But.place(x=10, y=280)

CalJ5But = Button(tab2,  borderwidth=3, text="Calibrate J5 Only", height=1, width=20, command = calRobotJ5)
CalJ5But.place(x=10, y=310)

CalJ5But = Button(tab2,  borderwidth=3, text="Calibrate J6 Only", height=1, width=20, command = calRobotJ6)
CalJ5But.place(x=10, y=340)


CalTrackBut = Button(tab2,  borderwidth=3, text="Calibrate Track to 0", height=1, width=20, command = CalTrackPos)
CalTrackBut.place(x=170, y=190)


J1OpenLoopCbut = Checkbutton(tab2, text="J1 Open Loop (disable encoder)",variable = J1OpenLoopStat)
J1OpenLoopCbut.place(x=5, y=460)

J2OpenLoopCbut = Checkbutton(tab2, text="J2 Open Loop (disable encoder)",variable = J2OpenLoopStat)
J2OpenLoopCbut.place(x=5, y=480)

J3OpenLoopCbut = Checkbutton(tab2, text="J3 Open Loop (disable encoder)",variable = J3OpenLoopStat)
J3OpenLoopCbut.place(x=5, y=500)

J4OpenLoopCbut = Checkbutton(tab2, text="J4 Open Loop (disable encoder)",variable = J4OpenLoopStat)
J4OpenLoopCbut.place(x=5, y=520)

J5OpenLoopCbut = Checkbutton(tab2, text="J5 Open Loop (disable encoder)",variable = J5OpenLoopStat)
J5OpenLoopCbut.place(x=5, y=540)

J6OpenLoopCbut = Checkbutton(tab2, text="J6 Open Loop (disable encoder)",variable = J6OpenLoopStat)
J6OpenLoopCbut.place(x=5, y=560)


#### 2 ENTRY FIELDS##########################################################
#############################################################################

   ### User Frame ###

UFxEntryField = Entry(tab2,width=5)
UFxEntryField.place(x=1080, y=40)
UFyEntryField = Entry(tab2,width=5)
UFyEntryField.place(x=1120, y=40)
UFzEntryField = Entry(tab2,width=5)
UFzEntryField.place(x=1160, y=40)
UFrxEntryField = Entry(tab2,width=5)
UFrxEntryField.place(x=1200, y=40)
UFryEntryField = Entry(tab2,width=5)
UFryEntryField.place(x=1240, y=40)
UFrzEntryField = Entry(tab2,width=5)
UFrzEntryField.place(x=1280, y=40)



   ### Tool Frame ###

TFxEntryField = Entry(tab2,width=5)
TFxEntryField.place(x=1080, y=65)
TFyEntryField = Entry(tab2,width=5)
TFyEntryField.place(x=1120, y=65)
TFzEntryField = Entry(tab2,width=5)
TFzEntryField.place(x=1160, y=65)
TFrxEntryField = Entry(tab2,width=5)
TFrxEntryField.place(x=1200, y=65)
TFryEntryField = Entry(tab2,width=5)
TFryEntryField.place(x=1240, y=65)
TFrzEntryField = Entry(tab2,width=5)
TFrzEntryField.place(x=1280, y=65)


fineCalEntryField = Entry(tab2,fg="orange4",bg="khaki2",width=58)
fineCalEntryField.place(x=10, y=153)



J1NegAngLimEntryField = Entry(tab2,width=8)
J1PosAngLimEntryField = Entry(tab2,width=8)
J1StepLimEntryField = Entry(tab2,width=8)

J2NegAngLimEntryField = Entry(tab2,width=8)
J2PosAngLimEntryField = Entry(tab2,width=8)
J2StepLimEntryField = Entry(tab2,width=8)

J3NegAngLimEntryField = Entry(tab2,width=8)
J3PosAngLimEntryField = Entry(tab2,width=8)
J3StepLimEntryField = Entry(tab2,width=8)

J4NegAngLimEntryField = Entry(tab2,width=8)
J4PosAngLimEntryField = Entry(tab2,width=8)
J4StepLimEntryField = Entry(tab2,width=8)

J5NegAngLimEntryField = Entry(tab2,width=8)
J5PosAngLimEntryField = Entry(tab2,width=8)
J5StepLimEntryField = Entry(tab2,width=8)

J6NegAngLimEntryField = Entry(tab2,width=8)
J6PosAngLimEntryField = Entry(tab2,width=8)
J6StepLimEntryField = Entry(tab2,width=8)


J1NegAngLimEntryField.place(x=380, y=30)
J1PosAngLimEntryField.place(x=380, y=55)
J1StepLimEntryField.place(x=380, y=80)

J2NegAngLimEntryField.place(x=380, y=130)
J2PosAngLimEntryField.place(x=380, y=155)
J2StepLimEntryField.place(x=380, y=180)

J3NegAngLimEntryField.place(x=380, y=230)
J3PosAngLimEntryField.place(x=380, y=255)
J3StepLimEntryField.place(x=380, y=280)

J4NegAngLimEntryField.place(x=380, y=330)
J4PosAngLimEntryField.place(x=380, y=355)
J4StepLimEntryField.place(x=380, y=380)

J5NegAngLimEntryField.place(x=380, y=430)
J5PosAngLimEntryField.place(x=380, y=455)
J5StepLimEntryField.place(x=380, y=480)

J6NegAngLimEntryField.place(x=380, y=530)
J6PosAngLimEntryField.place(x=380, y=555)
J6StepLimEntryField.place(x=380, y=580)





TrackLengthEntryField = Entry(tab2,width=8)
TrackStepLimEntryField = Entry(tab2,width=8)

TrackLengthEntryField.place(x=380, y=630)
TrackStepLimEntryField.place(x=380, y=655)





DHr1EntryField = Entry(tab2,width=8)
DHr2EntryField = Entry(tab2,width=8)
DHr3EntryField = Entry(tab2,width=8)
DHr4EntryField = Entry(tab2,width=8)
DHr5EntryField = Entry(tab2,width=8)
DHr6EntryField = Entry(tab2,width=8)

DHa1EntryField = Entry(tab2,width=8)
DHa2EntryField = Entry(tab2,width=8)
DHa3EntryField = Entry(tab2,width=8)
DHa4EntryField = Entry(tab2,width=8)
DHa5EntryField = Entry(tab2,width=8)
DHa6EntryField = Entry(tab2,width=8)

DHd1EntryField = Entry(tab2,width=8)
DHd2EntryField = Entry(tab2,width=8)
DHd3EntryField = Entry(tab2,width=8)
DHd4EntryField = Entry(tab2,width=8)
DHd5EntryField = Entry(tab2,width=8)
DHd6EntryField = Entry(tab2,width=8)

DHt1EntryField = Entry(tab2,width=8)
DHt2EntryField = Entry(tab2,width=8)
DHt3EntryField = Entry(tab2,width=8)
DHt4EntryField = Entry(tab2,width=8)
DHt5EntryField = Entry(tab2,width=8)
DHt6EntryField = Entry(tab2,width=8)



DHr1EntryField.place(x=650, y=30)
DHr2EntryField.place(x=650, y=55)
DHr3EntryField.place(x=650, y=80)
DHr4EntryField.place(x=650, y=105)
DHr5EntryField.place(x=650, y=130)
DHr6EntryField.place(x=650, y=155)

DHa1EntryField.place(x=650, y=180)
DHa2EntryField.place(x=650, y=205)
DHa3EntryField.place(x=650, y=230)
DHa4EntryField.place(x=650, y=255)
DHa5EntryField.place(x=650, y=280)
DHa6EntryField.place(x=650, y=305)

DHd1EntryField.place(x=650, y=330)
DHd2EntryField.place(x=650, y=355)
DHd3EntryField.place(x=650, y=380)
DHd4EntryField.place(x=650, y=405)
DHd5EntryField.place(x=650, y=430)
DHd6EntryField.place(x=650, y=455)

DHt1EntryField.place(x=650, y=480)
DHt2EntryField.place(x=650, y=505)
DHt3EntryField.place(x=650, y=530)
DHt4EntryField.place(x=650, y=555)
DHt5EntryField.place(x=650, y=580)
DHt6EntryField.place(x=650, y=605)



DHr1Lab.place(x=710, y=30)
DHr2Lab.place(x=710, y=55)
DHr3Lab.place(x=710, y=80)
DHr4Lab.place(x=710, y=105)
DHr5Lab.place(x=710, y=130)
DHr6Lab.place(x=710, y=155)

DHa1Lab.place(x=710, y=180)
DHa2Lab.place(x=710, y=205)
DHa3Lab.place(x=710, y=230)
DHa4Lab.place(x=710, y=255)
DHa5Lab.place(x=710, y=280)
DHa6Lab.place(x=710, y=305)

DHd1Lab.place(x=710, y=330)
DHd2Lab.place(x=710, y=355)
DHd3Lab.place(x=710, y=380)
DHd4Lab.place(x=710, y=405)
DHd5Lab.place(x=710, y=430)
DHd6Lab.place(x=710, y=455)

DHt1Lab.place(x=710, y=480)
DHt2Lab.place(x=710, y=505)
DHt3Lab.place(x=710, y=530)
DHt4Lab.place(x=710, y=555)
DHt5Lab.place(x=710, y=580)
DHt6Lab.place(x=710, y=605)



CalDirEntryField = Entry(tab2,width=6)
CalDirEntryField.place(x=10, y=390)

MotDirEntryField = Entry(tab2,width=6)
MotDirEntryField.place(x=10, y=420)



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 3



### 3 LABELS#################################################################
#############################################################################

servo0onequalsLab = Label(tab3, text = "=")
servo0onequalsLab.place(x=70, y=12)

servo0offequalsLab = Label(tab3, text = "=")
servo0offequalsLab.place(x=70, y=52)

servo1onequalsLab = Label(tab3, text = "=")
servo1onequalsLab.place(x=70, y=92)

servo1offequalsLab = Label(tab3, text = "=")
servo1offequalsLab.place(x=70, y=132)

servo2onequalsLab = Label(tab3, text = "=")
servo2onequalsLab.place(x=70, y=172)

servo2offequalsLab = Label(tab3, text = "=")
servo2offequalsLab.place(x=70, y=212)

servo3onequalsLab = Label(tab3, text = "=")
servo3onequalsLab.place(x=70, y=252)

servo3offequalsLab = Label(tab3, text = "=")
servo3offequalsLab.place(x=70, y=292)



Do1onequalsLab = Label(tab3, text = "=")
Do1onequalsLab.place(x=210, y=12)

Do1offequalsLab = Label(tab3, text = "=")
Do1offequalsLab.place(x=210, y=52)

Do2onequalsLab = Label(tab3, text = "=")
Do2onequalsLab.place(x=210, y=92)

Do2offequalsLab = Label(tab3, text = "=")
Do2offequalsLab.place(x=210, y=132)

Do3onequalsLab = Label(tab3, text = "=")
Do3onequalsLab.place(x=210, y=172)

Do3offequalsLab = Label(tab3, text = "=")
Do3offequalsLab.place(x=210, y=212)

Do4onequalsLab = Label(tab3, text = "=")
Do4onequalsLab.place(x=210, y=252)

Do4offequalsLab = Label(tab3, text = "=")
Do4offequalsLab.place(x=210, y=292)

Do5onequalsLab = Label(tab3, text = "=")
Do5onequalsLab.place(x=210, y=332)

Do5offequalsLab = Label(tab3, text = "=")
Do5offequalsLab.place(x=210, y=372)

Do6onequalsLab = Label(tab3, text = "=")
Do6onequalsLab.place(x=210, y=412)

Do6offequalsLab = Label(tab3, text = "=")
Do6offequalsLab.place(x=210, y=452)


inoutavailLab = Label(tab3, text = "NOTE: the following are available IO's on the Arduino Mega:       Inputs = 0-27  /  Outputs = 28-53  /  Servos = A0-A7")
inoutavailLab.place(x=10, y=645)


### 3 BUTTONS################################################################
#############################################################################

servo0onBut = Button(tab3, bg="light blue", text="Servo 0", height=1, width=6, command = Servo0on)
servo0onBut.place(x=10, y=10)

servo0offBut = Button(tab3, bg="light blue", text="Servo 0", height=1, width=6, command = Servo0off)
servo0offBut.place(x=10, y=50)

servo1onBut = Button(tab3, bg="light blue", text="Servo 1", height=1, width=6, command = Servo1on)
servo1onBut.place(x=10, y=90)

servo1offBut = Button(tab3, bg="light blue", text="Servo 1", height=1, width=6, command = Servo1off)
servo1offBut.place(x=10, y=130)

servo2onBut = Button(tab3, bg="light blue", text="Servo 2", height=1, width=6, command = Servo2on)
servo2onBut.place(x=10, y=170)

servo2offBut = Button(tab3, bg="light blue", text="Servo 2", height=1, width=6, command = Servo2off)
servo2offBut.place(x=10, y=210)

servo3onBut = Button(tab3, bg="light blue", text="Servo 3", height=1, width=6, command = Servo3on)
servo3onBut.place(x=10, y=250)

servo3offBut = Button(tab3, bg="light blue", text="Servo 3", height=1, width=6, command = Servo3off)
servo3offBut.place(x=10, y=290)





DO1onBut = Button(tab3, bg="light blue", text="DO on", height=1, width=6, command = DO1on)
DO1onBut.place(x=150, y=10)

DO1offBut = Button(tab3, bg="light blue", text="DO off", height=1, width=6, command = DO1off)
DO1offBut.place(x=150, y=50)

DO2onBut = Button(tab3, bg="light blue", text="DO on", height=1, width=6, command = DO2on)
DO2onBut.place(x=150, y=90)

DO2offBut = Button(tab3, bg="light blue", text="DO off", height=1, width=6, command = DO2off)
DO2offBut.place(x=150, y=130)

DO3onBut = Button(tab3, bg="light blue", text="DO on", height=1, width=6, command = DO3on)
DO3onBut.place(x=150, y=170)

DO3offBut = Button(tab3, bg="light blue", text="DO off", height=1, width=6, command = DO3off)
DO3offBut.place(x=150, y=210)

DO4onBut = Button(tab3, bg="light blue", text="DO on", height=1, width=6, command = DO4on)
DO4onBut.place(x=150, y=250)

DO4offBut = Button(tab3, bg="light blue", text="DO off", height=1, width=6, command = DO4off)
DO4offBut.place(x=150, y=290)

DO5onBut = Button(tab3, bg="light blue", text="DO on", height=1, width=6, command = DO5on)
DO5onBut.place(x=150, y=330)

DO5offBut = Button(tab3, bg="light blue", text="DO off", height=1, width=6, command = DO5off)
DO5offBut.place(x=150, y=370)

DO6onBut = Button(tab3, bg="light blue", text="DO on", height=1, width=6, command = DO6on)
DO6onBut.place(x=150, y=410)

DO6offBut = Button(tab3, bg="light blue", text="DO off", height=1, width=6, command = DO6off)
DO6offBut.place(x=150, y=450)



#### 3 ENTRY FIELDS##########################################################
#############################################################################


servo0onEntryField = Entry(tab3,width=5)
servo0onEntryField.place(x=90, y=15)

servo0offEntryField = Entry(tab3,width=5)
servo0offEntryField.place(x=90, y=55)

servo1onEntryField = Entry(tab3,width=5)
servo1onEntryField.place(x=90, y=95)

servo1offEntryField = Entry(tab3,width=5)
servo1offEntryField.place(x=90, y=135)

servo2onEntryField = Entry(tab3,width=5)
servo2onEntryField.place(x=90, y=175)

servo2offEntryField = Entry(tab3,width=5)
servo2offEntryField.place(x=90, y=215)


servo3onEntryField = Entry(tab3,width=5)
servo3onEntryField.place(x=90, y=255)

servo3offEntryField = Entry(tab3,width=5)
servo3offEntryField.place(x=90, y=295)





DO1onEntryField = Entry(tab3,width=5)
DO1onEntryField.place(x=230, y=15)

DO1offEntryField = Entry(tab3,width=5)
DO1offEntryField.place(x=230, y=55)

DO2onEntryField = Entry(tab3,width=5)
DO2onEntryField.place(x=230, y=95)

DO2offEntryField = Entry(tab3,width=5)
DO2offEntryField.place(x=230, y=135)

DO3onEntryField = Entry(tab3,width=5)
DO3onEntryField.place(x=230, y=175)

DO3offEntryField = Entry(tab3,width=5)
DO3offEntryField.place(x=230, y=215)

DO4onEntryField = Entry(tab3,width=5)
DO4onEntryField.place(x=230, y=255)

DO4offEntryField = Entry(tab3,width=5)
DO4offEntryField.place(x=230, y=295)

DO5onEntryField = Entry(tab3,width=5)
DO5onEntryField.place(x=230, y=335)

DO5offEntryField = Entry(tab3,width=5)
DO5offEntryField.place(x=230, y=375)

DO6onEntryField = Entry(tab3,width=5)
DO6onEntryField.place(x=230, y=415)

DO6offEntryField = Entry(tab3,width=5)
DO6offEntryField.place(x=230, y=455)



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 4




### 4 LABELS#################################################################
#############################################################################

R1Lab = Label(tab4, text = "R1")
R1Lab.place(x=70, y=30)

R2Lab = Label(tab4, text = "R2")
R2Lab.place(x=70, y=60)

R3Lab = Label(tab4, text = "R3")
R3Lab.place(x=70, y=90)

R4Lab = Label(tab4, text = "R4")
R4Lab.place(x=70, y=120)

R5Lab = Label(tab4, text = "R5")
R5Lab.place(x=70, y=150)

R6Lab = Label(tab4, text = "R6")
R6Lab.place(x=70, y=180)

R7Lab = Label(tab4, text = "R7")
R7Lab.place(x=70, y=210)

R8Lab = Label(tab4, text = "R8")
R8Lab.place(x=70, y=240)

R9Lab = Label(tab4, text = "R9")
R9Lab.place(x=70, y=270)

R10Lab = Label(tab4, text = "R10")
R10Lab.place(x=70, y=300)

R11Lab = Label(tab4, text = "R11")
R11Lab.place(x=70, y=330)

R12Lab = Label(tab4, text = "R12")
R12Lab.place(x=70, y=360)

R13Lab = Label(tab4, text = "R14")
R13Lab.place(x=70, y=390)

R14Lab = Label(tab4, text = "R14")
R14Lab.place(x=70, y=420)

R15Lab = Label(tab4, text = "R15")
R15Lab.place(x=70, y=450)

R16Lab = Label(tab4, text = "R16")
R16Lab.place(x=70, y=480)


SP1Lab = Label(tab4, text = "SP1 (vision)")
SP1Lab.place(x=640, y=30)

SP2Lab = Label(tab4, text = "SP2")
SP2Lab.place(x=640, y=60)

SP3Lab = Label(tab4, text = "SP3")
SP3Lab.place(x=640, y=90)

SP4Lab = Label(tab4, text = "SP4")
SP4Lab.place(x=640, y=120)

SP5Lab = Label(tab4, text = "SP5")
SP5Lab.place(x=640, y=150)

SP6Lab = Label(tab4, text = "SP6")
SP6Lab.place(x=640, y=180)

SP7Lab = Label(tab4, text = "SP7")
SP7Lab.place(x=640, y=210)

SP8Lab = Label(tab4, text = "SP8")
SP8Lab.place(x=640, y=240)

SP9Lab = Label(tab4, text = "SP9")
SP9Lab.place(x=640, y=270)

SP10Lab = Label(tab4, text = "SP10")
SP10Lab.place(x=640, y=300)

SP11Lab = Label(tab4, text = "SP11")
SP11Lab.place(x=640, y=330)

SP12Lab = Label(tab4, text = "SP12")
SP12Lab.place(x=640, y=360)

SP13Lab = Label(tab4, text = "SP14")
SP13Lab.place(x=640, y=390)

SP14Lab = Label(tab4, text = "SP14")
SP14Lab.place(x=640, y=420)

SP15Lab = Label(tab4, text = "SP15")
SP15Lab.place(x=640, y=450)

SP16Lab = Label(tab4, text = "SP16")
SP16Lab.place(x=640, y=480)


SP_E1_Lab = Label(tab4, text = "X")
SP_E1_Lab.place(x=410, y=10)

SP_E2_Lab = Label(tab4, text = "Y")
SP_E2_Lab.place(x=450, y=10)

SP_E3_Lab = Label(tab4, text = "Z")
SP_E3_Lab.place(x=490, y=10)

SP_E4_Lab = Label(tab4, text = "W")
SP_E4_Lab.place(x=530, y=10)

SP_E5_Lab = Label(tab4, text = "P")
SP_E5_Lab.place(x=570, y=10)

SP_E6_Lab = Label(tab4, text = "R")
SP_E6_Lab.place(x=610, y=10)



### 4 BUTTONS################################################################
#############################################################################




#### 4 ENTRY FIELDS##########################################################
#############################################################################

R1EntryField = Entry(tab4,width=5)
R1EntryField.place(x=30, y=30)

R2EntryField = Entry(tab4,width=5)
R2EntryField.place(x=30, y=60)

R3EntryField = Entry(tab4,width=5)
R3EntryField.place(x=30, y=90)

R4EntryField = Entry(tab4,width=5)
R4EntryField.place(x=30, y=120)

R5EntryField = Entry(tab4,width=5)
R5EntryField.place(x=30, y=150)

R6EntryField = Entry(tab4,width=5)
R6EntryField.place(x=30, y=180)

R7EntryField = Entry(tab4,width=5)
R7EntryField.place(x=30, y=210)

R8EntryField = Entry(tab4,width=5)
R8EntryField.place(x=30, y=240)

R9EntryField = Entry(tab4,width=5)
R9EntryField.place(x=30, y=270)

R10EntryField = Entry(tab4,width=5)
R10EntryField.place(x=30, y=300)

R11EntryField = Entry(tab4,width=5)
R11EntryField.place(x=30, y=330)

R12EntryField = Entry(tab4,width=5)
R12EntryField.place(x=30, y=360)

R13EntryField = Entry(tab4,width=5)
R13EntryField.place(x=30, y=390)

R14EntryField = Entry(tab4,width=5)
R14EntryField.place(x=30, y=420)

R15EntryField = Entry(tab4,width=5)
R15EntryField.place(x=30, y=450)

R16EntryField = Entry(tab4,width=5)
R16EntryField.place(x=30, y=480)




SP_1_E1_EntryField = Entry(tab4,width=5)
SP_1_E1_EntryField.place(x=400, y=30)

SP_2_E1_EntryField = Entry(tab4,width=5)
SP_2_E1_EntryField.place(x=400, y=60)

SP_3_E1_EntryField = Entry(tab4,width=5)
SP_3_E1_EntryField.place(x=400, y=90)

SP_4_E1_EntryField = Entry(tab4,width=5)
SP_4_E1_EntryField.place(x=400, y=120)

SP_5_E1_EntryField = Entry(tab4,width=5)
SP_5_E1_EntryField.place(x=400, y=150)

SP_6_E1_EntryField = Entry(tab4,width=5)
SP_6_E1_EntryField.place(x=400, y=180)

SP_7_E1_EntryField = Entry(tab4,width=5)
SP_7_E1_EntryField.place(x=400, y=210)

SP_8_E1_EntryField = Entry(tab4,width=5)
SP_8_E1_EntryField.place(x=400, y=240)

SP_9_E1_EntryField = Entry(tab4,width=5)
SP_9_E1_EntryField.place(x=400, y=270)

SP_10_E1_EntryField = Entry(tab4,width=5)
SP_10_E1_EntryField.place(x=400, y=300)

SP_11_E1_EntryField = Entry(tab4,width=5)
SP_11_E1_EntryField.place(x=400, y=330)

SP_12_E1_EntryField = Entry(tab4,width=5)
SP_12_E1_EntryField.place(x=400, y=360)

SP_13_E1_EntryField = Entry(tab4,width=5)
SP_13_E1_EntryField.place(x=400, y=390)

SP_14_E1_EntryField = Entry(tab4,width=5)
SP_14_E1_EntryField.place(x=400, y=420)

SP_15_E1_EntryField = Entry(tab4,width=5)
SP_15_E1_EntryField.place(x=400, y=450)

SP_16_E1_EntryField = Entry(tab4,width=5)
SP_16_E1_EntryField.place(x=400, y=480)





SP_1_E2_EntryField = Entry(tab4,width=5)
SP_1_E2_EntryField.place(x=440, y=30)

SP_2_E2_EntryField = Entry(tab4,width=5)
SP_2_E2_EntryField.place(x=440, y=60)

SP_3_E2_EntryField = Entry(tab4,width=5)
SP_3_E2_EntryField.place(x=440, y=90)

SP_4_E2_EntryField = Entry(tab4,width=5)
SP_4_E2_EntryField.place(x=440, y=120)

SP_5_E2_EntryField = Entry(tab4,width=5)
SP_5_E2_EntryField.place(x=440, y=150)

SP_6_E2_EntryField = Entry(tab4,width=5)
SP_6_E2_EntryField.place(x=440, y=180)

SP_7_E2_EntryField = Entry(tab4,width=5)
SP_7_E2_EntryField.place(x=440, y=210)

SP_8_E2_EntryField = Entry(tab4,width=5)
SP_8_E2_EntryField.place(x=440, y=240)

SP_9_E2_EntryField = Entry(tab4,width=5)
SP_9_E2_EntryField.place(x=440, y=270)

SP_10_E2_EntryField = Entry(tab4,width=5)
SP_10_E2_EntryField.place(x=440, y=300)

SP_11_E2_EntryField = Entry(tab4,width=5)
SP_11_E2_EntryField.place(x=440, y=330)

SP_12_E2_EntryField = Entry(tab4,width=5)
SP_12_E2_EntryField.place(x=440, y=360)

SP_13_E2_EntryField = Entry(tab4,width=5)
SP_13_E2_EntryField.place(x=440, y=390)

SP_14_E2_EntryField = Entry(tab4,width=5)
SP_14_E2_EntryField.place(x=440, y=420)

SP_15_E2_EntryField = Entry(tab4,width=5)
SP_15_E2_EntryField.place(x=440, y=450)

SP_16_E2_EntryField = Entry(tab4,width=5)
SP_16_E2_EntryField.place(x=440, y=480)




SP_1_E3_EntryField = Entry(tab4,width=5)
SP_1_E3_EntryField.place(x=480, y=30)

SP_2_E3_EntryField = Entry(tab4,width=5)
SP_2_E3_EntryField.place(x=480, y=60)

SP_3_E3_EntryField = Entry(tab4,width=5)
SP_3_E3_EntryField.place(x=480, y=90)

SP_4_E3_EntryField = Entry(tab4,width=5)
SP_4_E3_EntryField.place(x=480, y=120)

SP_5_E3_EntryField = Entry(tab4,width=5)
SP_5_E3_EntryField.place(x=480, y=150)

SP_6_E3_EntryField = Entry(tab4,width=5)
SP_6_E3_EntryField.place(x=480, y=180)

SP_7_E3_EntryField = Entry(tab4,width=5)
SP_7_E3_EntryField.place(x=480, y=210)

SP_8_E3_EntryField = Entry(tab4,width=5)
SP_8_E3_EntryField.place(x=480, y=240)

SP_9_E3_EntryField = Entry(tab4,width=5)
SP_9_E3_EntryField.place(x=480, y=270)

SP_10_E3_EntryField = Entry(tab4,width=5)
SP_10_E3_EntryField.place(x=480, y=300)

SP_11_E3_EntryField = Entry(tab4,width=5)
SP_11_E3_EntryField.place(x=480, y=330)

SP_12_E3_EntryField = Entry(tab4,width=5)
SP_12_E3_EntryField.place(x=480, y=360)

SP_13_E3_EntryField = Entry(tab4,width=5)
SP_13_E3_EntryField.place(x=480, y=390)

SP_14_E3_EntryField = Entry(tab4,width=5)
SP_14_E3_EntryField.place(x=480, y=420)

SP_15_E3_EntryField = Entry(tab4,width=5)
SP_15_E3_EntryField.place(x=480, y=450)

SP_16_E3_EntryField = Entry(tab4,width=5)
SP_16_E3_EntryField.place(x=480, y=480)




SP_1_E4_EntryField = Entry(tab4,width=5)
SP_1_E4_EntryField.place(x=520, y=30)

SP_2_E4_EntryField = Entry(tab4,width=5)
SP_2_E4_EntryField.place(x=520, y=60)

SP_3_E4_EntryField = Entry(tab4,width=5)
SP_3_E4_EntryField.place(x=520, y=90)

SP_4_E4_EntryField = Entry(tab4,width=5)
SP_4_E4_EntryField.place(x=520, y=120)

SP_5_E4_EntryField = Entry(tab4,width=5)
SP_5_E4_EntryField.place(x=520, y=150)

SP_6_E4_EntryField = Entry(tab4,width=5)
SP_6_E4_EntryField.place(x=520, y=180)

SP_7_E4_EntryField = Entry(tab4,width=5)
SP_7_E4_EntryField.place(x=520, y=210)

SP_8_E4_EntryField = Entry(tab4,width=5)
SP_8_E4_EntryField.place(x=520, y=240)

SP_9_E4_EntryField = Entry(tab4,width=5)
SP_9_E4_EntryField.place(x=520, y=270)

SP_10_E4_EntryField = Entry(tab4,width=5)
SP_10_E4_EntryField.place(x=520, y=300)

SP_11_E4_EntryField = Entry(tab4,width=5)
SP_11_E4_EntryField.place(x=520, y=330)

SP_12_E4_EntryField = Entry(tab4,width=5)
SP_12_E4_EntryField.place(x=520, y=360)

SP_13_E4_EntryField = Entry(tab4,width=5)
SP_13_E4_EntryField.place(x=520, y=390)

SP_14_E4_EntryField = Entry(tab4,width=5)
SP_14_E4_EntryField.place(x=520, y=420)

SP_15_E4_EntryField = Entry(tab4,width=5)
SP_15_E4_EntryField.place(x=520, y=450)

SP_16_E4_EntryField = Entry(tab4,width=5)
SP_16_E4_EntryField.place(x=520, y=480)

SP_1_E5_EntryField = Entry(tab4,width=5)
SP_1_E5_EntryField.place(x=560, y=30)

SP_2_E5_EntryField = Entry(tab4,width=5)
SP_2_E5_EntryField.place(x=560, y=60)

SP_3_E5_EntryField = Entry(tab4,width=5)
SP_3_E5_EntryField.place(x=560, y=90)

SP_4_E5_EntryField = Entry(tab4,width=5)
SP_4_E5_EntryField.place(x=560, y=120)

SP_5_E5_EntryField = Entry(tab4,width=5)
SP_5_E5_EntryField.place(x=560, y=150)

SP_6_E5_EntryField = Entry(tab4,width=5)
SP_6_E5_EntryField.place(x=560, y=180)

SP_7_E5_EntryField = Entry(tab4,width=5)
SP_7_E5_EntryField.place(x=560, y=210)

SP_8_E5_EntryField = Entry(tab4,width=5)
SP_8_E5_EntryField.place(x=560, y=240)

SP_9_E5_EntryField = Entry(tab4,width=5)
SP_9_E5_EntryField.place(x=560, y=270)

SP_10_E5_EntryField = Entry(tab4,width=5)
SP_10_E5_EntryField.place(x=560, y=300)

SP_11_E5_EntryField = Entry(tab4,width=5)
SP_11_E5_EntryField.place(x=560, y=330)

SP_12_E5_EntryField = Entry(tab4,width=5)
SP_12_E5_EntryField.place(x=560, y=360)

SP_13_E5_EntryField = Entry(tab4,width=5)
SP_13_E5_EntryField.place(x=560, y=390)

SP_14_E5_EntryField = Entry(tab4,width=5)
SP_14_E5_EntryField.place(x=560, y=420)

SP_15_E5_EntryField = Entry(tab4,width=5)
SP_15_E5_EntryField.place(x=560, y=450)

SP_16_E5_EntryField = Entry(tab4,width=5)
SP_16_E5_EntryField.place(x=560, y=480)




SP_1_E6_EntryField = Entry(tab4,width=5)
SP_1_E6_EntryField.place(x=600, y=30)

SP_2_E6_EntryField = Entry(tab4,width=5)
SP_2_E6_EntryField.place(x=600, y=60)

SP_3_E6_EntryField = Entry(tab4,width=5)
SP_3_E6_EntryField.place(x=600, y=90)

SP_4_E6_EntryField = Entry(tab4,width=5)
SP_4_E6_EntryField.place(x=600, y=120)

SP_5_E6_EntryField = Entry(tab4,width=5)
SP_5_E6_EntryField.place(x=600, y=150)

SP_6_E6_EntryField = Entry(tab4,width=5)
SP_6_E6_EntryField.place(x=600, y=180)

SP_7_E6_EntryField = Entry(tab4,width=5)
SP_7_E6_EntryField.place(x=600, y=210)

SP_8_E6_EntryField = Entry(tab4,width=5)
SP_8_E6_EntryField.place(x=600, y=240)

SP_9_E6_EntryField = Entry(tab4,width=5)
SP_9_E6_EntryField.place(x=600, y=270)

SP_10_E6_EntryField = Entry(tab4,width=5)
SP_10_E6_EntryField.place(x=600, y=300)

SP_11_E6_EntryField = Entry(tab4,width=5)
SP_11_E6_EntryField.place(x=600, y=330)

SP_12_E6_EntryField = Entry(tab4,width=5)
SP_12_E6_EntryField.place(x=600, y=360)

SP_13_E6_EntryField = Entry(tab4,width=5)
SP_13_E6_EntryField.place(x=600, y=390)

SP_14_E6_EntryField = Entry(tab4,width=5)
SP_14_E6_EntryField.place(x=600, y=420)

SP_15_E6_EntryField = Entry(tab4,width=5)
SP_15_E6_EntryField.place(x=600, y=450)

SP_16_E6_EntryField = Entry(tab4,width=5)
SP_16_E6_EntryField.place(x=600, y=480)











####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 5




### 5 LABELS#################################################################
#############################################################################

VisFileLocLab = Label(tab5, text = "Vision File Location:")
VisFileLocLab.place(x=10, y=12)

VisCalPixLab = Label(tab5, text = "Calibration Pixels:")
VisCalPixLab.place(x=10, y=75)

VisCalmmLab = Label(tab5, text = "Calibration Robot MM:")
VisCalmmLab.place(x=10, y=105)

VisCalOxLab = Label(tab5, text = "Orig: X")
VisCalOxLab.place(x=150, y=42)

VisCalOyLab = Label(tab5, text = "Orig: Y")
VisCalOyLab.place(x=210, y=42)

VisCalXLab = Label(tab5, text = "End: X")
VisCalXLab.place(x=270, y=42)

VisCalYLab = Label(tab5, text = "End: Y")
VisCalYLab.place(x=330, y=42)



VisInTypeLab = Label(tab5, text = "Choose Vision Format")
VisInTypeLab.place(x=500, y=38)

VisXfoundLab = Label(tab5, text = "X found position (mm)")
VisXfoundLab.place(x=540, y=100)

VisYfoundLab = Label(tab5, text = "Y found position (mm)")
VisYfoundLab.place(x=540, y=130)

VisRZfoundLab = Label(tab5, text = "R found position (ang)")
VisRZfoundLab.place(x=540, y=160)

VisXpixfoundLab = Label(tab5, text = "X pixes returned from camera")
VisXpixfoundLab.place(x=760, y=100)

VisYpixfoundLab = Label(tab5, text = "Y pixes returned from camera")
VisYpixfoundLab.place(x=760, y=130)

### 5 BUTTONS################################################################
#############################################################################

visoptions=StringVar(tab5)
menu=OptionMenu(tab5, visoptions, "Openvision", "Roborealm 1.7.5", "x,y,r")
menu.grid(row=2,column=2)
menu.place(x=500, y=60)


testvisBut = Button(tab5, borderwidth=3, text="test", height=1, width=15, command = testvis)
testvisBut.place(x=500, y=190)

saveCalBut = Button(tab5, borderwidth=3, text="SAVE VISION DATA", height=1, width=26, command = SaveAndApplyCalibration)
saveCalBut.place(x=1150, y=630)


#### 5 ENTRY FIELDS##########################################################
#############################################################################

VisFileLocEntryField = Entry(tab5,width=70)
VisFileLocEntryField.place(x=125, y=12)

VisPicOxPEntryField = Entry(tab5,width=5)
VisPicOxPEntryField.place(x=155, y=75)

VisPicOxMEntryField = Entry(tab5,width=5)
VisPicOxMEntryField.place(x=155, y=105)

VisPicOyPEntryField = Entry(tab5,width=5)
VisPicOyPEntryField.place(x=215, y=75)

VisPicOyMEntryField = Entry(tab5,width=5)
VisPicOyMEntryField.place(x=215, y=105)

VisPicXPEntryField = Entry(tab5,width=5)
VisPicXPEntryField.place(x=275, y=75)

VisPicXMEntryField = Entry(tab5,width=5)
VisPicXMEntryField.place(x=275, y=105)

VisPicYPEntryField = Entry(tab5,width=5)
VisPicYPEntryField.place(x=335, y=75)

VisPicYMEntryField = Entry(tab5,width=5)
VisPicYMEntryField.place(x=335, y=105)

VisXfindEntryField = Entry(tab5,width=5)
VisXfindEntryField.place(x=500, y=100)

VisYfindEntryField = Entry(tab5,width=5)
VisYfindEntryField.place(x=500, y=130)

VisRZfindEntryField = Entry(tab5,width=5)
VisRZfindEntryField.place(x=500, y=160)

VisXpixfindEntryField = Entry(tab5,width=5)
VisXpixfindEntryField.place(x=720, y=100)

VisYpixfindEntryField = Entry(tab5,width=5)
VisYpixfindEntryField.place(x=720, y=130)




####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 6

Elogframe=Frame(tab6)
Elogframe.place(x=40,y=15)
scrollbar = Scrollbar(Elogframe) 
scrollbar.pack(side=RIGHT, fill=Y)
tab6.ElogView = Listbox(Elogframe,width=150,height=40, yscrollcommand=scrollbar.set)
try:
  Elog = pickle.load(open("ErrorLog","rb"))
except:
  Elog = ['##BEGINNING OF LOG##']
  pickle.dump(Elog,open("ErrorLog","wb"))
time.sleep(.2)
for item in Elog:
  tab6.ElogView.insert(END,item) 
tab6.ElogView.pack()
scrollbar.config(command=tab6.ElogView.yview)

def clearLog():
 tab6.ElogView.delete(1,END)
 value=tab6.ElogView.get(0,END)
 pickle.dump(value,open("ErrorLog","wb"))

clearLogBut = Button(tab6, borderwidth=3, text="Clear Log", height=1, width=26, command = clearLog)
clearLogBut.place(x=1000, y=630)



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 7

link = Label(tab7, font='12', text="https://www.anninrobotics.com/tutorials", fg="blue", cursor="hand2")
link.bind("<Button-1>", lambda event: webbrowser.open(link.cget("text")))
link.place(x=10, y=9)

def callback():
    webbrowser.open_new(r"https://www.paypal.me/ChrisAnnin")

donateBut = Button(tab7, height=30, width=80, command = callback)
donatePhoto=PhotoImage(file="pp.gif")
donateBut.config(image=donatePhoto,width="80",height="30")
donateBut.place(x=1250, y=2)


scroll = Scrollbar(tab7)
scroll.pack(side=RIGHT, fill=Y)
configfile = Text(tab7, wrap=WORD, width=166, height=40, yscrollcommand=scroll.set)
filename='information.txt'
with open(filename, 'r', encoding='utf-8-sig') as file:
  configfile.insert(INSERT, file.read())
configfile.pack(side="left")
scroll.config(command=configfile.yview)
configfile.place(x=10, y=40)



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 10

### 10 LABELS#################################################################
#############################################################################

testSendLab = Label(tab10, text = "Test string to send to arduino")
testSendLab.place(x=10, y=20)

testRecLab = Label(tab10, text = "Message echoed back from arduino")
testRecLab.place(x=10, y=70)

### 10 BUTTONS################################################################
#############################################################################

testSendBut = Button(tab10, borderwidth=3, text="SEND TO ARDUINO", height=1, width=20, command = TestString)
testSendBut.place(x=10, y=120)

testClearBut = Button(tab10, borderwidth=3, text="CLEAR RECEIVED", height=1, width=20, command = ClearTestString)
testClearBut.place(x=180, y=120)

#### 10 ENTRY FIELDS##########################################################
#############################################################################

testSendEntryField = Entry(tab10,width=222)
testSendEntryField.place(x=10, y=40)

testRecEntryField = Entry(tab10,width=222)
testRecEntryField.place(x=10, y=90)



##############################################################################################################################################################
### OPEN CAL FILE AND LOAD LIST ##############################################################################################################################
##############################################################################################################################################################

calibration = Listbox(tab2,width=20,height=60)
#calibration.place(x=160,y=170)


try:
  Cal = pickle.load(open("ARbot.cal","rb"))
except:
  Cal = "0"
  pickle.dump(Cal,open("ARbot.cal","wb"))
for item in Cal:
  calibration.insert(END,item)
J1StepCur   =calibration.get("0")
J1AngCur    =calibration.get("1")
J2StepCur   =calibration.get("2")
J2AngCur    =calibration.get("3")
J3StepCur   =calibration.get("4")
J3AngCur    =calibration.get("5")
J4StepCur   =calibration.get("6")
J4AngCur    =calibration.get("7")
J5StepCur   =calibration.get("8")
J5AngCur    =calibration.get("9")
J6StepCur   =calibration.get("10")
J6AngCur    =calibration.get("11")
comPort     =calibration.get("12")
Prog        =calibration.get("13")
Servo0on    =calibration.get("14")
Servo0off   =calibration.get("15")
Servo1on    =calibration.get("16")
Servo1off   =calibration.get("17")
DO1on       =calibration.get("18")
DO1off      =calibration.get("19")
DO2on       =calibration.get("20")
DO2off      =calibration.get("21")
UFx         =calibration.get("22")
UFy         =calibration.get("23")
UFz         =calibration.get("24")
UFrx        =calibration.get("25")
UFry        =calibration.get("26")
UFrz        =calibration.get("27")
TFx         =calibration.get("28")
TFy         =calibration.get("29")
TFz         =calibration.get("30")
TFrx        =calibration.get("31")
TFry        =calibration.get("32")
TFrz        =calibration.get("33")
FineCalPos  =calibration.get("34")
J1NegAngLim =calibration.get("35")
J1PosAngLim =calibration.get("36")
J1StepLim   =calibration.get("37")
J2NegAngLim =calibration.get("38")
J2PosAngLim =calibration.get("39")
J2StepLim   =calibration.get("40")
J3NegAngLim =calibration.get("41")
J3PosAngLim =calibration.get("42")
J3StepLim   =calibration.get("43")
J4NegAngLim =calibration.get("44")
J4PosAngLim =calibration.get("45")
J4StepLim   =calibration.get("46")
J5NegAngLim =calibration.get("47")
J5PosAngLim =calibration.get("48")
J5StepLim   =calibration.get("49")
J6NegAngLim =calibration.get("50")
J6PosAngLim =calibration.get("51")
J6StepLim   =calibration.get("52")
DHr1        =calibration.get("53")
DHr2        =calibration.get("54")
DHr3        =calibration.get("55")
DHr4        =calibration.get("56")
DHr5        =calibration.get("57")
DHr6        =calibration.get("58")
DHa1        =calibration.get("59")
DHa2        =calibration.get("60")
DHa3        =calibration.get("61")
DHa4        =calibration.get("62")
DHa5        =calibration.get("63")
DHa6        =calibration.get("64")
DHd1        =calibration.get("65")
DHd2        =calibration.get("66")
DHd3        =calibration.get("67")
DHd4        =calibration.get("68")
DHd5        =calibration.get("69")
DHd6        =calibration.get("70")
DHt1        =calibration.get("71")
DHt2        =calibration.get("72")
DHt3        =calibration.get("73")
DHt4        =calibration.get("74")
DHt5        =calibration.get("75")
DHt6        =calibration.get("76")
CalDir      =calibration.get("77")
MotDir      =calibration.get("78")
TrackcurPos =calibration.get("79")
TrackLength =calibration.get("80")
TrackStepLim=calibration.get("81")
VisFileLoc  =calibration.get("82")
VisProg     =calibration.get("83")
VisOrigXpix =calibration.get("84")
VisOrigXmm  =calibration.get("85")
VisOrigYpix =calibration.get("86")
VisOrigYmm  =calibration.get("87")
VisEndXpix  =calibration.get("88")
VisEndXmm   =calibration.get("89")
VisEndYpix  =calibration.get("90")
VisEndYmm   =calibration.get("91")
com2Port    =calibration.get("92")
J1OpenLoopVal=calibration.get("93")
J2OpenLoopVal=calibration.get("94")
J3OpenLoopVal=calibration.get("95")
J4OpenLoopVal=calibration.get("96")
J5OpenLoopVal=calibration.get("97")
J6OpenLoopVal=calibration.get("98")


####

J1curAngEntryField.insert(0,str(J1AngCur))
J2curAngEntryField.insert(0,str(J2AngCur))
J3curAngEntryField.insert(0,str(J3AngCur))
J4curAngEntryField.insert(0,str(J4AngCur))
J5curAngEntryField.insert(0,str(J5AngCur))
J6curAngEntryField.insert(0,str(J6AngCur))
comPortEntryField.insert(0,str(comPort))
com2PortEntryField.insert(0,str(com2Port))
speedEntryField.insert(0,"25")
ACCdurField.insert(0,"15")
ACCspeedField.insert(0,"10")
DECdurField.insert(0,"20")
DECspeedField.insert(0,"5")
ProgEntryField.insert(0,(Prog))
SavePosEntryField.insert(0,"1")
J1jogDegsEntryField.insert(0,"10")
J2jogDegsEntryField.insert(0,"10")
J3jogDegsEntryField.insert(0,"10")
J4jogDegsEntryField.insert(0,"10")
J5jogDegsEntryField.insert(0,"10")
J6jogDegsEntryField.insert(0,"10")
XjogEntryField.insert(0,"20")
YjogEntryField.insert(0,"20")
ZjogEntryField.insert(0,"20")
RxjogEntryField.insert(0,"20")
RyjogEntryField.insert(0,"20")
RzjogEntryField.insert(0,"20")
TXjogEntryField.insert(0,"20")
TYjogEntryField.insert(0,"20")
TZjogEntryField.insert(0,"20")
TRxjogEntryField.insert(0,"20")
TRyjogEntryField.insert(0,"20")
TRzjogEntryField.insert(0,"20")
R1EntryField.insert(0,"0")
R2EntryField.insert(0,"0")
R3EntryField.insert(0,"0")
R4EntryField.insert(0,"0")
R5EntryField.insert(0,"0")
R6EntryField.insert(0,"0")
R7EntryField.insert(0,"0")
R8EntryField.insert(0,"0")
R9EntryField.insert(0,"0")
R10EntryField.insert(0,"0")
R11EntryField.insert(0,"0")
R12EntryField.insert(0,"0")
R13EntryField.insert(0,"0")
R14EntryField.insert(0,"0")
R15EntryField.insert(0,"0")
R16EntryField.insert(0,"0")
SP_1_E1_EntryField.insert(0,"0")
SP_2_E1_EntryField.insert(0,"0")
SP_3_E1_EntryField.insert(0,"0")
SP_4_E1_EntryField.insert(0,"0")
SP_5_E1_EntryField.insert(0,"0")
SP_6_E1_EntryField.insert(0,"0")
SP_7_E1_EntryField.insert(0,"0")
SP_8_E1_EntryField.insert(0,"0")
SP_9_E1_EntryField.insert(0,"0")
SP_10_E1_EntryField.insert(0,"0")
SP_11_E1_EntryField.insert(0,"0")
SP_12_E1_EntryField.insert(0,"0")
SP_13_E1_EntryField.insert(0,"0")
SP_14_E1_EntryField.insert(0,"0")
SP_15_E1_EntryField.insert(0,"0")
SP_16_E1_EntryField.insert(0,"0")
SP_1_E2_EntryField.insert(0,"0")
SP_2_E2_EntryField.insert(0,"0")
SP_3_E2_EntryField.insert(0,"0")
SP_4_E2_EntryField.insert(0,"0")
SP_5_E2_EntryField.insert(0,"0")
SP_6_E2_EntryField.insert(0,"0")
SP_7_E2_EntryField.insert(0,"0")
SP_8_E2_EntryField.insert(0,"0")
SP_9_E2_EntryField.insert(0,"0")
SP_10_E2_EntryField.insert(0,"0")
SP_11_E2_EntryField.insert(0,"0")
SP_12_E2_EntryField.insert(0,"0")
SP_13_E2_EntryField.insert(0,"0")
SP_14_E2_EntryField.insert(0,"0")
SP_15_E2_EntryField.insert(0,"0")
SP_16_E2_EntryField.insert(0,"0")
SP_1_E3_EntryField.insert(0,"0")
SP_2_E3_EntryField.insert(0,"0")
SP_3_E3_EntryField.insert(0,"0")
SP_4_E3_EntryField.insert(0,"0")
SP_5_E3_EntryField.insert(0,"0")
SP_6_E3_EntryField.insert(0,"0")
SP_7_E3_EntryField.insert(0,"0")
SP_8_E3_EntryField.insert(0,"0")
SP_9_E3_EntryField.insert(0,"0")
SP_10_E3_EntryField.insert(0,"0")
SP_11_E3_EntryField.insert(0,"0")
SP_12_E3_EntryField.insert(0,"0")
SP_13_E3_EntryField.insert(0,"0")
SP_14_E3_EntryField.insert(0,"0")
SP_15_E3_EntryField.insert(0,"0")
SP_16_E3_EntryField.insert(0,"0")
SP_1_E4_EntryField.insert(0,"0")
SP_2_E4_EntryField.insert(0,"0")
SP_3_E4_EntryField.insert(0,"0")
SP_4_E4_EntryField.insert(0,"0")
SP_5_E4_EntryField.insert(0,"0")
SP_6_E4_EntryField.insert(0,"0")
SP_7_E4_EntryField.insert(0,"0")
SP_8_E4_EntryField.insert(0,"0")
SP_9_E4_EntryField.insert(0,"0")
SP_10_E4_EntryField.insert(0,"0")
SP_11_E4_EntryField.insert(0,"0")
SP_12_E4_EntryField.insert(0,"0")
SP_13_E4_EntryField.insert(0,"0")
SP_14_E4_EntryField.insert(0,"0")
SP_15_E4_EntryField.insert(0,"0")
SP_16_E4_EntryField.insert(0,"0")
SP_1_E5_EntryField.insert(0,"0")
SP_2_E5_EntryField.insert(0,"0")
SP_3_E5_EntryField.insert(0,"0")
SP_4_E5_EntryField.insert(0,"0")
SP_5_E5_EntryField.insert(0,"0")
SP_6_E5_EntryField.insert(0,"0")
SP_7_E5_EntryField.insert(0,"0")
SP_8_E5_EntryField.insert(0,"0")
SP_9_E5_EntryField.insert(0,"0")
SP_10_E5_EntryField.insert(0,"0")
SP_11_E5_EntryField.insert(0,"0")
SP_12_E5_EntryField.insert(0,"0")
SP_13_E5_EntryField.insert(0,"0")
SP_14_E5_EntryField.insert(0,"0")
SP_15_E5_EntryField.insert(0,"0")
SP_16_E5_EntryField.insert(0,"0")
SP_1_E6_EntryField.insert(0,"0")
SP_2_E6_EntryField.insert(0,"0")
SP_3_E6_EntryField.insert(0,"0")
SP_4_E6_EntryField.insert(0,"0")
SP_5_E6_EntryField.insert(0,"0")
SP_6_E6_EntryField.insert(0,"0")
SP_7_E6_EntryField.insert(0,"0")
SP_8_E6_EntryField.insert(0,"0")
SP_9_E6_EntryField.insert(0,"0")
SP_10_E6_EntryField.insert(0,"0")
SP_11_E6_EntryField.insert(0,"0")
SP_12_E6_EntryField.insert(0,"0")
SP_13_E6_EntryField.insert(0,"0")
SP_14_E6_EntryField.insert(0,"0")
SP_15_E6_EntryField.insert(0,"0")
SP_16_E6_EntryField.insert(0,"0")
servo0onEntryField.insert(0,str(Servo0on))
servo0offEntryField.insert(0,str(Servo0off))
servo1onEntryField.insert(0,str(Servo1on))
servo1offEntryField.insert(0,str(Servo1off))
DO1onEntryField.insert(0,str(DO1on))
DO1offEntryField.insert(0,str(DO1off))
DO2onEntryField.insert(0,str(DO2on))
DO2offEntryField.insert(0,str(DO2off))
UFxEntryField.insert(0,str(UFx))
UFyEntryField.insert(0,str(UFy))
UFzEntryField.insert(0,str(UFz))
UFrxEntryField.insert(0,str(UFrx))
UFryEntryField.insert(0,str(UFry))
UFrzEntryField.insert(0,str(UFrz))
TFxEntryField.insert(0,str(TFx))
TFyEntryField.insert(0,str(TFy))
TFzEntryField.insert(0,str(TFz))
TFrxEntryField.insert(0,str(TFrx))
TFryEntryField.insert(0,str(TFry))
TFrzEntryField.insert(0,str(TFrz))
fineCalEntryField.insert(0,str(FineCalPos))
J1NegAngLimEntryField.insert(0,str(J1NegAngLim))
J1PosAngLimEntryField.insert(0,str(J1PosAngLim))
J1StepLimEntryField.insert(0,str(J1StepLim))
J2NegAngLimEntryField.insert(0,str(J2NegAngLim))
J2PosAngLimEntryField.insert(0,str(J2PosAngLim))
J2StepLimEntryField.insert(0,str(J2StepLim))
J3NegAngLimEntryField.insert(0,str(J3NegAngLim))
J3PosAngLimEntryField.insert(0,str(J3PosAngLim))
J3StepLimEntryField.insert(0,str(J3StepLim))
J4NegAngLimEntryField.insert(0,str(J4NegAngLim))
J4PosAngLimEntryField.insert(0,str(J4PosAngLim))
J4StepLimEntryField.insert(0,str(J4StepLim))
J5NegAngLimEntryField.insert(0,str(J5NegAngLim))
J5PosAngLimEntryField.insert(0,str(J5PosAngLim))
J5StepLimEntryField.insert(0,str(J5StepLim))
J6NegAngLimEntryField.insert(0,str(J6NegAngLim))
J6PosAngLimEntryField.insert(0,str(J6PosAngLim))
J6StepLimEntryField.insert(0,str(J6StepLim))
DHr1EntryField.insert(0,str(DHr1))
DHr2EntryField.insert(0,str(DHr2))
DHr3EntryField.insert(0,str(DHr3))
DHr4EntryField.insert(0,str(DHr4))
DHr5EntryField.insert(0,str(DHr5))
DHr6EntryField.insert(0,str(DHr6))
DHa1EntryField.insert(0,str(DHa1))
DHa2EntryField.insert(0,str(DHa2))
DHa3EntryField.insert(0,str(DHa3))
DHa4EntryField.insert(0,str(DHa4))
DHa5EntryField.insert(0,str(DHa5))
DHa6EntryField.insert(0,str(DHa6))
DHd1EntryField.insert(0,str(DHd1))
DHd2EntryField.insert(0,str(DHd2))
DHd3EntryField.insert(0,str(DHd3))
DHd4EntryField.insert(0,str(DHd4))
DHd5EntryField.insert(0,str(DHd5))
DHd6EntryField.insert(0,str(DHd6))
DHt1EntryField.insert(0,str(DHt1))
DHt2EntryField.insert(0,str(DHt2))
DHt3EntryField.insert(0,str(DHt3))
DHt4EntryField.insert(0,str(DHt4))
DHt5EntryField.insert(0,str(DHt5))
DHt6EntryField.insert(0,str(DHt6))
CalDirEntryField.insert(0,str(CalDir))
MotDirEntryField.insert(0,str(MotDir))
TrackcurEntryField.insert(0,str(TrackcurPos))
TrackjogEntryField.insert(0,"10")
TrackLengthEntryField.insert(0,str(TrackLength))
TrackStepLimEntryField.insert(0,str(TrackStepLim))
VisFileLocEntryField.insert(0,str(VisFileLoc))
visoptions.set(VisProg)
VisPicOxPEntryField.insert(0,str(VisOrigXpix))
VisPicOxMEntryField.insert(0,str(VisOrigXmm))
VisPicOyPEntryField.insert(0,str(VisOrigYpix))
VisPicOyMEntryField.insert(0,str(VisOrigYmm))
VisPicXPEntryField.insert(0,str(VisEndXpix))
VisPicXMEntryField.insert(0,str(VisEndXmm))
VisPicYPEntryField.insert(0,str(VisEndYpix))
VisPicYMEntryField.insert(0,str(VisEndYmm))
if (J1OpenLoopVal == 1):
  J1OpenLoopCbut.select()
if (J2OpenLoopVal == 1):
  J2OpenLoopCbut.select()
if (J3OpenLoopVal == 1):
  J3OpenLoopCbut.select()
if (J4OpenLoopVal == 1):
  J4OpenLoopCbut.select()
if (J5OpenLoopVal == 1):
  J5OpenLoopCbut.select()
if (J6OpenLoopVal == 1):
  J6OpenLoopCbut.select()  
  

SaveAndApplyCalibration()
DisplaySteps()
CalcFwdKin()
setCom()
setCom2()


loadProg()
msg = "ANNIN ROBOTICS SOFTWARE AND MODELS ARE FREE:\n\
\n\
*for personal use.\n\
*for educational use.\n\
*for building your own robot(s).\n\
*for automating your own business.\n\
\n\
IT IS NOT OK TO RESELL THIS SOFTWARE\n\
FOR A PROFIT - IT MUST REMAIN FREE.\n\
\n\
IT IS NOT OK TO SELL AR2 ROBOTS,\n\
ROBOT PARTS, OR ANY OTHER VERSION \n\
OF ROBOT OR SOFTWARE BASED ON THE \n\
AR2 ROBOT DESIGN FOR PROFIT.\n\
\n\
Copyright (c) 2019, Chris Annin"

tkinter.messagebox.showwarning("ARCS License / Copyright notice", msg)
xboxUse = 0

global blockEncPosCal
blockEncPosCal = 0
global blockEncPosMove
blockEncPosMove = 0
  
monitor = threading.Thread(target=monitorEnc)
monitor.start()

tab1.mainloop()




#manEntryField.delete(0, 'end')
#manEntryField.insert(0,value)