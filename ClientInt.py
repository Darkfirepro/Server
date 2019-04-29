import pymysql
import json

from sqlalchemy import Column, String, create_engine, exists, JSON, INT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#global variables put here:

listC = []

#functions will be called:

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class PlantSet(Base):
    # 表的名字:
    __tablename__ = 'PlantSet'

    # 表的结构:
    p_name = Column(String(50), primary_key=True)
    p_loc = Column(JSON)
    p_rot = Column(JSON)
    p_hash = Column(String(255))

class SingPlantDetails(Base):
    __tablename__ = 'SingPlant'

    sp_name = Column(String(100), primary_key=True)
    sp_param1 = Column(String(100))
    sp_param2 = Column(String(100))
    sp_param3 = Column(String(100))


def querySession(q_class, q_attr, condition, choice):
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://Wennan:Furniture123456@localhost:3306/PlantInnovation', encoding = "utf-8", echo = False)
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if choice == 0:
        data = session.query(q_class).filter(q_attr == condition).first()
    elif choice == 1:
        data = session.query(q_class).filter(q_attr == condition).all()
    else:
        print("you have to use 0 or 1 for choice")
    session.close()   
    return data

def exist_or_not(q_attr, condition):
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://Wennan:Furniture123456@localhost:3306/PlantInnovation', encoding = "utf-8", echo = False)
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    data = session.query(exists().where(q_attr == condition)).scalar()
    return data

def addSession(data):  
    # 初始化数据库连接:
    engine = create_engine('mysql+pymysql://Wennan:Furniture123456@localhost:3306/PlantInnovation', encoding = "utf-8", echo = False)
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    new_plantSet = PlantSet(p_name = data["Name"], p_loc = json.dumps(data["pos"]), p_rot = json.dumps(data["rotate"]), p_hash = str(hash(json.dumps(data).encode("utf-8"))))
    session.add(new_plantSet)
    session.commit()
    session.close()

def updateSession(q_class, q_attr, data):
    engine = create_engine('mysql+pymysql://Wennan:Furniture123456@localhost:3306/PlantInnovation', encoding = "utf-8", echo = False)
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    result = session.query(q_class).filter(q_attr == data["Name"]).first()
    result.p_loc = json.dumps(data["pos"])
    result.p_rot = json.dumps(data["rotate"])
    result.p_hash = str(hash(json.dumps(data).encode("utf-8")))
    print(result.p_hash)
    session.commit()
    session.close()

def deleteSession(q_class, q_attr, condition):
    engine = create_engine('mysql+pymysql://Wennan:Furniture123456@localhost:3306/PlantInnovation', encoding = "utf-8", echo = False)
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    will_del = session.query(q_class).filter(q_attr == condition).first()
    session.delete(will_del)
    session.commit()
    session.close()

def query_pysql(name):
    db = pymysql.connect("localhost", "Wennan", "Furniture123456", "PlantInnovation")
    cursor = db.cursor()
    sql = "select p_hash from PlantSet where p_name='{}'".format(name)
    try:
        cursor.execute(sql)
        results = cursor.fetchone()[0]
    except:
        print("Error: unable to fetch data")
    db.close()
    return results




