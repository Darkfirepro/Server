import pymysql
import json

from sqlalchemy import Column, String, create_engine, exists, JSON, LargeBinary, BLOB, ForeignKey, Integer, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#global variables put here:

listC = []
temp_str = ""

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
    p_data = Column(BLOB)

class SingPlantDetails(Base):
    __tablename__ = 'SingPlant'

    uid = Column(Integer, primary_key=True, autoincrement = True)
    sp_id = Column(Integer)
    sp_location = Column(String(255))
    sp_pot_num = Column(String(255))
    sp_param1 = Column(String(255))
    sp_param2 = Column(String(255))
    sp_param3 = Column(String(255))
    sp_show_plant = Column(String(255))
    sp_hash = Column(String(255))
    sp_name = Column(String(255), ForeignKey("PlantSet.p_name"))

#### test on latency time:
class LatencyTimeDetails(Base):
    __tablename__ = 'LatencyTime'

    uid = Column(Integer, primary_key=True, autoincrement = True)
    p_num = Column(String(255))
    wa_start_time = Column(String(255))
    wa_complete_time = Column(String(255))
    sk_start_time = Column(String(255))
    sk_complete_time = Column(String(255))
    latency_type = Column(String(255))
#########################

class WorldAnchor(Base):
    __tablename__ = 'AnchorData'

    space_name = Column(String(255), primary_key = True)
    whole_data = Column(String(255))
    

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
    elif cond == "wa":
        result = session.query(exists().where(WorldAnchor.space_name == data["spaceName"])).scalar()
    return result

def addSession(data, cond, data_byte):  
    session = create_session()
    if cond == "ps":
        new_plantSet = PlantSet(p_name = data["Name"], p_loc = data["pos"], p_rot =\
                    data["rotate"], p_hash = str(hash(data_byte)), p_data = data_byte)
    elif cond == "pds":
        location, pot_num = get_location(data["singName"], data["singId"])
        new_plantSet = SingPlantDetails(sp_id = data["singId"], sp_location = location, sp_pot_num = pot_num, sp_param1 = data["param1"], sp_param2 = data["param2"],sp_param3 = data["param3"], \
                    sp_hash = str(hash(data_byte)), sp_show_plant = data["showPlant"], sp_name = data["singName"])
    elif cond == "wa":
        new_plantSet = WorldAnchor(space_name = data["spaceName"], whole_data = data_byte)
    session.add(new_plantSet)
    session.commit()
    session.close()

def updateSession(data, cond, data_byte):
    session = create_session()
    if cond == "ps":
        result = session.query(PlantSet).filter(PlantSet.p_name == data["Name"]).first()
        result.p_loc = data["pos"]
        result.p_rot = data["rotate"]
        result.p_hash = str(hash(data_byte))
        result.p_data = data_byte
        session.commit()
        session.close()
    elif cond == "pds":
        result = session.query(SingPlantDetails).filter(and_(SingPlantDetails.sp_name == data["singName"], SingPlantDetails.sp_id == data["singId"])).first()
        result.sp_param1 = data["param1"]
        result.sp_param2 = data["param2"]
        result.sp_param3 = data["param3"]
        result.sp_show_plant = data["showPlant"]
        result.sp_hash = str(hash(data_byte))
        session.commit()
        session.close()
    elif cond == "wa":
        result = session.query(WorldAnchor).filter(WorldAnchor.space_name == data["spaceName"]).first()
        result.whole_data = data_byte
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

def get_location(name, sp_id):
    tray_num_string = name.split("_")[0]
    tray_num = int(tray_num_string)
    list_A = ["A", "B", "C", "D"]
    list_1 = [1, 2, 3, 4, 5]
    list_combine = []
    for i in list_1:
        for n in list_A:
            list_combine.append(n + str(i))
    location = tray_num_string + list_combine[sp_id-1]
    pot_num = (tray_num * len(list_A) * len(list_1)) - (len(list_A) * len(list_1)) + sp_id
    return location, pot_num

def sync_plant_set():
    session = create_session()
    list_plant_set = session.query(PlantSet.p_data).all()
    return list_plant_set

def sync_plant_infor():
    session = create_session()
    list_plant_infor = session.query(SingPlantDetails).all()
    return list_plant_infor

########## test on latency: ####################
def UpdateLatencyTime(data):
    session = create_session()
    new_latency_time = LatencyTimeDetails(p_num = data["anchorNumber"], wa_start_time = data["waStart"], wa_complete_time = data["waComplete"], \
        sk_start_time = data["socketStart"], sk_complete_time = data["socketComplete"], latency_type = data["latencyType"])
    session.add(new_latency_time)
    session.commit()
    session.close()
################################





