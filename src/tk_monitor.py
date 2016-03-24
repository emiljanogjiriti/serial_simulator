'''
Author:    max@embeddedprofessional.com
'''
from __future__ import print_function
from __future__ import unicode_literals
from Tkinter import *
import tkFont
from threading import Thread
import time

class Application(Frame):
    def __init__(self, master=None, screen_size=(1080, 720)):
        Frame.__init__(self, master)
        self.is_alive = True
        self.screen_w = screen_size[0]
        self.screen_h = screen_size[1]
        self.displayed_struct = None
        self.pack()
        self.createWidgets()

    def delete_stuff(self):
        self.w.delete(ALL)

    def draw_periodic(self):
        font = tkFont.Font(family='Helvetica',size=16, name="font16s")
        while self.is_alive:
            #monitor.sample_stream_once()
            if self.displayed_struct:
                self.w.delete(ALL)
                for float_var in ['adsBody[8]', 'ltcBody[17]', 'tivaBody[12]', 'alarm[8]']:
                    try:
                        samples = self.displayed_struct
                        for i, sample in enumerate(samples):
                            bar_height = -sample / 5 * self.screen_h / 2
                            bar_width = self.screen_w / len(samples)
                            self.w.create_rectangle(i * bar_width, self.screen_h / 2, i * bar_width + bar_width, bar_height + self.screen_h / 2, fill='#ff0')
                            self.w.create_text(i * bar_width + bar_width / 2, self.screen_h / 2, text='%5.3f' % sample, justify='center', fill='black', font=font)
                        break
                    except KeyError, e:
                        pass
                self.w.create_text(500, 200, text=self.displayed_struct.__repr__(), font=font, anchor='e')
                self.w.update()
            time.sleep(0.01)

    def quit(self):
        self.is_alive = False
        Frame.quit(self)

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT['text'] = 'QUIT'
        self.QUIT['fg']   = 'red'
        self.QUIT['command'] =  self.quit

        self.QUIT.pack({'side': 'left'})

        self.id_buttons = []
        i = 0
        for c_struct in ['abc', 'def']:#monitor.name_dict.values():
            id_button = Button(self)
            id_button['text'] = 'barf'#c_struct.name
            id_button.pack({'side':'left'})
            #id_button['command'] = lambda x=c_struct.name: self.set_displayed(x)
            i += 1
            self.id_buttons.append(id_button)

        self.w = Canvas(self.master, width=self.screen_w, height=self.screen_h)
        self.w.pack()

    def set_displayed(self, c_struct):
        self.displayed_struct = c_struct

    def mainloop(self):
        go = Thread(target=self.draw_periodic)
        go.start()
        Frame.mainloop(self)
        go.join()

if __name__ == '__main__':
    root = Tk()
    app = Application(master=root, screen_size=(1080, 720))
    app.master.minsize(500, 500)
    app.mainloop()
    root.destroy()

