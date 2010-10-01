class ObjFromDict(object):
    '''
    Takes a dictionary and returns an object that can use dot notation
    '''
    def __init__(self, d):

        for a, b in d.iteritems():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [ObjFromDict(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, ObjFromDict(b) if isinstance(b, dict) else b)

    # TODO: return a descriptive object string representation
    # def __repr__(self):
    #     return self.obj_label
    