

"""

Coffee roaster



:created:       Jul-2016

:author:        Michi

:revised:       12-Feb-2017 by Roli



.. todo:: d gain implementation

"""



import sys
import matplotlib
import serial
import time
import io
import Tkinter
from Tkinter import *
import pylab
from pylab import *
import numpy
import scipy as sp
import scipy.signal as signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
matplotlib.use("TkAgg")
import platform

# prevents os x going to sleep mode
if platform.system() == 'Darwin':
    import caffeine

if platform.system() == 'Windows':
    import winsound

style.use('ggplot')

temp_list=[0]

temp_list_filterd=[0]

time_list=[0]

power_list=[0]

temp_record=0

Time=0

t0=0

timer_zeit=30

pgain=0.14

igain=0.00007

dgain=3

I=0

P0=60

P=40

points_mean=15

d_bin=9

reftemp=np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.linspace(80,123,50),np.linspace(123,155,50)]),np.linspace(155,187,50)]),np.linspace(187,199,50)]),np.linspace(199,210,50)]),np.linspace(210,220,50)]),np.linspace(220,229,50)]),np.linspace(229,237,50)]),np.linspace(237,244,50)]),np.linspace(244,250,50)]),np.linspace(250,250,100)]),np.zeros(120)])



#reftemp=np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.hstack([np.linspace(80,123,60),np.linspace(123,155,60)]),np.linspace(155,187,60)]),np.linspace(187,199,60)]),np.linspace(199,210,60)]),np.linspace(210,220,60)]),np.linspace(220,229,60)]),np.linspace(229,237,60)]),np.linspace(237,244,60)]),np.linspace(244,250,60)]),np.linspace(250,250,1)]),np.zeros(120)])

#reftemp=np.hstack([np.hstack([np.hstack([np.hstack([np.linspace(80,180,4*60),np.linspace(180,210,4*60)]),np.linspace(210,230,30)]),np.linspace(230,250,6*60)]),np.zeros(120)])

reftemp2=np.hstack([np.hstack([np.hstack([np.hstack([np.linspace(0,180,3*60),np.linspace(180,210,3*60)]),np.linspace(210,230,30)]),np.linspace(230,250,6*60)]),np.zeros(120)])


def main():

    def send_power_to_arduino(event):

        print('serial write')

        power=str(slider.get())

        if len(power)==1:

            power="0"+str(power)

        print(power)

        ser.write("1"+power)

        time.sleep(0.1)

        print(ser.read(ser.inWaiting()))

    def turn_power_off():

        slider.set(0)

        send_power_to_arduino(1)

    def _quit():

        root.quit()     # stops mainloop

        root.destroy()

    def get_temp():

        ser.write("200")

        time.sleep(0.1)

        return ser.read(ser.inWaiting())

    def update_temp():

        global power_list, temp_list, temp_list_filterd, time_list, t0,  timer_zeit, P, I, pgain, igain, dgain, reftemp

        print("temp updated")

        temp=get_temp()

        label4.config(text="Temperatur:   "+ str(temp)+" C")

        roestzeit=int(time.time()-t0)

        if controlling.get()==1 and temp_record==1:

            print "controlling"

            P=slider.get()

            print "roestzeit = ", roestzeit

            if roestzeit>len(reftemp):

                winsound.Beep(2500,1000)

                P=0

            else:

                Tc=int(reftemp[roestzeit])

                E=Tc-int(temp)

                print "E=  ", E

                I=I+E

                steig=0

                if len(time_list)>25:

                    steig=(temp_list_filterd[-2]-temp_list_filterd[-5])/3.0

                    D=-steig+(reftemp[roestzeit-2]-reftemp[roestzeit-5])/3.0

                else:

                    D=0

                P=P+E*pgain+I*igain+D*dgain

                print "P =  " , P, "; Pgain= ", E*pgain, "; Igain= ", I*igain, "; Dgain= ", D*dgain, " Steigung= ",steig," Ref Steugung = ",(reftemp[roestzeit]-reftemp[roestzeit-d_bin])/d_bin

                if P<=0:

                    P=0

                if P>=100:

                    P=100

            slider.set(P)

            send_power_to_arduino(1)

        if temp_record==1:

            temp_list.append(abs(int(temp)))           #hier abs eingefuegt

            if len(temp_list)>10:

                temp_list_filterd = butterWorthFilter(temp_list)

            else:

                temp_list_filterd = temp_list

            time_list.append(roestzeit)

            power_list.append(slider.get())

            label5.config(text="Roestzeit:   "+ str(roestzeit/60) + " min  "+str(mod(roestzeit,60))+" sec")

            line1[0].set_data(pylab.array(time_list[1:]),pylab.array(temp_list[1:]))

            line1[1].set_data(reftime,reftemp)

            line2[0].set_data(pylab.array(time_list[1:]),pylab.array(power_list[1:]))

            line3[0].set_data(pylab.array(time_list[1:]),pylab.array(temp_list_filterd[1:]))

            line3[0].set_linewidth(3.0)

            line3[0].set_alpha(0.6)

            line3[0].set_color('b')

            if (time.time()-t0)/60.0>timer_zeit:

                stop_temp_record()

                turn_power_off()

        canvas.draw()

        rightFrame.after(900,update_temp)

    def start_temp_record():

        global temp_record, t0

        t0=time.time()

        temp_record=1


    def stop_temp_record():

        global temp_record

        global temp_list

        global time_list

        thefile = open('test.txt', 'w')

        thefile.write("time \n")

        for item in time_list:

            thefile.write("%s\n" % item)

        thefile.write("temp \n")

        for item in temp_list:

            thefile.write("%s\n" % item)

        thefile.write("temp_avg \n")

        # VAR temp_list_filtered not defined

        # for item in temp_list_filterd:
        #
        #     thefile.write("%s\n" % item)

        temp_record=0

        temp_list=[0]

        time_list=[0]

    def timer_eingabe():

        global timer_zeit, dgain, pgain, igain, d_bin

        timer_zeit = float(eingabe_timer.get())

        pgain=float(eingabe_p_gain.get())

        dgain=float(eingabe_d_gain.get())

        igain=float(eingabe_i_gain.get())

        d_bin=int(float(eingabe_d_bin.get()))

        print("Timer auf "+str(timer_zeit)+" min gestellt und gains upgedated.")


    def movingaverage(temp_data, points_mean):

        temp_data = np.asarray(temp_data, dtype=float)

        if len(temp_data)>points_mean:

            temp_data[-1] = numpy.mean(temp_data[-points_mean:len(temp_data)])

            temp_data = np.round(temp_data,2)

        return temp_data.tolist()


    def butterWorthFilter(temp_data):

        # First, design the Buterworth filter

        N  = 2    # Filter order

        Wn = 0.05 # Cutoff frequency

        B, A = signal.butter(N, Wn, output='ba')

        # Second, apply the filter

        temp_data = signal.filtfilt(B,A, temp_data)

        return temp_data


    ###################################################################################################################
    ##################################### START #######################################################################
    ###################################################################################################################

    if platform.system() == 'Darwin':

        for serialNumber in [411,641,14311,14321,14421]:

            try:

                ser = serial.Serial('/dev/tty.usbmodem'+str(serialNumber), 9600)

            except:

                pass


    if platform.system() == 'Windows':

        ser=serial.Serial('COM3',9600)


    print('wait 2 sec')

    time.sleep(2)


    root= Tk()

    controlling=Tkinter.IntVar()

    root.wm_title("Coffe roaster")


    xAchse=pylab.arange(0,1,1)

    yAchse=pylab.array([0]*1)


    fig = pylab.figure(1)

    ax = fig.add_subplot(111)

    ax.grid(True)

    ax.set_title("Roestkurve")

    ax.set_xlabel("Time")

    ax.set_ylabel("Temperature")

    ax.axis([0,(18*60),0,300])


    reftime=pylab.arange(len(reftemp))

    line1=ax.plot(xAchse,yAchse,reftime,reftemp)

    line2=ax.plot(xAchse,yAchse,reftime,reftemp)

    line3=ax.plot(xAchse,yAchse,reftime,reftemp)


    leftFrame=Frame(root)

    leftFrame.pack(side=LEFT)

    rightFrame=Frame(root)

    rightFrame.pack(side=RIGHT)

    ### Temperatur anzeigen
    label4=Label(rightFrame,text="Temperatur:   "+ str(get_temp()) + " C")

    label4.pack()

    label5=Label(rightFrame,text="Roestzeit:   "+ str(0) + " min")

    label5.pack()


    canvas = FigureCanvasTkAgg(fig, rightFrame)

    canvas.show()

    canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)


    toolbar = NavigationToolbar2TkAgg(canvas, rightFrame)

    toolbar.update()

    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)


    c = Checkbutton(leftFrame, text="Temperature controlling", variable=controlling,onvalue=1, offvalue=0)

    c.pack()


    label1=Label(leftFrame,text="Power")

    label1.pack()


    slider = Scale(leftFrame, from_=0, to=99, orient=VERTICAL)

    slider.set(P0)

    slider.bind("<ButtonRelease-1>", send_power_to_arduino)

    slider.pack()

    send_power_to_arduino(1)


    button_off=Tkinter.Button(leftFrame,text="Off",command=turn_power_off)

    button_off.pack()

    button_start=Tkinter.Button(leftFrame,text="Start",command=start_temp_record)

    button_start.pack()

    button_stop=Tkinter.Button(leftFrame,text="Stop",command=stop_temp_record)

    button_stop.pack()

    label6=Tkinter.Label(leftFrame,text="Timer in min (integer)")

    label6.pack()

    entryText10 = Tkinter.StringVar()

    eingabe_timer=Tkinter.Entry(leftFrame,textvariable=entryText10)

    entryText10.set("30")

    eingabe_timer.pack()

    label7=Tkinter.Label(leftFrame,text="P Gain")

    label7.pack()

    entryText1 = Tkinter.StringVar()

    eingabe_p_gain=Tkinter.Entry(leftFrame,textvariable=entryText1)

    entryText1.set(str(pgain))

    eingabe_p_gain.pack()

    label8=Tkinter.Label(leftFrame,text="D Gain")

    label8.pack()

    entryText2 = Tkinter.StringVar()

    eingabe_d_gain=Tkinter.Entry(leftFrame,textvariable=entryText2)

    entryText2.set(str(dgain))

    eingabe_d_gain.pack()

    label9=Tkinter.Label(leftFrame,text="I Gain")

    label9.pack()

    entryText3 = Tkinter.StringVar()

    eingabe_i_gain=Tkinter.Entry(leftFrame,textvariable=entryText3)

    entryText3.set(str(igain))

    eingabe_i_gain.pack()

    label10=Tkinter.Label(leftFrame,text="d_bin")

    label10.pack()

    entryText4 = Tkinter.StringVar()

    eingabe_d_bin=Tkinter.Entry(leftFrame,textvariable=entryText4)

    entryText4.set(str(d_bin))

    eingabe_d_bin.pack()

    button_timer_ok=Tkinter.Button(leftFrame,text="OK",command=timer_eingabe)

    button_timer_ok.pack()


    root.protocol("WM_DELETE_WINDOW", _quit)  #thanks aurelienvlg

    root.after(1000,update_temp)

    root.mainloop()

    ser.close()

    # releases any power assertion (os x can go sleep again)
    if platform.system() == 'Darwin':
        caffeine.off()

if __name__ == "__main__":

    main()
