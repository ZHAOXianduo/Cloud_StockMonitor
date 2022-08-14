import akshare as ak
import datetime
import os
import EmailModule as EM
stock_list = ak.stock_zh_a_spot_em()
refreshment = 'Stock List Unchanged'
if len(stock_list) >5000:
    stock_list.to_csv(r'C:\Users\Administrator\Desktop\DailyCollection\StockList\StockList.csv')
    refreshment = 'Refresh Stock List'

today = datetime.datetime.now().strftime('%Y-%m-%d')
sdate = today+' 09:30:00'
edate = today+' 15:00:00'
File_Path = os.getcwd()+'\\'+'DailyCollection\\DailyInfo\\'+str(today)+'\\'
trade_day = 'not a trade day...did not download dailyinfo'
for i in stock_list['代码']:
    try:
        daily = ak.stock_zh_a_hist_min_em(symbol=i, start_date=sdate, end_date=edate, period='1', adjust='')
        if len(daily) > 0:
            if not os.path.exists(File_Path):
                os.makedirs(File_Path)
                daily.to_csv(File_Path+i+'_'+today+'.csv')
                print('success')
                trade_day = 'trade day...dailyinfo downloaded'
            else:
                daily.to_csv(File_Path+i+'_'+today+'.csv')
                print('success')
                trade_day = 'trade day...dailyinfo downloaded'
    except:
        continue
path = os.getcwd()+'\\'+'DailyCollection\\DailyInfo'
fileszie = 0
def get_dir_size(dir):
    filesize = 0
    for root, dirs, files in os.walk(dir):
        filesize += sum([os.path.getsize(os.path.join(root,name)) for name in files])
    return filesize
filesize = get_dir_size(path)
filesize = filesize/(2**30)

host_server = 'smtp.qq.com'  #qq邮箱smtp服务器
sender_qq = '3470465838@qq.com' #发件人邮箱
pwd = 'nmstebkpovdudcbf'
receiver = ['1755394544@qq.com','1184934839@qq.com']
mail_title = '<数令1.0>分时线数据下载_V1.0' #邮件标题
mail = 'Today is ' + today + '\r\n' + refreshment + '\r\n' + trade_day + '\r\n' + 'storage used is ' + str(round(filesize,2)) + 'G'

content = EM.content(mail,sender_qq,mail_title)
for i in receiver:
    try:
        account = i
        EM.sendbyqq(content,account,host_server,sender_qq,pwd)
        print('email sent to'+str(i) + '!')
    except:
        continue

