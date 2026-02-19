class Object:
    def __init__(self, vector, collider, obj_list):
        self.pos = vector
        self.collider = collider
        obj_list.add(self)

    def delete(self, obj_list):
        obj_list.delete(self)

class ObjectList:
    def __init__(self):
        self.list = list()

    def add(self, obj):
        if not isinstance(obj, Object) and not issubclass(obj, Object):
            raise TypeError("obj type is not Object")
        self.list.append(obj)

    def delete(self, obj):
        if not isinstance(obj, Object) and not issubclass(obj, Object):
            raise TypeError("obj type is not Object")
        self.list.remove(obj)



