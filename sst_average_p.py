# sst: state,space,time weighted average price
import math
from pandas import Series

def sst_average_p(rawdata,timelen):
    list=[];
    reslen=len(rawdata)-timelen;
    for i in range(0,reslen):
        price=0.5*rawdata.open[i]+0.5*rawdata.close[i];
        tweight=0;
        tamount=0;
        for j in range(timelen,0,-1):
            index=i+timelen-j;
            current_p=0.5*rawdata.close[index]+0.5*rawdata.open[index];
            current_w=math.exp(-abs(price - current_p))*(rawdata.volume[index])*j;
            tweight+=current_w;
            tamount+=current_p*current_w;
        list.append(tamount/tweight);
    res=Series(list,index=rawdata.index[0:reslen]);
    res.name='averagep';
    return(res);
