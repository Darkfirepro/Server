import pymysql
import json

from sqlalchemy import Column, String, create_engine, exists, JSON, ForeignKey, Integer, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#global variables put here:

listC = []

#functions will be called:

# create base class:
Base = declarative_base()

# define user object:
class PlantSet(Base):
    # table name:
    __tablename__ = 'PlantSet'

    # table attributes:
    p_name = Column(String(255), primary_key=True)
    p_loc = Column(JSON)
    p_rot = Column(JSON)
    p_hash = Column(String(255))

class SingPlantDetails(Base):
    __tablename__ = 'SingPlant'

    uid = Column(Integer, primary_key=True, autoincrement = True)
    sp_id = Column(Integer)
    sp_param1 = Column(String(255))
    sp_param2 = Column(String(255))
    sp_param3 = Column(String(255))
    sp_hash = Column(String(255))
    sp_name = Column(String(255), ForeignKey("PlantSet.p_name"))

def create_session():
    # init connection of db:
    engine = create_engine('mysql+pymysql://Wennan:Furniture123456@localhost:3306/PlantInnovation', encoding = "utf-8", echo = False)
    # create type of conn:
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def querySession(q_class, q_attr, condition, choice):
    session = create_session()
    if choice == 0:
        data = session.query(q_class).filter(q_attr == condition).first()
    elif choice == 1:
        data = session.query(q_class).filter(q_attr == condition).all()
    else:
        print("you have to use 0 or 1 for choice")
    session.close()   
    return data

def exist_or_not(data, cond):
    session = create_session()
    if cond == "ps":
        result = session.query(exists().where(PlantSet.p_name == data["Name"])).scalar()
    elif cond == "pds":
        #result = session.query(exists().where(SingPlantDetails.sp_id == data["singId"]) & SingPlantDetails.sp_name == data["singName"]).scalar()
        result = bool(session.query(PlantSet).filter(and_(SingPlantDetails.sp_name == data["singName"], SingPlantDetails.sp_id == data["singId"])).first())
    else:
        pass
    return result

def addSession(data, cond):  
    session = create_session()
    if cond == "ps":
        new_plantSet = PlantSet(p_name = data["Name"], p_loc = json.dumps(data["pos"]), p_rot =\
                    json.dumps(data["rotate"]), p_hash = str(hash(json.dumps(data).encode("utf-8"))))
    elif cond == "pds":
        new_plantSet = SingPlantDetails(sp_id = data["singId"], sp_param1 = data["param1"], sp_param2 = data["param2"],sp_param3 = data["param3"], \
                    sp_hash = str(hash(json.dumps(data).encode("utf-8"))), sp_name = data["singName"])
    else:
        pass
    session.add(new_plantSet)
    session.commit()
    session.close()

def updateSession(data, cond):
    session = create_session()
    if cond == "ps":
        result = session.query(PlantSet).filter(PlantSet.p_name == data["Name"]).first()
        result.p_loc = json.dumps(data["pos"])
        result.p_rot = json.dumps(data["rotate"])
        result.p_hash = str(hash(json.dumps(data).encode("utf-8")))
        session.commit()
        session.close()
    elif cond == "pds":
        result = session.query(SingPlantDetails).filter(and_(SingPlantDetails.sp_name == data["singName"], SingPlantDetails.sp_id == data["singId"])).first()
        result.sp_param1 = data["param1"]
        result.sp_param2 = data["param2"]
        result.sp_param3 = data["param3"]
        result.sp_hash = str(hash(json.dumps(data).encode("utf-8")))
        session.commit()
        session.close()



def deleteSession(q_class, q_attr, condition):
    session = create_session()
    will_del = session.query(q_class).filter(q_attr == condition).first()
    session.delete(will_del)
    session.commit()
    session.close()

def query_getHash(data, cond):
    db = pymysql.connect("localhost", "Wennan", "Furniture123456", "PlantInnovation")
    cursor = db.cursor()
    if cond == "ps":
        sql = "select p_hash from PlantSet where p_name='{}'".format(data["Name"])
    elif cond == "pds":
        sql = "select sp_hash from SingPlant where (sp_name='{}' and sp_id='{}')".format(data["singName"], data["singId"])
    else:
        pass
    try:
        cursor.execute(sql)
        results = cursor.fetchone()[0]
    except:
        print("Error: unable to fetch data")
    db.close()
    return results




