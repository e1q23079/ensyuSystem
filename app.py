from flask import Flask, request, render_template
import DataBase
import DataOperate
from pyngrok import ngrok,conf
from dotenv import load_dotenv
import os

app = Flask(__name__)

#ngrokトークン設定
load_dotenv()
conf.get_default().auth_token = os.getenv('ngrokToken')

#提出状況ステータス
def statusJudgement(syussekiNum,kadaiNum):
    if(kadaiNum==0):
        return "全員未提出"
    elif(syusseki==kadaiNum):
        return "全員提出済み"
    else:
        try:
            return f"{round((kadaiNum/syussekiNum),1)*100}%が提出済み"
        except:
            return "エラーが発生しました．"

#home表示
@app.route("/home")
def home():
    return render_template("home.html")

#課題提出
@app.route("/putkadai", methods=["POST"])
def putkadai():
    tableCode = request.form["tableCode"]
    DataOperate.regist(DataBase.KADAI,tableCode)
    mes = "課題の提出"
    back = "home"
    return render_template("completion.html",text = mes,back = back)

#出席登録
@app.route("/syusseki", methods=["POST"])
def syusseki():
    tableCode = request.form["tableCode"]
    DataOperate.regist(DataBase.SYUSSEKI,tableCode)
    mes = "出席の登録"
    back = "home"
    return render_template("completion.html",text = mes,back = back)

#質問登録
@app.route("/shitsumon", methods=["POST"])
def question():
    tableCode = request.form["tableCode"]
    DataOperate.regist(DataBase.SHITSUMON,tableCode)
    mes = "質問の登録"
    back = "home"
    return render_template("completion.html",text = mes,back = back)

#質問登録解除
@app.route("/cancelshitsumon/<int:id>")
def cancelshitsumon(id):
    DataOperate.deleteId(DataBase.SHITSUMON,id)
    mes = "質問の解除"
    back = "showshitsumon"
    return render_template("completion.html",text = mes,back = back)

#出席登録解除
@app.route("/cancelsyusseki/<int:id>")
def cancelsyusseki(id):
    DataOperate.deleteId(DataBase.SYUSSEKI,id)
    mes = "出席登録の解除"
    back = "showsyusseki"
    return render_template("completion.html",text = mes,back = back)

#課題取り消し
@app.route("/cancelkadai/<int:id>")
def cancelkadai(id):
    DataOperate.deleteId(DataBase.KADAI,id)
    mes = "課題の取り消し"
    back = "showkadai"
    return render_template("completion.html",text = mes,back = back)

#課題をリセットする
@app.route("/resetkadai")
def resetkadai():
    mes = "課題のリセット"
    back = "management"
    DataOperate.allClear(DataBase.KADAI)
    return render_template("completion.html",text = mes,back = back)

#出席状況表示
@app.route("/showsyusseki")
def showsyusseki():
    #出席者数
    syussekiNum = DataOperate.showCount(DataBase.SYUSSEKI)
    #出席者（データベース）
    SYUSSEKI_DB = DataBase.SYUSSEKI
    return render_template("showsyusseki.html",syussekiNum = syussekiNum,SYUSSEKI_DB = SYUSSEKI_DB)

@app.route("/showkadai")
def showkadai():
    #出席人数
    syussekiNum = DataOperate.showCount(DataBase.SYUSSEKI)
    #課題の提出人数
    kadaiNum = DataOperate.showCount(DataBase.KADAI)
    #課題提出者（データベース）
    KADAI_DB = DataBase.KADAI
    #ステータス
    status = statusJudgement(syussekiNum,kadaiNum)
    #課題未提出者（データベース処理）
    KADAIMITEISYUTU_DB = set(DataBase.SYUSSEKI) - set(DataBase.KADAI)
    return render_template("showkadai.html",syussekiNum = syussekiNum,kadaiNum = kadaiNum,KADAI_DB = KADAI_DB,status = status, KADAIMITEISYUTU_DB = KADAIMITEISYUTU_DB)

#質問状況表示
@app.route("/showshitsumon")
def showshitsumon():
    #質問人数
    shitsumonNum = DataOperate.showCount(DataBase.SHITSUMON)
    #質問者（データベース）
    SHITSUMON_DB = DataBase.SHITSUMON
    return render_template("showshitsumon.html",shitsumonNum = shitsumonNum,SHITSUMON_DB = SHITSUMON_DB)

#管理画面
@app.route("/management")
def management():
    return render_template("management.html")

if __name__ == '__main__':
    #app.debug = True    #デバッグモードを利用する
    url = ngrok.connect(5000)
    print(f"URL:{url}")
    app.run(port=5000)