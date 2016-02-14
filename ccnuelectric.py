# -*- coding: UTF-8 -*- 
import sys,requests, json,re,string,sqlite3,time,datetime
#2016-01-31 18:05:05 by sixer
#TEST DATA
#南湖11-307：30901*Meter
#国4-1520：23437*Meter
reload(sys) 
sys.setdefaultencoding('utf8') #设置编码，解决中文乱码

def GetNowTime():

    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def getMeterData(room,unit,type,roomname):
	url='此处为反推的数据接口地址，涉及到安全问题，不予公开！请见谅！'
	
	query = {'nodeInText':room,'PartList':'','SelectPart':1}
	
	data=json.dumps(query)
	headers={'content-type':'application/json','Connection':'close'}
	timeout=30
	#s = requests.session()
	#s.config['keep_alive'] = False#及时关闭连接
	
	response = requests.post(url,data=data,headers=headers,timeout=timeout)

	regex=ur"tdSYValue\\u0027\\u003e[0-9]*[.]{0,1}[0-9]*" #剩余金额或度数
	result=response.text
	match = re.search(regex, result)
	if match:
    		result=match.group()
	#print result

	leftMoney=result[result.find('tdSYValue\u0027\u003e')+21:]
	if (unit=='yuan'):
		leftMoney=str(round(string.atof(leftMoney)/0.5950,2))
	if (type=='air'):
		print roomname+'（【空调】剩余电量）：'+leftMoney+'度'
	else:
		print roomname+'（【照明】剩余电量）：'+leftMoney+'度'
	cx = sqlite3.connect("ccnumeter.db")
	cu=cx.cursor()
	cx.execute("insert into meterlog (mroom,mvalue,type,roomname) values ('"+room+"','"+leftMoney+"','"+type+"','"+roomname+"')")
	cx.commit();
	cu.close()
	cx.close()

print GetNowTime()

f = open("meters_boy_girl.txt","r")
for m in f:
	meter_list=m.strip().split("：")
	#print meter_list[0]+','+meter_list[1]+','+meter_list[2]
	try:
		getMeterData(meter_list[1],meter_list[3],meter_list[2],meter_list[0])
	except requests.exceptions.Timeout:
  		print "服务器没有响应，获取（"+meter_list[0]+"）电量超时！"
	time.sleep(30)