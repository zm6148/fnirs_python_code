import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from math import *

def discreteHaarWaveletTransform(x):
    N = len(x)
    output = [0.0]*N

    length = N >> 1
    while True:
        for i in xrange(0,length):
            summ = x[i * 2] + x[i * 2 + 1]
            difference = x[i * 2] - x[i * 2 + 1]
            output[i] = summ
            output[length + i] = difference

        if length == 1:
            return np.asarray(output)

        #Swap arrays to do next iteration
        #System.arraycopy(output, 0, x, 0, length << 1)
        x = output[:length << 1]

        length >>= 1

def haar_1d_inverse(x):
    n=len(x)
    s = sqrt ( 2.0 )
    y=[0.0]*n
    
    
    k = 1
    while ( k * 2 <= n ):
        for ii in range(0,k):
            y[2*ii]   = ( x[ii] + x[ii+k] ) / s;
            y[2*ii+1] = ( x[ii] - x[ii+k] ) / s;
        for ii in range(0,k*2):
            x[ii] = y[ii];
        k = k * 2;
    return np.asarray(y)


mat_contents = sio.loadmat('C:\\Users\\zmmin_000\Desktop\\fnir experiment new\\subject_01_4\\New folder\\20160112_1154_01_antje_timed.mat')
dc=np.asarray(mat_contents['dc'])
s=np.asarray(mat_contents['s'])

channel=1
dc_channel=dc[:,0,channel]

dc_channel_fd=[]

for ii in range(0,len(dc_channel)-1):
    dc_channel_fd.append(dc_channel[ii+1]-dc_channel[ii])
np.asarray(dc_channel_fd)

### zero padding to 2**17 ###
dc_channel_padded=np.pad(dc_channel, (0,2**17-len(dc_channel)), mode='constant', constant_values=0)
dc_channel_fd_padded=np.pad(dc_channel_fd, (0,2**17-len(dc_channel_fd)), mode='constant', constant_values=0)

### drift estimation ###
dc_channel_drift=np.subtract(dc_channel_padded, dc_channel_fd_padded)

### use haar wavelet to DWT on drift estimation ###
dc_channel_drift_DWT=discreteHaarWaveletTransform(dc_channel_drift)


### use threshold the find drift wavelet coeffiecent ###
threshold=sqrt(2*log(2**17))
dc_channel_drift_DWT_thresholded=[]
for ii in range(0,len(dc_channel_drift_DWT)):
    dummy=np.sign(dc_channel_drift_DWT[ii])*(np.absolute(dc_channel_drift_DWT[ii])-threshold)
    dc_channel_drift_DWT_thresholded.append(dummy)
    
## inverse haar to get drift ###
drift=haar_1d_inverse(dc_channel_drift_DWT_thresholded)    
drift_test=haar_1d_inverse(dc_channel_drift_DWT)    
    

### drift removes ###
dc_channel_drift_removed=np.subtract(dc_channel_padded, drift_test/100)   
    

### do block average ###  
dc_channle_final=dc_channel_drift_removed[0:len(dc_channel)]


### block is [-5 45] 50hz sampling rate ###
s_count=0
dummy=[0.0]*(50*5+45*50)
for ii in range(0,len(s)):
    if s[ii]==1:
        s_count=s_count+1
        block=dc_channel[ii-5*50:ii+45*50]
        dummy=np.add(dummy,block)
block_average_original=dummy/s_count

### block is [-5 45] 50hz sampling rate ###
s_count=0
dummy=[0.0]*(50*5+45*50)
for ii in range(0,len(s)):
    if s[ii]==1:
        s_count=s_count+1
        block=dc_channle_final[ii-5*50:ii+45*50]
        dummy=np.add(dummy,block)
block_average=dummy/s_count
        
s_count=0
dummy=[0.0]*(50*5+45*50)
for ii in range(0,len(s)):
    if s[ii]==1:
        s_count=s_count+1
        block=dc_channel_fd[ii-5*50:ii+45*50]
        dummy=np.add(dummy,block)
block_average_fd=dummy/s_count
        
step=np.arange(-5,45,0.02)    
       
plt.figure(1)

plt.subplot(511)
plt.plot(dc_channel_padded)

plt.subplot(512)
plt.plot(dc_channel_fd_padded)

plt.subplot(513)
plt.plot(dc_channel_drift)

plt.subplot(514)
plt.plot(drift_test)

plt.subplot(515)
plt.plot(dc_channel_drift_removed)

plt.show()

plt.figure(2)

plt.subplot(311)
plt.plot(step,block_average_original)
plt.axvline(0,color='r')
plt.axvline(15,color='r')

plt.subplot(312)
plt.plot(step,block_average)
plt.axvline(0,color='r')
plt.axvline(15,color='r')

plt.subplot(313)
plt.plot(step,block_average_fd)
plt.axvline(0,color='r')
plt.axvline(15,color='r')

plt.show()

