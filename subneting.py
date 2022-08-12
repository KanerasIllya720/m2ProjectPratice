from tkinter import *
from tkinter import Label, messagebox, Menu

Window = Tk()
Window.title("서브네팅 자동 완성 v3")
Window.geometry("300x150+400+100")

subSub = 0
subPer = ""
subClear = False
classInfo = 3

subnetSplit = [4, 8, 16, 32, 64, 128, 256]  # 주소 범위 값 저장 된 리스트 변수
strAdd = ['0', '0', '0', '0']  # 주소 저장 리스트 변수
subSplitStatus = 6  # 사용 가능 주소 범위
lastAddress = 0  # 주소의 마지막 자리
addressPrint = ""  # 주소 출력
nextAddressPrint = ""  # 다음 address 주소 address 엔트리에 출력할 값 저장 변수


def clearE():  # 엔트리 초기화
    e1.delete(0, len(e1.get()))
    e2.delete(0, len(e2.get()))
    e3.delete(0, len(e3.get()))


def enter():  # 입력 버튼 커멘드 함수
    global subSub, subPer, strAdd, subnetSplit, subSplitStatus, lastAddress, addressPrint, nextAddressPrint, subClear, classInfo
    if (e1.get() != "" and e2.get() == "") or (e1.get() == "" and e2.get() != ""):  # 둘 중 하나가 비워져야 실행
        if e2.get() == "":
            if int(e1.get()) <= 2:
                subSub = 252
                subSplitStatus = 0
                classInfo = 3
            elif int(e1.get()) <= 6:
                subSub = 248
                subSplitStatus = 1
                classInfo = 3
            elif int(e1.get()) <= 14:
                subSub = 240
                subSplitStatus = 2
                classInfo = 3
            elif int(e1.get()) <= 30:
                subSub = 224
                subSplitStatus = 3
                classInfo = 3
            elif int(e1.get()) <= 62:
                subSub = 192
                subSplitStatus = 4
                classInfo = 3
            elif int(e1.get()) <= 126:
                subSub = 128
                subSplitStatus = 5
                classInfo = 3
            elif int(e1.get()) > 126:
                subSub = 0
                subSplitStatus = 6
                classInfo = 3
        else:
            if int(e2.get()) == 1:
                subSub = 0
                subSplitStatus = 6
                classInfo = 3
            elif int(e2.get()) <= 2:
                subSub = 248
                subSplitStatus = 1
                classInfo = 3
            elif int(e2.get()) <= 4:
                subSub = 128
                subSplitStatus = 5
                classInfo = 3
            elif int(e2.get()) <= 8:
                subSub = 192
                subSplitStatus = 4
                classInfo = 3
            elif int(e2.get()) <= 16:
                subSub = 224
                subSplitStatus = 3
                classInfo = 3
            elif int(e2.get()) <= 32:
                subSub = 240
                subSplitStatus = 2
                classInfo = 3
            elif int(e2.get()) == 64:
                subSub = 252
                subSplitStatus = 0
                classInfo = 3

        if e3.get() != "":
            strAdd = e3.get().split('.')
            lastAddress = int(strAdd[classInfo]) + subnetSplit[subSplitStatus] - 2
            if int(strAdd[0]) < 255 and int(strAdd[1]) < 255 and int(strAdd[2]) < 255 and int(strAdd[3]) < 255 \
                    and lastAddress < 255 and int(strAdd[0]) > -1 and int(strAdd[1]) > -1 and int(strAdd[2]) > -1 \
                    and int(strAdd[3]) > -1 and classInfo == 3:
                addressPrint = str(strAdd[0]) + "." + str(strAdd[1]) + "." + str(strAdd[2]) + "." + str(
                    int(strAdd[3]) + 1) + "~" + str(lastAddress)
                l5t.set("Address: " + addressPrint)
                nextAddressPrint = str(strAdd[0]) + "." + str(strAdd[1]) + "." + str(strAdd[2]) + "." + str(
                    lastAddress + 1)
            elif classInfo == "B":
                pass
            elif classInfo == "A":
                pass
            else:
                messagebox.showwarning("어드레스 범위 오류", "해당 주소는 범위를 초과했습니다!")
                subClear = True
        else:
            pass

        subPer = "255.255.255." + str(subSub)
        l4t.set("Subnet Mask: " + subPer)
        clearE()
        if nextAddressPrint != "":
            if subClear:
                clearE()
                subClear = False
            else:
                e3.insert(0, nextAddressPrint)
    else:  # 호스트 네트워크 둘다 사용 시
        messagebox.showwarning("칸 오류", "호스트, 네트워크 칸은\n 1개만 사용 가능합니다")
        clearE()


def information():  # 메뉴바 설명
    messagebox.showinfo("설명",
                        "호스트와 네트워크 칸은 한 곳만 입력하세요\n "
                        "어드레스 입력 시 해당 네트워크 주소를 입력해주세요\n"
                        "※ 숫자만 입력하세요\n제작자 \"매운맛 연두\"")


def updateInfo():
    messagebox.showinfo("업데이트 내용",
                        "V1: 네트워크 범위 표시 및 서브넷 마스크 표시\n "
                        "V2: 계산한 네트워크의 다음 네트워크 주소를 \n    주소 입력창에 표시\n"
                        "V3: GUI 변경 및 네트워크 범위 계산 버그 수정")


def closeWindow():  # 메뉴바 종료
    Window.quit()
    Window.destroy()


# 메뉴바 설정
menuBar = Menu(Window)
menuItem1 = Menu(menuBar, tearoff=0)
menuItem1.add_command(label="설명", command=information)
menuItem1.add_command(label="업데이트 내용", command=updateInfo)
menuItem1.add_separator()
menuItem1.add_command(label="종료", command=closeWindow)
menuBar.add_cascade(label="도구", menu=menuItem1)

# 라벨 글씨 변수
l4t = StringVar()
l5t = StringVar()

l1: Label = Label(Window, text="호스트", bg="red", width=21)
l2 = Label(Window, text="네트워크", bg="aqua", width=21)
l3 = Label(Window, text="어드레스", bg="lawn green", width=21)
l4 = Label(Window, textvariable=l4t)
l5 = Label(Window, textvariable=l5t)
# 라벨 글씨 설정
l4t.set("Subnet Mask:")
l5t.set("Address:")

e1 = Entry(Window, width=21)
e2 = Entry(Window, width=21)
e3 = Entry(Window, width=21)

b1 = Button(Window, text="입력", command=enter)
b5 = Button(Window)

l1.place(x=0, y=0)
l2.place(x=150, y=0)
l3.place(x=0, y=40)
l4.place(x=0, y=80)
l5.place(x=0, y=100)

e1.place(x=0, y=20)
e2.place(x=150, y=20)
e3.place(x=0, y=60)

b1.place(x=200, y=50, width=50)

Window.config(menu=menuBar)
Window.mainloop()  # 그래픽 닫음
