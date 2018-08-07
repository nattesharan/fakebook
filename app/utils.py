from bson import ObjectId

def get_id_from_rooms(rooms):
    for room in rooms:
        try:
            return ObjectId(room)
        except:
            print "This is room id"