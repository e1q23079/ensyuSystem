#データが登録されているか確認する
def confirm(Data,tableCode):
    return tableCode in Data

#データを登録する
def regist(Data,tableCode):
    if(confirm(Data,tableCode)==False):
        Data.append(tableCode)
        return True
    else:
        return False

#データを削除する
def delete(Data,tableCode):
    if(confirm(Data,tableCode)==True):
        Data.remove(tableCode)
        return True
    else:
        return False
    
#すべてのデータを削除する
def allClear(Data):
    Data.clear()

#データ数を取得する
def showCount(Data):
    return len(Data)

#データをid指定で削除する
def deleteId(Data,id):
    try:
        del Data[id]
    except:
        pass
