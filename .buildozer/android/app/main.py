#!/usr/bin/env python3

import random
import json, glob
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from pathlib import Path
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        with open('users.json') as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
            self.manager.transition.direction = 'left'
        else:
            self.ids.login_wrong.text = "Wrong username or password"


class SignUpScreen(Screen):
    def add_user(self, uname, pword, retypePword):
        with open("users.json") as file:
            users = json.load(file)
   
 
        if uname in users.keys():
            self.ids.mismatch.text = "Username already taken"

        elif pword != retypePword:
            self.ids.mismatch.text = "Password do not match"

        else:
            users[uname] = {
                    'username': uname, 
                    'password': pword,
                    'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                }
            with open("users.json", 'w') as file:
                json.dump(users, file)

            self.manager.current = "sign_up_screen_success"

    def login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
        

class SignUpScreenSuccess(Screen):
    def login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower().strip()
        availabe_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in availabe_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(ButtonBehavior, HoverBehavior, Image,):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
