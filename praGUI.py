from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import pymysql as sql
import time as timer
import cv2
from datetime import datetime
import sys

conn = sql.connect(host='192.168.137.97', user='root', passwd='darker0723', db='raspMDP', charset='utf8')
cursor = conn.cursor(sql.cursors.DictCursor)

tm = timer.localtime()

numsColor = "floral white"
statusColor = "LavenderBlush"
numsLabelColor = "LavenderBlush4"
barColor = "ivory2"
statusButtonColor = "misty rose"

frame = Tk()
frame.title("MDP GUI")
frame.geometry("1280x720+0+0")
frame.iconbitmap(".\\subnet.ico")
frame.resizable(False, False)
frame.overrideredirect(True)  # 라파에 쓸땐 true로
frame.lift()
tImg = PhotoImage()

resetToggle = False
listToggle = True
started = False
NFCSignal = True  # 원래 값 False
sqlDex = False
isOut = False
whileBoolean = True


def convTk(strPath, width, height):
    src = cv2.imread(strPath)
    src = cv2.resize(src, (width, height))
    img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    return imgtk


sSPerson = ""
sPerson = StringVar()
r4c = StringVar()

frameNums = Frame(frame, relief="solid", bg=numsColor)

numsFrame = Frame(frameNums, relief="solid", bg="white", bd=3, width=400, height=220)
numsFrame2 = Frame(frameNums, relief="solid", bg="white", bd=3, width=400, height=300)
shOptionFrame = Frame(frameNums, bg=barColor, width=100, height=720)

mainFont = font.Font(family="여기어때 잘난체", size=15)
listFont = font.Font(family="여기어때 잘난체", size=17)
l2Font = font.Font(family="여기어때 잘난체", size=22)
numsSFont = font.Font(family="여기어때 잘난체", size=25)
statusFont = font.Font(family="여기어때 잘난체", size=21)
numsFont = font.Font(family="여기어때 잘난체", size=100)

pngLabel = Label()

scroll = Scrollbar(numsFrame2)
listScroll = Listbox(numsFrame2, yscrollcommand=scroll.set, width=28, font=listFont, selectbackground="white",
                     bg="white", selectforeground="black", activestyle="none")

imageEnter = convTk(".\\img\\enter.png", 120, 120)
imageExit = convTk(".\\img\\exit.png", 120, 120)
imageSemiExit = convTk(".\\img\\semiexit.png", 120, 120)
imageBusiness = convTk(".\\img\\business.png", 120, 120)


def sqlExcute(sqlQ):
    cursor.execute(sqlQ)
    conn.commit()
    result = cursor.fetchall()
    return result


def sqlExecute(sqlQ):
    cursor.execute(sqlQ)
    conn.commit()


query = "SELECT * FROM data;"
query2 = ""
personNums = sqlExcute(query)
lPersonNums = personNums


def closeFrame():
    global frame, whileBoolean
    frame.quit()
    frame.destroy()
    whileBoolean = False
    sys.exit(0)


def resetTime():
    global resetToggle
    resetToggle = True


def listClick(evt):
    global NFCSignal, r4c, personNums, tImg, pngLabel, exitImage, statusFont, statusButtonColor, imageEnter, imageExit, imageBusiness, imageSemiExit
    e = evt.widget
    num = int(e.curselection()[0])

    if num != 0:
        teImg = ".\\img\\" + str(num) + ".png"
        tImg = convTk(teImg, 200, 200)

        NFCSignal = False

        examWindow = Toplevel(frame, bg=numsColor)
        examWindow.title("출근 확인 창")
        examWindow.overrideredirect(True)
        examWindow.geometry("1280x720+0+0")
        examWindow.lift()

        def executeEnter(evt2):
            global query2, sqlDex
            #  여기에 nfc 태그 비교
            query2 = "UPDATE data SET Status = '재실' WHERE No = " + str(num) + ";"
            sqlDex = True
            examWindow.quit()
            examWindow.destroy()

        def executeBusiness(evt2):
            global query2, sqlDex
            #  여기에 nfc 태그 비교
            query2 = "UPDATE data SET Status = '출장' WHERE No = " + str(num) + ";"
            sqlDex = True
            examWindow.quit()
            examWindow.destroy()

        def executeSemiExit(evt2):
            global query2, sqlDex
            #  여기에 nfc 태그 비교
            query2 = "UPDATE data SET Status = '외출' WHERE No = " + str(num) + ";"
            sqlDex = True
            examWindow.quit()
            examWindow.destroy()

        def executeExit(evt2):
            global query2, sqlDex
            #  여기에 nfc 태그 비교
            query2 = "UPDATE data SET Status = '퇴근' WHERE No = " + str(num) + ";"
            sqlDex = True
            examWindow.quit()
            examWindow.destroy()

        def closeExecute():
            examWindow.quit()
            examWindow.destroy()

        r4c.set(str(personNums[num - 1]['Name']))

        pngLabel = Label(examWindow, width=200, height=200, relief="solid", bg="white")
        pngLabel.pack(anchor="center", pady=40)
        pngLabel.config(image=tImg)

        textLabel = Label(examWindow, textvariable=r4c, bg=numsColor, font=listFont)
        textLabel.place(x=600, y=250)

        buttonExecuteClose = Button(examWindow, image=exitImage2, command=closeExecute, bg=statusButtonColor)
        buttonExecuteClose.place(x=1195, y=635)

        frameWidth = 200
        frameHeight = 300

        frameEnter = Frame(examWindow, width=frameWidth, height=frameHeight, bg=statusButtonColor)
        frameEnter.place(x=60, y=300)
        labelEnter = Label(frameEnter, image=imageEnter, bg=statusButtonColor)
        labelEnter.place(x=40, y=30)
        frameEnter.bind("<Button-1>", executeEnter)
        labelEnter.bind("<Button-1>", executeEnter)
        textEnter = Label(frameEnter, font=statusFont, text="재실", bg=statusButtonColor, fg="white")
        textEnter.place(x=70, y=160)
        textEnter.bind("<Button-1>", executeEnter)

        frameBusiness = Frame(examWindow, width=frameWidth, height=frameHeight, bg=statusButtonColor)
        frameBusiness.place(x=360, y=300)
        labelBusiness = Label(frameBusiness, image=imageBusiness, bg=statusButtonColor)
        labelBusiness.place(x=40, y=30)
        frameBusiness.bind("<Button-1>", executeBusiness)
        labelBusiness.bind("<Button-1>", executeBusiness)
        textBusiness = Label(frameBusiness, font=statusFont, text="출장", bg=statusButtonColor, fg="white")
        textBusiness.place(x=70, y=160)
        textBusiness.bind("<Button-1>", executeBusiness)

        frameSemiExit = Frame(examWindow, width=frameWidth, height=frameHeight, bg=statusButtonColor)
        frameSemiExit.place(x=700, y=300)
        labelSemiExit = Label(frameSemiExit, image=imageSemiExit, bg=statusButtonColor)
        labelSemiExit.place(x=40, y=30)
        frameSemiExit.bind("<Button-1>", executeSemiExit)
        labelSemiExit.bind("<Button-1>", executeSemiExit)
        textSemiExit = Label(frameSemiExit, font=statusFont, text="외출", bg=statusButtonColor, fg="white")
        textSemiExit.place(x=70, y=160)
        textSemiExit.bind("<Button-1>", executeSemiExit)

        frameExit = Frame(examWindow, width=frameWidth, height=frameHeight, bg=statusButtonColor)
        frameExit.place(x=1000, y=300)
        labelExit = Label(frameExit, image=imageExit, bg=statusButtonColor)
        labelExit.place(x=40, y=30)
        frameExit.bind("<Button-1>", executeExit)
        labelExit.bind("<Button-1>", executeExit)
        textExit = Label(frameExit, font=statusFont, text="퇴근", bg=statusButtonColor, fg="white")
        textExit.place(x=70, y=160)
        textExit.bind("<Button-1>", executeExit)

        if lPersonNums[num - 1]['Status'] == '재실':
            starLabel = Label(frameEnter, width=7, height=3, bg="yellow")
            starLabel.place(x=70, y=210)
        elif lPersonNums[num - 1]['Status'] == '출장':
            starLabel = Label(frameBusiness, width=7, height=3, bg="yellow")
            starLabel.place(x=70, y=210)
        elif lPersonNums[num - 1]['Status'] == '외출':
            starLabel = Label(frameSemiExit, width=7, height=3, bg="yellow")
            starLabel.place(x=70, y=210)
        elif lPersonNums[num - 1]['Status'] == '퇴근':
            starLabel = Label(frameExit, width=7, height=3, bg="yellow")
            starLabel.place(x=70, y=210)


def resetList():
    global listToggle, started, sqlDex
    listScroll.delete(0, len(personNums) + 1)
    listToggle = True
    started = False
    sqlDex = False


def listAllTime():
    global exitImage, statusButtonColor, l2Font, personNums, barColor, listImage
    listWindow = Toplevel(frame, bg=numsColor)
    listWindow.title("시간 확인 창")
    listWindow.overrideredirect(True)
    listWindow.geometry("1280x720+0+0")
    listWindow.lift()

    def closeExecute2():
        listWindow.quit()
        listWindow.destroy()

    def listTimeAll():
        listAllWindow = Toplevel(listWindow, bg=numsColor)
        listAllWindow.title("전체 확인 창")
        listAllWindow.overrideredirect(True)
        listAllWindow.geometry("1280x720+0+0")
        listAllWindow.lift()

        def close2Execute():
            listAllWindow.quit()
            listAllWindow.destroy()

        showListExtraFrame = Frame(listAllWindow, bg=barColor, width=100, height=720)
        showListExtraFrame.place(x=1180, y=0)
        buttonListClose = Button(showListExtraFrame, image=exitImage, command=close2Execute, bg=statusButtonColor)
        buttonListClose.place(x=15, y=635)

        list2Frame = Frame(listAllWindow, relief="solid", bd=3)
        list2Frame.place(x=60, y=90)
        listScrollBar2 = Scrollbar(list2Frame)
        listList2 = Listbox(list2Frame, yscrollcommand=scroll.set, width=50, height=17, font=l2Font,
                           selectbackground="white", bg="white", selectforeground="black", activestyle="none")
        listScrollBar2.pack(side="right", fill="y")
        listList2.pack(side="left", fill="both")

        listTimeNums = sqlExcute("SELECT * FROM time")

        str2Extra = "\t\t\t\t\t\t\t\t{0:<15s} {1:<23s} {2:<s}".format("이름", "상태", "총시간")
        listList2.insert(0, str2Extra)
        for k in range(len(listTimeNums)):  # 표시용 포문
            name2Extra = listTimeNums[k]['Name']
            status2Extra = str(listTimeNums[k]['Status'])
            totalTime2Extra = str(listTimeNums[k]['TotalTime'])
            str2ExtraT = "\t\t\t\t\t\t{0:<15s} {1:<9s} {2:<s}".format(name2Extra, status2Extra, totalTime2Extra)
            listList2.insert(k + 1, str2ExtraT)

    listFrame = Frame(listWindow, relief="solid", bd=3)
    listFrame.place(x=60, y=90)
    listScrollBar = Scrollbar(listFrame)
    listList = Listbox(listFrame, yscrollcommand=scroll.set, width=50, height=17, font=l2Font, selectbackground="white", bg="white", selectforeground="black", activestyle="none")
    listScrollBar.pack(side="right", fill="y")
    listList.pack(side="left", fill="both")

    strExtra = "\t\t\t\t\t\t\t\t{0:<15s} {1:<10s} {2:<15s} {3:<14s} {4:<s}".format("이름", "상태", "입장시간", "퇴장시간", "총시간")
    listList.insert(0, strExtra)
    for j in range(len(personNums)):  # 표시용 포문
        nameExtra = personNums[j]['Name']
        startTimeExtra = str(personNums[j]['StartTime'])
        stopTimeExtra = str(personNums[j]['StopTime'])
        statusExtra = str(personNums[j]['Status'])
        strExtraT = ""
        if personNums[j]['StartTime'] is not None and personNums[j]['StopTime'] is not None:
            totalTimeExtra = str(personNums[j]['StopTime'] - personNums[j]['StartTime'])
            strExtraT += "\t\t\t\t\t\t{0:<15s} {1:<9s} {2:<18s} {3:<16s} {4:<s}".format(nameExtra, statusExtra, startTimeExtra, stopTimeExtra, totalTimeExtra)
        elif personNums[j]['StartTime'] is not None and personNums[j]['StopTime'] is None:
            strExtraT += "\t\t\t\t\t\t{0:<15s} {1:<9s} {2:<21s} {3:<16s} {4:<s}".format(nameExtra, statusExtra, startTimeExtra, "None", "None")
        elif personNums[j]['StartTime'] is None and personNums[j]['StopTime'] is None:
            strExtraT += "\t\t\t\t\t\t{0:<15s} {1:<12s} {2:<19s} {3:<17s} {4:<s}".format(nameExtra, statusExtra, "None", "None", "None")
        listList.insert(j + 1, strExtraT)

    showListFrame = Frame(listWindow, bg=barColor, width=100, height=720)
    showListFrame.pack(side="right")
    buttonExecuteClose = Button(showListFrame, image=exitImage, command=closeExecute2, bg=statusButtonColor)
    buttonExecuteClose.place(x=15, y=635)
    listButtonExtra = Button(showListFrame, width=65, height=65, bg=barColor, image=listImage, command=listTimeAll)
    listButtonExtra.place(x=15, y=540)


numsButton = Button(frameNums, text="리셋", font=mainFont, width=10, height=3, command=resetTime)

exitImage = convTk(".\\img\\stop.png", 65, 65)
exitImage2 = convTk(".\\img\\stop2.png", 65, 65)
exitButton = Button(shOptionFrame, width=65, height=65, command=closeFrame, image=exitImage, bg=barColor)

listImage = convTk(".\\img\\list.png", 65, 65)
listButton = Button(shOptionFrame, width=65, height=65, bg=barColor, image=listImage, command=listAllTime)
extraButton0 = Button(shOptionFrame, width=9, height=4, bg=barColor)
extraButton1 = Button(shOptionFrame, width=9, height=4, bg=barColor)
extraButton2 = Button(shOptionFrame, width=9, height=4, bg=barColor)

numsLabelS = Label(numsFrame, bg="white", fg="red", font=numsSFont, text="현재 인원")

sPerson.set(sSPerson)
numsLabel = Label(numsFrame, bg="White", fg="red", font=numsFont, textvariable=sPerson)

frameNums.pack(fill="both", expand=True)
shOptionFrame.pack(side="right")

numsFrame.pack(side="top", anchor="center", pady=40)
numsFrame2.pack(anchor="center")
numsButton.pack(side="bottom", anchor="center")
numsLabelS.place(x=120, y=10)
numsLabel.place(x=150, y=60)

scroll.pack(side="right", fill="y")
listScroll.pack(side="left", fill="both")
listScroll.bind('<<ListboxSelect>>', listClick)
scroll.config(command=listScroll.yview)
exitButton.place(x=15, y=635)
listButton.place(x=15, y=540)
extraButton0.place(x=15, y=20)
extraButton1.place(x=15, y=120)
extraButton2.place(x=15, y=220)

while whileBoolean:
    if lPersonNums != personNums:
        resetList()
        lPersonNums = personNums
    if sqlDex:
        sqlExecute(query2)
        resetList()
    if resetToggle or (tm.tm_hour == 24 and tm.tm_min == 0 and tm.tm_sec == 0):
        for i in range(len(personNums)):
            if personNums[i]['StartTime'] is not None and personNums[i]['StopTime'] is not None:
                tTime = personNums[i]['StopTime'] - personNums[i]['StartTime']
                year = datetime.today().year
                month = datetime.today().month
                day = datetime.today().day
                dSql = "INSERT INTO time(`Name`,StartTime,StopTime,TotalTime,Status) VALUES('%s','%s','%s','%s-%s-%s %s','%s')" % (
                    personNums[i]['Name'], personNums[i]['StartTime'], personNums[i]['StopTime'], year, month, day, tTime, personNums[i]['Status'])
                sqlExecute(dSql)
        sqlExecute("UPDATE data SET StartTime = null, StopTime = null;")
        resetToggle = False
        listScroll.delete(0, len(personNums) + 1)
        listToggle = True
        started = False
    person = 0

    for i in range(len(personNums)):
        if personNums[i]['Status'] == '재실':
            person += 1
            if personNums[i]['StartTime'] is None:
                sqlExecute("UPDATE data SET StartTime = CURTIME() WHERE NO = " + str(i + 1) + ";")
            if started:
                listScroll.itemconfig(i + 1, bg="Lightgreen", selectbackground="Lightgreen")
            isOut = True  # 외출하고 종료시간 바꿀 수 있게 할 때 조건문에 사용
        elif personNums[i]['Status'] == '퇴근':
            if personNums[i]['StartTime'] is not None and isOut:
                sqlExecute("UPDATE data SET StopTime = CURTIME() WHERE NO = " + str(i + 1) + ";")
                isOut = False
            if started:
                listScroll.itemconfig(i + 1, bg="deep pink", selectbackground="deep pink")
        elif personNums[i]['Status'] == '외출':
            if started:
                listScroll.itemconfig(i + 1, bg="aqua", selectbackground="aqua")
        elif personNums[i]['Status'] == '출장':
            if started:
                listScroll.itemconfig(i + 1, bg="light gray", selectbackground="light gray")

    if listToggle:
        strE = "\t\t\t\t\t\t\t\t\t\t\t\t\t\t{0:<26s} {1:<13s}".format("이름", "상태")
        listScroll.insert(0, strE)
        for i in range(len(personNums)):  # 표시용 포문
            name = personNums[i]['Name']
            status = str(personNums[i]['Status'])
            strF = "\t\t\t\t\t\t\t\t\t\t\t\t{0:<25s} {1:<s}".format(name, status)
            listScroll.insert(i + 1, strF)
    listToggle = False

    sSPerson = str(person)
    sPerson.set(sSPerson)
    started = True
    personNums = sqlExcute(query)
    try:
        frame.update()
    except TclError:
        pass

frame.mainloop()
