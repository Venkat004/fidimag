#! /usr/bin/python

from __future__ import print_function
import math
import os
import sys
import numpy as np
import struct


class OMF2:

    def __init__(self, file_name, filter=False):
        self.file_name = file_name
        self.read()
        if filter:
            pass

    def read(self):
        f = open(self.file_name, 'rb')
        line = f.readline()
        # print line
        if line != b"# OOMMF OVF 2.0\n":
            print(self.file_name + ": NOT OOMMF OVF 2.0!")
            sys.exit(0)

        while not line.startswith(b"# Begin: Data Binary"):
            line = f.readline()

            if line.startswith(b"# xnodes:"):
                self.xnodes = int(line.split(b":")[1])
            elif line.startswith(b"# ynodes:"):
                self.ynodes = int(line.split(b":")[1])
            elif line.startswith(b"# znodes:"):
                self.znodes = int(line.split(b":")[1])
            elif line.startswith(b"# ystepsize:"):
                self.ystepsize = float(line.split(b":")[1])

        msb = f.read(8)

        if struct.unpack('d', msb)[0] != 123456789012345.0:
            print('check value error!')
            return

        count = 3 * self.xnodes * self.ynodes * self.znodes
        data = f.read(8 * count)
        self.data = np.frombuffer(data)
        self.data = np.reshape(self.data, (-1, 3))
        f.close()
        return

    def get_mag(self, id_x, id_y, id_z, comp='x'):
        """
        return x, y or z component of magnetisation at index (i,j,k)
        """

        index = self.xnodes * self.ynodes * id_z + self.xnodes * id_y + id_x

        id_comp = ord(comp) - ord('x')

        return self.data[index][id_comp]

    def get_all_mag(self, comp='x'):
        """
        return x, y or z component of magnetisation of all nodes
        """
        index = ord(comp) - ord('x')
        return self.data[:, index]

    def get_all_mags(self, order='xyz'):
        """
        Return the x, y AND z components of the magnetisation
        field for every node as a numpy array
        """
        if order == 'xyz':
            d = self.data.copy()
            d.shape = (-1)
            return d

        elif order == 'xxx':
            return np.array([self.data[:, 0],
                             self.data[:, 1],
                             self.data[:, 2]])
