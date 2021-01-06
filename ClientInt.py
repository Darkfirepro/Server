#import pymysql
import json

from sqlalchemy import Column, String, create_engine, exists, JSON, LargeBinary, BLOB, ForeignKey, Integer, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#global variables put here:

listC = []
temp_str = ""
temp_byte = b''
temp_navi = 0


#functions will be called:

# create base class:
Base = declarative_base()

# define user object:
class Navigation(Base):
    __tablename__ = 'navigation'

    uid = Column(Integer, primary_key=True, autoincrement = True)
    a_type = Column(String(255))
    p_loc = Column(JSON)
    p_rot = Column(JSON)
    anchor_to = Column(String(255))
    p_time = Column(String(255))
    action = Column(String(255))
    p_data = Column(BLOB)

class AnchorInfo(Base):
    __tablename__ = 'anchor_info'

    uid = Column(Integer, primary_key=True, autoincrement = True)
    anchor_name = Column(String(255))
    anchor_pos = Column(JSON)

    

def create_session():
    # init connection of db:
    engine = create_engine('mysql+pymysql://wennan1:Abc_123456@localhost:3306/PlantInnovation', encoding = "utf-8", echo = False)
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

def sync_loc_camera():
    session = create_session()
    list_loc_infor = session.query(Navigation).all()
    return list_loc_infor

def UpdateNavigationTable(data, data_byte):
    session = create_session()
    new_navi_data = Navigation(a_type = data["devType"], p_loc = data["pos"], p_rot = data["rot"], anchor_to = data["anchorName"], p_time = data["timeAction"], \
                               action = data["actionType"], p_data = data_byte.encode('ascii') + b'<EOF>')
    session.add(new_navi_data)
    session.commit()
    session.close()

def UpdateAnchorPosTable(data):
    session = create_session()
    new_pos_data = AnchorInfo(anchor_name = data["anchorName"], anchor_pos = data["anchorPos"])
    session.add(new_pos_data)
    session.commit()
    session.close()




