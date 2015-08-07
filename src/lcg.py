#!/usr/bin/python
# coding: utf-8

class LCG(object):
    """Linear congruential generator"""
    def __init__(self, seed):
        super(LCG, self).__init__()
        self.seed = seed
        self._val = seed
        self.mod = 2 ** 32
        self.mul = 1103515245
        self.inc = 12345

    def val(self):
        ret = '{0:031b}'.format(self._val)
        ret = ret[::-1]
        ret = ret[16:31]
        ret = ret[::-1]
        return int(ret, 2)

    def next(self):
        self._val = (self.mul * self._val + self.inc) % self.mod
        return self.val()


def main():
    gen = LCG(17)
    for i in range(10):
        print gen.val()
        gen.next()

if __name__ == '__main__':
    main()
