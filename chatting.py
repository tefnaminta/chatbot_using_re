import datetime
import random
import re
from chatterbot import ChatBot
chatbot = ChatBot("tefna")
from chatterbot.trainers import ListTrainer
import pyttsx3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager,Screen
import speech_recognition as sr
import pymysql
connection = pymysql.connect(host='localhost',user='root',db='chatbot')
cursor = connection.cursor()
Builder.load_file('chaterkivy.kv')
class chatter(Screen):
    ques = ObjectProperty()
    ans = ObjectProperty()
    engine = pyttsx3.init()
    engine.say(str("its me hana"))
    engine.runAndWait()
    def textchat(self,ques):
        time = str(datetime.datetime.time(datetime.datetime.now()))
        now = int(time[0] + time[1])
        if (now >= 0 and now < 12):
            time_greeting = "Good Morning!"
        elif (now >= 12 and now < 16):
            time_greeting = "Good Afternoon!"
        elif (now >= 16):
            time_greeting = "Good Evening!"
        a = "select user_response,bot_response,conversation_mode from conversation"
        cursor.execute(a)
        user = ques
        ai = cursor.fetchall()
        for i in ai:
            if(user==i[0] and i[2]=="greetings"):
                response = str(i[1]+" "+time_greeting)
                break
            elif (user == i[0]):
                response = str(i[1])
                break
        else:
            responses = {
                "question": {
                    "what's today's weather?":
                        ["cloudy", "sunny"],
                    "what is your name?":
                        ["am a robot,what is your name?", "hana..Your sweet name please?"],
                    "how are you?": ["great,what about you?", "fine,what about you?", "am good,what about you?",
                                     "am okay,what about you?", "i feel good,what about you?"],
                    "what?": ["don't you understand.", "do you feel something wrong"],
                    "what you want?": ["let's talk", "i like to talk with you"]
                },
                "statement": {
                    "I love building chatbots":
                        ["I too love you", "I love humans"],
                    "hello": ["hi", "hello", "hii", "oi", "hi there!"],
                    "good": ["that's nice", "nice to here that", "oh that's good"],
                    "bye": ["see you later", "bye", "bye-bye", "okay nice to meet you"],
                    "thank you": ["welcome", "no mension"],
                    "yes": ["okay,then", "okay"],
                    "no": ["why?", "okay.i don't mind it"],
                    "okay": ["okay", "yes.fine"],
                    "then": ["then,what?", "then.tell something"]
                },
                "rules": {"do you remember(.*)": ["yes.. i remember", "sorry.. am not remember"],
                          "do you think(.*)": ["yes i think", "nope. i don't think"],
                          "do you[^remember](.*)": ["yes.i", "no.am not"],
                          "are you(.*)": ["yes.i am", 'no.am not'],
                          "can you(.*)": ['yes.i can', "no.i can't"],
                          "could you please(.*)": ['yes.i will', 'no.i will not'],
                          "should i(.*)": ['yes.you should', 'no.you should not'],
                          "am(.*)": ["glad to meet you", "nice to meet you"],
                          "my name is(.*)": ["glad to meet you", "nice to meet you"]}
            }
            if ques.endswith("?"):
                # Return a random question
                response = random.choice(responses["question"][ques])
                # Return a random statement
            else:
                try:
                    response= random.choice(responses["statement"][ques])
                except:
                    try:
                        for pattern,response in responses['rules'].items():
                            match = re.match(pattern, ques)
                            if match is not None:
                                response1 = random.choice(response)
                        response = response1
                    except:
                        response = ques + "? what is that?"
        if (response != "Bye-Bye"):
            self.ques.text = str(response)
            self.ans.text = ""
            engine = pyttsx3.init()
            engine.say(response)
            engine.runAndWait()
        elif (response == "Bye-Bye"):
            self.manager.current = "bye"
            engine = pyttsx3.init()
            engine.say(response)
            engine.runAndWait()
    def exit(self):
        engine = pyttsx3.init()
        engine.say("Bye-Bye")
        engine.runAndWait()
        self.manager.cureent = "bye"
class bye(Screen):
    pass
class DemoApp(App):
    def build(self):
        s = ScreenManager()
        s.add_widget(chatter(name="chat"))
        s.add_widget(bye(name="bye"))
        return s
if __name__ == '__main__':
    DemoApp().run()

