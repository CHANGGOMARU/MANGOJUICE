from pymongo import MongoClient

def check_login(ID, Passwd):
    # MongoDB에 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Users']
    collection = db['Users']

    # 사용자 정보 확인
    user = collection.find_one({'ID': ID, 'password': Passwd})
    if user:
        return True
    else:
        return False

# 사용 예시
if __name__ == "__main__":
    ID = input("ID: ")
    Passwd = input("Passwd: ")
    if check_login(ID, Passwd):
        print("로그인 성공")
    else:
        print("로그인 실패")