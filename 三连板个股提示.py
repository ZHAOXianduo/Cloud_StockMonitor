import os
import akshare as ak
import datetime
import pandas as pd
import EmailModule as EM
import istradeday as ist
if ist.is_trade_day(datetime.datetime.now()) == False: os._exit(0)
stock_list = pd.read_csv(r'C:\Users\Administrator\Desktop\DailyCollection\StockList\StockList.csv',converters= {'代码':str})
stock_list['代码'] = stock_list['代码'].astype(str)
zhuban = stock_list.set_index(['代码'])[:]
zhuban['新浪代码'] = ''
for i in zhuban.index:
    if i[:3] not in ('600','601','602','603','000','001','002','003'):
        zhuban = zhuban.drop(i)
    elif i[:3] in ('600','601','602','603'):
        zhuban['新浪代码'][i] = 'sh'+str(i)
    else:
        zhuban['新浪代码'][i] = 'sz'+str(i)
zhuban = zhuban[zhuban['涨跌幅']<=10.5]
zhuban = zhuban[zhuban['涨跌幅']>=-10.5]
DT = zhuban[(zhuban['涨跌幅']>=-10.5) & (zhuban['涨跌幅']<=-9.9)]
ZT = zhuban[(zhuban['涨跌幅']>=9.9) & (zhuban['涨跌幅']<=10.5)]

def xlianban(x,ZT):
    x = x-1
    cnt = 1
    back = 0
    while cnt <= x:
        sdate = (datetime.datetime.now()+datetime.timedelta(days=-(back+2))).strftime('%Y%m%d') #因为这个任务是设置在第二天开盘前，所以取前面一天股票信息 要+2， 但是测试的时候用+1
        edate = (datetime.datetime.now()+datetime.timedelta(days=-(back+2))).strftime('%Y%m%d')
        #print(sdate)
        try:
            if len(ZT.index) == 0 : return 0
            for i in ZT.index:
                try:
                    stock_info = ak.stock_zh_a_hist_163(symbol=ZT.loc[i]['新浪代码'], start_date=sdate, end_date=edate)
                except:
                    print('error',i,sdate)
                    ZT = ZT.drop(i)
                if stock_info['涨跌幅'][0] <= 9.9:
                    ZT= ZT.drop(i)
                    #print('drop')
            #print(sdate,ZT,back,cnt,len(ZT))
            cnt = cnt+1
            back = back+1
        except:
            back = back+1
        #print(back)
        #print(len(ZT),ZT)
        #print(cnt)
    return ZT

today = datetime.datetime.now().strftime('%Y-%m-%d')
xlist = xlianban(3,ZT)
xlist['放量'] = 0
judge = 0
back = 2
while judge == 0:
    try:
        for i in xlist.index:
            date_ = (datetime.datetime.now() + datetime.timedelta(days=-back)).strftime('%Y%m%d') #同上，测试的时候-1，设置的时候-2
            stock_info = ak.stock_zh_a_hist_163(symbol=ZT.loc[i]['新浪代码'], start_date=date_, end_date=date_)
            if 2*stock_info['成交量'][0] <= xlist.loc[i]['成交量']: xlist.loc[i]['放量'] = 1
        judge = 1
    except:
        back = back + 1
xlist.to_csv(r'C:\Users\Administrator\Desktop\DailyCollection\3limits\3limits'+'_'+today+'.csv')

back = 1
judge = 0
while judge == 0:
    try:
        yesterday = (datetime.datetime.now() + datetime.timedelta(days=-back)).strftime('%Y-%m-%d')
        fanliang = pd.read_csv(r'C:\Users\Administrator\Desktop\DailyCollection\3limits\3limits'+'_'+yesterday+'.csv',converters= {'代码':str})
        judge = 1
    except:
        back = back + 1

candidate = list(xlist.index)
fanliang = fanliang.set_index(['代码'])[:]
print(fanliang)
print(xlist)
alarm = []
for i in fanliang.index:
    print(i)
    if i not in candidate:
        judge = 0
        back = 1
        while judge == 0:
            gdate = datetime.datetime.now() + datetime.timedelta(days=-back)
            gdate_ = (datetime.datetime.now() + datetime.timedelta(days=-back)).strftime('%Y%m%d')
            if ist.is_trade_day(gdate):
                judge = 1
                stock_info = ak.stock_zh_a_hist_163(symbol=fanliang.loc[i]['新浪代码'], start_date=gdate_, end_date=gdate_)
                print(stock_info)
                volumn_KB = stock_info['成交量']
                volumn_ZT = fanliang.loc[i]['成交量']
                if volumn_KB[0] >= 2*volumn_ZT:
                    alarm.append('开板放量股票：'+fanliang.loc[i]['名称']+' 编码：'+i)
            else: back = back + 1

host_server = 'smtp.qq.com'  #qq邮箱smtp服务器
sender_qq = '3470465838@qq.com' #发件人邮箱
pwd = 'nmstebkpovdudcbf'
receiver = ['1755394544@qq.com','389465980@qq.com','mystic111218@163.com']
mail_title = '<数令1.0>连板放量个股提示_V1.0' #邮件标题
mail = today+' 连板放量个股提示'+'<br>'
count = 1
for i in xlist.index:
    mail = mail + '序号【' + str(count) + '】 股票编码：' + i +' '+ xlist.loc[i]['名称'] +'<br>'
    count = count + 1
for i in alarm:
    mail = mail + i + '.' + '<br>'
content = EM.content(mail,sender_qq,mail_title)
for i in receiver:
    try:
        account = i
        EM.sendbyqq(content,account,host_server,sender_qq,pwd)
        print('email sent to '+str(i) + '!')
    except:
        continue