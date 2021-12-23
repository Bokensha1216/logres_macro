import sys
import tkinter as tk


import main_macro


if __name__ == "__main__":
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
            global mainThread
            if mainThread is None or not mainThread.is_alive():
                messageLabel["text"] = "開始"
                mainThread = main_macro.syukaiQuest(questTimes)
            else:
                messageLabel["text"] = "すでに開始しています"


    def stop():
        sys.exit( )

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

    frame3 = tk.Frame(masterFrame)
    frame3.pack(pady=10)
    messageLabel = tk.Label(frame3)
    messageLabel.pack()

    mainThread = None

    root.mainloop()
