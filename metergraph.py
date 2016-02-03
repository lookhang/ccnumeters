#!/usr/bin/env python
# -*- coding: utf-8 -*-
#2016-02-02 13:18:28 by sixer

import matplotlib.pyplot as pl,sqlite3,sys
from matplotlib.ticker import MultipleLocator, FuncFormatter
import numpy as np
import matplotlib as mpl
import datetime

#mpl.rcParams['font.family'] = 'sans-serif'
#mpl.rcParams['font.sans-serif'] = [u'Microsoft Yahei']
zhfont = mpl.font_manager.FontProperties(fname='font/Microsoft Yahei.ttf')

MultipleLocator.MAXTICKS = 100000



def makeGraphic(howmanydays,roomname,picname):

	#print roomname+","+picname

	fig = pl.figure(1,figsize=(10,5))

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

	pl.title(u'华中师范大学-教育信息技术学院-2015级研究生宿舍剩余电量',fontproperties=zhfont)  
	#pl.xlabel(u'日期')  
	pl.ylabel(u'剩余电量（单位：度）',fontproperties=zhfont) 

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

	fig = pl.figure(2,figsize=(10,3))


	#pl.sca(p1)

	cx = sqlite3.connect("ccnumeter.db")

	y = []
	t = []

	mydate= datetime.date.today() - datetime.timedelta(days=1)
	cu=cx.execute("select mvalue,roomname from meterlog where  mdate='"+str(mydate)+"' and type='"+type+"' order by CAST(mvalue AS float) desc")
	counter_y=0
	for row in cu:
		y.append(row[0])
		t.append(row[1])
		counter_y=counter_y+1

	if counter_y==0:
		y.append(0)
	x = np.arange(0, counter_y, 1)

	if type=='air':
		label=u'空调'
		colorsyle='-bo'
	else:
		label=u'照明'
		colorsyle='-ro'

	pl.plot(x, y,colorsyle,label=label)



	cu.close()
	cx.close()
	#print y
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

	pl.title(u'昨日 '+str(mydate)+' '+label+u'剩余电量 排行榜（注意及时充电）',fontproperties=zhfont)  
	#pl.xlabel(u'日期')  
	pl.ylabel(u'剩余电量（单位：度）',fontproperties=zhfont) 

	pl.legend(prop=zhfont)

	#自动调整label显示方式，如果太挤则倾斜显示
	fig.autofmt_xdate()

	#保存曲线为图片格式
	pl.savefig("./pics/warning-"+type+".png")
	#pl.show()
	#print 'succ'
	pl.close(2)

f = open("roomnames.txt","r")
for m in f:
	makeGraphic(30,m.strip().decode('utf-8'),m[m.find('-')+1:].strip())
makeWarningGraphic("light")
makeWarningGraphic("air")