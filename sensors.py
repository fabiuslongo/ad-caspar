from phidias.Types import *
import threading
import time

class TIMEOUT(Reactor): pass


class HotwordDetect(Sensor):

    def on_start(self):
       self.running = True
       print("\nStarting Hotword detection...")
       # put instantiation hotword code here

    def on_stop(self):
        print("\nStopping Hotword detection...")
        self.running = False

    def sense(self):
        while self.running is True:
           time.sleep(1)
           # --------------> put hotword detection code here <---------------
           # when right hotword is detected: self.assert_belief(HOTWORD_DETECTED("ON"))


class UtteranceDetect(Sensor):

    def on_start(self):
       self.running = True
       print("\nStarting utterance detection...")
       # instantiate hotword engine here

    def on_stop(self):
        print("\nStopping utterance detection...")
        self.running = False

    def sense(self):
        while self.running:
           time.sleep(1)
           # --------------> put utterance detection code here <---------------
           # when incoming new utterance detected: self.assert_belief(SST(utterance))


class Timer(Sensor):

    def on_start(self, uTimeout):
        evt = threading.Event()
        self.event = evt
        self.timeout = uTimeout()
        self.do_restart = False

    def on_restart(self, uTimeout):
        self.do_restart = True
        self.event.set()

    def on_stop(self):
        self.do_restart = False
        self.event.set()

    def sense(self):
        while True:
            self.event.wait(self.timeout)
            self.event.clear()
            if self.do_restart:
                self.do_restart = False
                continue
            if self.stopped:
                return
            else:
                self.assert_belief(TIMEOUT("ON"))
                return



"""
BOT = None

class Chatbot(Sensor):

    def on_start(self):
        global BOT
        BOT = telegram.Bot("761251160:AAFI63ErogZxLFeS8X8ur6O1TxFjCjv1530")
        self.update_id = None
        self.msgs = [ ]

    def sense(self):
        global BOT
        while True:
            if self.msgs == []:
                for m in BOT.get_updates(offset=self.update_id): #, timeout=10):
                    if self.update_id is None:
                        self.update_id = m.update_id
                    self.update_id = self.update_id + 1
                    if m.message:
                        self.msgs.append(m)
            if self.msgs == []:
                continue
            m = self.msgs[0]
            del self.msgs[0]
            print(m.message.text)
            if m.message.text is None:
                continue

            message_data = m.message.text.lower().split()
            message_data.insert(0, m.message.chat.id)
            print(message_data)

            self.assert_belief(message(m.message.chat.id, m.message.text))


class Reply(Action):

    def execute(self, *args):
        m = []
        sender = args[0]()
        for v in args[1:]:
            m.append(v())
        message = " ".join(m)
        BOT.sendMessage(sender, message)
"""