import pymongo
import os
import datetime

myclient = pymongo.MongoClient(os.getenv('MONGO_CLIENT'))
pc_db = myclient[os.getenv('MONGO_DB')]


def insert_pseudocode_into_db(pseudocode):
    coll_name = pc_db["pseudocodes"]
    coll_name_temp = pc_db["pseudocodes_temp"]
    time = datetime.datetime.now()
    pc = {"PseudoCode": pseudocode, "Time": time}

    coll_name.insert_one(pc)
    coll_name_temp.insert_one(pc)


def insert_intents_into_db(record):
    coll_name = pc_db["intents"]
    # coll_name.insert_one(record+{"Time": time})
    print(record)
    coll_name.insert_one(record)


def get_pseudocode_from_db():
    coll_name = pc_db["pseudocodes_temp"]
    records = list(coll_name.find({}))
    lines = []
    for x in records:
        lines.append(x['PseudoCode'])

    return lines


def insert_standard_pc_into_db(pseudocode):
    coll_name = pc_db["Output"]
    time = datetime.datetime.now()
    pc = {"PseudoCode": pseudocode, "Time": time}

    coll_name.insert_one(pc)


def delete_all_documents(collection):
    coll_name = pc_db[collection]
    coll_name.remove({})
