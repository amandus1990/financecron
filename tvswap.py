# tvswap: time,volume,state weighted average price
# 算法的思想是通过加权方法计算“真实平均价格”，权重的三个方面包括：时间权重，交易量（空间）权重，以及状态权重
# 时间权重的含义是，离当前时间越近则权重越高
# 交易量权重为交易量的大小，交易量大则权重高
# 状态权重为过去成交价与现在成交价的价差，价差小则过去交易的持仓不容易改变，所以权重高
# 在以下实现中，current_w中的状态权重为：math.exp(-abs(price - current_p))，交易量权重为：(rawdata.volume[index])，时间权重为：j;
# 可调整权重的具体实现方式，而建模思想相同。

# 两种好情况：
# (1)p线主导，p线高于tvswap，tvswastd小
# (2)tvswap主导，tvswap高于p线，tvswastd大
# 两种“坏”情况：
# (1)p线主导，p线低于tvswap，tvswastd大
# (2)tvswap主导，tvswap低于p线，tvswastd小

import math
from pandas import Series

# 函数中的第一个参数是从tushare下载的一只个股的完整历史数据，第二个参数是算法中计算时间权重时使用的时间窗口的大小
def tvswap(rawdata,timelen):
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
    res.name='tvswap';
    return(res);

def tvswastd(rawdata,timelen):
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
            tamount+=(current_p-price)**2*current_w;
        list.append(math.sqrt(tamount/tweight));
    res=Series(list,index=rawdata.index[0:reslen]);
    res.name='tvswap';
    return(res);
