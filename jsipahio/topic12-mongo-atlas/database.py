# from mongita import MongitaClientDisk
from bson.objectid import ObjectId
from pprint import pprint
from pymongo import MongoClient


client = MongoClient("mongodb+srv://jsipahio:RwnVv21rT7Rmc2SL@adsd.cutie.mongodb.net/?retryWrites=true&w=majority&appName=adsd")
pets_db = client.get_database('pets_db')


# i'm lazy and declaring these global. sue me.
pets = pets_db.get_collection('pets_collection')
kinds = pets_db.get_collection('kind_collection')


def get_all_pets_join_kinds():
    pipeline = [{
        '$lookup': {
            "from":"kind_collection", 
            "localField": "kind_id", 
            "foreignField": "_id", 
            "as":"kind"
            }
        },
        {"$unwind": "$kind"}
    ]
    pets_list = list(pets.aggregate(pipeline))
    # manually unpack kind instead of doing the 500 step pipeline for the aggregate
    for pet in pets_list:
        kind = pet['kind']
        pet['kind_name'] = kind['kind_name']
        pet['food'] = kind['food']
        pet['noise'] = kind['noise']
        del pet['kind']
    return pets_list


def get_all_kinds():
    kinds_list = kinds.find()
    return list(kinds_list)



def get_single_pet(objId):
    pipeline = [{
        "$match": {
            "_id": ObjectId(objId)
            },
        },
        {
            "$lookup": {
            "from":"kind_collection", 
            "localField": "kind_id", 
            "foreignField": "_id", 
            "as":"kind"
            }
        },
        {"$unwind": "$kind"},
        {"$limit": 1}
    ]
    pet = list(pets.aggregate(pipeline))[0]
    kind = pet['kind']
    pet['kind_name'] = kind['kind_name']
    pet['food'] = kind['food']
    pet['noise'] = kind['noise']
    del pet['kind']
    return pet


def get_single_kind(objId):
    kind = kinds.find_one({"_id": ObjectId(objId)})
    return kind


def get_all_kinds_simple():
    pipeline = [
        {"$project":{
            "food": 0,
            "noise": 0
        }}
    ]
    kinds_list = list(kinds.aggregate(pipeline))
    return kinds_list


def delete_pet(objId):
    pets.delete_one({"_id": ObjectId(objId)})
    return


def delete_kind(objId):
    pet_list = get_all_pets_join_kinds()
    for pet in pet_list:
        if pet['kind_id'] == objId:
            return False
    kinds.delete_one({"_id": ObjectId(objId)})
    return True


def create_pet(data):
    data['kind_id'] = ObjectId(data['kind_id'])
    result = pets.insert_one(data)
    return result.inserted_id


def create_kind(data):
    result = kinds.insert_one(data)
    return result.inserted_id


def update_pet(data):
    pets.update_one({
        "_id": ObjectId(data["_id"])
        }, 
        {
            "$set": {
                'name': data['name'], 
                'age': data['age'], 
                'owner': data['owner'], 
                'kind': ObjectId(data['kind_id'])
            }
        }
    )
    return


def update_kind(data):
    kinds.update_one({"_id": ObjectId(data["_id"])}, {"$set": {'kind_name': data['kind_name'], 'noise': data['noise'], 'food': data['food']}})
    return


def test_get_pets():
    print('testing get_all_pets')
    pets_list = get_all_pets_join_kinds()
    pprint(pets_list)
    return


def test_get_kinds():
    print('testing get_all_kinds')
    kinds_list = get_all_kinds()
    print(kinds_list)
    return


def test_get_kinds_simple():
    print('testing get_all_kinds_simple')
    kinds_list = get_all_kinds_simple()
    print(kinds_list)
    return
    

def test_get_single_pet(objId = '67295522b6fd32103311c7b5'):
    print('testing get_single_pet')
    pet_list = get_all_pets_join_kinds()
    sample_pet = pet_list[0]
    pet = get_single_pet(sample_pet['_id'])
    print(pet_list[0])
    print(pet)
    assert pet_list[0] == pet
    return


def test_get_single_kind(objId = '67295522b6fd32103311c7b3'):
    print('testing get_single_kind')
    kind = get_single_kind(objId=objId)
    reference_kind = {
        '_id': ObjectId('67295522b6fd32103311c7b3'),
        'food': 'kibble',
        'kind_id': 1,
        'kind_name': 'dog',
        'noise': 'bark'}
    assert kind == reference_kind
    return


def test_create_and_delete_pet():
    print('testing create_pet')
    data = {
        'kind': 1,
        'name': 'dog1',
        'owner': 'owner1',
        'age': 7
    }
    result_id = create_pet(data)
    inserted_pet = get_single_pet(result_id)
    assert(inserted_pet['name'] == data['name'] and inserted_pet['age'] == data['age'] and inserted_pet['owner'] == data['owner'] and inserted_pet['kind'] == inserted_pet['kind'])
    print('testing delete pet')
    delete_pet(result_id)
    assert(get_single_pet(result_id) is None)
    return


def test_create_and_delete_kind():
    print('testing create_kind')
    data = {
        'kind_id': 30000,
        'kind_name': 'aardvark',
        'noise': 'i have no idea',
        'food': 'ants'
    }
    result_id = create_kind(data)
    inserted_kind = get_single_kind(result_id)
    assert(inserted_kind['kind_id'] == data['kind_id'] and inserted_kind['kind_name'] == data['kind_name'] and inserted_kind['noise'] == data['noise'] and inserted_kind['food'] == data['food'])
    print('testing delete kind')
    delete_kind(result_id)
    assert(get_single_kind(result_id) is None)


def test_update_pet():
    print('testing update_pet')
    reference_pet = {
        '_id': ObjectId('67295522b6fd32103311c7b5'),
        'age': 3,
        'kind': 1,
        'name': 'fido',
        'owner': 'nhoj'}
    updated_pet = reference_pet
    updated_pet['age'] = 14
    updated_pet['name'] = 'dog12'
    update_pet(updated_pet)
    assert get_single_pet(reference_pet['_id']) == updated_pet
    update_pet(reference_pet)
    assert get_single_pet(reference_pet['_id']) == reference_pet


def test_update_kind():
    print('testing update kind')
    reference_kind = {
        '_id': ObjectId('67295522b6fd32103311c7b3'),
        'food': 'kibble',
        'kind_id': 1,
        'kind_name': 'dog',
        'noise': 'bark'}
    updated_kind = reference_kind
    updated_kind['food'] = 'dog food'
    updated_kind['noise'] = 'woof'
    update_kind(updated_kind)
    assert get_single_kind(reference_kind['_id']) == updated_kind
    update_kind(reference_kind)
    assert get_single_kind(reference_kind['_id']) == reference_kind 


if __name__ == "__main__":
    # pprint(get_all_pets_join_kinds())
    # exit()
    test_get_pets()
    test_get_single_pet()
    test_get_kinds()
    test_get_kinds_simple()
    exit()
    test_get_single_kind()
    test_create_and_delete_pet()
    test_create_and_delete_kind()
    exit()
    test_update_pet()
    test_update_kind()
    print("all tests passed.")
    exit()