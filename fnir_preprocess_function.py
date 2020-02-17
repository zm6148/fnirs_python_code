import os
import scipy.io as sio
import numpy
import fn
import matplotlib.pyplot as plt
import pywt
import math

def all2con(mat_path_name):
    
    #####################
    ## load .mat files ##
    #####################
    file_path = os.path.dirname(os.path.realpath(__file__))
    mat_path = file_path + '/data/' + mat_path_name
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
    #################0 # 1 # 2#######      
    return dc,test_mark,s_marked

dc,test_mark,s_marked=all2con('20160108_1658_01_nima_01.mat')

#########################
## wavelet dcompsition ##
#########################
### channel selection ###
channel=[3]
#########################

for ele in channel:
    dc_channel=dc[ele][2,:]
    wavelet = pywt.Wavelet('db2')
    levels  = int( math.floor(math.log(dc_channel.shape[0])))
    WaveletCoeffs = pywt.wavedec(dc_channel, wavelet, level=levels)
    
    for ii in range(0,levels):
        q25, q50, q75 = numpy.percentile(WaveletCoeffs[ii], [25,50,75])
        for jj in range(0,len(WaveletCoeffs[ii])):
            if WaveletCoeffs[ii][jj]>q75 or WaveletCoeffs[ii][jj]<q25:
                WaveletCoeffs[ii][jj]=0
    
    new_dc_channel = pywt.waverec(WaveletCoeffs, wavelet)
    sub_dc_channel = numpy.subtract(dc_channel, new_dc_channel)
    
    dc_channel_block = fn.blockavg(dc_channel,s_marked)  
    new_dc_channel_block = fn.blockavg(new_dc_channel,s_marked)          
    sub_dc_channel_block = fn.fblockavg(sub_dc_channel,s_marked)


    
        
            
                

                    
                                        
                                                            
                                                                                            
                        
                                
###########
## plot ###
###########
    
channel=[0]
for ele in channel:    
    ## total time ##    
    plt.figure(3)
    plt.plot(dc[ele][2,:])
    for time in test_mark:
        plt.axvline(time,color='r')
        plt.show()
       
    ## block average ##
       
    dc_channel_block=fn.blockavg(dc[ele][0,:],s_marked)       
    plt.figure(4)
    step=numpy.arange(-5,30,0.02)      
    plt.plot(step,dc_channel_block-numpy.mean(dc_channel_block))
    plt.axhline(0,color='b')
    plt.axvline(0,color='r')
    plt.axvline(15,color='r')    
    plt.show()

