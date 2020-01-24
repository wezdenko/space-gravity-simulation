class Writer:

    def __init__(self, obj):
        self.obj = obj


class ImageWriter(Writer):

    def write(self):
        return {"image": {
                    "size": self.obj.size,
                    "scale": self.obj.scale}}


class StepsWriter(Writer):

    def write(self):
        return {"steps": self.obj}


class TimeWriter(Writer):

    def write(self):
        return {"time_per_step": self.obj}


class CentralObjectWriter(Writer):

    def write(self):
        return {"central_object": {
                    "mass": self.obj._mass,
                    "radius": self.obj._radius,
                    "position": {
                        "x": self.obj.x_axis,
                        "y": self.obj.y_axis}}}


class PointObjectWriter(Writer):

    def write(self):
        return {"point_object": {
                    "position": {
                        "x": self.obj.x_axis,
                        "y": self.obj.y_axis},
                    "velocity": {
                        "x": self.obj._velocity[0],
                        "y": self.obj._velocity[1]}}}


class PointObjectsListWriter:

    def __init__(self, objects_list):
        self.objects_list = objects_list

    def write(self):
        new_list = []
        for point_object in self.objects_list:
            new_list.append(PointObjectWriter(point_object).write())
        return {"point_objects_list": new_list}
