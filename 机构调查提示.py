import akshare as ak
import EmailModule as EM
import datetime
import istradeday as ist
import os
import pandas as pd

if ist.is_trade_day(datetime.datetime.now()) == False:
    print('exit!')
    os._exit(0)
mail = ''
today = datetime.datetime.now().strftime('%Y-%m-%d')
try:
    stock_jgdy_detail_em_df = ak.stock_jgdy_detail_em(date=today)
    print('loading')
    #print(stock_jgdy_detail_em_df)
    #print(stock_jgdy_detail_em_df.columns)
    invite = stock_jgdy_detail_em_df
    stock_jgdy_detail_em_df.to_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\ISrecord\\ISrecord_'+today+'_.csv')
except:
    path = 'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\ISrecord\\'
    lists = os.listdir(path)
    lists.sort(key = lambda x: os.path.getmtime(path+x))
    invite = os.path.join(path,lists[-1])
    invite = pd.read_csv(invite)
    #print(invite)
    #print(invite['代码'].unique())
mail = mail + '于 ' + today + ' 共发生：' + str(len(invite)) + '次个股调研' + '<br>'
mail = mail + '其中共调研个股 ' + str(len(invite['代码'].unique())) + ' 支' + '<br>'
mail = mail + '涉及机构 ' + str(len(invite['调研机构'].unique())) + '家' + '<br>'
mail = mail + '其中：' + '<br style = \"text-indent:4em;\">'
    #print(mail)
for i in invite['名称'].unique():
    mail = mail + '$' +' '*10 + i + ' 得到 ' + str(len(invite[invite['名称'] == i])) + '次 调研' + '<br>'
    #for i in range(len(stock_jgdy_detail_em_df)):
        #mail = '【'+invite['调研机构'][i]+'】于 '+str(invite['调研日期'][i])+' 调研：'+invite['名称'][i]+' 股票代号：'+invite['代码'][i] + '<br>' + mail
if mail == '': os._exit(0)
host_server = 'smtp.qq.com'  #qq邮箱smtp服务器
sender_qq = '3470465838@qq.com' #发件人邮箱
pwd = 'nmstebkpovdudcbf'
receiver = ['1755394544@qq.com']
mail_title = '<数令1.0>机构调查提示' #邮件标题
content = EM.content(mail,sender_qq,mail_title)
for i in receiver:
    try:
        account = i
        EM.sendbyqq(content,account,host_server,sender_qq,pwd)
        print('email sent to '+str(i) + '!')
    except:
        continue
