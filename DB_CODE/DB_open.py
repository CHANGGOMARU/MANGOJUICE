from pymongo import MongoClient

def check_login(ID, Passwd):
    # MongoDB에 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Users']
    collection = db['Users']

    # 사용자 정보 확인
    user = collection.find_one({'ID': ID, 'Passwd': Passwd})
    print (user)  # 디버깅을 위한 출력
    print( "유저 출력 완")
    if user:
        return True
    else:
        return False
    

def make_user(ID, Passwd, name, email, phone_number):
    # MongoDB에 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Users']
    collection = db['Users']

    # 사용자 정보 생성
    user = {
        'ID': ID,
        'Passwd': Passwd,
        'name': name,
        'email': email,
        'phone_number': phone_number
    }
    collection.insert_one(user)
    user = collection.find_one({'ID': ID, 'Passwd': Passwd})
    if user:
        return True
    else:
        return False

