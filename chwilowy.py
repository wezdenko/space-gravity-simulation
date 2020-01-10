import json

with open('saves/save1.json') as f:
    data = f.read()

data = json.loads(data)
print(len(data["point_objects_list"]))
