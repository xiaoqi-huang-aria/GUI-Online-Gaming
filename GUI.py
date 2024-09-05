#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import string
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter.messagebox import *
from chat_utils import *
import json
import pickle
from tictactoe import *

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""
        self.read_users()
    
    def read_users(self):
        try:
            f = open("users.txt", "rb")
            self.user_dict = pickle.load(f)
            f.close()
        except:
            self.user_dict = {}

    def update_users(self):
        f = open("users.txt", "wb")
        pickle.dump(self.user_dict, f)
        f.close()

    def quit_system(self):
        self.state = S_OFFLINE
        self.login.destroy()

    def register(self):
        # register
        self.register = Toplevel()
        
        self.register.title("Register")
        self.register.resizable(width=False, 
                                height=False)
        self.register.configure(width=400, 
                                height=300)
        # new user register
        self.Labelregister = Label(self.register, 
                         text="New user? Please register here", 
                         justify=CENTER, 
                         font="Helvetica 14 bold")
        
        self.Labelregister.place(relheight=0.15, 
                       relx=0.2, 
                       rely=0.02)
        
        self.Labelpwdtips = Label(self.register,
                                  text="NOTE: Password should be at least 8 characters",
                                  justify=CENTER,
                                  font="Helvetica 12 bold")

        self.Labelpwdtips.place(relheight=0.04,
                                relx=0.02,
                                rely=0.14)
        
        self.LabelrName = Label(self.register, 
                                text="Username: ", 
                                font="Helvetica 12")
        
        self.LabelrName.place(relheight=0.2, 
                              relx=0.1, 
                              rely=0.2)
        
        self.EntryrName = Entry(self.register, 
                                font="Helvetica 14")
        
        self.EntryrName.place(relwidth=0.4, 
                              relheight=0.12, 
                              relx=0.35, 
                              rely=0.2)
        
        # set the password
        self.LabelrPass1 = Label(self.register, 
                                text="Password: ", 
                                font="Helvetica 12")
        
        self.LabelrPass1.place(relheight=0.2, 
                              relx=0.1, 
                              rely=0.35)
        
        self.EntryrPass1 = Entry(self.register, 
                                font="Helvetica 14", 
                                show="*")
        
        self.EntryrPass1.place(relwidth=0.4, 
                              relheight=0.12, 
                              relx=0.35, 
                              rely=0.35)
        
        # confirm the password
        self.LabelrPass2 = Label(self.register, 
                                 text="Confirm Password: ", 
                                 font="Helvetica 8")
        
        self.LabelrPass2.place(relheight=0.2, 
                               relx=0.1, 
                               rely=0.5)
        
        self.EntryrPass2 = Entry(self.register, 
                                 font="Helvetica 14", 
                                 show="*")
        
        self.EntryrPass2.place(relwidth=0.4, 
                               relheight=0.12, 
                               relx=0.35, 
                               rely=0.5)
        
        # set the focus of the curser
        self.EntryrName.focus()

        # save
        self.confirm = Button(self.register,
                              text="Confirm",
                              font="Helvetica 14 bold",
                              command=lambda: self.reg_new_user(self.EntryrName.get(),
                                                                self.EntryrPass1.get(),
                                                                self.EntryrPass2.get()))

        self.confirm.place(relx=0.2,
                           rely=0.8)
        
        self.cancel = Button(self.register,
                             text="Cancel",
                             font="Helvetica 14 bold",
                             command=self.register.destroy)
        
        self.cancel.place(relx=0.6,
                          rely=0.8)
        
    def reg_new_user(self, user, p1, p2):
        if self.format_check(p1, p2):
            if user not in self.user_dict.keys():
                self.user_dict[user] = p1
                showinfo(message="User register success")
                self.register.destroy()
    
    def format_check(self, p1, p2):
        if p1 != p2:
            showinfo(message="Two input password not the same, check it")
            return False
        elif len(p1) < 8:
            showinfo(message="Password should at least include 8 characters")
            return False
        for i in p1:
            if not (i.isdigit() or i.isalpha() or i in string.punctuation):
                showinfo(message=f"Password should only include digits, alphabet and" \
                                 f" these include special characters:\n{string.punctuation}")
                return False

        return True

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")
          
        self.pls.place(relheight = 0.15,
                       relx = 0.2, 
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 12")
          
        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.2)
          
        # create a entry box for 
        # tyoing the message
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14")
          
        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
        
        # set the focus of the curser
        self.entryName.focus()

        # enter the password
        self.labelPass = Label(self.login, 
                               text="Password: ", 
                               font="Helvetica 12")
        
        self.labelPass.place(relheight=0.2, 
                             relx=0.1, 
                             rely=0.35)
        
        self.entryPass = Entry(self.login, 
                               font="Helvetica 14", 
                               show="*")
        
        self.entryPass.place(relwidth=0.4, 
                             relheight=0.12, 
                             relx=0.35, 
                             rely=0.35)

        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.goAhead(self.entryName.get(), self.entryPass.get()))
          
        self.go.place(relx = 0.1,
                      rely = 0.62)
        
        self.register = Button(self.login, 
                               text="Register", 
                               font="Helvetica 14 bold", 
                               command = self.register)
        self.register.place(relx = 0.4,
                            rely = 0.62)
        
        self.quitsystem = Button(self.login,
                                 text="Quit",
                                 font="Helvetica 14 bold",
                                 command=self.quit_system)
        self.quitsystem.place(relx=0.7,
                              rely=0.62)
        
        self.Window.mainloop()
  
    def goAhead(self, name, pwd):
        self.update_users()
        if len(name) > 0 and self.user_dict.get(name) == pwd:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
        else:
            if name in self.user_dict.keys():
                showinfo(message="Wrong Password")
            else:
                showinfo(message='User not exist')
    
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#C8F7C8")
        self.labelHead = Label(self.Window,
                             bg = "#C8F7C8", 
                              fg = "#1A1B1C",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#85A185")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#C8F7C8",
                             fg = "#1A1B1C",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#85A185",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#F4FDF4",
                              fg = "#1A1B1C",
                              font = "Helvetica 13")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)
          
        self.textCons.config(cursor = "arrow")

        # create a time button
        self.buttontime = Button(self.Window,
                                 text="Time",
                                 font="Helvetica 10 bold",
                                 width=20,
                                 bg="#ABB2B9",
                                 command=lambda: self.useButton("time"))

        self.buttontime.place(relx=0.005,
                              rely=0.94,
                              relheight=0.06,
                              relwidth=0.33)
        
        # create a game button
        self.buttongame = Button(self.Window,
                                 text="Game",
                                 font="Helvetica 10 bold",
                                 width=20,
                                 bg="#ABB2B9",
                                 command=lambda: self.useButton("game"))

        self.buttongame.place(relx=0.335,
                              rely=0.94,
                              relheight=0.06,
                              relwidth=0.33)
        
        # create a who button
        self.buttonwho = Button(self.Window,
                                text="Who",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.useButton("who"))

        self.buttonwho.place(relx=0.665,
                             rely=0.94,
                             relheight=0.06,
                             relwidth=0.33)
        
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
  
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        # self.textCons.config(state=DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
        self.textCons.config(state=NORMAL)
        # self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    
    # work with time and who button
    def useButton(self, msg):
        self.my_msg = "button_only" + string.punctuation + msg
    
    # play game
    def showGame(self,your_turn = False):
        game = TicTacToe(self.send, self.recv)
        game.your_turn= your_turn
        game.start_game()
        while not game.game_is_over():  
            pass
        winner = 'X' 
        result_screen = ResultScreen(winner)
        result_screen.run()

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                if self.system_msg.startswith("Server:") and "game" in self.system_msg:
                    if self.system_msg.startswith("Server: You are playing game with"):
                        self.showGame(your_turn=True)
                    else:
                        self.showGame(your_turn=False)


    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()