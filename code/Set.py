
class Set(dict):
    """Set is a set implementation based on the built-in dictionary.

    It inherits len, in, not in, and update from dictionary.

    It overrides dict.update, dict.copy and dict.__str__

    No other dictionary methods should be used.

    It implements add, remove, union and intersection.

    This class has two reasons for existence:

    1) It is a quick and dirty replacement for the built-in set class
       in Python 2.4+

    2) It demonstrates the pros and cons on inheriting from built-in
       classes:

       pro: several of the methods inherited from dict work correctly
            for sets.

       pro: several of the set methods can be implemented trivially with
            dictionary methods

       con: users can invoke dictionary methods (which are not part of
            the set interface) on set objects
       
       con: this implementation of sets has the same limitation as
            dict and the built-in set -- the elements have to be hashable.

    
    """
    def __init__(self, seq=[]):
        """create a new Set object.  (seq) can be a sequence or another Set"""
        dict.__init__(self, zip(seq, seq))

    def update(self, seq):
        dict.update(self, zip(seq, seq))

    def copy(self):
        """return a shallow copy of this Set"""
        return Set(self)

    def add(self, key):
        """add (key) to this Set"""
        self[key] = key

    def remove(self, key):
        """remove (key) from this Set or raise KeyError if isn't in the Set"""
        del self[key]

    def union(self, other):
        """return a new Set that contains all the elements
        in (self) or (other)"""
        res = self.copy()
        res.update(other)   
        return res

    def intersection(self, other):
        """return a new Set that contains all the elements
        in (self) and (other)"""
        res = Set()
        for key in self:
            if key in other:
                res.add(key)
        return res

    __or__ = union
    __and__ = intersection

    def __str__(self):
        """the string representation of a Set is the list of keys
        (in arbitrary order)"""
        return str(self.keys())
    
class SetQueue:
    """a SetQueue contains a list and a Set with the same
    elements so that it can maintain order and also check
    membership in constant time.
    """
    def __init__(self, seq=[]):
        self.list = list(seq)
        self.set = Set(seq)

    def __len__(self):
        return len(self.list)

    def remove(self, i=0):
        res = self.list.pop(i)
        self.set.remove(res)
        return res

    def add(self, x):
        self.list.append(x)
        self.set.add(x)

    def __contains__(self, x):
        return x in self.set


def main(script, *args):
    s1 = Set(range(3))
    s2 = Set([3, 2, 1])
    s3 = Set('allen')
    s4 = s3.copy()
    
    print s1
    print s2
    print s3
    print s4
    
    print s1.intersection(s2)
    print s1 & s2
    print s1.union(s2)
    print s1 | s2

    s1.update(s3)
    print s1
    
if __name__ == '__main__':
    import sys
    main(*sys.argv)


