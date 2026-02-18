class Object:
    def __init__(self, vector, collider, obj_list):
        self.pos = vector
        self.collider = collider
        obj_list.add(self)

    def del(self):

class ObjectList:
    def __init__(self):
        self.list = list()

    def add(self, obj):
        if not isinstance(obj, Object):
            raise TypeError("obj type is not Object")
        self.list.append(obj)

    def del(self, obj):
        if not isinstance(obj, Object):
            raise TypeError("obj type is not Object")
        self.list.remove(obj)



