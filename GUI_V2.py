# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:21:44 2021

@author: jko
"""
import tkinter as tk
from PIL import Image, ImageTk
from datetime import date
import os
import WeatherScraper_V3

data = WeatherScraper_V3.forecast()
forecast = data[0]
city = data[1]['city']
state = data[1]['state']

pic_files = [f for f in os.listdir('images') if os.path.isfile(os.path.join('images',f))]
cond_names = [f['shortForecast'] for f in forecast]

x = 650
y = 500

# Retrieves image path. Make sure image folder in same directory as Weather_GUI
def imgPath(filename):
    return os.path.join('images', filename)
def pic(cond):
    for file in pic_files:
        if cond in file:
            img = file
            break
        else:
            img = None
    return img
    
class MainApp(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill = 'both', expand = 1)
        font = 'Arial'
        
        # Top 
        cs_sz = 30
        day_sz = 20
        cond_sz = 20
        relx=0.5
        
        city_state = tk.Label(self, text = city + ' ' + state, bg = "white")
        city_state.place(relx=relx, anchor='n')
        city_state.config(font = (font, cs_sz))
        
        day = tk.Label(self, text = date.today().strftime("%B %d, %Y"),
                        bg = "white", fg = "gray")
        day.place(relx=relx,y=cs_sz+day_sz,anchor='n')
        day.config(font = (font,day_sz))
        
        cond = tk.Label(self,text = forecast[0]['shortForecast'],bg = "white", fg = "gray")
        cond.place(relx=relx,y=cs_sz+3*cond_sz, anchor='n')
        cond.config(font = (font, cond_sz))
        
        # Center 
        t_sz = 40
        deg_sz = 15
        relx = .55
        rely=.4
        
        temp = tk.Label(self, text = forecast[0]['temperature'], bg = "white")
        temp.place(relx=relx,rely=rely,anchor='center')
        temp.config(font = (font, t_sz))
        
        deg = tk.Label(self, text = u'\N{DEGREE SIGN}'+forecast[0]['temperatureUnit'], bg = 'white')
        deg.place(relx=relx,x=deg_sz*2,rely=rely,y=-(t_sz-deg_sz))
        deg.config(font = (font, deg_sz))  
        
        cond = cond_names[0]
        cond = cond.split(' ')
        for str_ in cond:
            img_name = pic(str_.lower())
            if img_name != None:
                break
        try:
            load = Image.open(imgPath(img_name))
            load = load.resize((60, 60), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(load)
            img = tk.Label(self, image = render, bg = 'white')
            img.image = render
            img.place(relx = (relx - 0.13), rely = rely, anchor='center')
        except:
            print('Something is wrong')
        details = forecast[0]['detailedForecast']
        details = details.split('.')
        rely = 0.55
        for str_ in details[1:]:
            det = tk.Label(self, text=str_,bg='white',fg = "gray")
            det.place(relx=0.5,rely=rely, anchor = 'center')
            det.config(font=(font,15))
            rely+=0.1
            
        # Bottom
        relx=0.5
        days = []
        icons = []
        for i,d in zip(forecast[1:],cond_names[1:]):
            day = i['name']
            if len(day) <= len('saturday'): # excludes names like Friday night etc.
                days.append(day)
                cond = d.lower().split(' ')
                for con in cond:
                    img_name = pic(con)
                    if img_name != None:
                        icons.append(img_name)
                        break
        days = tk.Label(self,text=days,bg = "white")
        days.place(relx=relx,rely=0.8,anchor='s')
        days.config(font=(font,15))

        # Icons
        relx = 0.2  
        try:
            paths=[]
            for i in icons:
                paths.append(imgPath(i))
            for path in paths:
                load = Image.open(path)
                load = load.resize((40, 40), Image.ANTIALIAS)
                render = ImageTk.PhotoImage(load)
                img = tk.Label(self, image = render, bg = 'white')
                img.image = render
                img.place(relx = relx, rely = 0.92, anchor='s')
                relx+=0.12
        except:
            print('Something is wrong')      
    
if __name__ == '__main__':  
    root = tk.Tk()
    root.geometry(str(x)+'x'+str(y))
    app = MainApp(root)
    app.configure(bg='white')
    root.mainloop()