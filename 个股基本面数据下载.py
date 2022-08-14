import EmailModule as EM
import akshare as ak
import datetime
import pandas as pd
import Record as Re

record = Re.loading('record.npy')
#Re.changing('record.npy',['zygc_date'],['null'])
Stocks = pd.read_csv(r'C:\Users\Administrator\Desktop\DailyCollection\StockList\StockList.csv',converters= {'代码':str})
# 登记业务组成
status_zyyw = '主营业务未更新'
for i in Stocks['代码']:
    try:
        zygc = ak.stock_zygc_ym(symbol=i)
        #print(zygc)
    except:
        continue
    try:
        recent = zygc['报告期'][0][:4]
    except:
        recent = recent
    if recent == record['zygc_date']:
        break
    else:
        zygc.to_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\zygc\\'+i+'_'+str(recent)+'_'+'_zygc.csv')
        status_zyyw = '主营业务数据已更新完成'
        #print(i)
Re.changing('record.npy',['zygc_date'],[recent])

##新浪财经财务报告数据
for i in Stocks['代码']:
    try:
        cash = ak.stock_financial_report_sina(stock=i, symbol=r"现金流量表")
        try:
            cash_r = pd.read_csv(
                'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_cash.csv')
            if cash_r['报表日期'][0] == cash['报表日期'][0]:
                continue
            else:
                cash = cash_r.append(cash[cash['报表日期'] <= cash_r['报表日期'][0]])
                cash.to_csv(
                    'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_cash.csv')
        except:
            cash.to_csv(
                'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_cash.csv')
    except:
        continue
###
for i in Stocks['代码']:
    try:
        benefit = ak.stock_financial_report_sina(stock=i, symbol=r"利润表")
        try:
            benefit_r = pd.read_csv(
                'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_benefit.csv')
            if benefit_r['报表日期'][0] == benefit['报表日期'][0]:
                continue
            else:
                benefit = benefit_r.append(benefit[benefit['报表日期'] <= benefit_r['报表日期'][0]])
                benefit.to_csv(
                    'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_benefit.csv')
        except:
            benefit.to_csv(
                'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_benefit.csv')
    except:
        continue
###
for i in Stocks['代码']:
    try:
        assets = ak.stock_financial_report_sina(stock=i, symbol=r"资产负债表")
        try:
            assets_r = pd.read_csv(
                'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_assets.csv')
            if assets_r['报表日期'][0] == assets['报表日期'][0]:
                continue
            else:
                assets = assets_r.append(assets[assets['报表日期'] <= assets_r['报表日期'][0]])
                assets.to_csv(
                    'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_assets.csv')
        except:
            assets.to_csv(
                'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_assets.csv')
    except:
        continue
###
##新浪财经财务报告数据
for i in Stocks['代码']:
    try:
        indicator = ak.stock_financial_analysis_indicator(symbol=i)
        try:
            indicator_r = pd.read_csv(
                'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_indicator.csv')
            if indicator_r['日期'][0] == indicator['日期'][0]:
                continue
            else:
                indicator = indicator_r.append(indicator[indicator['日期'] <= indicator_r['日期'][0]])
                indicator.to_csv(
                    'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_indicator.csv')
        except:
            indicator.to_csv(
                'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\Basic\\' + i + '_indicator.csv')
    except:
        continue

for i in Stocks['代码']:
    for j in ('SH','BJ','sz'):
        code = j+str(i)
        try:
            balance = ak.stock_balance_sheet_by_report_em(symbol=code)
            try:
                balance_r = pd.read_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\DC_Basic\\' + code + '_balance.csv')
                balance = balance_r.append(balance)
                balance = balance.drop_duplicates()
            except: print('no file')
            balance.to_csv(
                'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\DC_Basic\\' + code + '_balance.csv')
            profit = ak.stock_profit_sheet_by_report_em(symbol=code)
            try:
                profit_r = pd.read_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\DC_Basic\\' + code + '_profit.csv')
                profit = profit_r.append(profit)
                profit = profit.drop_duplicates()
            except: print('no file')
            profit.to_csv(
                'C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\DC_Basic\\' + code + '_profit.csv')
            cash = ak.stock_cash_flow_sheet_by_report_em(symbol=code)
            try:
                cash_r = pd.read_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\DC_Basic\\' + code + '_cash.csv')
                cash = cash_r.append(cash)
                cash = cash.drop_duplicates()
            except : print('no file')
            cash.to_csv('C:\\Users\\Administrator\\Desktop\\DailyCollection\\StockInfo\\DC_Basic\\' + code + '_cash.csv')
        except:
            continue


host_server = 'smtp.qq.com'  #qq邮箱smtp服务器
sender_qq = '3470465838@qq.com' #发件人邮箱
pwd = 'nmstebkpovdudcbf'
receiver = ['1755394544@qq.com']
mail_title = '<数令1.0>基本面数据更新，每月一次' #邮件标题
mail = status_zyyw
content = EM.content(mail,sender_qq,mail_title)
for i in receiver:
    try:
        account = i
        EM.sendbyqq(content,account,host_server,sender_qq,pwd)
        print('email sent to '+str(i) + '!')
    except:
        continue