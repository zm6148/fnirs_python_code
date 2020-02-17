import os
import scipy.io as sio
import numpy
import fn


#####################
## load .mat files ##
#####################
file_path = os.path.dirname(os.path.realpath(__file__))
mat_path = file_path + '/data/20160108_1658_01_nima_01.mat'
mat_contents = sio.loadmat(mat_path)

## load vairables from mat file ##
d=numpy.asmatrix(mat_contents['d'])
s=numpy.asarray(mat_contents['s'])
aux=numpy.asarray(mat_contents['aux'])
ml=numpy.asarray(mat_contents['ml'])


################################
## convert to optical density ##
################################

dm = numpy.mean(abs(d),axis=0)
ones = numpy.ones(shape = (d.shape[0], 1))
dod=-numpy.log(numpy.divide(abs(d),numpy.dot(ones,dm)))
      
