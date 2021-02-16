from json import dumps
from requests import post,get
#import requests
from re import findall,sub
from tkinter import Tk,Text,Button,Listbox,messagebox,Label,font,Menu,Entry,Checkbutton,IntVar,PhotoImage,Toplevel
from tkinter import ttk
#import tkinter.messagebox
from time import sleep
import os
import base64
import stateDict
import copy

# 本查价器使用python原生桌面编译器tkinter制作

global shanhui_flag # 是否存在闪回赛季
global season_num   # 赛季数 S13,S14...
global postUrl
global geturl
global OrbTrans
global disable
global impdicts
global expdicts
global dictlist
global disableHelmAccessory
disableHelmAccessory = [1,1,1,1,1,1,1,1]
disable = [1,1,1,1,1]
img = '''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'''''
OrbTrans = {'混沌石':'chaos','幻色石':'chrom','改造石':'alt','重铸石':'scour','点金石':'alch','后悔石':'regret','链接石':'fuse','神圣石':'divine','机会石':'chance','珠宝匠的棱镜':'gcp','瓦尔宝珠':'vaal','工匠石':'jew'}
season_num = '10'
shanhui_flag = 0
postUrl = 'http://poe.game.qq.com/api/trade/search/S'+ season_num + '%E8%B5%9B%E5%AD%A3'
geturl = 'http://poe.game.qq.com/trade/search/S'+ season_num + '%E8%B5%9B%E5%AD%A3'
state = stateDict.state
impdicts = {}
expdicts = {}
encdicts = {}
dictlist = ['','']
explitlist =  state['result'][1]['entries']  #外延词缀
implitlist =  state['result'][2]['entries']  #基底词缀
enclitlist =  state['result'][4]['entries']  #附魔词缀
for i in explitlist:
	dictlist[0] = i['id']
	dictlist[1] = i['type']
	expdicts[copy.deepcopy(i['text'])] = copy.deepcopy(dictlist)

for i in implitlist:
	dictlist[0] = i['id']
	dictlist[1] = i['type']
	impdicts[copy.deepcopy(i['text'])] = copy.deepcopy(dictlist)

for i in enclitlist:
	dictlist[0] = i['id']
	dictlist[1] = i['type']
	encdicts[copy.deepcopy(i['text'])] = copy.deepcopy(dictlist)


impdicts['魔力保留降低 #%'] = impdicts['魔力保留提高 #%'] #游戏内词缀与网页词缀不一致，下同
expdicts['魔力保留降低 #%'] = impdicts['魔力保留提高 #%']
expdicts['物理伤害提高 #%'] = ['explicit.stat_1310194496','explicit']
expdicts['武器物理伤害提高 #%'] = ['explicit.stat_1509134228','explicit']
expdicts['该装备的护甲与能量护盾提高 #%'] = expdicts['该装备的护甲与能量护盾提高 #% (区域)']
expdicts['该装备的闪避与能量护盾提高 #%'] = expdicts['该装备的闪避与能量护盾提高 #% (区域)']
expdicts['该装备的护甲与闪避提高 #%'] = expdicts['该装备的护甲与闪避提高 #% (区域)']
win = Tk()
win.title("POE国服简易查价器V2.1")    # 窗口标题
screenWidth = win.winfo_screenwidth()
screenHeight = win.winfo_screenheight()
     
x = int((screenWidth -600) / 2)
y = int((screenHeight - 600) / 2)
win.geometry("600x600+%s+%s" % (x,y)) 

tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(img))
tmp.close()
win.iconbitmap('tmp.ico')  # 加图标
os.remove("tmp.ico") 
#menubar = Menu(win)
#filemenu = Menu(menubar, tearoff=0)
#menubar.add_cascade(label='区服选择', menu=filemenu)


#切换赛季区
def season():
	global postUrl
	global geturl
	postUrl = 'http://poe.game.qq.com/api/trade/search/S'+ season_num + '%E8%B5%9B%E5%AD%A3'
	geturl = 'http://poe.game.qq.com/trade/search/S'+ season_num + '%E8%B5%9B%E5%AD%A3'

#切换永久区
def forever():
	global postUrl
	global geturl
	postUrl = 'http://poe.game.qq.com/api/trade/search/%E6%B0%B8%E4%B9%85'
	geturl = 'http://poe.game.qq.com/trade/search/%E6%B0%B8%E4%B9%85'

#切换闪回区
def shanhui():
	global postUrl
	global geturl
	postUrl = 'http://poe.game.qq.com/api/trade/search/S'+ season_num + '%E9%97%AA%E5%9B%9E%E7%8B%82%E6%AC%A2'
	geturl = 'http://poe.game.qq.com/trade/search/S'+ season_num + '%E9%97%AA%E5%9B%9E%E7%8B%82%E6%AC%A2'
	
#filemenu.add_command(label='永久区', command=forever)
#filemenu.add_command(label='S11赛季区', command=season)

#win.config(menu=menubar)
# 查价函数
def searchPrice(types,name = [],kind = 0,mapLevel = '1',gemLevel = '1',money='chaos',payloadList = {}):
	# payloadData数据
	if name and kind != 5:
		payloadData = {
			"query":{"status":{"option":"any"},"type":types,"name":name,"stats":[{"type":"and","filters":[], "disabled": "false"}]},
			"sort":{"price":"asc"}
		}
	elif kind == 1:
		payloadData ={
			"query":{
			"status":{"option":"any"},"type":{"option":types,"discriminator":"warfortheatlas"},
			"stats":[{"type":"and","filters":[],"disabled":1}],
			"filters":{"map_filters":{"filters":{"map_tier":{"min":mapLevel,"max":mapLevel}},"disabled":0}}
			},
			"sort":{"price":"asc"}
			}
	elif kind == 2:
		payloadData ={
			"query":{
			"status":{"option":"any"},"type":types,
			"stats":[{"type":"and","filters":[],"disabled":1}],
			"filters":{"misc_filters":{"filters":{"gem_level":{"min":gemLevel,"max":gemLevel}},"disabled":0}}
			},
			"sort":{"price":"asc"}
			}
		#filters: {trade_filters: {filters: {price: {min: null, max: null, option: "chaos"}}, disabled: false}}
	elif kind == 3:
		payloadData ={
			"query":{
			"status":{"option":"any"},"type":types,
			"stats":[{"type":"and","filters":[],"disabled":1}],
			"filters":{"trade_filters":{"filters":{"price":{"min":"null","max":"null","option":money}},"disabled":0}}
			},
			"sort":{"price":"asc"}
			}
	elif kind == 4:
		payloadData ={
			"query":{
			"status":{"option":"any"},"type":{"option":types,"discriminator":"warfortheatlas"},
			"stats":[{"type":"and","filters":[],"disabled":1}],
			"filters":{"map_filters":{"filters":{"map_tier":{"min":mapLevel,"max":mapLevel},"map_blighted": {"option": "true"}},"disabled":0}}
			},
			"sort":{"price":"asc"}
			}
	elif kind == 5:
		
		payloadData ={
			"query":{
			"status":{"option":"any"},
			"type":{"option":types,"discriminator":"warfortheatlas"},
			"name":{"option":name,"discriminator":"warfortheatlas"},
			"stats":[{"type":"and","filters":[],"disabled":1}],
			"filters":{"map_filters":{"filters":{"map_tier":{"min":mapLevel,"max":mapLevel}},"disabled":0}}
			},
			"sort":{"price":"asc"}
			}
	elif kind == 6:
		payloadData = payloadList
	else:
		payloadData = {
			"query":{"status":{"option":"any"},"type":types,"stats":[{"type":"and","filters":[], "disabled": 1}]},
			"sort":{"price":"asc"}
		}
	# 请求头设置
	
	payloadHeader = {
		'Host': 'poe.game.qq.com',
		'Content-Type': 'application/json',
	}
	try:
		r = post(postUrl, data=dumps(payloadData), headers=payloadHeader) # 根据请求头获取query ID以及物品ID
		sleep(0.5)
		id = findall(r'"id":"([\d\D]*?)"',r.text) # query ID
		item = findall(r'"result":\[([\d\D]*?)\]',r.text)[0][1:-1].replace('"','').split(',') # 物品ID
		RequestURL = "http://poe.game.qq.com/api/trade/fetch/"+','.join(item[0:10])+"?query="+id[0]
		res= get(RequestURL)
		sleep(0.5)
		text1 = findall(r'"note":"([\d\D]*?)",',res.text)
		if len(item) >= 10:
			RequestURL = "http://poe.game.qq.com/api/trade/fetch/"+','.join(item[10:20])+"?query="+id[0] # 根据协议以及query ID和物品ID获取物品实际属性（价格，物主ID等...）
			res= get(RequestURL)
			sleep(0.1)
			text2 = findall(r'"note":"([\d\D]*?)",',res.text)
			text = text1 +text2
		else:
		   text = text1 
		text.reverse()
		m = ','.join(text).replace('\\','').replace('~b','   ~b')
		text = m.split(',')
		for i in list(range(len(text)-1,-1,-1)):
			if text[i][0] != '~' and text[i][0] != '=' and text[i][0] != ' ' :
				text.pop(i)	
		return text
	except:
		return []




def search(types,name = [],kind = 0,mapLevel = '1',gemLevel = '1',money = 'chaos',payloadList = {}, is_show_info = 1):
	for i in range(3):
		listText = searchPrice(types,name,kind,mapLevel,gemLevel, money = money,payloadList = payloadList)
		if listText:
			return listText
		elif i == 2:
			if is_show_info == 1:
				messagebox.showinfo('提示','无数据返回！请重试！\n原因可能是版本过低、网络环境差、交易网站崩溃或市集无货')
			return []

def Noresult():
	messagebox.showinfo('提示','不支持当前查找或查询方式错误')

#查询赛季信息
	
def search_season_information():
	global shanhui_flag
	global season_num
	global postUrl
	global geturl
	RequestURL = 'http://poe.game.qq.com/trade/search/'
	for _ in range(3):
		res = get(RequestURL).text
		season_num = findall(r'S([0-9]{2})\\u8d5b\\u5b63',res)
		if season_num != []:
			season_num = season_num[0]
			shanhui_flag = findall(r'S([0-9]{2})\\u95ea\\u56de',res)
			if shanhui_flag != []:
				shanhui_flag = 1
			else:
				shanhui_flag = 0
			break
	season()

search_season_information()

def findID(text):
	false = 0 
	true = 1

	talentnum = 0
	groovenum = 0
	id = ['enchant.stat_3086156145', '', 'explicit.stat_4288473380', 'explicit.stat_3274270612', 'explicit.stat_507505131', 'explicit.stat_4079888060']
	disable = [1,1,1,1,1,1]
	id[2] = 'explicit.stat_4288473380'
	talant = findall('其中 [1-2] 个增加的天赋为【([\d\D]*?)】',text)
	
	global expdicts
	global impdicts 
	talendoptiondict = stateDict.talendoptiondict
	
	talentnum = int(findall('增加 ([\d]{1,2}) 个天赋技能',text)[0])
	
	id[0] =  'enchant.stat_3086156145'
	
	for i in range(len(talant)):
		if talant[i] != '珠宝槽':
			id[i+2] = expdicts['其中 1 个增加的天赋为【'+talant[i] +'】'][0]
			disable[i+2] = 0
		else:
			id[5] = expdicts['其中 # 个增加的天赋为【'+talant[i] +'】'][0]
			disable[5] = 0
			groovenum = int(findall('其中 ([1-2]) 个增加的天赋为【珠宝槽】',text)[0])
	if not findall('妄想症',text):
		disable[0] = 0
		disable[1] = 0
		talenttext = findall('增加的小天赋获得：([\d\D]*?) \(',text)[0]
		option = int(talendoptiondict[talenttext])
		load = {"query":{"status":{"option":"any"},"filters": {"misc_filters": {"disabled": 0, "filters": {"corrupted": {"option": "false"}}}},"stats":[{"type":"and","filters":[{"id":id[2],"disabled":disable[2]},{"id":id[3],"disabled":disable[3]},{"id":id[4],"disabled":disable[4]},{"id":id[5],"disabled":disable[5],"value":{"min":groovenum,"max":groovenum}},{"id":id[0],"disabled":disable[0],"value":{"min":talentnum,"max":talentnum}},{"id":"enchant.stat_3948993189","disabled":disable[1],"value":{"option":option}}],"disabled":false}]},"sort":{"price":"asc"}}
	else:
		option = 1
		load = {"query":{"status":{"option":"any"},"name":"妄想症","type":"中型星团珠宝","filters": {"misc_filters": {"disabled": 1, "filters": {"corrupted": {"option": "false"}}}},"stats":[{"type":"and","filters":[{"id":id[2],"disabled":disable[2]},{"id":id[3],"disabled":disable[3]},{"id":id[4],"disabled":disable[4]},{"id":id[5],"disabled":disable[5],"value":{"min":groovenum,"max":groovenum}},{"id":id[0],"disabled":disable[0],"value":{"min":talentnum,"max":talentnum}},{"id":"enchant.stat_3948993189","disabled":disable[1],"value":{"option":option}}],"disabled":false}]},"sort":{"price":"asc"}}
	return load


def d(selectwin,var1,var2,var3,var4,stataTextList):
	selectwin.quit()

def charge(stataTextList,index):
	global disable
	if stataTextList[index] != '无':
		if disable[index] == 0:
			disable[index] = 1
		else:
			disable[index] = 0

def stateSelectFrame(stataTextList,value,disable):
	selectwin = Tk()
	selectwin.title("POE国服简易查价器V2.0")    # #窗口标题
	screenWidth = selectwin.winfo_screenwidth()
	screenHeight = selectwin.winfo_screenheight()
	x = int((screenWidth -300) / 2)
	y = int((screenHeight - 200) / 2)
	selectwin.geometry("300x200+%s+%s" % (x,y))
	ft2 = font.Font(size=13) 
	#selectt = Text(selectwin)
	#selectt.place(relx=0, rely=0, relwidth=0.8, relheight=0.86)
	#selectt.delete(0.0,'end')
	#selectt.insert('1.4','\n'.join(stataTextList))
	while len(stataTextList) < 4:
		stataTextList.append('无')
	var1 = IntVar()
	var2 = IntVar()
	var3 = IntVar()
	var4 = IntVar()
	chkb1 = Checkbutton(selectwin,text = stataTextList[0],width = 30, pady = 15,anchor = 'w',variable = var1,command= lambda:charge(stataTextList,0))
	chkb1.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.20)
	chkb1.select()
	chkb2 = Checkbutton(selectwin,text = stataTextList[1],width = 30, pady = 15,anchor = 'w',variable = var2,command= lambda:charge(stataTextList,1))
	chkb2.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.20)
	chkb2.select()
	chkb3 = Checkbutton(selectwin,text = stataTextList[2],width = 30, pady = 15,anchor = 'w',variable = var3,command= lambda:charge(stataTextList,2))
	chkb3.place(relx=0.2, rely=0.4, relwidth=0.8, relheight=0.20)
	chkb3.select()
	chkb4 = Checkbutton(selectwin,text = stataTextList[3],width = 30, pady = 15,anchor = 'w',variable = var4,command= lambda:charge(stataTextList,3))
	chkb4.place(relx=0.2, rely=0.6, relwidth=0.8, relheight=0.2)
	chkb4.select()
	chkB2 = Button(selectwin, text ="确       定", command= lambda:d(selectwin,var1,var2,var3,var4,stataTextList))#, command=root.destroy
	chkB2.place(relx=0.25, rely=0.8, relwidth=0.5, relheight=0.15)
	selectwin.mainloop()
	selectwin.destroy()



def findjewstate(items,threeJew = 0):
	items = '\n'.join(items).split('--------')
	id = ['enchant.stat_3086156145', 'explicit.stat_3274270612', 'explicit.stat_507505131', 'explicit.stat_4079888060','explicit.stat_3299347043']
	global disable
	disable = [1,1,1,1,1]
	value = [0,0,0,0]
	change = 1
	global encdicts
	global expdicts
	global impdicts
	if items[-2].strip() == '已腐化':
		stataText = items[-3-threeJew].strip()
		if items[-5].strip()[-3:] == 'it)' :
			change = 0
			t = items[-5].strip()[:-11]
			t = sub('[0-9\.]{1,5}','#',t)
			id[4] = impdicts[t][0]
			disable[4] = 0
	else:
		stataText = items[-2-threeJew].strip()
	if threeJew :
		stataTextList = stataText.split('\n')[3:]
	else:
		stataTextList = stataText.split('\n')
	if len(stataTextList)<=4:
		for i in range(len(stataTextList)):
		
			stataTextList[i] = stataTextList[i].replace('+','')
			t = sub('[0-9\.]{1,5}','#',stataTextList[i])
		
		
			valuelist = findall('[0-9\.]{1,5}',stataTextList[i])
			if not expdicts.__contains__(t):
				for j in range(len(valuelist)):
					t = sub(valuelist[j],'#',stataTextList[i])
					if expdicts.__contains__(t):
						id[i] = expdicts[t][0]
						disable[i] = 0
						break
			else :
				id[i] = expdicts[t][0]
				disable[i] = 0
			if len(valuelist) == 1:
				try:
					value[i] = int(valuelist[0])
				except:
					value[i] = float(valuelist[0])
			else:
				value[i] = int(valuelist[0] + valuelist[1])
	else:
		messagebox.showinfo('提示','暂不支持复合词缀的查价！')
		return {}
	stateSelectFrame(stataTextList,value,disable)
	
	load = {"query":{"status":{"option":"any"},"filters": {"misc_filters": {"disabled": change, "filters": {"corrupted": {"option": "true"}}}},"stats":[{"type":"and","filters":[{"id":id[0],"disabled":disable[0],"value":{"min":value[0]}},{"id":id[1],"disabled":disable[1],"value":{"min":value[1]}},{"id":id[2],"disabled":disable[2],"value":{"min":value[2]}},{"id":id[3],"disabled":disable[3],"value":{"min":value[3]}},{"id":id[4],"disabled":disable[4]}],"disabled":0}]},"sort":{"price":"asc"}}
	disable = [1,1,1,1,1]
	return load

#生成护甲或饰品的请求头
#def findHelmAccessory(items):
#	global encdicts
#	global expdicts
#	global impdicts
#	id = ['enchant.stat_3086156145', 'explicit.stat_3274270612', 'enchant.stat_3086156145', 'explicit.stat_3274270612','explicit.stat_507505131', 'explicit.stat_4079888060','explicit.stat_3299347043']
#	global disableHelmAccessory
#	disableHelmAccessory = [1,1,1,1,1,1,1,1]
#	value = [0,0,0,0,0,0,0,0]
#	ObjectKinds = {'符':'accessory.amulet','带':'accessory.belt','指':'accessory.ring',
#			   '冠':'armour.helmet','盔':'armour.helmet','兜':'armour.helmet','帽':'armour.helmet','面':'armour.helmet', '环':'armour.helmet',
#			   '手':'armour.gloves','手套':'armour.gloves','套':'',
#			    '心':'armour.chest','外套':'armour.chest','衣':'armour.chest','袍':'armour.chest','甲':'armour.chest','铠':'armour.chest','装':'armour.chest',
#				'胫甲':'armour.boots','鞋':'armour.boots','靴':'armour.boots',
#			   }
#	specialState = ['塑界','裂界','圣战','督军','救赎','狩猎']
#	if items[2][-1] == '甲' :
#		if items[2][-2:] == '胫甲':
#			option = ObjectKinds[items[2][-2:]]
#		else:
#			option = ObjectKinds[items[2][-1]]
#	elif items[2][-1] == '套':
#		option = ObjectKinds[items[2][-2:]]
#	else:
#		option = ObjectKinds[items[2][-1]]
#	specialStateList = [0,0,0,0,0,0]
#	trueFalseList = ["false","true"]
#	item = '\n'.join(items).split('--------')
#	specialStateItem = item[-2].strip().split('\n')
#	for i in specialStateItem:
#		if i[0:2] in specialState:
#			specialStateList[specialState.index(i[0:2])] = 1
#		else:
#		   break
#	if (not (1 in specialStateList)):
#		if item[-2].strip() != '已腐化':
#			stataTextList = item[-2].strip().split('\n')
#		else:
#			stataTextList = item[-3].strip().split('\n')
#	else: 
#		if item[-3].strip() != '已腐化':
#			stataTextList = item[-3].strip().split('\n')
#		else:
#			stataTextList = item[-4].strip().split('\n')
#	if len(stataTextList)<=7:
#		for i in range(len(stataTextList)):
#			stataTextList[i] = stataTextList[i].replace('+','')
#			t = sub('[0-9\.]{1,5}','#',stataTextList[i])
#			valuelist = findall('[0-9\.]{1,5}',stataTextList[i])
#			if not expdicts.__contains__(t):
#				for j in range(len(valuelist)):
#					t = sub(valuelist[j],'#',stataTextList[i])
#					if expdicts.__contains__(t):
#						id[i] = expdicts[t][0]
#						disableHelmAccessory[i] = 0
#						break
#			else :
#				id[i] = expdicts[t][0]
#				disableHelmAccessory[i] = 0
#			if len(valuelist) == 1:
#				try:
#					value[i] = int(valuelist[0])
#				except:
#					value[i] = float(valuelist[0])
#			else:
#				value[i] = (int(int(valuelist[0]) + int(valuelist[1])))/2
#	else:
#		messagebox.showinfo('提示','暂不支持复合词缀的查价！')
#		return {}
#	stateSelectFrame(stataTextList,value,disableHelmAccessory)
#	payload = {"query":{"status":{"option":"any"},"stats":[{"type":"and","filters":[{"id":"explicit.stat_4079888060","disabled":false,"value":{"min":1}},{"id":"explicit.stat_177215332","disabled":false}],"disabled":false}],"filters":{"type_filters":{"filters":{"category":{"option":option}}},"misc_filters":{"disabled":false,"filters":{"shaper_item":{"option":"true"},"crusader_item":{"option":"true"},"hunter_item":{"option":"true"},"elder_item":{"option":"true"},"redeemer_item":{"option":"true"},"warlord_item":{"option":"true"},"ilvl":{"min":82}}}}},"sort":{"price":"asc"}}


def getSearchType():
	items = t.get(0.0,'end').split('\n')
	ObjectKinds = {'符':'accessory.amulet','带':'accessory.belt','指':'accessory.ring',
			   '冠':'armour.helmet','盔':'armour.helmet','兜':'armour.helmet','帽':'armour.helmet','面':'armour.helmet','冠':'armour.helmet','环':'armour.helmet',
			   '手':'armour.gloves','手套':'armour.gloves','套':'',
			    '心':'armour.chest','外套':'armour.chest','衣':'armour.chest','袍':'armour.chest','甲':'armour.chest','铠':'armour.chest','装':'armour.chest',
				'胫甲':'armour.boots','鞋':'armour.boots','靴':'armour.boots',
			   }
	if len(items) <=2 :
		Noresult()
		return 0
	if (items[2][-4:] == '星团珠宝' or items[1][-4:] == '星团珠宝') and (items[1] == '天神之音' or items[0] != '稀 有 度: 传奇' or items[1] == '妄想症'):
		if items[1] == '天神之音':
			pricenum = int(findall('增加 ([1-9]) 个无特殊效果的小天赋','\n'.join(items))[0])
			payloadList = {"query":{"status":{"option":"any"},"name":"天神之音","type":"大型星团珠宝","stats":[{"type":"and","filters":[{"id":"explicit.stat_1085446536","value":{"min":pricenum,"max":pricenum},"disabled":0}]}]},"sort":{"price":"asc"}}
		else:
			payloadList = findID('\n'.join(items))
		priceList = search('',kind = 6,payloadList = payloadList)
	elif (items[2][-3:] == '蓝珠宝' or items[1][-3:] == '蓝珠宝' or items[2][-3:] == '红珠宝' or items[1][-3:] == '红珠宝' or items[2][-3:] == '绿珠宝' or items[1][-3:] == '绿珠宝') and items[0] != '稀 有 度: 传奇':
		payloadList = findjewstate(items)
		if payloadList != {}:
			priceList = search('',kind = 6,payloadList = payloadList)
	#elif items[2][-4:] == '三相珠宝':
	#	payloadList = findjewstate(items,threeJew = 1)
	#	priceList = search('',kind = 6,payloadList = payloadList)
	#elif ObjectKinds.__contains__(items[2][-1]):
	#	payloadList = findHelmAccessory(items)
	elif items[3] == '--------':
		if items[4][0:2] == '地图':
			name = []
			types = items[2].split()[0].split(':')[-1]
			kind = 1
			if types == '菌潮':
				kind = 4
				types = items[2].split()[1].split(':')[-1]
			level = items[4].split()[1]
			if items[0] == '稀 有 度: 传奇':
				kind = 5
				name = items[1].split()[0].split(':')[-1]
			priceList = search(types,name = name,kind = kind,mapLevel = level)
		else:
			types = items[2]
			name = items[1]
			priceList = search(types,name)

	elif items[-3] == '右键点击后赋予你的角色预言之力。':
			name = items[1].split('/')[0]
			types = "预言"
			priceList = search(types,name)

	elif items[3][0:2] == '地图':
		if findall('(地图)',items[1]):
			items[1] = ' '.join(items[1].split()[0:-1])
		types = items[1].split('的')[-1].split('之')[-1].split()[0].split(':')[-1]
		kind = 1
		if len(types) == 1 :
			types = items[1][-4:]
		elif types == '菌潮':
			types = items[1].split('的')[-1].split('之')[-1].split()[1].split(':')[-1]
		if findall('(菌潮)',items[1]):
			kind = 4
			#types = items[1].split('的')[-1].split('之')[-1].split()[1].split(':')[-1]
		level = items[3].split()[1]
		priceList = search(types,kind = kind,mapLevel = level)

	elif items[2] == '--------':
		if items[0] == '稀 有 度: 命运卡':
			types = items[1].split('[')[0]
			priceList = search(types)
		elif items[0] == '稀 有 度: 宝石':
			types = items[1].split('[')[0]
			kind = 2
			gemLevel = items[4].split()[1][0:2]
			priceList = search(types,kind = kind,gemLevel = gemLevel)
		else :
			types = items[1].split('[')[0]
			if types[0:2] == '奴役' or types[0:2] == '压迫' or types[0:2] == '灭绝' or types[0:2] == '清算' :
				types = types[0:4]
			elif types[0:2] == '地图':
				types = types.split()[0].split(':')[-1]
			
			priceList = search(types)

	else: 
		Noresult()
		return 0
	
	listb.delete(0, 'end')
	for item in priceList:
		listb.insert(0,item)



def deleteText():
	t.delete(0.0,'end')

def searchEXA():
	global OrbTrans
	text = Cmb2.get()
	money = OrbTrans[text]
	priceList = search('崇高石',kind = 3,money = money)
	if priceList == [] or priceList[0]=='':
		t2.delete(0.0,'end')
		t2.insert('1.4','无')
	else:
		price = priceList[int(len(priceList)/2)].split()[1]
		t2.delete(0.0,'end')
		t2.insert('1.4',' '+price)

#def closeSupportFrame(supportwin):
#	supportwin.destroy()
#def supportFrame():
#	supportwin = Toplevel()
#	supportwin.title("POE国服简易查价器V2.1")    # #窗口标题
#	screenWidth = supportwin.winfo_screenwidth()
#	screenHeight = supportwin.winfo_screenheight()
#	maimg = '''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'''''
#	authormaimg = '''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'''''
#	x = int((screenWidth -400) / 2)
#	y = int((screenHeight - 300) / 2)
#	supportwin.geometry("400x300+%s+%s" % (x,y))   # #窗口位置500后面是字母x
#	supportInfoL1 = Label(supportwin, text="微信扫码赞助 感谢(*╯3╰)：")
#	supportInfoL1.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)
#	supportInfoL2 = Label(supportwin, text="加微信私聊定制详情：")
#	supportInfoL2.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.1)
#	supportt = Text(supportwin)
#	tmp = open("tmp.png", "wb+")
#	tmp.write(base64.b64decode(maimg))
#	tmp.close()
#	photo = PhotoImage(file='tmp.png')
#	supportt.image_create('end', image=photo)
#	os.remove("tmp.png") 
#	supportt.place(relx=0, rely=0.1, relwidth=0.5, relheight=0.72)
#	customt = Text(supportwin)
#	tmp1 = open("tmp.png", "wb+")
#	tmp1.write(base64.b64decode(authormaimg))
#	tmp1.close()
#	photo2 = PhotoImage(file='tmp.png')
#	customt.image_create('end', image=photo2)
#	os.remove("tmp.png") 
#	customt.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.72)
#	supportCheckB = Button(supportwin, text ="返   回", command = lambda:closeSupportFrame(supportwin))
#	supportCheckB.place(relx=0.25, rely=0.82, relwidth=0.5, relheight=0.18)
#	supportwin.mainloop()


listb  = Listbox(win)          #  创建列表组件
listb.place(relx=0.5, rely=0.04, relwidth=0.5, relheight=0.84)#side = tkinter.RIGHT) 
ft = font.Font(size=20) 
ft2 = font.Font(size=13) 

#supportL = Label(win, text="支持赞助作者/功能定制（你的支持是我不断更新下去的不竭动力~(～￣▽￣)～）请点击->")
#supportL.place(relx=0, rely=0, relwidth=0.8, relheight=0.04)
#supportB = Button(win, text ="支 持 / 定 制", command = supportFrame)
#supportB.place(relx=0.8, rely=0, relwidth=0.21, relheight=0.044)



t = Text(win,height=30,width = 40)
t.place(relx=0, rely=0.04, relwidth=0.5, relheight=0.84)

t2 = Text(win,font = ft)
t2.place(relx=0.663, rely=0.94, relwidth=0.137, relheight=0.06)

B1 = Button(win, text ="查    找", command = getSearchType)
B1.place(relx=0.25, rely=0.88, relwidth=0.253, relheight=0.12)


B2 = Button(win, text ="删    除", command = deleteText)
B2.place(relx=0, rely=0.88, relwidth=0.25, relheight=0.12)

B3 = Button(win, text ="查  询", command = searchEXA)
B3.place(relx=0.903, rely=0.94, relwidth=0.097, relheight=0.06)

Cmb = ttk.Combobox(win,font = ft2, state='readonly')
Cmb.place(relx=0.663, rely=0.88, relwidth=0.337, relheight=0.06)
cmb_tuple = ()
if shanhui_flag == 0:
	cmb_tuple = ('      '+ season_num + '赛季区','       永久区')
else:
	cmb_tuple = ('      '+ season_num + '赛季区', '       永久区', '      '+ season_num + '闪回区')
Cmb['value'] = cmb_tuple
Cmb.current(0)

def Selectarea(event):
	text = Cmb.get()
	if '赛季区' in text:
		season()
	elif '永久区' in text:
		forever()
	else:
		shanhui()
Cmb.bind("<<ComboboxSelected>>",Selectarea,)

Cmb2 = ttk.Combobox(win, state='readonly')
Cmb2.place(relx=0.800, rely=0.94, relwidth=0.103, relheight=0.06)
Cmb2['value'] = ('混沌石','幻色石','改造石','重铸石','点金石','后悔石','链接石','神圣石','机会石','珠宝匠的棱镜','瓦尔宝珠','工匠石')
Cmb2.current(0)

#def SelectOrb(event):
#	text = Cmb.get()
#	if text == '      S11赛季区':
#		season()
#	else:
#		forever()
#Cmb2.bind("<<ComboboxSelected>>",Selectarea,)

L1 = Label(win, text="当前区服：",font = ft2)
L1.place(relx=0.503, rely=0.88, relwidth=0.16, relheight=0.06)

L2 = Label(win, text="当前E价：",font = ft2)
L2.place(relx=0.503, rely=0.94, relwidth=0.16, relheight=0.06)
#label1=tkinter.Label(win,text="物品输入框")
#label1.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)

messagebox.showinfo('提示','作者游戏论坛ID：Setless\n发布日期：2020.4.25\n最后更新日期：2021.2.16\n当前支持游戏版本为：所有，\n第一时间获取更新或者BUG反馈及建议请加Q群：975332215')
searchEXA()
win.mainloop()  
#dumpJsonData = json.dumps(payloadData)
#text = json.dumps(res.text)
#print(text)
#print(f"dumpJsonData = {dumpJsonData}")

#print(f"statusCode = {r.status_code}, r text = {r.text}")
#http://poe.game.qq.com/api/trade/data/stats  词缀
#http://poe.game.qq.com/api/trade/data/items  物品