dic1 = {"image": {
        "size": "int",
        "scale": "float"}}

dic2 = {"central_object": {
            "mass": "float",
            "radius": "float",
            "position": {
                "x": "float",
                "y": "flaot"
        }}}

dicc = {}
dicc.update(dic1)
dicc.update(dic2)
print(dicc)