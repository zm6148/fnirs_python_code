# -*- coding: utf-8 -*-
import os
import scipy.io as sio
import numpy
import fn
import pywt
import matplotlib.pyplot as plt
import math

#####################
## load .mat files ##
#####################
file_path = os.path.dirname(os.path.realpath(__file__))
mat_path = file_path + '/data/' + '20160108_1658_01_nima_01.mat'
mat_contents = sio.loadmat(mat_path)

## load vairables from mat file ##
d=numpy.asmatrix(mat_contents['d'])
s=numpy.asarray(mat_contents['s'])
aux=numpy.asarray(mat_contents['aux'])
ml=numpy.asarray(mat_contents['ml'])

################################
## Place stim marks           ##
################################
s_marked=fn.stimmark(aux,s)
#plt.figure(1)
#plt.plot(aux[:,0])
#plt.plot(s_marked)
test_mark=[]
for ii in range(0,len(s_marked)):
    if s_marked[ii]==1:
        test_mark.append(ii)
#plt.figure(2)
#plt.plot(test_mark)
#plt.show()

################################
## convert to optical density ##
################################
dod=fn.intensity2OD(d)

################################
## convert to Concetration    ##
################################
dc=fn.OD2con(dod,ml)
#################################
## dc[channel][(HbO,HbR,HbT),:]##
################## 0 # 1 # 2 ###

#####################
## select channel ##
####################
channel=[0]

###########################
## wavelet decomposition ##
###########################
for ele in channel:
    dc_channel=dc[ele][2,:]
    ## do z transform ##
    dc_channel_z= numpy.divide(numpy.subtract(dc_channel,numpy.mean(dc_channel)),numpy.std(dc_channel))
    wavelet = pywt.Wavelet('db2')
    levels = pywt.dwt_max_level(data_len=len(dc_channel), filter_len=wavelet.dec_len)
   
#Parameters:
#[cA_n, cD_n, cD_n-1, ..., cD2, cD1],	
#data – Input signal can be NumPy array, Python list or other iterable object. Both single and double precision floating-point data types are supported and the output type depends on the input type. If the input data is not in one of these types it will be converted to the default double precision data format before performing computations.
#wavelet – Wavelet to use in the transform. This can be a name of the wavelet from the wavelist() list or a Wavelet object instance.
#mode – Signal extension mode to deal with the border distortion problem. See MODES for details.
#level – Number of decomposition steps to perform. If the level is None, then the full decomposition up to the level computed with dwt_max_level() function for the given data and wavelet lengths is performed.	
#part –
#Defines the input coefficients type:
#‘a’ - approximations reconstruction is performed
#‘d’ - details reconstruction is performed
#coeffs – Coefficients array to reconstruct.
#wavelet – Wavelet to use in the transform. This can be a name of the wavelet from the wavelist() list or a Wavelet object instance.
#level – If level value is specified then a multilevel reconstruction is performed (first reconstruction is of type specified by part and all the following ones with part type a)
#take – If take is specified then only the central part of length equal to the take parameter value is returned.  
    #n = len(dc_channel_z)          
    #dc_channel_component_a=pywt.upcoef('a', WaveletCoeffs[0], 'db2',take=n)
    #count=1
    for ii in range(1,levels+1):
        WaveletCoeffs = pywt.wavedec(dc_channel_z, wavelet, level=levels)
        dc_channel_z_rec=pywt.waverec(WaveletCoeffs,'db2')
        plt.figure(ii)
        plt.plot(dc_channel_z_rec)
        
        
        
        
        
        
        
        
        
        
        
        
      #  plt.subplot(211)
      #  plt.plot(dc_channel)
      #  for time in test_mark:
      #      plt.axvline(time,color='r')
      #      
      #  plt.subplot(212)
      #  plt.plot(dc_channel_z)
      #  for time in test_mark:
      #      plt.axvline(time,color='r')
      #
      #  plt.figure(2)
      #  plt.subplot(211)
      #  plt.plot(step,dc_channel_component_block-numpy.mean(dc_channel_component_block))
      #  plt.axhline(0,color='b')
      #  plt.axvline(0,color='r')
      #  plt.axvline(15,color='r')
      #  
      #  plt.subplot(211)
      #  plt.plot(step,dc_channel_component_block-numpy.mean(dc_channel_component_block))
      #  plt.axhline(0,color='b')
      #  plt.axvline(0,color='r')
      #  plt.axvline(15,color='r')
        
    
        
    



############
### plot ###
############
#    
#for ele in channel:
#    
#    ## total time ##
#    plt.figure(3)
#    plt.plot(dc[ele][2,:])#plot total
#    for time in test_mark:
#        plt.axvline(time,color='r')
#    plt.show()
#       
#    ## block average ##
#    dc_channel_block=fn.blockavg(dc[ele][0,:],s_marked,50,[-5,30])       
#    plt.figure(4)
#    step=numpy.arange(-5,30,0.02)      
#    plt.plot(step,dc_channel_block-numpy.mean(dc_channel_block))
#    plt.axhline(0,color='b')
#    plt.axvline(0,color='r')
#    plt.axvline(15,color='r')
#    plt.show()