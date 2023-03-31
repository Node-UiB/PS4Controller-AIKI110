#!/usr/bin/env python
from evdev import InputDevice, ecodes
from time import sleep
from gpiozero import Motor

class Controller():
    def __init__(self):
        
        # Henter verdier fra device

        self.dev = InputDevice('/dev/input/event4')

        # Verdi for hvor mye fart hver motor har

        self.left = 0
        self.right = 0

        # Variabel for høyre og venstre motor.
        # Tallverdien står for hvilke pins i GPIO som gjør hva

        self.left_motor = Motor(forward=(13), backward=(19))
        self.right_motor = Motor(forward=(6), backward=(5))

    def get_values_x(self):
        
        # Får verdi fra device i X retning

        x = self.dev.absinfo(ecodes.ABS_X)
        return x[0]

    def get_values_y(self):
        
        # Får verdi fra device i Y retning

        y = self.dev.absinfo(ecodes.ABS_Y)
        return y[0]
    
    def update_motor(self):
        
        # Henter verdier fra device med funksjonen
        #
        # Device returnerer verdi mellom 0-255
        # Y-opp er 0, Y-ned er 255
        # X-venstre er 0, X-høyre er 255
        # Regnestykket justerer verdien slik at den blir mellom -1 og 1

        x = (self.get_values_x() - 127.5) / 127.5
        y = (self.get_values_y() - 127.5) / 127.5

        # Terskel for når Joystick skal gripe inn i aksjon
        # Senere i koden benyttes den for å definere i området -treshold og treshold = 0
        
        treshold = 0.08

        # Joystick i Y retning
        # Skriver til variablene left og right
        # Variablene brukes til å sette hastighet på hver enkelt motor, både frem og tilbake

        if y < -abs(treshold):
            self.left = abs(y)
            self.right = abs(y)
        elif y > treshold:
            self.left = -abs(y)
            self.right = -abs(y)
        else:
            self.left = 0
            self.right = 0

        # Joystick i X retning
        # Justerer venstre og høyre verdi med 1/3 av seg selv.
        # Funksjonen bremser hjulet den veien man skal svinge

        if x < -abs(treshold):
            self.left -= abs(x)/3

        elif x > treshold:

            self.right -= x/3
        else:
            pass

        # Ny implementasjon
        # Hvis y retning er mellom treshold (altså 0) og x retning er til siden, snur den hjulene i hver sin retning

        if y < treshold and y > -abs(treshold) and x < -abs(treshold):
            self.left = x
            self.right = abs(x)

        elif y < treshold and y > -abs(treshold) and x > treshold:
            self.left = -abs(x)
            self.right = x
        else:
            pass


    def drive_motor(self):

        # Hovedfunksjon for å kjøre motor
        # Kaller på venstre og høyre motor

        self.update_motor()
        self.drive_motor_left()
        self.drive_motor_right()

    def drive_motor_left(self):

        # Kjøring av venstre motor
        # Setter hastighet ut i fra variabelen left

        if self.left > 0:
            self.left_motor.forward(speed=abs(round(self.left, 2)))
        elif self.left < 0:
            self.left_motor.backward(speed=abs(round(self.left)))
        else:
            self.left_motor.forward(speed=0)

    def drive_motor_right(self):

        # Kjøring av høyre motor
        # Setter hastighet ut i fra variabelen right

        if self.right > 0:
            self.right_motor.forward(speed=abs(round(self.right,2)))
        elif self.right < 0:
            self.right_motor.backward(speed=abs(round(self.right)))
        else:
            self.right_motor.forward(speed=0)   


controller = Controller()
while True:
    controller.drive_motor()

    # Oppdateringshastighet
    # Juster sleep for å endre syklus

    sleep(0.2)
