import Record as Re
import datetime
import akshare as ak
import pandas as pd
import EmailModule as EM

today = datetime.datetime.now().strftime('%Y-%m-%d')
#record_f = Re.changing('record.npy',['qfq_factor_date'],['null'])
#Re.saving(Re.recording([],[]),'record.npy')
#Re.changing('record.npy',['qfq_date'],['null'])
#Re.changing('record.npy',['hfq_date'],['null'])
#Re.changing('record.npy',['qfqfactor_date'],['null'])
#Re.changing('record.npy',['hfqfactor_date'],['null'])
record = Re.loading('record.npy')
#if record['fq_factor_date'] == 'null':
#print(record)
#record = Re.delete('record.npy',['fq_factor_date'],['null'])
print(record)
stock_list = pd.read_csv(r'C:\Users\Administrator\Desktop\DailyCollection\StockList\StockList.csv',converters= {'代码':str})
for i in stock_list['代码']:
    print(i)
    for forward in ('sz','sh','bj'):
        try:
            symbol = forward + i
            print(symbol)
            if record['qfqfactor_date'] != today:
                qfq_factor_df = ak.stock_zh_a_daily(symbol=symbol, adjust="qfq-factor")
                qfq_factor_df.to_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\fqData\\qfq_factor\\' + i + '_qfqfactor.csv')
            if record['qfqfactor_date'] != today:
                hfq_factor_df = ak.stock_zh_a_daily(symbol=symbol, adjust="hfq-factor")
                hfq_factor_df.to_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\fqData\\hfq_factor\\' + i + '_hfqfactor.csv')
            if record['qfq_date'] == 'null':
                data = ak.stock_zh_a_daily(symbol=symbol, end_date=today, adjust="qfq")
                data.to_csv(
                    'C:\\Users\\Administrator\\Desktop\\DailyCollection\\fqData\\qfq_data\\' + i + '_qfqdata.csv')
            elif record['qfq_date'] != today:
                raw = pd.read_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\fqData\\qfq_data\\' + i + '_qfqdata.csv')
                data = ak.stock_zh_a_daily(symbol=symbol, start_date=record['qfq_date'], end_date=today, adjust="qfq")
                new = raw.append(data)
                new.to_csv(
                    'C:\\Users\\Administrator\\Desktop\\DailyCollection\\fqData\\hfq_data\\' + i + '_qfqdata.csv')
            if record['hfq_date'] == 'null':
                data = ak.stock_zh_a_daily(symbol=symbol, end_date=today, adjust="hfq")
                data.to_csv(
                    'C:\\Users\\Administrator\\Desktop\\DailyCollection\\fqData\\hfq_data\\' + i + '_hfqdata.csv')
            elif record['hfq_date'] != today:
                raw = pd.read_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\fqData\\hfq_data\\' + i + '_hfqdata.csv')
                data = ak.stock_zh_a_daily(symbol=symbol, start_date=record['hfq_date'], end_date=today, adjust="hfq")
                new = raw.append(data)
                new.to_csv(
                    'C:\\Users\\Administrator\\Desktop\\DailyCollection\\fqData\\hfq_data\\' + i + '_hfqdata.csv')
        except:
            continue
Re.changing('record.npy',['qfq_date','hfq_date','qfqfactor_date','hfqfactor_date'],
            [today,today,today,today])
record = Re.loading('record.npy')


host_server = 'smtp.qq.com'  #qq邮箱smtp服务器
sender_qq = '3470465838@qq.com' #发件人邮箱
pwd = 'nmstebkpovdudcbf'
receiver = ['1755394544@qq.com']
mail_title = '<数令1.0>复权数据自动更新' #邮件标题
mail = today+' 每周复权数据自动下载'+ '<br>' + '当前进度：' + '<br>' + str(record)
print(mail)
content = EM.content(mail,sender_qq,mail_title)
for i in receiver:
    try:
        account = i
        EM.sendbyqq(content,account,host_server,sender_qq,pwd)
        print('email sent to'+str(i) + '!')
    except:
        continue
