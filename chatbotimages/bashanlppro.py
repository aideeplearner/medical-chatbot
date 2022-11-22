import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
import cv2
import re 
import json 
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from nltk.tokenize import word_tokenize
import os
import pyttsx3
import requests
import json
import re
from sklearn.preprocessing  import LabelEncoder   
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pygame
from pygame import mixer
import random
import sys

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "newproject"


class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        def reply():
            ps=WordNetLemmatizer()
            tfidf=joblib.load("tfidf")
            lb=joblib.load("encode")
            model=joblib.load("bayes")
            responses=joblib.load("responses")
            question=self.chatentry.get()
            if question=="p":
                  mixer.music.pause()
                  self.chatentry.delete(0,tk.END)
                  self.chatten.insert(tk.END,"you : "+question+"\n\n")
                  return
            self.chatten.insert(tk.END,"you : "+question+"\n\n")
            self.chatentry.delete(0,tk.END)
            question2=question.lower()
            question1=re.sub('[^a-zA-Z]',' ',question2)
            split1=question1.split()
            port=[ps.lemmatize(i) for i in split1]
            port=" ".join(port)
            x=tfidf.transform([port])
            x_dense=x.todense()
            p=model.predict(x_dense)
            pred2=model.predict_proba(x_dense)[0]
            des=max(pred2)
            pred=lb.inverse_transform(p)
            if pred=="laugh":
               print("medbot  : ha ha \U0001F923\U0001F923\U0001F923\U0001F923")
            elif pred=="song":
               mixer.init()
               folder="C:\\Users\\thota\\Videos\\songs"
               apps=[]
               for i in os.listdir(folder):
                  apps.append(i)      
            x=random.choice(responses[pred[0]])
            if des<0.3:
                self.chatten.insert(tk.END,"medbot : i dont understand your problem please consult your doctor")
        
            if des>0.3:
                self.chatten.insert(tk.END,"medbot : "+x+"\n\n")
            if pred=="song":
                n1=random.choice(apps)    
                mixer.music.load(folder+"\\"+n1)
                mixer.music.play()
                self.chatten.insert(tk.END,"medbot : "+"please enter letter p to stop song"+"\n\n")        
        def clear():
            self.chatten.delete('1.0',tk.END)
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.bot = tk.Label(self.toplevel1)
        self.img_chat = tk.PhotoImage(file='chat.png')
        self.bot.configure(compound='center', font='TkSmallCaptionFont', image=self.img_chat)
        self.bot.place(anchor='nw', relheight='0.3', relwidth='0.36', rely='0.0', x='0', y='0')
        self.label3 = tk.Label(self.toplevel1)
        self.label3.configure(anchor='w', background='#61eefa', font='{8514oem} 24 {}', foreground='#e1031e')
        self.label3.configure(text='   MEDICAL CHATBOT')
        self.label3.place(anchor='nw', relheight='0.3', relwidth='1.0', relx='0.36', x='0', y='0')
        self.basha = tk.Frame(self.toplevel1)
        self.chatten = tk.Text(self.basha)
        self.chatten.configure(background='#fc6184', height='10', width='50',font='{8514oem} 10 {}')
        self.chatten.place(anchor='nw', relheight='0.62', relwidth='1.0', x='0', y='0')
        self.scrollbar3 = tk.Scrollbar(self.basha)
        self.scrollbar3.configure(orient='vertical')
        self.scrollbar3.config(command=self.chatten.yview)
        self.scrollbar3.place(anchor='nw', relx='0.975', rely='0.25', x='0', y='0')
        self.chatten.configure(yscrollcommand=self.scrollbar3.set)
        self.chatentry = tk.Entry(self.basha)
        self.chatentry.configure(background='#fef9b4', font='{8514oem} 10 {}')
        self.chatentry.place(anchor='nw', relheight='0.08', relwidth='0.73', rely='0.623', x='0', y='0')
        self.send = tk.Button(self.basha)
        self.img_send = tk.PhotoImage(file='send.png')
        self.send.configure(background='#ffffff', image=self.img_send,command=reply)
        self.send.place(anchor='nw', relheight='0.08', relwidth='0.14', relx='0.90', rely='0.62', x='0', y='0')
        self.clear = tk.Button(self.basha)
        self.img_clear1 = tk.PhotoImage(file='clear1.png')
        self.clear.configure(background='#ffffff', image=self.img_clear1,command=clear)
        self.clear.place(anchor='nw', relheight='0.08', relwidth='0.19', relx='0.72', rely='0.62', x='0', y='0')
        self.basha.configure(background='#5601e2', height='200', width='200')
        self.basha.place(anchor='nw', relheight='1.0', relwidth='1.0', rely='0.304', x='0', y='0')
        self.toplevel1.configure(height='200', width='200')
        self.toplevel1.geometry('640x480')
        # Main widget
        self.mainwindow = self.toplevel1
    def run(self):
        self.mainwindow.mainloop()
    def scrollbar3(self, first, last):
        pass

if __name__ == '__main__':
    app = NewprojectApp()
    app.run()

