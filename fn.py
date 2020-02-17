import numpy

###############################################################################
def intensity2OD (d):
    dm = numpy.mean(abs(d),axis=0)
    ones = numpy.ones(shape = (d.shape[0], 1))
    dod = -numpy.log(numpy.divide(abs(d),numpy.dot(ones,dm)))  
    return dod

###############################################################################
def OD2con (dod,ml):
    ## define variables ##
    e_HbO_690=415.5
    e_HbR_690=2141.8
    e_HbO_830=1008.0
    e_HbR_830=778.0
    ppf=6
    sd_distance=30
    coe_HbO_690=e_HbO_690*ppf*sd_distance
    coe_HbR_690=e_HbR_690*ppf*sd_distance
    coe_HbO_830=e_HbO_830*ppf*sd_distance
    coe_HbR_830=e_HbR_830*ppf*sd_distance
    
    ## form coefficent matrix ##
    ## A*B=C ; B=inv(A)*C     ##
    coe_matrix=numpy.matrix([[coe_HbO_690,coe_HbR_690],[coe_HbO_830,coe_HbR_830]])
    coe_inv=numpy.linalg.inv(coe_matrix)
    
    ## form OD matrix for each channel ##
    idx1=numpy.argwhere(ml[:,3]==1)
    idx2=numpy.argwhere(ml[:,3]==2)
    dc=[]
    for ii in range(0,dod.shape[1]/2):
        od_matrix=numpy.concatenate((dod[:,idx1[ii]],dod[:,idx2[ii]]),axis=1)
        con_HbO_HbR=numpy.dot(coe_inv,od_matrix.transpose())
        con_HbO_HbR_HbT=numpy.concatenate((con_HbO_HbR,con_HbO_HbR[0,:]+con_HbO_HbR[1,:]),axis=0)
        dc.append(numpy.asarray(con_HbO_HbR_HbT))
    return dc

###############################################################################
def stimmark(aux,s):
    sound=aux[:,0]   
    stim_index_1=[]
    for ii in range (2,len(sound)-1):
        if sound[ii]-sound[ii-1]>0.01:
            stim_index_1.append(ii)           
    stim_index_2=[]
    for jj in range(2,len(stim_index_1)-1):
        if stim_index_1[jj]-stim_index_1[jj-1]>500:
            stim_index_2.append(stim_index_1[jj])            
    for count in range(0,len(s)):
        for ele in stim_index_2:
            if count==ele:
                s[count]=1                
    return s

###############################################################################
def blockavg (dc,s,Fs,window):
    s_count=0.0
    dummy=[0.0]*(Fs*(-(window[0]))+Fs*window[1])
    for ii in range(0,len(s)):
        if s[ii]==1:
            s_count=s_count+1
            block=dc[ii-5*50:ii+30*50]
            dummy=numpy.add(dummy,block)
            block_average=dummy/s_count
    return block_average
        
        
