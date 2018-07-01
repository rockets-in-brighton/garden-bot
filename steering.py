# steering.py

import RPi.GPIO as GPIO
import time
import config
import urllib.request
import urllib.parse

LogServerURL = config.CONFIG['LogServerURL']

GPIO.setmode(GPIO.BOARD)

LeftButton  = config.CONFIG['Left.Button']
RightButton = config.CONFIG['Right.Button']


LeftMotorA  = config.CONFIG['Left.Motor.A']
LeftMotorB  = config.CONFIG['Left.Motor.B']

RightMotorA = config.CONFIG['Right.Motor.A']
RightMotorB = config.CONFIG['Right.Motor.B']

GPIO.setwarnings(False)

GPIO.setup(LeftMotorA, GPIO.OUT)
GPIO.setup(LeftMotorB, GPIO.OUT)
GPIO.setup(RightMotorA, GPIO.OUT)
GPIO.setup(RightMotorB, GPIO.OUT)

PWMFreq = config.CONFIG['PWM.Frequency'] # 100 Hz

LeftMotorA_PWM  = GPIO.PWM(LeftMotorA,  PWMFreq)
LeftMotorB_PWM  = GPIO.PWM(LeftMotorB,  PWMFreq)
RightMotorA_PWM = GPIO.PWM(RightMotorA, PWMFreq)
RightMotorB_PWM = GPIO.PWM(RightMotorB, PWMFreq)

GPIO.setup(LeftButton,  GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RightButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

Speed = 0
MaxSpeed = config.CONFIG['Speed.Max']
IncSpeed = config.CONFIG['Speed.Increment']

LeftMotorA_PWM.start(0)
LeftMotorB_PWM.start(0)
RightMotorA_PWM.start(0)
RightMotorB_PWM.start(0)

LB = False
RB = False

State = "Stop"

while 1:

    Previous_LB = LB
    Previous_RB = RB
    Previous_Speed = Speed
    Previous_State = State

    try:

        LB = GPIO.input(LeftButton) == True
        RB = GPIO.input(RightButton) == True

        if (LB and RB):

            State = "Forward"

            if Speed <= MaxSpeed - IncSpeed:
                Speed += IncSpeed

            LeftMotorA_PWM.ChangeDutyCycle(0)       # low
            LeftMotorB_PWM.ChangeDutyCycle(Speed)   # PWM (CCW)
            
            RightMotorA_PWM.ChangeDutyCycle(Speed)  # PWM (CW)
            RightMotorB_PWM.ChangeDutyCycle(0)      # low

        if (LB and not RB):

            State = "Left"

            if Speed <= MaxSpeed - IncSpeed:
                Speed += IncSpeed

            LeftMotorA_PWM.ChangeDutyCycle(Speed)   # PWM (CW)
            LeftMotorB_PWM.ChangeDutyCycle(0)       # low
            
            RightMotorA_PWM.ChangeDutyCycle(Speed)  # PWM (CW)
            RightMotorB_PWM.ChangeDutyCycle(0)      # low

        if (not LB and RB):

            State = "Right"

            if Speed <= MaxSpeed - IncSpeed:
                Speed += IncSpeed

            LeftMotorA_PWM.ChangeDutyCycle(0)       # low
            LeftMotorB_PWM.ChangeDutyCycle(Speed)   # PWM (CCW)
            
            RightMotorA_PWM.ChangeDutyCycle(0)      # low
            RightMotorB_PWM.ChangeDutyCycle(Speed)  # PWM (CCW)

        if (not LB and not RB):

            State = "Stop"

            Speed = 0

            LeftMotorA_PWM.ChangeDutyCycle(0)       # low
            LeftMotorB_PWM.ChangeDutyCycle(0)       # low
            
            RightMotorA_PWM.ChangeDutyCycle(0)      # low
            RightMotorB_PWM.ChangeDutyCycle(0)      # low

        # logger.debug('LB/RB/State/Speed: ' + str(LB) + '/' + str(RB) + '/' + State + '/' + str(Speed))

        if not(Previous_LB == LB and Previous_RB == RB and Previous_State == State):
            data = urllib.parse.quote('LB={}, RB={}, State={}, Speed={}'.format(LB, RB, State, Speed))
            urllib.request.urlopen(LogServerURL + data)

        time.sleep(config.CONFIG['Sleep.Time.Seconds']) # 50 ms, 20 Hz

    except KeyboardInterrupt:
        GPIO.cleanup()

