import os
import scipy.io as sio
import numpy as np
import pywt
import matplotlib.pyplot as plt
import math

#####################
## define Functions##
#####################

def blockavg (dc,s):
    s_count=0.0
    dummy=[0.0]*(50*5+30*50)
    for ii in range(0,len(s)):
        if s[ii]==1:
            s_count=s_count+1
            block=dc[ii-5*50:ii+30*50]
            dummy=np.add(dummy,block)
            block_average=dummy/s_count
    return block_average
    
#####################
## load .mat files ##
#####################
file_path = os.path.dirname(os.path.abspath(__file__))
#file_name='/20160108_1658_01_nima_01_dc.mat'
file_name='/20160108_1716_01_Min_dc.mat'
#file_name='/20160112_1154_01_antje_dc.mat'
mat_path=file_path+file_name
mat_contents = sio.loadmat(mat_path)

#d=np.asarray(mat_contents['d'])
#s=np.asarray(mat_contents['s'])
#ml=np.asarray(mat_contents['ml'])
s=np.asarray(mat_contents['s'])
aux=np.asarray(mat_contents['aux'])
dc=np.asarray(mat_contents['dc'])

########################
### wavelet denosing ###
########################
#for ii in range(0,dc.shape[2]):
### channel selection ###
channel=[3]

for ele in channel:
    dc_channel=dc[:,2,ele]
    wavelet = pywt.Wavelet('db2')
    levels  = int( math.floor(math.log(dc_channel.shape[0])))
    WaveletCoeffs = pywt.wavedec(dc_channel, wavelet, level=levels)
    
    for ii in range(0,levels):
        q25, q50, q75 = np.percentile(WaveletCoeffs[ii], [25,50,75])
        for jj in range(0,len(WaveletCoeffs[ii])):
            if WaveletCoeffs[ii][jj]>q75 or WaveletCoeffs[ii][jj]<q25:
                WaveletCoeffs[ii][jj]=0
    
    new_dc_channel = pywt.waverec(WaveletCoeffs, wavelet)
    sub_dc_channel = np.subtract(dc_channel, new_dc_channel)
    
    dc_channel_block = blockavg(dc_channel,s)  
    new_dc_channel_block = blockavg(new_dc_channel,s)          
    sub_dc_channel_block = blockavg(sub_dc_channel,s)
    
    ###########
    ## plot ###
    ###########
    
    ## block average ##
    plt.figure(1)
    step=np.arange(-5,30,0.02)  
    plt.subplot(211)     
    plt.plot(step,dc_channel_block-np.mean(dc_channel_block))
    plt.axhline(0,color='b')
    plt.axvline(0,color='r')
    plt.axvline(15,color='r')
    
    plt.subplot(212)     
    plt.plot(step,sub_dc_channel_block-np.mean(sub_dc_channel_block))
    plt.axhline(0,color='b')
    plt.axvline(0,color='r')
    plt.axvline(15,color='r')
    
    
    ## block whole channel ##
    plt.figure(2)
    plt.subplot(211)     
    plt.plot(dc_channel)
    plt.axhline(0,color='b')
    plt.axvline(0,color='r')
    plt.axvline(15,color='r')
    
    plt.subplot(212)     
    plt.plot(sub_dc_channel)
    plt.axhline(0,color='b')
    plt.axvline(0,color='r')
    plt.axvline(15,color='r')
    
    plt.figure(3)
    plt.plot(aux[:,0])
    plt.plot(s)
    
    plt.show()
    
    


