#!/usr/bin/env python
# -*- coding: utf-8 -*-
#2016-02-02 13:18:28 by sixer

import matplotlib.pyplot as pl,sqlite3,sys
from matplotlib.ticker import MultipleLocator, FuncFormatter
import numpy as np
import matplotlib as mpl
import datetime,time

#mpl.rcParams['font.family'] = 'sans-serif'
#mpl.rcParams['font.sans-serif'] = [u'Microsoft Yahei']
zhfont = mpl.font_manager.FontProperties(fname='font/Microsoft Yahei.ttf')

MultipleLocator.MAXTICKS = 100000

def GetNowTime():

    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))


def makeGraphic(howmanydays,roomname,picname):

	#print roomname+","+picname

	fig = pl.figure(1,figsize=(11,5))

	cx = sqlite3.connect("ccnumeter.db")

	x = np.arange(0, howmanydays, 1)
	y = []#空调度数
	z = []#照明度数
	t = []#日期

 	today = datetime.date.today() #获得今天的日期

 	for i in xrange(1-howmanydays,1):
 		mydate= today + datetime.timedelta(days=i-1)
 		#print mydate

 		t.append(str(mydate))
		#以下查询最新的10条记录
		#cu=cx.execute("select * from (select mvalue,mdate from meterlog where roomname='"+roomname+"' and type='"+type+"' group by mdate order by mdate desc  limit 0,10) order by mdate")
		cu=cx.execute("select mdate, CASE WHEN type='light' THEN mvalue ELSE 0 END mvalue from meterlog where roomname='"+roomname+"' and mdate='"+str(mydate)+"' and type='light' group by mdate")
		cu_result=cu.fetchall()
		#print cu_result
		if len(cu_result)!=0 :
			#print 't'
			for row in cu_result:
				z.append(row[1])
		else:
			#print 'f'
			z.append(0)

		cu=cx.execute("select mdate, CASE WHEN type='air' THEN mvalue ELSE 0 END mvalue from meterlog where roomname='"+roomname+"' and mdate='"+str(mydate)+"' and type='air' group by mdate")
		cu_result=cu.fetchall()
		if len(cu_result)!=0 :
			for row in cu_result:
				y.append(row[1])
		else:
			y.append(0)


	cu.close()
	cx.close()
	#print z
	#print y
	#print x
	#print t
	#print np.max(x)
	

	pl.plot(x, z,'-ro', label=roomname+u'照明')
	pl.plot(x, y,'-bo',label=roomname+u'空调')

	for xz in zip(x,z):
    		pl.annotate(xz[1], xy=xz, xytext=(2,5),fontsize=6,fontproperties=zhfont,textcoords = 'offset points')

	for xy in zip(x,y):
    		pl.annotate(xy[1], xy=xy, xytext=(2,5),fontsize=6,fontproperties=zhfont,textcoords = 'offset points')
	
	ax = pl.gca()

	ax.xaxis.set_major_locator(MultipleLocator(1))
	ax.yaxis.set_major_locator( MultipleLocator(25) )

	

	# 设置两个坐标轴的范围
	pl.ylim(0,250)
	pl.xlim(1, np.max(x)-1)



	# 设置图的底边距
	pl.subplots_adjust(bottom = 0.15)

	pl.grid() #开启网格


	#获取当前x轴的label
	locs,labels = pl.xticks()
	#print locs
	#重新设置新的label,用时间t设置
	pl.xticks(locs, t, fontsize=8)
	#设置Y轴字体
	pl.yticks(fontsize=9,fontproperties=zhfont)

	pl.title(u'华中师大-信技学院-2015级研究生宿舍剩余电量',fontsize=12,fontproperties=zhfont)  
	#pl.xlabel(u'日期')  
	pl.ylabel(u'剩余电量（单位：度）',fontsize=8,fontproperties=zhfont) 

	pl.legend(prop=zhfont)

	#自动调整label显示方式，如果太挤则倾斜显示
	fig.autofmt_xdate()

	#保存曲线为图片格式
	pl.savefig("./pics/"+picname+".png")
	#pl.show()
	#print 'succ'
	pl.close(1)


def makeWarningGraphic(type):

	#print roomname+","+picname

	fig = pl.figure(2,figsize=(11,4))


	#pl.sca(p1)

	cx = sqlite3.connect("ccnumeter.db")

	y = []
	t = []

	mydate= datetime.date.today() - datetime.timedelta(days=1)
	cu=cx.execute("select mvalue,roomname from meterlog where  mdate='"+str(mydate)+"' and type='"+type+"' group by roomname order by CAST(mvalue AS float) desc")
	cu_result=cu.fetchall()

	counter_y=len(cu_result)
	if len(cu_result)!=0 :
		for row in cu_result:
			y.append(row[0])
			t.append(row[1])
	else:
		y.append(0)
		t.append(u'暂无数据')
		counter_y=1
	
	x = np.arange(0, counter_y, 1)

	if type=='air':
		label=u'空调'
		colorsyle='-bo'
	else:
		label=u'照明'
		colorsyle='-ro'

	print x
	print y

	pl.plot(x, y,colorsyle,label=label)

	for xy in zip(x,y):
    		pl.annotate(xy[1], xy=xy, xytext=(2,5),fontsize=7,fontproperties=zhfont,textcoords = 'offset points')
    		#print xy

	cu.close()
	cx.close()
	
	#print np.max(x)
	
	
	ax = pl.gca()

	ax.xaxis.set_major_locator(MultipleLocator(1))
	ax.yaxis.set_major_locator( MultipleLocator(25) )

	

	# 设置两个坐标轴的范围
	pl.ylim(0,250)
	pl.xlim(1, np.max(x)-1)



	# 设置图的底边距
	pl.subplots_adjust(bottom = 0.15)

	pl.grid() #开启网格


	#获取当前x轴的label
	locs,labels = pl.xticks()
	#print locs
	#重新设置新的label,用时间t设置
	pl.xticks(locs, t, fontsize=8,fontproperties=zhfont)

	#设置Y轴字体
	pl.yticks(fontsize=9,fontproperties=zhfont)


	pl.title(u'昨日 '+str(mydate)+' '+label+u'剩余电量 排行榜（注意及时充电）',fontsize=12,fontproperties=zhfont)  
	#pl.xlabel(u'日期')  
	pl.ylabel(u'剩余电量（单位：度）',fontsize=8,fontproperties=zhfont) 

	pl.legend(prop=zhfont)

	#自动调整label显示方式，如果太挤则倾斜显示
	fig.autofmt_xdate()

	#保存曲线为图片格式
	pl.savefig("./pics/warning-"+type+".png")
	#pl.show()
	#print 'succ'
	pl.close(2)

print GetNowTime()
f = open("roomnames.txt","r")
for m in f:
	makeGraphic(30,m.strip().decode('utf-8'),m[m.find('-')+1:].strip())
makeWarningGraphic("light")
makeWarningGraphic("air")