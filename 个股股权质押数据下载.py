import akshare as ak
import datetime
import Record as Re
import EmailModule as EM
import pandas as pd

record = Re.loading('record.npy')
start = datetime.datetime.strptime(record['gqzy_date'],'%Y%m%d')
oneday = datetime.timedelta(days=1)
today = datetime.datetime.now()#.strftime('%Y-%m-%d')
while start < today:
    timing = str(start)[:10].replace('-','')
    try:
        gqzy= ak.stock_gpzy_pledge_ratio_em(date=timing)
    except:
        start = start + oneday
        print('fail and continue:',start)
        continue
    print(start)
    gqzy.to_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\gqzy\\'+'gqzy_'+timing+'.csv')
    start = start + oneday
    Re.changing('record.npy',['gqzy_date'],[start])
##重要股东质押权重
stock_gpzy_pledge_ratio_detail_em_df = ak.stock_gpzy_pledge_ratio_detail_em()
raw = pd.read_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\zygd\\'+'zygdzyWeight_'+'.csv')
if str(raw['公告日期'][0]) != str(stock_gpzy_pledge_ratio_detail_em_df['公告日期'][0]):
    recent_record = stock_gpzy_pledge_ratio_detail_em_df[:]
    recent = datetime.datetime.strptime(raw['公告日期'][0], '%Y%m%d')
    raw.append(recent_record[recent_record['公告日期'] > recent])
raw.to_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\zygd\\'+'zygdzyWeight_'+'.csv')
host_server = 'smtp.qq.com'  #qq邮箱smtp服务器
sender_qq = '3470465838@qq.com' #发件人邮箱
pwd = 'nmstebkpovdudcbf'
receiver = ['1755394544@qq.com']
mail_title = '<数令1.0>股权质押数据更新，每周一次' #邮件标题
mail = str(today) + ' 股权质押数据已完成下载'
content = EM.content(mail,sender_qq,mail_title)
for i in receiver:
    try:
        account = i
        EM.sendbyqq(content,account,host_server,sender_qq,pwd)
        print('email sent to '+str(i) + '!')
    except:
        continue