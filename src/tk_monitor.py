'''
Author:    max@embeddedprofessional.com
'''
from __future__ import print_function, unicode_literals, division
if 'raw_input' not in dir(__builtins__): raw_input = input
from Tkinter import *
import tkFont
import ttk
from threading import Thread
import time
import logging
from opbots import *

class Application(Frame):
    def __init__(self,master=None,screen_size=(1080, 720)):
        Frame.__init__(self, master)
        self.screen_w = screen_size[0]
        self.screen_h = screen_size[1]
        self.displayed_struct = None
        self.pack()
        self.createWidgets()

    def delete_stuff(self):
        self.w.delete(ALL)

    def draw_periodic(self):
        #font = tkFont.Font(family='Helvetica',size=16, name="font16s")
        self.canvas.after(50, self.draw_periodic)

    def quit(self):
        Frame.quit(self)

    def list_serial_ports(self,*args):
        ser = SerialManager()
        self.ser_info['text'] = 'Serial ports available:\n'
        for port in ser.find_ports():
            self.ser_info['text'] += str(port)

    def createWidgets(self):
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)

        self.frame_left = Frame(self,bd=1,relief=SUNKEN)
        self.frame_left.grid(column=0,row=0,sticky=NW)
        self.frame_left.grid_columnconfigure(0,weight=1,minsize=500)
        #self.frame_left.grid_propagate(0)

        self.frame_right = Frame(self,bd=1,relief=SUNKEN)
        self.frame_right.grid(column=1,row=0,sticky=NE)
        self.frame_right.grid_columnconfigure(0,weight=1,minsize=500)

        self.QUIT = Button(self.frame_left)
        self.QUIT['text'] = 'QUIT'
        self.QUIT['fg']   = 'red'
        self.QUIT['command'] =  self.quit
        self.QUIT.grid(column=0,row=0)

        self.out = ttk.Label(self.frame_left,text='Output')
        self.out.grid(column=0,row=2,sticky=W)

        photo = PhotoImage(file='../img/test_marker.gif')
        w = Label(self.frame_left,image=photo)
        w.photo = photo
        w.grid(column=0,row=3,sticky=S)

        photo = PhotoImage(file='../img/test_marker.gif')
        w = Label(self.frame_right,image=photo)
        w.photo = photo
        w.grid(column=0,row=3,sticky=S)

        self.console = Text(self.frame_left,height=1,width=50)
        self.console.grid(column=0,row=1,sticky=W)
        self.console.bind('<Return>',self.t)

        self.ser_info = ttk.Label(self.frame_right,text='Output')
        self.ser_info.grid(column=0,row=2,sticky=W)
        self.ser_info['text'] = 'Serial data here'
        
        self.list_button = Button(self.frame_right)
        self.list_button['text'] = 'List serial ports'
        self.list_button['command'] = self.list_serial_ports
        self.list_button.grid(column=0,row=0)
        '''
        self.serial_console = ttk.Label(self.frame_left,text='Oh shitt',width=20)
        self.serial_console.grid(column=0,row=2,sticky=W)
        self.serial_console['text'] = 'Serial stuff'
        self.serial_console.configure(background='#4D4D4D')

        self.text = Text(self,height=1)
        self.text.grid(column=0,row=1,columnspan=2)
        self.text.bind("<Return>",self.t)
        '''
        self.canvas = Canvas(self.master,width=self.screen_w,height=self.screen_h)
        #self.canvas.pack()

    def t(self,*args):
        self.out['text'] = self.console.get('1.0',END)
        #input = self.myText_Box.get("1.0",'end-1c')

    def set_displayed(self, c_struct):
        self.displayed_struct = c_struct

    def mainloop(self):
        go = Thread(target=self.draw_periodic)
        go.start()
        Frame.mainloop(self)
        go.join()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    mainlog = logging.getLogger('main')
    root = Tk()
    app = Application(master=root,screen_size=(1080,720))
    #app.master.minsize(500,500)
    app.mainloop()
    root.destroy()

