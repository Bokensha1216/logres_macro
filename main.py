import sys
import threading
import tkinter as tk

import main_macro
from exception import *
from coordinate import *
from observer import *
from questData import *

if __name__ == "__main__":
    global mainThread, checkMacroThread


    def start():
        messageLabel["text"] = ""
        questTimes = questTimesEntry.get()
        try:
            questTimes = int(questTimes)
        except ValueError as error:
            if len(questTimes) == 0:
                messageLabel["text"] = "繰り返す回数を入力"
            else:
                messageLabel["text"] = "数字以外が入力されています"
        else:
            global mainThread, checkMacroThread

            def makeThread():
                global mainThread, checkMacroThread
                if var.get() == 0:
                    QuestData.dayOrNight = Stage.DAY
                else:
                    QuestData.dayOrNight = Stage.NIGHT

                print(QuestData.dayOrNight)

                messageLabel["text"] = "開始"
                mainThread = main_macro.syukaiQuest(questTimes)
                checkMacroThread = threading.Thread(target=checkMacro)
                checkMacroThread.start()
                appWindow.observer = Observer()
                appWindow.observer.start()

            try:
                if mainThread.is_alive():
                    messageLabel["text"] = "すでに開始しています"
                else:
                    makeThread()

            except NameError:
                makeThread()


    def stop():
        try:
            if mainThread.is_alive():
                appWindow.eventQueue.put(FinishButtonException())
                appWindow.observer.eventQueue.put(FinishButtonException())
                if checkMacroThread.is_alive():
                    messageLabel["text"] = "マクロ終了中"
            else:
                messageLabel["text"] = "すでに終了しています"
        except NameError as e:
            print(e)
            messageLabel["text"] = "開始されていません"


    def checkMacro():
        mainThread.join()
        messageLabel["text"] = "マクロが終了しました"


    root = tk.Tk()
    root.geometry("260x200")
    root.title("logres_macro")
    root.iconbitmap(default="icon.ico")

    masterFrame = tk.Frame()
    masterFrame.place(x=20, y=20)

    frame1 = tk.Frame(masterFrame)
    frame1.pack()
    startButton = tk.Button(frame1, text="start", font=("Helvetica", 14), command=start)
    startButton.pack(side=tk.LEFT, padx=25)
    stopButton = tk.Button(frame1, text="終了", font=("Helvetica", 14), command=stop)
    stopButton.pack(side=tk.LEFT, padx=30)

    frame2 = tk.Frame(masterFrame)
    frame2.pack(pady=10)
    tk.Label(frame2, text="何回繰り返すか入力", font=("Helvetica", 11)).pack()
    questTimesEntry = tk.Entry(frame2, width=10)
    questTimesEntry.pack()

    questInfoFrame = tk.Frame(masterFrame)
    questInfoFrame.pack(pady=0)
    chuyaLabel = tk.Label(questInfoFrame, text="クエストの昼夜")
    chuyaLabel.pack(side=tk.LEFT, padx=10)
    # チェック有無変数
    var = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    var.set(0)
    # ラジオボタン作成
    hiru = tk.Radiobutton(questInfoFrame, value=0, variable=var, text='昼')
    hiru.pack(side=tk.LEFT, padx=10)
    yoru = tk.Radiobutton(questInfoFrame, value=1, variable=var, text='夜')
    yoru.pack(side=tk.LEFT, padx=10)

    frame3 = tk.Frame(masterFrame)
    frame3.pack(pady=10)
    messageLabel = tk.Label(frame3)
    messageLabel.pack()

    root.mainloop()
