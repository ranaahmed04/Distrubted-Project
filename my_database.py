import redis

host ='192.168.1.104'
port = 6379


my_database = redis.StrictRedis(host=host,port=port)

def StoreDatabase(playerNum , carImg,x,crashed):
    realdata = f"['{carImg}','{x}','{crashed}']"
    my_database.set(playerNum,realdata)
    


def Getdatabase(playerNum):
    ReturnedData = my_database.get(playerNum)
    value = eval(ReturnedData)
    return value

def NewCarDatabase(playerNum , carImage):
    crashed = False
    carImg = carImage
    X_Position = 800 * 0.45
    Y_Position = 600 * 0.8
    width = 49
    StoreDatabase(playerNum,carImg,X_Position,crashed)
