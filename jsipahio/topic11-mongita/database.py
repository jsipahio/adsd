from mongita import MongitaClientDisk
from bson.objectid import ObjectId
from pprint import pprint

client = MongitaClientDisk()
pets_db = client.pets_db

pets = pets_db.pets_collection
kinds = pets_db.kind_collection

# pets.delete_many({})
# kinds.delete_many({})

# kinds.insert_many([
#     {'kind_id': 1,'kind_name': 'dog', 'noise': 'bark', 'food': 'kibble'},
#     {'kind_id': 2,'kind_name': 'cat', 'noise': 'meow', 'food': 'meow-mix'}])

# pets.insert_many([
#     {'name': 'fido', 'age': 3, 'owner': 'nhoj', 'kind': 1}, 
#     {'name': 'mittens', 'age': 6, 'owner': 'xela', 'kind': 2}])


# PET_KEYS = ('name', 'age', 'owner', 'kind')
# KIND_KEYS = ('kind_id', 'kind_name', 'noise', 'food')

def get_all_pets_join_kinds():
    pets_list = list(pets.find())

    pets_list_w_kind = []

    for pet in pets_list:
        kind = kinds.find_one({'kind_id': {'$eq': int(pet['kind'])}})
        pets_list_w_kind.append({
            'obj_id': pet["_id"],
            'name': pet['name'],
            'age': pet['age'],
            'owner': pet['owner'],
            'kind_id': kind['kind_id'],
            'kind': kind['kind_name'],
            'noise': kind['noise'],
            'food': kind['food'],
            'kind_obj_id': kind['_id']
        })
    return pets_list_w_kind


def get_all_kinds():
    kinds_list = kinds.find()
    return list(kinds_list)



def get_single_pet(objId):
    pet = pets.find_one({"_id": ObjectId(objId)})
    return pet


def get_single_kind(objId):
    kind = kinds.find_one({"_id": ObjectId(objId)})
    return kind


def get_all_kinds_simple():
    kinds_list = list(kinds.find())
    kinds_list_simple = []
    for kind in kinds_list:
        kinds_list_simple.append({
            'kind_name': kind['kind_name'],
            '_id': kind['_id'],
            'kind_id': kind['kind_id']
        })
    return kinds_list_simple


def delete_pet(objId):
    pets.delete_one({"_id": ObjectId(objId)})
    return


def delete_kind(objId):
    pet_list = get_all_pets_join_kinds()
    for pet in pet_list:
        if pet['kind_obj_id'] == objId:
            return False
    kinds.delete_one({"_id": ObjectId(objId)})
    return True


def create_pet(data):
    result = pets.insert_one(data)
    return result.inserted_id


def create_kind(data):
    kinds_list = get_all_kinds()
    max_id = 0
    for kind in kinds_list:
        if int(kind['kind_id']) > max_id:
            max_id = kind['kind_id']
    data['kind_id'] = max_id + 1
    result = kinds.insert_one(data)
    return result.inserted_id


def update_pet(data):
    pets.update_one({"_id": ObjectId(data["_id"])}, {"$set": {'name': data['name'], 'age': data['age'], 'owner': data['owner'], 'kind': data['kind']}})
    return


def update_kind(data):
    kinds.update_one({"_id": ObjectId(data["_id"])}, {"$set": {'kind_id': data['kind_id'], 'kind_name': data['kind_name'], 'noise': data['noise'], 'food': data['food']}})
    return


def test_get_pets():
    print('testing get_all_pets')
    pets_list = get_all_pets_join_kinds()
    # pets.update_one({'_id': ObjectId('67200cf282da56327ac531d2')}, {"$set": {'name':'fido', 'age': 3}})
    # pprint(pets_list)
    # kinds.update_one({'_id': ObjectId('67200cf282da56327ac531d0')}, {'$set': {'food': 'kibble', 'noise': 'bark'}})
    # exit()
    reference_pets_list = [
        {'age': 3,
        'food': 'kibble',
        'kind': 'dog',
        'kind_id': 1,
        'kind_obj_id': ObjectId('67295522b6fd32103311c7b3'),
        'name': 'fido',
        'noise': 'bark',
        'obj_id': ObjectId('67295522b6fd32103311c7b5'),
        'owner': 'nhoj'},
        {'age': 6,
        'food': 'meow-mix',
        'kind': 'cat',
        'kind_id': 2,
        'kind_obj_id': ObjectId('67295522b6fd32103311c7b4'),
        'name': 'mittens',
        'noise': 'meow',
        'obj_id': ObjectId('67295522b6fd32103311c7b6'),
        'owner': 'xela'}]
    assert all(pet in pets_list for pet in reference_pets_list)
    return


def test_get_kinds():
    print('testing get_all_kinds')
    kinds_list = get_all_kinds()
    reference_kinds_list = [
        {'_id': ObjectId('67295522b6fd32103311c7b3'),
        'food': 'kibble',
        'kind_id': 1,
        'kind_name': 'dog',
        'noise': 'bark'},
        {'_id': ObjectId('67295522b6fd32103311c7b4'),
        'food': 'meow-mix',
        'kind_id': 2,
        'kind_name': 'cat',
        'noise': 'meow'}]
    assert all(kind in kinds_list for kind in reference_kinds_list)
    return


def test_get_kinds_simple():
    print('testing get_all_kinds_simple')
    kinds_list = get_all_kinds_simple()
    reference_kinds_list = [
        {'_id': ObjectId('67295522b6fd32103311c7b3'),
        'kind_id': 1,
        'kind_name': 'dog'},
        {'_id': ObjectId('67295522b6fd32103311c7b4'),
        'kind_id': 2,
        'kind_name': 'cat'}]
    assert all(kind in kinds_list for kind in reference_kinds_list)
    return
    

def test_get_single_pet(objId = '67295522b6fd32103311c7b5'):
    print('testing get_single_pet')
    pet = get_single_pet(objId)
    reference_pet = {
        '_id': ObjectId('67295522b6fd32103311c7b5'),
        'age': 3,
        'kind': 1,
        'name': 'fido',
        'owner': 'nhoj'}
    assert pet == reference_pet
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
    test_get_kinds()
    test_get_kinds_simple()
    test_get_single_pet()
    test_get_single_kind()
    test_create_and_delete_pet()
    test_create_and_delete_kind()
    exit()
    test_update_pet()
    test_update_kind()
    print("all tests passed.")
    exit()