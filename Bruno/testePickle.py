import pickle
import os

filename = '/home/bruno/ryu/Bruno/classes.conf'

classlist = []
if os.path.isfile(filename):
    filec = open(filename,'rb')
    classlist = pickle.load(filec)
    filec.close()
