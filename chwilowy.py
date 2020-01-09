import json

with open('saves/save1.json') as f:
    data = f.read()

data = json.loads(data)
print(data["point_objects_list"][0]["point_object"]["position"])
