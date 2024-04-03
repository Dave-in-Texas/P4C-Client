from tkinter import *
import csv
import time
import socket
import _thread
import random
from dataclasses import dataclass
@dataclass

#Manual Mode Type
class ManualModeType :
    enabled:int
    speed: int
    aux:int
    wfalls:int
    
#Manual Mode Variable Declaration
ManualSwim  = ManualModeType(0,0,0,0)
ManualClean = ManualModeType(0,0,0,0)
Waterfalls = ManualModeType(0,0,0,0)
AuxPump = ManualModeType(0,0,0,0)
MainPump = ManualModeType(0,0,0,0)

ManualSwim.enabled = 0
ManualClean.enabled = 0

######################

#Control Variable Type
class ControlVariableType():
    def __init__ (AirTemp, WaterTemp,FPL,CurrentTime):
        self.AirTemp =  AirTemp = 0
        self.WaterTemp =  WaterTemp = 0
        self.FreezeProtectLevel =  FPL = 0
        self.CurrentTime =  CurrentTime = 0
        self.TimerinOperation =  Timer = 0
        self.NextTimer =  NextTimer = 0      
        self.TimerinOperation =  socket = 0      
        self.Transferfile =  Transferfile = 0      
    

#Control Variable Declaration
CV = ControlVariableType
CV.AirTemp = 70
CV.WaterTemp = 70
CV.FPL = 0
CV.CurrentTime = 0
CV.Timer = 0
CV.NextTimer = 0
CV.socket = 1
CV.Transferfile = "none"

######################
#Timer Table Type
class TimerProgram :
    def __init__ (self, name, enabled, start, stop, speed, aux, wfalls):
        self.name = name =""
        self.enabled = enabled = 0
        self.start =  start = 0
        self.stop =  stop = 0
        self.speed =  speed = 0
        self.aux =  aux = 0
        self.wfalls =  wfalls = 0
        self.TimeTill = TT = 0
        self.TimetoGo = TTG = 0

#Timer Table Variables

Timer = []

for i in range (9):
    Timer.append(TimerProgram("",0,0,0,0,0,0))

######################
#Freeze Table Type
class FreezeProgram():
    def __init__ (self, mode, temp, speed, aux):
        self.mode = mode = 0
        self.temp = temp = 0
        self.speed =  speed = 0
        self.aux =  aux = 0

#Freeze Table Variables

FreezeProtectLevel = 0

Freeze = []

for i in range (5):
    Freeze.append(FreezeProgram('test', 0,0,0))


######################
#Pump Speed Table Type
class PumpSpeedType():
    def __init__ (self, speed):
        self.speed =  speed

#Pump Speed Variables

SpeedTable = []

for i in range (9):
    SpeedTable.append(PumpSpeedType(0))


######################

HOST = '192.168.1.244'
PORT = 9090
StatusTransfersAllowed = 1

###########Function Declarations############

#Manual Mode Functions
def readManualModesTable(ManualSwim, ManualClean):
    csvFile = open("ManualModes.csv","r")

    a,b,c,d,e = csvFile.readline().strip().split(",") #read & ignore header row
    a,b,c,d,e = csvFile.readline().strip().split(",")
    ManualSwim.enabled=0
    ManualSwim.speed=c
    ManualSwim.aux=d
    ManualSwim.wfalls=e
    a,b,c,d,e = csvFile.readline().strip().split(",")
    ManualClean.enabled=0
    ManualClean.speed=c
    ManualClean.aux=d
    ManualClean.wfalls=e

    csvFile.close()

def writeManualModesTable(ManualSwim, ManualClean):
    with open("ManualModes.csv","w",newline='') as f:
        cw = csv.writer(f)
        cw.writerow(["Manual Overrides", "Mode", "Speed", "Aux", "Waterfalls"])
        cw.writerow(["Swim","-",ManualSwim.speed,ManualSwim.aux, ManualSwim.wfalls])
        cw.writerow(["Clean","-",ManualClean.speed,ManualClean.aux, ManualClean.wfalls])
    f.close()


def MMbuttonclicked():

    def MMUpdateClicked():

        ManualSwim.speed = int(txt11.get())
        ManualSwim.aux = int(txt12.get())
        ManualSwim.wfalls = int(txt13.get())

        ManualClean.speed = int(txt21.get())
        ManualClean.aux = int(txt22.get())
        ManualClean.wfalls = int(txt23.get())

        writeManualModesTable(ManualSwim, ManualClean)
        CV.Transferfile = "ManualModes.csv"

        MMwindow.destroy()
        
    def MMCancelClicked():
        MMwindow.destroy()

    MMwindow = Tk()

    MMwindow.title("Main 'Pump Timer' Speeds Table Update")

    MMwindow.geometry('500x800')

    Blank0=Label(MMwindow, justify = CENTER, text = "     ",font=("Arial", 18))
    Blank0.grid(row=0, column=0)
    #Heading row
    lblFPModeHead = Label(MMwindow, justify = CENTER, text="Manual Mode",font=("Arial", 12))
    lblFPSpeedHead = Label(MMwindow, justify = CENTER, text="Speed",font=("Arial", 12))
    lblFPAuxHead = Label(MMwindow, justify = CENTER, text="Aux",font=("Arial", 12))
    lblFPWaterfallsHead = Label(MMwindow, justify = CENTER, text="Waterfalls",font=("Arial", 12))
    lblFPModeHead.grid(row=1,column=1)
    lblFPSpeedHead.grid(row=1,column=2)
    lblFPAuxHead.grid(row=1,column=3)
    lblFPWaterfallsHead.grid(row=1,column=4)

    #Program 1 row
    txt20 = Entry(MMwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt11 = Entry(MMwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt12 = Entry(MMwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt13 = Entry(MMwindow, justify = CENTER, width=10,font=("Arial", 12))
    Row11=Label(MMwindow, justify = CENTER, text = "Swim",font=("Arial", 12))
    Row11.grid(row=2, column=1)
    txt11.grid(row=2, column=2)
    txt11.insert(0,ManualSwim.speed)
    txt12.grid(row=2, column=3)
    txt12.insert(0,ManualSwim.aux)
    txt13.grid(row=2, column=4)
    txt13.insert(0,ManualSwim.wfalls)


    #Program 2 row
    txt20 = Entry(MMwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt21 = Entry(MMwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt22 = Entry(MMwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt23 = Entry(MMwindow, justify = CENTER, width=10,font=("Arial", 12))
    Row21=Label(MMwindow, justify = CENTER, text = "Clean",font=("Arial", 12))
    Row21.grid(row=3, column=1)
    txt21.grid(row=3, column=2)
    txt21.insert(0,ManualClean.speed)
    txt22.grid(row=3, column=3)
    txt22.insert(0,ManualClean.aux)
    txt23.grid(row=3, column=4)
    txt23.insert(0,ManualClean.wfalls)


    Blank1=Label(MMwindow, justify = CENTER, text = "",font=("Arial", 2))
    Blank1.grid(row=10, column=1)

    CancelButton = Button(MMwindow, justify = CENTER, text="Cancel",font=("Arial", 12), command=MMCancelClicked)
    CancelButton.grid(row = 11, column=3)

    Blank2=Label(MMwindow, justify = CENTER, text = "",font=("Arial", 2))
    Blank2.grid(row=12, column=1)

    UpdateButton = Button(MMwindow, justify = CENTER, text="Update", font = ("Arial", 12), command=MMUpdateClicked)
    UpdateButton.grid(row = 13, column=3)

    Blank3=Label(MMwindow, justify = CENTER, text = "",font=("Arial", 12))
    Blank3.grid(row=14, column=1)

    Disclaim0=Label(MMwindow, justify = CENTER, text = "For Waterfalls and Aux, \n use 1 for 'run', 0 for 'don't run'",font=("Arial", 12))
    Disclaim0.place(x=120, y=250)
    
    Disclaim1=Label(MMwindow, justify = CENTER, text = "Use only allowed Pump Speeds:",font=("Arial", 12))
    Disclaim1.place(x=120, y=300)

    speedtext=str(SpeedTable[1].speed)+"\n"+str(SpeedTable[2].speed)+"\n"+str(SpeedTable[3].speed)+"\n"+str(SpeedTable[4].speed)\
               +"\n"+str(SpeedTable[5].speed)+"\n"+str(SpeedTable[6].speed)+"\n"+str(SpeedTable[7].speed)+"\n"+str(SpeedTable[8].speed)
    Disclaim1=Label(MMwindow, justify = CENTER, text = speedtext,font=("Arial", 12))
    Disclaim1.place(x=200, y=325)
    
    MMwindow.mainloop()       



######################

#Timer Table Functions
def readTimerTable(Timer):
    csvFile = open("Timers.csv","r")
    a,b,c,d,e,f,g,h = csvFile.readline().strip().split(",")
    for index in range(1,9):
        a,b,c,d,e,f,g,h = csvFile.readline().strip().split(",")
        #Timer[index].prog=int(a)
        Timer[index].name=b
        Timer[index].enabled=int(c)
        Timer[index].start=int(d)
        Timer[index].stop=int(e)
        Timer[index].speed=int(f)
        Timer[index].aux=int(g)
        Timer[index].wfalls=int(h)
    csvFile.close()

def writeTimerTable(Timer):
    with open("Timers.csv","w",newline='') as f:
        cw = csv.writer(f)
        cw.writerow(["Program", "Name", "Enabled", "Start", "Stop", "Speed", "Aux", "Waterfalls"])
        for i in range(1,9):
            cw.writerow([i,Timer[i].name,Timer[i].enabled,Timer[i].start,Timer[i].stop,Timer[i].speed,Timer[i].aux,Timer[i].wfalls])
    f.close()


def TTbuttonclicked():

    def TTUpdateClicked():

        Timer[1].prog = "1"
        Timer[1].name = txt11.get()
        Timer[1].enabled = int(txt12.get())
        Timer[1].start = int(txt13.get())
        Timer[1].stop = int(txt14.get())
        Timer[1].speed = int(txt15.get())
        Timer[1].aux = int(txt16.get())
        Timer[1].wfalls = int(txt17.get())

        Timer[2].prog = "2"
        Timer[2].name = txt21.get()
        Timer[2].enabled = int(txt22.get())
        Timer[2].start = int(txt23.get())
        Timer[2].stop = int(txt24.get())
        Timer[2].speed = int(txt25.get())
        Timer[2].aux = int(txt26.get())
        Timer[2].wfalls = int(txt27.get())

        Timer[3].prog = "3"
        Timer[3].name = txt31.get()
        Timer[3].enabled = int(txt32.get())
        Timer[3].start = int(txt33.get())
        Timer[3].stop = int(txt34.get())
        Timer[3].speed = int(txt35.get())
        Timer[3].aux = int(txt36.get())
        Timer[3].wfalls = int(txt37.get())

        Timer[4].prog = "4"
        Timer[4].name = txt41.get()
        Timer[4].enabled = int(txt42.get())
        Timer[4].start = int(txt43.get())
        Timer[4].stop = int(txt44.get())
        Timer[4].speed = int(txt45.get())
        Timer[4].aux = int(txt46.get())
        Timer[4].wfalls = int(txt47.get())

        Timer[5].prog = "5"
        Timer[5].name = txt51.get()
        Timer[5].enabled = int(txt52.get())
        Timer[5].start = int(txt53.get())
        Timer[5].stop = int(txt54.get())
        Timer[5].speed = int(txt55.get())
        Timer[5].aux = int(txt56.get())
        Timer[5].wfalls = int(txt57.get())

        Timer[6].prog = "6"
        Timer[6].name = txt61.get()
        Timer[6].enabled = int(txt62.get())
        Timer[6].start = int(txt63.get())
        Timer[6].stop = int(txt64.get())
        Timer[6].speed = int(txt65.get())
        Timer[6].aux = int(txt66.get())
        Timer[6].wfalls = int(txt67.get())

        Timer[7].prog = "7"
        Timer[7].name = txt71.get()
        Timer[7].enabled = int(txt72.get())
        Timer[7].start = int(txt73.get())
        Timer[7].stop = int(txt74.get())
        Timer[7].speed = int(txt75.get())
        Timer[7].aux = int(txt76.get())
        Timer[7].wfalls = int(txt77.get())

        Timer[8].prog = "8"
        Timer[8].name = txt81.get()
        Timer[8].enabled = int(txt82.get())
        Timer[8].start = int(txt83.get())
        Timer[8].stop = int(txt84.get())
        Timer[8].speed = int(txt85.get())
        Timer[8].aux = int(txt86.get())
        Timer[8].wfalls = int(txt87.get()) 

        writeTimerTable(Timer)
        CV.Transferfile = "Timers.csv"
        
        TTwindow.destroy()

    def TTCancelClicked():
        TTwindow.destroy()


    TTwindow = Tk()

    TTwindow.title("Timer Table Update")

    TTwindow.geometry('500x800')

    Title0 = Label(TTwindow, text = "",font=("Arial", 20), bg=wc)

    Blank0=Label(TTwindow, justify = CENTER, text = "",font=("Arial", 12))
    Blank0.grid(row=0, column=0)

    lblFPProgramHead = Label(TTwindow, text="")
    lblFPNameHead = Label(TTwindow, text="Name")
    lblFPEnabledHead = Label(TTwindow, text="E*")
    lblFPStartHead = Label(TTwindow, text="Start")
    lblFPStopHead = Label(TTwindow, text="Stop")
    lblFPSpeedHead = Label(TTwindow, text="Speed")
    lblFPAuxHead = Label(TTwindow, text="Aux")
    lblFPWaterfallsHead = Label(TTwindow, text="W*")
    lblFPProgramHead.grid(row=1,column=0)
    lblFPNameHead.grid(row=1,column=1)
    lblFPEnabledHead.grid(row=1,column=2)
    lblFPStartHead.grid(row=1,column=3)
    lblFPStopHead.grid(row=1,column=4)
    lblFPSpeedHead.grid(row=1,column=5)
    lblFPAuxHead.grid(row=1,column=6)
    lblFPWaterfallsHead.grid(row=1,column=7)

    #Program 1 row
    txt11 = Entry(TTwindow, justify = CENTER, width=26, font=("Arial",11))
    txt12 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    txt13 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt14 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt15 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt16 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    txt17 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    Row10=Label(TTwindow, text = "1", font=("Arial",11))
    Row10.grid(row=2, column=0)
    txt11.grid(row=2, column=1)
    txt11.insert(0,Timer[1].name)
    txt12.grid(row=2, column=2)
    txt12.insert(0,Timer[1].enabled)
    txt13.grid(row=2, column=3)
    txt13.insert(0,Timer[1].start)
    txt14.grid(row=2, column=4)
    txt14.insert(0,Timer[1].stop)
    txt15.grid(row=2, column=5)
    txt15.insert(0,Timer[1].speed)
    txt16.grid(row=2, column=6)
    txt16.insert(0,Timer[1].aux)
    txt17.grid(row=2, column=7)
    txt17.insert(0,Timer[1].wfalls)

    #Program 2 row
    txt21 = Entry(TTwindow, justify = CENTER, width=26, font=("Arial",11), bg ='#DDFFFF')
    txt22 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    txt23 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt24 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt25 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt26 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    txt27 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    Row20=Label(TTwindow, text = "2", font=("Arial",11))
    Row20.grid(row=3, column=0)
    txt21.grid(row=3, column=1)
    txt21.insert(0,Timer[2].name)
    txt22.grid(row=3, column=2)
    txt22.insert(0,Timer[2].enabled)
    txt23.grid(row=3, column=3)
    txt23.insert(0,Timer[2].start)
    txt24.grid(row=3, column=4)
    txt24.insert(0,Timer[2].stop)
    txt25.grid(row=3, column=5)
    txt25.insert(0,Timer[2].speed)
    txt26.grid(row=3, column=6)
    txt26.insert(0,Timer[2].aux)
    txt27.grid(row=3, column=7)
    txt27.insert(0,Timer[2].wfalls)

    #Program 3 row
    txt31 = Entry(TTwindow, justify = CENTER, width=26, font=("Arial",11))
    txt32 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    txt33 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt34 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt35 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt36 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    txt37 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    Row30=Label(TTwindow, text = "3", font=("Arial",11))
    Row30.grid(row=4, column=0)
    txt31.grid(row=4, column=1)
    txt31.insert(0,Timer[3].name)
    txt32.grid(row=4, column=2)
    txt32.insert(0,Timer[3].enabled)
    txt33.grid(row=4, column=3)
    txt33.insert(0,Timer[3].start)
    txt34.grid(row=4, column=4)
    txt34.insert(0,Timer[3].stop)
    txt35.grid(row=4, column=5)
    txt35.insert(0,Timer[3].speed)
    txt36.grid(row=4, column=6)
    txt36.insert(0,Timer[3].aux)
    txt37.grid(row=4, column=7)
    txt37.insert(0,Timer[3].wfalls)

    #Program 4 row
    txt41 = Entry(TTwindow, justify = CENTER, width=26, font=("Arial",11), bg ='#DDFFFF')
    txt42 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    txt43 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt44 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt45 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt46 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    txt47 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    Row40=Label(TTwindow, text = "4", font=("Arial",11))
    Row40.grid(row=5, column=0)
    txt41.grid(row=5, column=1)
    txt41.insert(0,Timer[4].name)
    txt42.grid(row=5, column=2)
    txt42.insert(0,Timer[4].enabled)
    txt43.grid(row=5, column=3)
    txt43.insert(0,Timer[4].start)
    txt44.grid(row=5, column=4)
    txt44.insert(0,Timer[4].stop)
    txt45.grid(row=5, column=5)
    txt45.insert(0,Timer[4].speed)
    txt46.grid(row=5, column=6)
    txt46.insert(0,Timer[4].aux)
    txt47.grid(row=5, column=7)
    txt47.insert(0,Timer[4].wfalls)

    #Program 5 row
    txt51 = Entry(TTwindow, justify = CENTER, width=26, font=("Arial",11))
    txt52 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    txt53 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt54 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt55 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt56 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    txt57 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    Row50=Label(TTwindow, text = "5", font=("Arial",11))
    Row50.grid(row=6, column=0)
    txt51.grid(row=6, column=1)
    txt51.insert(0,Timer[5].name)
    txt52.grid(row=6, column=2)
    txt52.insert(0,Timer[5].enabled)
    txt53.grid(row=6, column=3)
    txt53.insert(0,Timer[5].start)
    txt54.grid(row=6, column=4)
    txt54.insert(0,Timer[5].stop)
    txt55.grid(row=6, column=5)
    txt55.insert(0,Timer[5].speed)
    txt56.grid(row=6, column=6)
    txt56.insert(0,Timer[5].aux)
    txt57.grid(row=6, column=7)
    txt57.insert(0,Timer[5].wfalls)

    #Program 6 row
    txt61 = Entry(TTwindow, justify = CENTER, width=26, font=("Arial",11), bg ='#DDFFFF')
    txt62 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    txt63 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt64 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt65 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt66 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    txt67 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    Row60=Label(TTwindow, text = "6", font=("Arial",11))
    Row60.grid(row=7, column=0)
    txt61.grid(row=7, column=1)
    txt61.insert(0,Timer[6].name)
    txt62.grid(row=7, column=2)
    txt62.insert(0,Timer[6].enabled)
    txt63.grid(row=7, column=3)
    txt63.insert(0,Timer[6].start)
    txt64.grid(row=7, column=4)
    txt64.insert(0,Timer[6].stop)
    txt65.grid(row=7, column=5)
    txt65.insert(0,Timer[6].speed)
    txt66.grid(row=7, column=6)
    txt66.insert(0,Timer[6].aux)
    txt67.grid(row=7, column=7)
    txt67.insert(0,Timer[6].wfalls)

    #Program 7 row
    txt71 = Entry(TTwindow, justify = CENTER, width=26, font=("Arial",11))
    txt72 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    txt73 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt74 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt75 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11))
    txt76 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    txt77 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11))
    Row70=Label(TTwindow, text = "7", font=("Arial",11))
    Row70.grid(row=8, column=0)
    txt71.grid(row=8, column=1)
    txt71.insert(0,Timer[7].name)
    txt72.grid(row=8, column=2)
    txt72.insert(0,Timer[7].enabled)
    txt73.grid(row=8, column=3)
    txt73.insert(0,Timer[7].start)
    txt74.grid(row=8, column=4)
    txt74.insert(0,Timer[7].stop)
    txt75.grid(row=8, column=5)
    txt75.insert(0,Timer[7].speed)
    txt76.grid(row=8, column=6)
    txt76.insert(0,Timer[7].aux)
    txt77.grid(row=8, column=7)
    txt77.insert(0,Timer[7].wfalls)

    #Program 8 row
    txt81 = Entry(TTwindow, justify = CENTER, width=26, font=("Arial",11), bg ='#DDFFFF')
    txt82 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    txt83 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt84 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt85 = Entry(TTwindow, justify = CENTER, width=6, font=("Arial",11), bg ='#DDFFFF')
    txt86 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    txt87 = Entry(TTwindow, justify = CENTER, width=3, font=("Arial",11), bg ='#DDFFFF')
    Row80=Label(TTwindow, text = "8", font=("Arial",11))
    Row80.grid(row=9, column=0)
    txt81.grid(row=9, column=1)
    txt81.insert(0,Timer[8].name)
    txt82.grid(row=9, column=2)
    txt82.insert(0,Timer[8].enabled)
    txt83.grid(row=9, column=3)
    txt83.insert(0,Timer[8].start)
    txt84.grid(row=9, column=4)
    txt84.insert(0,Timer[8].stop)
    txt85.grid(row=9, column=5)
    txt85.insert(0,Timer[8].speed)
    txt86.grid(row=9, column=6)
    txt86.insert(0,Timer[8].aux)
    txt87.grid(row=9, column=7)
    txt87.insert(0,Timer[8].wfalls)

    Disclaim0=Label(TTwindow, justify = CENTER, text = "WARNING\nDo not set Start Time = Stop Time.  Error will occur.\nDo not run Aux and Waterfall at the same time.",font=("Arial", 12))
    Disclaim0.place(x=50, y=250)

    Disclaim1=Label(TTwindow, justify = CENTER, text = "* E = timer program Enabled, W = Waterfalls\nTimer Programs which are not Enabled will not run",font=("Arial", 12))
    Disclaim1.place(x=50, y=325)

    Disclaim2=Label(TTwindow, justify = CENTER, text = "For Waterfalls and Aux, \n use 1 for 'run', 0 for 'don't run'",font=("Arial", 12))
    Disclaim2.place(x=120, y=375)

    Disclaim3=Label(TTwindow, justify = CENTER, text = "Lower numbered programs take priority\nover higher numbered rograms",font=("Arial", 12))
    Disclaim3.place(x=100, y=425)

    CancelButton = Button(TTwindow, text="Cancel", font=("Arial",12),command=TTCancelClicked)
    CancelButton.place(x = 200, y = 475)

    UpdateButton = Button(TTwindow, text="Update", font=("Arial",12), command=TTUpdateClicked)
    UpdateButton.place(x = 200, y= 525)
    
    Disclaim4=Label(TTwindow, justify = CENTER, text = "Use only allowed Pump Speeds:",font=("Arial", 12))
    Disclaim4.place(x=120, y=575)

    speedtext=str(SpeedTable[1].speed)+"\n"+str(SpeedTable[2].speed)+"\n"+str(SpeedTable[3].speed)+"\n"+str(SpeedTable[4].speed)\
               +"\n"+str(SpeedTable[5].speed)+"\n"+str(SpeedTable[6].speed)+"\n"+str(SpeedTable[7].speed)+"\n"+str(SpeedTable[8].speed)
    Disclaim5=Label(TTwindow, justify = CENTER, text = speedtext,font=("Arial", 12))
    Disclaim5.place(x=200, y=600)

    TTwindow.mainloop()



######################

#Freeze Table Functions
    
#Freeze Table Functions
def readFreezeTable(Freeze):
    csvFile = open("Freeze.csv","r")
    a,b,c,d = csvFile.readline().strip().split(",")
    for index in range(5):
        a,b,c,d = csvFile.readline().strip().split(",")
        Freeze[index].mode=a
        Freeze[index].temp=b
        Freeze[index].speed=c
        Freeze[index].aux=d
    csvFile.close()


def writeFreezeTable(Freeze):
    with open("Freeze.csv","w",newline='') as f:
        cw = csv.writer(f)
        cw.writerow(["Mode", "Temp", "Speed", "Aux"])
        for i in range(5):
            cw.writerow([Freeze[i].mode,Freeze[i].temp,Freeze[i].speed,Freeze[i].aux])
    f.close()


def FTbuttonclicked():

    def FTUpdateClicked():

        Freeze[0].mode = "Off"
        Freeze[0].temp = int(txt11.get())
        Freeze[0].speed = int(txt12.get())
        Freeze[0].aux = int(txt13.get())
        
        Freeze[1].mode = "1"
        Freeze[1].temp = int(txt21.get())
        Freeze[1].speed = int(txt22.get())
        Freeze[1].aux = int(txt23.get())
        
        Freeze[2].mode = "2"
        Freeze[2].temp = int(txt31.get())
        Freeze[2].speed = int(txt32.get())
        Freeze[2].aux = int(txt33.get())
        
        Freeze[3].mode = "3"
        Freeze[3].temp = int(txt41.get())
        Freeze[3].speed = int(txt42.get())
        Freeze[3].aux = int(txt43.get())

        Freeze[4].mode = "4"
        Freeze[4].temp = int(txt51.get())
        Freeze[4].speed = int(txt52.get())
        Freeze[4].aux = int(txt53.get())

        writeFreezeTable(Freeze)
        CV.Transferfile = "Freeze.csv"
        FTwindow.destroy()

    def FTCancelClicked():
        FTwindow.destroy()

    
    FTwindow = Tk()

    FTwindow.title("Freeze Table Update")

    FTwindow.geometry('500x800')

    Blank0=Label(FTwindow, justify = CENTER, text = "     ",font=("Arial", 18))
    Blank0.grid(row=0, column=0)
    
    #Heading row
    lblFPModeHead = Label(FTwindow, text="Mode",font=("Arial", 12))
    lblFPTempHead = Label(FTwindow, text="Temp",font=("Arial", 12))
    lblFPSpeedHead = Label(FTwindow, text="Speed",font=("Arial", 12))
    lblFPAuxHead = Label(FTwindow, text="Aux",font=("Arial", 12))
    lblFPModeHead.grid(column=1, row=1)
    lblFPTempHead.grid(column=2, row=1)
    lblFPSpeedHead.grid(column=3, row=1)
    lblFPAuxHead.grid(column=4, row=1)

    #Level Zero row
    txt10 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt11 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt12 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt13 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    Row10=Label(FTwindow, text = "Off",font=("Arial", 12),width=10)
    Row10.grid(column=1, row=2)
    txt11.grid(column=2, row=2)
    txt11.insert(0,Freeze[0].temp)
    txt12.grid(column=3, row=2)
    txt12.insert(0,Freeze[0].speed)
    txt13.grid(column=4, row=2)
    txt13.insert(0,Freeze[0].aux)

    #Level One row
    txt20 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt21 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt22 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt23 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    Row20=Label(FTwindow, text = "Level 1",font=("Arial", 12),width=10)
    Row20.grid(column=1, row=3)
    txt21.grid(column=2, row=3)
    txt21.insert(0,Freeze[1].temp)
    txt22.grid(column=3, row=3)
    txt22.insert(0,Freeze[1].speed)
    txt23.grid(column=4, row=3)
    txt23.insert(0,Freeze[1].aux)

    #Level Two row
    txt30 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt31 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt32 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt33 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    Row30=Label(FTwindow, text = "Level 2",font=("Arial", 12),width=10)
    Row30.grid(column=1, row=4)
    txt31.grid(column=2, row=4)
    txt31.insert(0,Freeze[2].temp)
    txt32.grid(column=3, row=4)
    txt32.insert(0,Freeze[2].speed)
    txt33.grid(column=4, row=4)
    txt33.insert(0,Freeze[2].aux)

    #Level Three row
    txt40 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt41 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt42 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt43 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt43 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    Row40=Label(FTwindow, text = "Level 3",font=("Arial", 12),width=10)
    Row40.grid(column=1, row=5)
    txt41.grid(column=2, row=5)
    txt41.insert(0,Freeze[3].temp)
    txt42.grid(column=3, row=5)
    txt42.insert(0,Freeze[3].speed)
    txt43.grid(column=4, row=5)
    txt43.insert(0,Freeze[3].aux)

    #Level Four row
    txt50 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt51 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt52 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    txt53 = Entry(FTwindow, justify = CENTER, width=10,font=("Arial", 12))
    Row50=Label(FTwindow, text = "Level 4",font=("Arial", 12),width=10)
    Row50.grid(column=1, row=6)
    txt51.grid(column=2, row=6)
    txt51.insert(0,Freeze[4].temp)
    txt52.grid(column=3, row=6)
    txt52.insert(0,Freeze[4].speed)
    txt53.grid(column=4, row=6)
    txt53.insert(0,Freeze[4].aux)


    Blank1=Label(FTwindow, justify = CENTER, text = "",font=("Arial", 2))
    Blank1.grid(row=9, column=1)
    CancelButton = Button(FTwindow, text="Cancel", font=("Arial", 12), command=FTCancelClicked)
    CancelButton.grid(row = 10, column=3)
    Blank2=Label(FTwindow, justify = CENTER, text = "",font=("Arial", 2))
    Blank2.grid(row=11, column=1)
    UpdateButton = Button(FTwindow, text="Update",font=("Arial", 12), command=FTUpdateClicked)
    UpdateButton.grid(row = 12, column=3)



    Blank2=Label(FTwindow, justify = CENTER, text = "",font=("Arial", 2))
    Blank2.grid(row=12, column=1)

    Blank3=Label(FTwindow, justify = CENTER, text = "",font=("Arial", 12))
    Blank3.grid(row=14, column=1)

    Disclaim0=Label(FTwindow, justify = CENTER, text = "For Waterfalls and Aux, \n use 1 for 'run', 0 for 'don't run'",font=("Arial", 12))
    Disclaim0.place(x=120, y=300)
    
    Disclaim1=Label(FTwindow, justify = CENTER, text = "Use only allowed Pump Speeds:",font=("Arial", 12))
    Disclaim1.place(x=120, y=350)

    speedtext=str(SpeedTable[1].speed)+"\n"+str(SpeedTable[2].speed)+"\n"+str(SpeedTable[3].speed)+"\n"+str(SpeedTable[4].speed)\
               +"\n"+str(SpeedTable[5].speed)+"\n"+str(SpeedTable[6].speed)+"\n"+str(SpeedTable[7].speed)+"\n"+str(SpeedTable[8].speed)
    Disclaim1=Label(FTwindow, justify = CENTER, text = speedtext,font=("Arial", 12))
    Disclaim1.place(x=200, y=375)

    FTwindow.mainloop()

######################

#Pump Speed Table Functions
def readPumpSpeedTable(Speed):
    csvFile = open("PumpSpeeds.csv","r")
    for index in range(9):
        a,b = csvFile.readline().strip().split(",")
        SpeedTable[index].number=a
        SpeedTable[index].speed=b

    SpeedTable[1].speed = "0"
    csvFile.close()

def writePumpSpeedTable(Speed):
    with open("PumpSpeeds.csv","w",newline='') as f:
        cw = csv.writer(f)
        for i in range(9):
            cw.writerow([SpeedTable[i].number,SpeedTable[i].speed])
    f.close()

def PSbuttonclicked():
    

    def PSUpdateClicked():

        SpeedTable[1].number = "1"
        SpeedTable[1].speed = "0"

        SpeedTable[2].number = "2"
        SpeedTable[2].speed = txt21.get()

        SpeedTable[3].number = "3"
        SpeedTable[3].speed = txt31.get()

        SpeedTable[4].number = "4"
        SpeedTable[4].speed = txt41.get()

        SpeedTable[5].number = "5"
        SpeedTable[5].speed = txt51.get()

        SpeedTable[6].number = "6"
        SpeedTable[6].speed = txt61.get()

        SpeedTable[7].number = "7"
        SpeedTable[7].speed = txt71.get()

        SpeedTable[8].number = "8"
        SpeedTable[8].speed = txt81.get()

        writePumpSpeedTable(SpeedTable)
        CV.Transferfile = "PumpSpeeds.csv"

        PSwindow.destroy()
        
    def PSCancelClicked():
        PSwindow.destroy()

    PSwindow = Tk()

    PSwindow.title("Main 'Pump Timer' Speeds Table Update")

    PSwindow.geometry('500x800')
    
    Blank0=Label(PSwindow, justify = CENTER, text = "            ",font=("Arial", 22))
    Blank0.grid(row=0, column=0)

    #Heading row
    lblFPModeHead = Label(PSwindow, text="Pump Timer Speed", font=("Arial",12))
    lblFPSpeedHead = Label(PSwindow, text="Speed", font=("Arial",12))
    lblFPModeHead.grid(row=1,column=1)
    lblFPSpeedHead.grid(row=1,column=2)

    #Speed 1 row
    Row10=Label(PSwindow, text = "1", font=("Arial",12))
    txt11 = Entry(PSwindow, justify = CENTER, width=8, font=("Arial",12))
    Row10.grid(row=2, column=1)
    txt11.grid(row=2, column=2)
    txt11.insert(0,SpeedTable[1].speed)

    #Speed 2 row
    Row20=Label(PSwindow, text = "2", font=("Arial",12))
    txt21 = Entry(PSwindow, justify = CENTER, width=8, font=("Arial",12))
    Row20.grid(row=3, column=1)
    txt21.grid(row=3, column=2)
    txt21.insert(0,SpeedTable[2].speed)

    #Speed 3 row
    Row30=Label(PSwindow, text = "3", font=("Arial",12))
    txt31 = Entry(PSwindow, justify = CENTER, width=8, font=("Arial",12))
    Row30.grid(row=4, column=1)
    txt31.grid(row=4, column=2)
    txt31.insert(0,SpeedTable[3].speed)

    #Speed 4 row
    Row40=Label(PSwindow, text = "4", font=("Arial",12))
    txt41 = Entry(PSwindow, justify = CENTER, width=8, font=("Arial",12))
    Row40.grid(row=5, column=1)
    txt41.grid(row=5, column=2)
    txt41.insert(0,SpeedTable[4].speed)

    #Speed 5 row
    Row50=Label(PSwindow, text = "5", font=("Arial",12))
    txt51 = Entry(PSwindow, justify = CENTER, width=8, font=("Arial",12))
    Row50.grid(row=6, column=1)
    txt51.grid(row=6, column=2)
    txt51.insert(0,SpeedTable[5].speed)

    #Speed 6 row
    Row60=Label(PSwindow, text = "6", font=("Arial",12))
    txt61 = Entry(PSwindow, justify = CENTER, width=8, font=("Arial",12))
    Row60.grid(row=7, column=1)
    txt61.grid(row=7, column=2)
    txt61.insert(0,SpeedTable[6].speed)

    #Speed 7 row
    Row70=Label(PSwindow, text = "7", font=("Arial",12))
    txt71 = Entry(PSwindow, justify = CENTER, width=8, font=("Arial",12))
    Row70.grid(row=8, column=1)
    txt71.grid(row=8, column=2)
    txt71.insert(0,SpeedTable[7].speed)

    #Speed 8 row
    Row80=Label(PSwindow, text = "8", font=("Arial",12))
    txt81 = Entry(PSwindow, justify = CENTER, width=8, font=("Arial",12))
    Row80.grid(row=9, column=1)
    txt81.grid(row=9, column=2)
    txt81.insert(0,SpeedTable[8].speed)

    Blank1=Label(PSwindow, justify = CENTER, text = "",font=("Arial", 2))
    Blank1.grid(row=20, column=1)
    CancelButton = Button(PSwindow, text="Cancel", font=("Arial",12), command=PSCancelClicked)
    CancelButton.grid(row = 21, column=2)

    Blank2=Label(PSwindow, justify = CENTER, text = "",font=("Arial", 2))
    Blank2.grid(row=22, column=1)
    UpdateButton = Button(PSwindow, text="Update", font=("Arial",12), command=PSUpdateClicked)
    UpdateButton.grid(row = 23, column=2)


    Disclaim0=Label(PSwindow, justify = CENTER, text = "Pump Speed Table entries need to match\nthe speeds programmed into the \nTimers on the Main Pump\n\nFaulty operation may occur otherwise\n\nFIRST SPEED MUST BE 0",font=("Arial", 12))
    Disclaim0.place(x=100, y=400)

    speedtext=str(SpeedTable[1].speed)+"\n"+str(SpeedTable[2].speed)+"\n"+str(SpeedTable[3].speed)+"\n"+str(SpeedTable[4].speed)\
               +"\n"+str(SpeedTable[5].speed)+"\n"+str(SpeedTable[6].speed)+"\n"+str(SpeedTable[7].speed)+"\n"+str(SpeedTable[8].speed)
    Disclaim1=Label(PSwindow, justify = CENTER, text = speedtext,font=("Arial", 12))
    Disclaim1.place(x=200, y=550)

    PSwindow.mainloop()       


#################  Controller Logic Functions  ############

# Freeze Protection Logic

def FreezeProtect():
    
    if CV.FPL > 0:

        ManualSwim.enabled = 0
        MSbutton.config(text="Manual Swim is OFF", bg='black', command=turnMSon)
        MSbutton.config(state=NORMAL)

        ManualClean.enabled = 0
        MCbutton.config(text="Manual Clean is OFF", bg='black', command=turnMCon)
        MCbutton.config(state=NORMAL)

        Info1.config(text = ("  "))
        Info2.config(text = ("Freeze Protection: Level "+str(CV.FPL)),font = ('Arial', 14), fg='dark red', bg=wc)
        Info3.config(text = ("  "))
    
    Info2.after(5000,FreezeProtect)

# Timer Logic 

#set up the clock functionality
def clock():    
    global hour, min, sec, month, day, dayofweek, year
    hour = time.strftime("%H")
    min = time.strftime("%M")
    sec = time.strftime("%S")
    CV.CurrentTime = int(hour+min)
    month = time.strftime("%m")
    dayofweek = time.strftime("%A")
    day = time.strftime("%d")
    year = time.strftime("%y")

    Info0.config(text=dayofweek+", "+month+"/"+day+"/"+year+"  "+hour+":"+min+":"+sec)
    Info0.after(1000,clock)

def MinutesBetween(a,b):
    a_in_minutes = 60*(a//100) + (a%100)
    #print(a_in_minutes)
    b_in_minutes = 60*(b//100) + (b%100)
    #print(b_in_minutes)
    return(a_in_minutes - b_in_minutes)
    

def TimerLogic():
    clock()

    if CV.FPL == 0 and ManualSwim.enabled == 0 and ManualClean.enabled == 0:
        MinutesToNextTimer=2400
        
        #'easy' case - timer does not run past midnight
        if Timer[CV.Timer].stop > Timer[CV.Timer].start:          
            #Timer[CV.Timer].TTG = Timer[CV.Timer].stop - CV.CurrentTime
            Timer[CV.Timer].TTG = MinutesBetween(Timer[CV.Timer].stop, CV.CurrentTime)
            #print("theta", Timer[CV.Timer].TTG)
            # Calculate MinutesToNextTimer
            if CV.NextTimer !=0:
                if Timer[CV.NextTimer].start > CV.CurrentTime and Timer[CV.NextTimer].start <= 2359:
                    #MinutesToNextTimer = Timer[CV.NextTimer].start - CV.CurrentTime
                    MinutesToNextTimer = MinutesBetween(Timer[CV.NextTimer].start, CV.CurrentTime)
                else:
                    #MinutesToNextTimer = (2400-CV.CurrentTime) + Timer[CV.NextTimer].start 
                    MinutesToNextTimer = MinutesBetween(2400,CV.CurrentTime) + MinutesBetween(Timer[CV.NextTimer].start,0)
        # 'harder' case - timer runs past midnight                                           
        if Timer[CV.Timer].start > Timer[CV.Timer].stop:  
            if CV.CurrentTime >= Timer[CV.Timer].stop:  #current time is before midnight
                Timer[CV.Timer].TTG = MinutesBetween(2400,CV.CurrentTime) + MinutesBetween(Timer[CV.Timer].start,0)
            else:  #current time is after midnight
                Timer[CV.Timer].TTG = MinutesBetween(Timer[CV.Timer].stop, CV.CurrentTime)
            # Calculate MinutesToNextTimer
            if CV.NextTimer !=0:
                MinutesToNextTimer = MinutesBetween(Timer[CV.NextTimer].start, CV.CurrentTime)


        ###  the case where a Timer is running
        #print("Current timer in use is: ", CV.Timer)
        if CV.Timer != 0:
            Info1.config(text = "Current Timer in Use:",font = ('Arial', 12), fg='black', bg=wc)
            Info2.config(text = "Timer "+str(CV.Timer)+": "+str(Timer[CV.Timer].name),font = ('Arial', 14), fg='black', bg=wc)

            #print("TTG: ",Timer[CV.Timer].TTG, "Next: " ,MinutesToNextTimer)
            if Timer[CV.Timer].TTG < MinutesToNextTimer:
                Info3.config(text = "Terminates at "+str(Timer[CV.Timer].stop),font = ('Arial', 12), fg='black', bg=wc)
            else:
                Info3.config(text = "Timer "+str(CV.NextTimer)+" will start at "+str(Timer[CV.NextTimer].start),font = ('Arial', 12), fg='black', bg=wc)    
                
        ###  the case where no Timer is running
        else:
            MainPump.speed = 0
            AuxPump.speed = 0

            if CV.NextTimer < 9:
                Info1.config(text = "Next Timer:")
                Info2.config(text = Timer[CV.NextTimer].name)
                if Timer[CV.NextTimer].start <1000:
                    Info3.config(text = "Starts at "+"0"+str(Timer[CV.NextTimer].start))
                else:
                    Info3.config(text = "Starts at "+str(Timer[CV.NextTimer].start))
            else:
                Info1.config(text = "Next Timer:")
                Info2.config(text = "None enabled at this time")
                Info3.config(text = " ")


    Info2.after(5000,TimerLogic)

#################################################

def ExchangeStatuswithServer():

    HOST = '192.168.1.244'
    PORT = 9090

    while CV.socket == 1:

        print("Current time is: ",CV.CurrentTime)
        socket_one = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("opening socket")
        socket_one.connect((HOST, PORT))
        print("Connected")

        Transfertext = str(ManualSwim.enabled)
        #print("ManualSwim.enabled = ",Transfertext)
        socket_one.send(Transfertext.encode('utf-8'))
        CV.AirTemp = float((socket_one.recv(1024).decode('utf-8')))
        #print("airtemp: ",CV.AirTemp)

        Transfertext = str(ManualClean.enabled)
        socket_one.send(Transfertext.encode('utf-8'))
        CV.WaterTemp = float((socket_one.recv(1024).decode('utf-8')))
        #print("watertemp: ",CV.WaterTemp)

        Transfer_file = CV.Transferfile
        #print("file is ",Transfer_file)
        socket_one.send(Transfer_file.encode('utf-8'))
        CV.FPL = int((socket_one.recv(1024).decode('utf-8')))
        #print("FPL: ",CV.FPL)

        Transfertext = year
        socket_one.send(Transfertext.encode('utf-8'))
        CV.Timer = int((socket_one.recv(1024).decode('utf-8')))
        #print("current timer: ",CV.Timer)

        Transfertext = month
        socket_one.send(Transfertext.encode('utf-8'))
        CV.NextTimer = int((socket_one.recv(1024).decode('utf-8')))
        #print("next timer: ",CV.NextTimer)

        Transfertext = day
        socket_one.send(Transfertext.encode('utf-8'))
        MainPump.enabled = int((socket_one.recv(1024).decode('utf-8')))
        #print("Main Pump enabled: ",MainPump.enabled)

        Transfertext = hour
        socket_one.send(Transfertext.encode('utf-8'))
        MainPump.speed = int((socket_one.recv(1024).decode('utf-8')))
        #print("main pump speed: ",MainPump.speed)

        Transfertext = min
        socket_one.send(Transfertext.encode('utf-8'))
        AuxPump.enabled = int((socket_one.recv(1024).decode('utf-8')))
        #print("AP enabled:",AuxPump.enabled)

        Transfertext = sec
        socket_one.send(Transfertext.encode('utf-8'))
        AuxPump.speed = int((socket_one.recv(1024).decode('utf-8')))
        #print("aux pump speed: ",AuxPump.speed)

        Transfertext = dayofweek
        socket_one.send(Transfertext.encode('utf-8'))
        Waterfalls.enabled = int((socket_one.recv(1024).decode('utf-8')))
        #print("WF enabled: ",Waterfalls.enabled)

        Transfertext = "spare1"
        socket_one.send(Transfertext.encode('utf-8'))
        Waterfalls.speed = int((socket_one.recv(1024).decode('utf-8')))
        #print("waterfalls speed: ",Waterfalls.speed)

        Transfertext = "spare2"
        socket_one.send(Transfertext.encode('utf-8'))
        #print("alpha")
        Servertime = (socket_one.recv(1024).decode('utf-8'))
        #print("Servertime: ",Servertime)

        if Transfer_file == "Timers.csv" or \
           Transfer_file == "Freeze.csv" or \
           Transfer_file == "ManualModes.csv" or \
           Transfer_file == "PumpSpeeds.csv":
            file=open(Transfer_file,"rb")
            print("beginning file send: ",Transfer_file)
            data = file.read()
            socket_one.sendall(data)
            socket_one.send(b"<END>")
            print("finished with file transfer")
            file.close()
            CV.Transferfile = "none"
               
        print("Transfers finished")
        InfoAT.config(text = "The Current Air Temperature is "+str(CV.AirTemp)+chr(176)+"F")
        InfoWT.config(text = "The Current Water Temperature is "+str(CV.WaterTemp)+chr(176)+"F")

        if MainPump.enabled == 0:
            Info5.config(text = "Main Pump is OFFLINE")
        elif MainPump.speed == 0:
            Info5.config(text = "Main Pump is off")
        else:
            Info5.config(text = "Main Pump speed is "+str(MainPump.speed)+" rpm")

        if AuxPump.enabled == 0:
            AuxStatus = "Aux Pump is OFFLINE"
        elif AuxPump.speed == 0:
            AuxStatus = "Aux Pump is off"
        else:
            AuxStatus = "Aux Pump is ON"
            
#        if AuxPump.enabled == 0:
#            Info6.config(text = "Aux Pump is OFFLINE")
#        elif AuxPump.speed == 0:
#            Info6.config(text = "Aux Pump is off")
#        else:
#            Info6.config(text = "Aux Pump is ON")

        if Waterfalls.enabled == 0:
            WaterfallsStatus = "Waterfalls are OFFLINE"
        elif Waterfalls.speed == 0:
            WaterfallsStatus = "Waterfalls are off"
        else:
            WaterfallsStatus = "Waterfalls are ON"
            
#        if Waterfalls.enabled == 0:
#            Info7.config(text = "Waterfalls are OFFLINE")
#        elif Waterfalls.speed == 0:
#            Info7.config(text = "Waterfalls are off")
#        else:
#            Info7.config(text = "Waterfalls are ON")
            
        Info6.config(text = AuxStatus +"     "+ WaterfallsStatus)
        Info8.config(text = "Server Time is: " + Servertime)
        socket_one.close()
        
        time.sleep(1)

    MMwindow.destroy()
    exit()


######################

# Main Menu Functions

def readOnlineFlags(Waterfalls, AuxPump):
    csvFile = open("Online.csv","r")
    a,b = csvFile.readline().strip().split(",")
    a,b = csvFile.readline().strip().split(",")
    Waterfalls.enabled=int(a)
    AuxPump.enabled=int(b)
    csvFile.close()

def writeOnlineFlags(Waterfalls, AuxPump):
    with open("Online.csv","w",newline='') as f:
        cw = csv.writer(f)
        cw.writerow(["Waterfalls", "AuxPump"])
        cw.writerow([str(Waterfalls.enabled), str(AuxPump.enabled)])
    f.close()



###########Variable Declarations############

###########    Main Menu Routine    ############

#####  Establish socket with Server

# Start the second Thread        
_thread.start_new_thread(ExchangeStatuswithServer,())

#####  Read in all the files
readOnlineFlags(Waterfalls, AuxPump)
readManualModesTable(ManualSwim,ManualClean)
readTimerTable(Timer)
readFreezeTable(Freeze)
readPumpSpeedTable(SpeedTable)


MMwindow = Tk()

MMwindow.title("Main Menu")

MMwindow.geometry('500x800')
wc = "light blue"
MMwindow.configure(bg='light blue')

#Title Row
Title0 = Label(MMwindow, text = "",font=("Arial", 10), bg=wc)
Title0.pack()
Title1 = Label(MMwindow, text = "Pi Pico\nCustom Pool Pump Controller",font=("Arial", 16,'bold'), bg=wc)
Title1.pack()
Title2 = Label(MMwindow, text = "Version 1.0",font=("Arial", 10), bg=wc)
Title2.pack()
Title3 = Label(MMwindow, text = "Designed and implemented by David Jeffreys",font=("Arial", 12), bg=wc)
Title3.pack()

def turnMSon():
    if CV.FPL==0:
        ManualSwim.enabled = 1
        MainPump.speed = ManualSwim.speed
        AuxPump.speed = ManualSwim.aux
        Waterfalls.speed = ManualSwim.wfalls
        MSbutton.config(text="Manual Swim is ON", bg = 'green', command=turnMSoff)
        MCbutton.config(state=DISABLED)

def turnMSoff():
    ManualSwim.enabled = 0
    MSbutton.config(text="Manual Swim is OFF", bg='black', command=turnMSon)
    MCbutton.config(state=NORMAL)
        
#Manual Swim Button
MSbutton = Button(MMwindow, width=20, text="Manual Swim is OFF", font = ('Arial',14, 'bold') , bg = 'black', fg='white', borderwidth = 5, command=turnMSon)
MSbutton.pack(pady=15)

def turnMCon():
    if CV.FPL==0:
        ManualClean.enabled = 1
        MainPump.speed = ManualClean.speed
        AuxPump.speed = ManualClean.aux
        Waterfalls.speed = ManualClean.wfalls
        #print("Manual Clean",MainPump.speed, AuxPump.speed, Waterfalls.speed)
        MCbutton.config(text="Manual Clean is ON", bg = 'green', command=turnMCoff)
        MSbutton.config(state=DISABLED)

def turnMCoff():
    ManualClean.enabled = 0
    MCbutton.config(text="Manual Clean is OFF", bg='black', command=turnMCon)
    MSbutton.config(state=NORMAL)

#Manual Clean Button (Manual Clean Off)
MCbutton = Button(MMwindow, width=20, text="Manual Clean is OFF", font = ('Arial',14, 'bold') ,
              bg = 'black', fg='white', borderwidth = 6, command=turnMCon)
MCbutton.pack(pady=0)


#information section
Infospace = Label(MMwindow, text = "",font = ('Arial', 4), bg=wc)
Infospace.pack()
Info0 = Label(MMwindow, text = "",font = ('Arial', 13), bg=wc)
Info0.pack()
InfoAT = Label(MMwindow, text = "Air Temperature is ... ",font = ('Arial', 13), bg=wc)
InfoAT.pack()
InfoWT = Label(MMwindow, text = "Water Temperature is ...",font = ('Arial', 13), fg='black', bg=wc)
InfoWT.pack()
Infospace = Label(MMwindow, text = "",font = ('Arial', 4), bg=wc)
Infospace.pack()
Info1 = Label(MMwindow, text = "Current Timer in Use:",font = ('Arial', 12), bg=wc)
Info1.pack()
Info2 = Label(MMwindow, text = "High Speed",font = ('Arial', 13), bg=wc)
Info2.pack()
Info3 = Label(MMwindow, text = "Terminates at 1700",font = ('Arial', 12), bg=wc)
Info3.pack()

clock()
temperature = 0
FreezeProtect()
TimerLogic()


#Timer Tables Button
TTbutton = Button(MMwindow, width=28, text="Manage Timer Tables", font = ('Arial',12), borderwidth = 7,command=TTbuttonclicked)
TTbutton.pack(pady=15)

#Freeze Protection Button
FPbutton = Button(MMwindow, width=28, text="Manage Freeze Protection Tables", font = ('Arial',12), borderwidth = 7, command=FTbuttonclicked )
FPbutton.pack(pady=0)

#Pump Speeds Button
PSbutton = Button(MMwindow, width=28, text="Manage Pump Speed Tables", font = ('Arial',12), borderwidth = 7, command=PSbuttonclicked )
PSbutton.pack(pady=15)

#Manual Modes Button
MMbutton = Button(MMwindow, width=28, text="Manage Manual Mode Tables", font = ('Arial',12), borderwidth = 7, command=MMbuttonclicked )
MMbutton.pack()

Info5 = Label(MMwindow, text = "Main Pump is ...",font = ('Arial', 11), bg=wc)
Info5.pack()

Info6 = Label(MMwindow, text = "Aux Pump is ...",font = ('Arial', 11), bg=wc)
Info6.pack()

#Info7 = Label(MMwindow, text = "Waterfalls are ...",font = ('Arial', 11), bg=wc)
#Info7.pack()

Info8 = Label(MMwindow, text = "Server Time is:",font = ('Arial', 11), bg=wc)
Info8.pack()

#Close Socket Button
def CloseSocket():
    CV.socket = 0
    CSbutton.config(text="Closing socket and exiting",font = ('Arial',14, 'bold'), bg = 'red', fg='white')
    print("CV.Socket = ",CV.socket)

CSbutton = Button(MMwindow, width=28, text="Close Socket", font = ('Arial',12), borderwidth = 7,command=CloseSocket)
CSbutton.pack()

  
MMwindow.mainloop()
