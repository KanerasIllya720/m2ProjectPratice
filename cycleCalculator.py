from tkinter import *
from tkinter import font, messagebox

frame = Tk()
frame.title("인터럽트/PWM 주기 계산기")
frame.geometry("500x330+720+320")

selectIntMode = False
selectPWMMode = False

menuText = ["일반 모드(Normal Mode)", "CTC모드(Clear Timer on Compare Match Mode)", "고속 PWM모드(Fast PWM Mode)",
            "위상 교정 PWM 모드(Phase Correct PWM Mode)"]
menuText2 = ["인터럽트", "PWM"]
buttonText = ["8 Bit", "16 Bit"]

intBit = 8
pwmBit = 8
intColor = "Skyblue1"
pwmColor = "green yellow"
intString = ""
pwmString = ""
intValue = True
pwmValue = True

intLabel = StringVar()
pwmCycleLabel = StringVar()
pwmDutyLabel = StringVar()
intStatus = StringVar()
pwmStatus = StringVar()
intBitStatus = StringVar()
pwmBitStatus = StringVar()

mainFont = font.Font(family="여기어때 잘난체", size=15)


def calculatorInt():
    global selectIntMode, intValue, intLabel, intBit
    entryIntSum = [eIntClock.get(), eIntDiv.get(), eTCNT.get()]
    if eIntClock.get() == "" or eIntDiv.get() == "" or eTCNT.get() == "":
        if eIntClock.get() == "":
            messagebox.showwarning("빈칸 오류", "시스템 클록이 빈칸입니다! ")
        elif eIntDiv.get() == "":
            messagebox.showwarning("빈칸 오류", "분주비가 빈칸입니다!")
        elif eTCNT.get() == "":
            messagebox.showwarning("빈칸 오류", "TCNT가 빈칸입니다!")
    elif eIntClock.get() != "" and eIntDiv.get() != "" and eTCNT.get() != "":
        for i in entryIntSum:
            try:
                valueDex = float(i)
            except ValueError:
                intValue = False
        if not intValue:
            messagebox.showwarning("자료형 오류", "빈칸은 숫자로 채워주세요!")
            clearInt()
        else:
            clock = float(eIntClock.get())
            div = float(eIntDiv.get())
            cnt = float(eTCNT.get())
            if clock <= 0 or div <= 0 or cnt <= 0:
                messagebox.showwarning("입력 오류", "0보다 큰 숫자를 입력하세요")
                clearInt()
            else:
                if not selectIntMode:
                    clockDiv = 1 / (clock * 100000)
                    result = clockDiv * div * cnt
                    resultText = "주기:{0:0.5f}초".format(result)
                    intLabel.set(resultText)
                else:
                    clockDiv = 1 / (clock * 100000)
                    result = clockDiv * div * (cnt + 1)
                    resultText = "주기:{0:0.5f}초".format(result)
                    intLabel.set(resultText)
            if intBit == 8:
                if cnt > 255:
                    messagebox.showwarning("범위 오류", "8Bit일땐 \"255\"까지입니다")
                    clearInt()
            elif intBit == 16:
                if cnt > 65535:
                    messagebox.showwarning("범위 오류", "16Bit일땐 \"65535\"까지입니다")
                    clearInt()


def calculatorPWM():
    global selectPWMMode, pwmCycleLabel, pwmDutyLabel, pwmValue, pwmBit
    entryPWMSum = [ePWMClock.get(), ePWMDiv.get(), ePWMOCR.get()]
    if ePWMClock.get() == "" or ePWMDiv.get() == "" or ePWMOCR.get() == "":
        if ePWMClock.get() == "":
            messagebox.showwarning("빈칸 오류", "시스템 클록이 빈칸입니다!")
        elif ePWMDiv.get() == "":
            messagebox.showwarning("빈칸 오류", "분주비가 빈칸입니다!")
        elif ePWMOCR.get() == "":
            messagebox.showwarning("빈칸 오류", "OCR이 빈칸입니다!")
    elif ePWMClock.get() != "" and ePWMDiv.get() != "" and ePWMOCR.get() != "":
        for i in entryPWMSum:
            try:
                valueDex = float(i)
            except ValueError:
                pwmValue = False
        if not pwmValue:
            messagebox.showwarning("자료형 오류", "빈칸은 숫자로 채워주세요!")
            clearPWM()
        else:
            clock = float(ePWMClock.get())
            div = float(ePWMDiv.get())
            ocr = float(ePWMOCR.get())
            if clock <= 0 or div <= 0 or ocr <= 0:
                messagebox.showwarning("입력 오류", "0보다 큰 숫자를 입력하세요")
                clearPWM()
            else:
                if not selectPWMMode:
                    clockDiv = 1 / (clock * 100000)
                    result = clockDiv * div * 256
                    resultText = "주기:{0:0.5f}초".format(result)
                    td = clockDiv * div * (255 - ocr)
                    duty = td / result * 100
                    dutyText = "DutyCycle: {0:0.3f}%".format(duty)

                    pwmCycleLabel.set(resultText)
                    pwmDutyLabel.set(dutyText)
                else:
                    clockDiv = 1 / (clock * 100000)
                    result = clockDiv * div * 510
                    resultText = "주기:{0:0.5f}초".format(result)
                    td = clockDiv * div * ((256 - ocr) + (254 - ocr) - 1)
                    if ocr != 255:
                        duty = td / result * 100
                    else:
                        duty = 0.0
                    dutyText = "DutyCycle: {0:0.3f}%".format(duty)

                    pwmCycleLabel.set(resultText)
                    pwmDutyLabel.set(dutyText)
            if ocr > 255:
                messagebox.showwarning("범위 오류", "8Bit일땐 \"255\"까지입니다")
                clearPWM()


def selectCalculator(key):
    global selectIntMode, selectPWMMode, intString, pwmString
    if key == 0:
        selectIntMode = False
        intString = "Normal"
        intStatus.set("MODE: " + intString)
    elif key == 1:
        selectIntMode = True
        intString = "CTC"
        intStatus.set("MODE: " + intString)
    elif key == 2:
        selectPWMMode = False
        pwmString = "Fast PWM"
        pwmStatus.set("MODE: " + pwmString)
    elif key == 3:
        selectPWMMode = True
        pwmString = "PC PWM"
        pwmStatus.set("MODE: " + pwmString)


def bitSelect(key):
    global intBit, pwmBit
    if key == 0:
        intBit = 8
        intBitStatus.set("Bit: " + str(intBit))
    elif key == 1:
        intBit = 16
        intBitStatus.set("Bit: " + str(intBit))
    elif key == 2:
        pwmBit = 8
        pwmBitStatus.set("Bit: " + str(pwmBit))
    elif key == 3:
        pwmBit = 16
        pwmBitStatus.set("Bit: " + str(pwmBit))


def clearInt():
    global intLabel
    eIntClock.delete(0, len(eIntClock.get()))
    eIntDiv.delete(0, len(eIntDiv.get()))
    eTCNT.delete(0, len(eTCNT.get()))
    intLabel.set("주기: ")


def clearPWM():
    global pwmCycleLabel, pwmDutyLabel
    ePWMClock.delete(0, len(ePWMClock.get()))
    ePWMDiv.delete(0, len(ePWMDiv.get()))
    ePWMOCR.delete(0, len(ePWMOCR.get()))
    pwmCycleLabel.set("주기: ")
    pwmDutyLabel.set("DutyCycle: ")


def information():  # 메뉴바 설명
    messagebox.showinfo("설명",
                        "1. 왼쪽구역은 인터럽트, 오른쪽구역은 PWM을 계산합니다\n"
                        "2. 사용할 구역의 빈칸을 다 채워주세요\n"
                        "3. CTC모드의 경우 TCNT에 OCR값을 넣어주세요\n"
                        "4. 0보다 큰 숫자만 입력하세요\n"
                        "5. 시스템 클록의 단위는 [MHz] 입니다\n"
                        "6. 소수점 5자리까지만 표시합니다\n"
                        "제작자 \"오연우\"")


def updateInfo():
    messagebox.showinfo("업데이트 내용",
                        "버그 발견 및 기능 추가로 인한 \n업데이트때 "
                        "추가됩니다")


def closeFrame():
    messagebox.showinfo("프로그램 종료", "프로그램을 종료합니다")
    frame.quit()
    frame.destroy()


menubar = Menu(frame)
menuItem1 = Menu(menubar, tearoff=False)
menuItem2 = Menu(menubar, tearoff=False)
menuItemInt = Menu(menuItem1, tearoff=False)
menuItemPWM = Menu(menuItem1, tearoff=False)

frameInt = Frame(frame, relief="solid", bg=intColor)
framePWM = Frame(frame, relief="solid", bg=pwmColor)

menuItem2.add_command(label="설명", command=information)
menuItem2.add_command(label="업데이트 내용", command=updateInfo)
menuItem2.add_separator()
menuItem2.add_command(label="종료", command=closeFrame)
menubar.add_cascade(label="파일", menu=menuItem2)

menuTextCount = 0
for text in menuText:
    def process(cnt=menuTextCount):
        selectCalculator(cnt)


    if menuTextCount < 2:
        menuItemInt.add_command(label=text, command=process)
        if menuTextCount % 2 == 1:
            menuItem1.add_cascade(label="인터럽트", menu=menuItemInt)
    elif menuTextCount > 1:
        menuItemPWM.add_command(label=text, command=process)
        if menuTextCount % 2 == 1:
            menuItem1.add_cascade(label="PWM", menu=menuItemPWM)
    menuTextCount += 1
menubar.add_cascade(label="설정", menu=menuItem1)

eIntClock = Entry(frameInt, width=7, relief="solid", font=mainFont)
eIntDiv = Entry(frameInt, width=7, relief="solid", font=mainFont)
eTCNT = Entry(frameInt, width=10, relief="solid", font=mainFont)
eOCR = Entry(frameInt, width=10, relief="solid", font=mainFont)

buttonTextCount = 0
for text in buttonText * 2:
    def process(cnt=buttonTextCount):
        bitSelect(cnt)


    if buttonTextCount % 2 == 0:
        if buttonTextCount == 0:
            Button(frameInt, text=text, font=mainFont, command=process).place(x=10, y=160)
        elif buttonTextCount == 2:
            Button(framePWM, text=text, font=mainFont, command=process).place(x=10, y=160)
    elif buttonTextCount % 2 == 1:
        if buttonTextCount == 1:
            Button(frameInt, text=text, font=mainFont, command=process).place(x=90, y=160)
        elif buttonTextCount == 3:
            Button(framePWM, text=text, font=mainFont, command=process, state=DISABLED).place(x=90, y=160)
    buttonTextCount += 1

bINTCalculator = Button(frameInt, text="계산", font=mainFont, command=calculatorInt)
bPWMCalculator = Button(framePWM, text="계산", font=mainFont, command=calculatorPWM)
bINTReset = Button(frameInt, text="초기화", font=mainFont, command=clearInt)
bPWMReset = Button(framePWM, text="초기화", font=mainFont, command=clearPWM)

intStatus.set("MODE: Normal")
lIntStatus = Label(frameInt, textvariable=intStatus, font=mainFont, bg=intColor)
intBitStatus.set("Bit: " + str(intBit))
lIntBitStatus = Label(frameInt, textvariable=intBitStatus, font=mainFont, bg=intColor)
lIntClock = Label(frameInt, text="시스템 클록", bg=intColor, font=mainFont)
lIntDiv = Label(frameInt, text="분주비", bg=intColor, font=mainFont)
lTCNT = Label(frameInt, text="TCNT", bg=intColor, font=mainFont)
intLabel.set("주기:")
lIntCycle = Label(frameInt, textvariable=intLabel, font=mainFont, bg=intColor)

ePWMClock = Entry(framePWM, width=7, relief="solid", font=mainFont)
ePWMDiv = Entry(framePWM, width=7, relief="solid", font=mainFont)
ePWMOCR = Entry(framePWM, width=10, relief="solid", font=mainFont)

pwmStatus.set("MODE: Fast PWM")
lPWMStatus = Label(framePWM, textvariable=pwmStatus, font=mainFont, bg=pwmColor)
pwmBitStatus.set("Bit: " + str(pwmBit))
lPWMBitStatus = Label(framePWM, textvariable=pwmBitStatus, font=mainFont, bg=pwmColor)
lPWMClock = Label(framePWM, text="시스템 클록", bg=pwmColor, font=mainFont)
lPWMDiv = Label(framePWM, text="분주비", bg=pwmColor, font=mainFont)
lPWMOCR = Label(framePWM, text="OCR", bg=pwmColor, font=mainFont)
pwmCycleLabel.set("주기:")
pwmDutyLabel.set("DutyCycle:")
lPWMCycle = Label(framePWM, textvariable=pwmCycleLabel, bg=pwmColor, font=mainFont)
lPWMDuty = Label(framePWM, textvariable=pwmDutyLabel, bg=pwmColor, font=mainFont)

frameInt.pack(side="left", fill="both", expand=True)
framePWM.pack(side="right", fill="both", expand=True)

eIntClock.place(x=125, y=72)
eIntDiv.place(x=125, y=100)
eTCNT.place(x=85, y=132)

lIntStatus.place(x=10, y=10)
lIntBitStatus.place(x=10, y=40)
lIntClock.place(x=10, y=70)
lIntDiv.place(x=55, y=95)
lTCNT.place(x=10, y=130)
lIntCycle.place(x=10, y=200)

ePWMClock.place(x=125, y=72)
ePWMDiv.place(x=125, y=100)
ePWMOCR.place(x=85, y=132)

lPWMStatus.place(x=10, y=10)
lPWMBitStatus.place(x=10, y=40)
lPWMClock.place(x=10, y=70)
lPWMDiv.place(x=55, y=100)
lPWMOCR.place(x=10, y=130)
lPWMCycle.place(x=10, y=200)
lPWMDuty.place(x=10, y=225)

bINTCalculator.place(x=10, y=260)
bINTReset.place(x=80, y=260)

bPWMCalculator.place(x=10, y=260)
bPWMReset.place(x=80, y=260)

frame.config(menu=menubar)
frame.mainloop()
