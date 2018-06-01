# -*- coding: utf-8 -*-
import time
import lirc
import disp_util
import re
import random

def cluc_game(level):

    #Initialize lirc
    lirc.init("test05", blocking = False)
    disp_util.print_disp("READY?","LEVEL "+level)

    while True:
        codeIR = lirc.nextcode()
        # PLAYを押すと処理を開始する
        if(codeIR != [] and codeIR[0] == "PLAY"):
            disp_util.print_disp("GAME START!","")
            lirc.deinit()
            time.sleep(1)
            total_Number = 0
            # 数字をランダムで数回表示し、その値を合算する
            for i in range(int(level)+2):
                disp_Number = random.randint(1,int(level)*int(level)*int(level)+8)
                total_Number = total_Number + disp_Number
                disp_util.print_disp(str(disp_Number),"")
                time.sleep(1.3-0.01*int(level)*int(level))
                disp_util.print_disp("","")
            disp_util.print_disp("","")                

            return str(total_Number)
               
        else:
            time.sleep(1)

def cluc_game_anser(anser):

    user_anser = ""
    regex = r'[0-9]'

    #Initialize lirc
    lirc.init("test05", blocking = False)

    disp_util.print_disp("Input Anser","")
    
    while True:
        codeIR = lirc.nextcode()
        # リモコンのボタンが押された場合
        if codeIR != []:
            pattern = re.compile(regex)
            # PLAYが押された場合入力モードを終了する
            if str(codeIR[0]) == "PLAY":
                break
            # １つ前の文字を削除する
            elif str(codeIR[0]) == "prev":
                if len(user_anser) != 0:
                    user_anser = str(user_anser[0:len(user_anser)-1])
            # 入力された文字を表示する
            elif re.match(regex, str(codeIR[0])):
                user_anser += str(codeIR[0])

            disp_util.print_disp("Input Anser",user_anser)

        else:
            time.sleep(1)

    # ユーザの入力した値と答えが一致の場合、正解の表示をする
    if(user_anser == anser):
        disp_util.print_disp("Correct Answer", "Congratulations!")
    # ユーザの入力した値と答えが不一致の場合、不正解の表示をする
    else:
        disp_util.print_disp("Incorrect Answer", "Anser is "+anser)
        
try:
    loop_flg = False
    regex = r'[0-9]'
    
    #Initialize lirc
    lirc.init("test05", blocking = False)

    while True:
        codeIR = lirc.nextcode()

        # 一回目だけ表示
        if loop_flg == False:
            disp_util.print_disp("PLEASE INPUT","LEVEL(1-9)")
            
        # リモコンのボタンが押された場合
        if codeIR != []:
            pattern = re.compile(regex)
            # 1-9の数字が押された場合、フラッシュ暗算モードに入る
            if re.match(regex, str(codeIR[0])):
                anser = cluc_game(codeIR[0])
                anser = cluc_game_anser(anser)

                # PLAYを押すと次に遷移する
                while True:
                    codeIR = lirc.nextcode()
                    if(codeIR != [] and codeIR[0] == "PLAY"):
                        break
                    else:
                        time.sleep(1)
                        
            # 上記以外の値が押された場合、エラーメッセージを表示する
            else:
                disp_util.print_disp("ERROR!! PLEASE","INPUT 1-9 NUMBER")

                # PLAYを押すと次に遷移する
                while True:
                    codeIR = lirc.nextcode()
                    if(codeIR != [] and codeIR[0] == "PLAY"):
                        break
                    else:
                        time.sleep(1)

            loop_flg = False

        # 不要な液晶モジュール更新処理を行わないよう制御する
        else:
            loop_flg = True
            time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    disp_util.finally_disp()

