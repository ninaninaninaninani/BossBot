# -*- coding: utf-8 -*- 

################ V4 #####################

import os
import sys
import asyncio
import discord
import datetime
import random
import math
from discord.ext import commands
from gtts import gTTS
from github import Github
from github import GithubException
import base64
import re

if not discord.opus.is_loaded():
	discord.opus.load_opus('opus')

basicSetting = []
bossData = []
fixed_bossData = []

bossNum = 0
fixed_bossNum = 0
chkvoicechannel = 0
chkrelogin = 0
chflg = 0
LoadChk = 0

bossTime = []
tmp_bossTime = []

fixed_bossTime = []

bossTimeString = []
bossDateString = []
tmp_bossTimeString = []
tmp_bossDateString = []

bossFlag = []
bossFlag0 = []
fixed_bossFlag = []
fixed_bossFlag0 = []
bossMungFlag = []
bossMungCnt = []

channel_info = []
channel_name = []
channel_id = []
channel_voice_name = []
channel_voice_id = []
channel_type = []

client = discord.Client()


access_token = os.environ["BOT_TOKEN"]			
git_access_token = os.environ["GIT_TOKEN"]			
git_access_repo = os.environ["GIT_REPO"]			
git_access_repo_restart = os.environ["GIT_REPO_RESTART"]			

g = Github(git_access_token)
repo = g.get_repo(git_access_repo)
repo_restart = g.get_repo(git_access_repo_restart)

def init():
	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fixed_bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global voice_client1
		
	global task1
	
	global channel_info
	global channel_name
	global channel_voice_name
	global channel_voice_id
	global channel_id
	global channel_type
	global LoadChk
	
	tmp_bossData = []
	tmp_fixed_bossData = []
	f = []
	fb = []
	#print("test")
	
	inidata = repo.get_contents("test_setting.ini")
	file_data1 = base64.b64decode(inidata.content)
	file_data1 = file_data1.decode('utf-8')
	inputData = file_data1.split('\n')
	
	boss_inidata = repo.get_contents("boss.ini")
	file_data3 = base64.b64decode(boss_inidata.content)
	file_data3 = file_data3.decode('utf-8')
	boss_inputData = file_data3.split('\n')

	fixed_inidata = repo.get_contents("fixed_boss.ini")
	file_data2 = base64.b64decode(fixed_inidata.content)
	file_data2 = file_data2.decode('utf-8')
	fixed_inputData = file_data2.split('\n')

	for i in range(inputData.count('\r')):
		inputData.remove('\r')
		
	for i in range(boss_inputData.count('\r')):
		boss_inputData.remove('\r')

	for i in range(fixed_inputData.count('\r')):
		fixed_inputData.remove('\r')

	del(boss_inputData[0])
	del(fixed_inputData[0])
		
	basicSetting.append(inputData[0][11:])   #basicSetting[0] : timezone
	basicSetting.append(inputData[5][15:])   #basicSetting[1] : before_alert
	basicSetting.append(inputData[7][10:])   #basicSetting[2] : mungChk
	basicSetting.append(inputData[6][16:])   #basicSetting[3] : before_alert1
	basicSetting.append(inputData[1][14:16]) #basicSetting[4] : restarttime 시
	basicSetting.append(inputData[1][17:])   #basicSetting[5] : restarttime 분
	basicSetting.append(inputData[2][15:])   #basicSetting[6] : voice채널 ID
	basicSetting.append(inputData[3][14:])   #basicSetting[7] : text채널 ID
	basicSetting.append(inputData[4][16:])   #basicSetting[8] : 사다리 채널 ID
	basicSetting.append(inputData[8][14:])   #basicSetting[9] : !ㅂ 출력 수
	
	for i in range(len(basicSetting)):
		basicSetting[i] = basicSetting[i].strip()
	
	if basicSetting[6] != "":
		basicSetting[6] = int(basicSetting[6])
		
	if basicSetting[7] != "":
		basicSetting[7] = int(basicSetting[7])
	#print (inputData, len(inputData))
	
	### 강제 채널 고정###
	#basicSetting[6] = int('00000000000') #보이스채널ID
	#basicSetting[7] = int('00000000000') #택스트채널ID
	
	bossNum = int(len(boss_inputData)/5)

	fixed_bossNum = int(len(fixed_inputData)/4) 
	
	#print (bossNum)
	
	for i in range(bossNum):
		tmp_bossData.append(boss_inputData[i*5:i*5+5])

	for i in range(fixed_bossNum):
		tmp_fixed_bossData.append(fixed_inputData[i*4:i*4+4]) 
		
	#print (tmp_bossData)
		
	for j in range(bossNum):
		for i in range(len(tmp_bossData[j])):
			tmp_bossData[j][i] = tmp_bossData[j][i].strip()

	for j in range(fixed_bossNum):
		for i in range(len(tmp_fixed_bossData[j])):
			tmp_fixed_bossData[j][i] = tmp_fixed_bossData[j][i].strip()
	############## 일반보스 정보 리스트 #####################
	for j in range(bossNum):
		tmp_len = tmp_bossData[j][1].find(':')
		f.append(tmp_bossData[j][0][11:])         #0 : 보스명
		f.append(tmp_bossData[j][1][10:tmp_len])  #1 : 시
		f.append(tmp_bossData[j][2][13:])         #2 : 멍/미입력
		f.append(tmp_bossData[j][3][20:])         #3 : 분전 알림멘트
		f.append(tmp_bossData[j][4][13:])         #4 : 젠 알림멘트
		f.append(tmp_bossData[j][1][tmp_len+1:])  #5 : 분
		f.append('')                              #6 : 메세지
		bossData.append(f)
		f = []
		bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0])))
		tmp_bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0])))
		bossTimeString.append('99:99:99')
		bossDateString.append('9999-99-99')
		tmp_bossTimeString.append('99:99:99')
		tmp_bossDateString.append('9999-99-99')
		bossFlag.append(False)
		bossFlag0.append(False)
		bossMungFlag.append(False)
		bossMungCnt.append(0)
	
	tmp_fixed_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
	
	############## 고정보스 정보 리스트 #####################
	for j in range(fixed_bossNum):
		tmp_fixed_len = tmp_fixed_bossData[j][1].find(':')
		fb.append(tmp_fixed_bossData[j][0][11:])               #0 : 보스명
		fb.append(tmp_fixed_bossData[j][1][11:tmp_fixed_len])  #1 : 시
		fb.append(tmp_fixed_bossData[j][1][tmp_fixed_len+1:])  #2 : 분
		fb.append(tmp_fixed_bossData[j][2][20:])               #3 : 분전 알림멘트
		fb.append(tmp_fixed_bossData[j][3][13:])               #4 : 젠 알림멘트
		fixed_bossData.append(fb)
		fb = []
		fixed_bossFlag.append(False)
		fixed_bossFlag0.append(False)
		fixed_bossTime.append(tmp_fixed_now.replace(hour=int(fixed_bossData[j][1]), minute=int(fixed_bossData[j][2]), second = int(0)))
		if fixed_bossTime[j] < tmp_fixed_now :
			fixed_bossTime[j] = fixed_bossTime[j] + datetime.timedelta(days=int(1))

	print ('보탐봇 재시작 시간 : ', basicSetting[4], '시 ', basicSetting[5], '분')
	print ('보스젠알림시간1 : ', basicSetting[1])
	print ('보스젠알림시간2 : ', basicSetting[3])
	print ('보스멍확인시간 : ', basicSetting[2])

init()

endTime = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
endTime = endTime.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
tmp_endTime = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

if endTime < tmp_endTime:
	endTime = endTime + datetime.timedelta(days = 1)

channel = ''

async def task():
	await client.wait_until_ready()

	global channel
	global endTime
		
	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime
	
	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fiexd_bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global voice_client1
		
	global task1
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type
	
	if chflg == 1 : 
		if voice_client1.is_connected() == False :
			voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
			if voice_client1.is_connected() :
				await dbLoad()
				await client.get_channel(channel).send( '<다시 왔습니다.!>', tts=False)
			
	while not client.is_closed():
		now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
		priv0 = now+datetime.timedelta(minutes=int(basicSetting[3]))
		priv = now+datetime.timedelta(minutes=int(basicSetting[1]))
		aftr = now+datetime.timedelta(minutes=int(0-int(basicSetting[2])))

		nowTimeString = now.strftime('%H:%M:%S')
		nowDateString = now.strftime('%Y-%m-%d')
		endTimeString = endTime.strftime('%H:%M:%S')
		endDateString = endTime.strftime('%Y-%m-%d')


		if channel != '':			
			################ 보탐봇 재시작 ################ 
			if endTimeString == nowTimeString and endDateString == nowDateString:
				for i in range(bossNum):
					if bossMungFlag[i] == True:
						bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
						bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
				await dbSave()
				await client.get_channel(channel).send('<갑자기 인사해도 놀라지마세요!>', tts=False)
				await asyncio.sleep(2)

				inidata_restart = repo_restart.get_contents("restart.txt")
				file_data_restart = base64.b64decode(inidata_restart.content)
				file_data_restart = file_data_restart.decode('utf-8')
				inputData_restart = file_data_restart.split('\n')

				if len(inputData_restart) < 3:	
					contents12 = repo_restart.get_contents("restart.txt")
					repo_restart.update_file(contents12.path, "restart_0", "restart\nrestart\nrestrat\n", contents12.sha)
				else:
					contents12 = repo_restart.get_contents("restart.txt")
					repo_restart.update_file(contents12.path, "restart_1", "", contents12.sha)

				endTime = endTime + datetime.timedelta(days = 1)

			################ 고정 보스 확인 ################ 
			for i in range(fixed_bossNum):
				################ before_alert1 ################ 
				if fixed_bossTime[i] <= priv0 and fixed_bossTime[i] > priv:
					if basicSetting[3] != '0':
						if fixed_bossFlag0[i] == False:
							fixed_bossFlag0[i] = True
							await client.get_channel(channel).send("```" + fixed_bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + fixed_bossData[i][3] +' [' +  fixed_bossTime[i].strftime('%H:%M:%S') + ']```', tts=False)
							await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '알림1.mp3')

				################ before_alert ################ 
				if fixed_bossTime[i] <= priv and fixed_bossTime[i] > now:
					if basicSetting[1] != '0' :
						if fixed_bossFlag[i] == False:
							fixed_bossFlag[i] = True
							await client.get_channel(channel).send("```" + fixed_bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + fixed_bossData[i][3] +' [' +  fixed_bossTime[i].strftime('%H:%M:%S') + ']```', tts=False)
							await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '알림.mp3')
				
				################ 보스 젠 시간 확인 ################
				if fixed_bossTime[i] <= now :
					fixed_bossTime[i] = fixed_bossTime[i]+datetime.timedelta(days=int(1))
					fixed_bossFlag0[i] = False
					fixed_bossFlag[i] = False
					embed = discord.Embed(
							description= "```" + fixed_bossData[i][0] + '탐 ' + fixed_bossData[i][4] + "```" ,
							color=0x00ff00
							)
					await client.get_channel(channel).send(embed=embed, tts=False)
					await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '젠.mp3')

			################ 일반 보스 확인 ################ 
			for i in range(bossNum):
				################ before_alert1 ################ 
				if bossTime[i] <= priv0 and bossTime[i] > priv:
					if basicSetting[3] != '0':
						if bossFlag0[i] == False:
							bossFlag0[i] = True
							await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3] + " [" +  bossTimeString[i] + "]```", tts=False)
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림1.mp3')

				################ before_alert ################
				if bossTime[i] <= priv and bossTime[i] > now:
					if basicSetting[1] != '0' :
						if bossFlag[i] == False:
							bossFlag[i] = True
							await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3] + " [" +  bossTimeString[i] + "]```", tts=False)
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림.mp3')

				################ 보스 젠 시간 확인 ################ 
				if bossTime[i] <= now :
					#print ('if ', bossTime[i])
					bossMungFlag[i] = True
					tmp_bossTime[i] = bossTime[i]
					tmp_bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
					tmp_bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
					bossTimeString[i] = '99:99:99'
					bossDateString[i] = '9999-99-99'
					bossTime[i] = now+datetime.timedelta(days=365)
					embed = discord.Embed(
							description= "```" + bossData[i][0] + '탐 ' + bossData[i][4] + "```" ,
							color=0x00ff00
							)
					await client.get_channel(channel).send(embed=embed, tts=False)
					await PlaySound(voice_client1, './sound/' + bossData[i][0] + '젠.mp3')

				################ 보스 자동 멍 처리 ################ 
				if bossMungFlag[i] == True:
					if (bossTime[i]+datetime.timedelta(days=-365)) <= aftr:
						if basicSetting[2] != '0':
							################ 미입력 보스 ################
							if bossData[i][2] == '0':
								await client.get_channel(channel).send("```" +  bossData[i][0] + ' 미입력 됐습니다.```', tts=False)
								await PlaySound(voice_client1, './sound/' + bossData[i][0] + '미입력.mp3')
								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = bossMungCnt[i] + 1
								tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
								tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
								tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
								embed = discord.Embed(
									description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
									color=0xff0000
									)
								await client.get_channel(channel).send(embed=embed, tts=False)
							################ 멍 보스 ################
							else :
								await client.get_channel(channel).send("```" + bossData[i][0] + ' 멍 입니다.```')
								await PlaySound(voice_client1, './sound/' + bossData[i][0] + '멍.mp3')
								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = bossMungCnt[i] + 1
								tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
								tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
								tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
								embed = discord.Embed(
									description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
									color=0xff0000
									)
								await client.get_channel(channel).send(embed=embed, tts=False)

		await asyncio.sleep(1) # task runs every 60 seconds

#mp3 파일 생성함수(gTTS 이용, 남성목소리)
async def MakeSound(saveSTR, filename):
	tts = gTTS(saveSTR, lang = 'ko')
	tts.save('./' + filename + '.mp3')

#mp3 파일 재생함수	
async def PlaySound(voiceclient, filename):
	source = discord.FFmpegPCMAudio(filename)
	try:
		voiceclient.play(source)
	except discord.errors.ClientException:
		while voiceclient.is_playing():
			await asyncio.sleep(1)
	while voiceclient.is_playing():
		await asyncio.sleep(1)
	voiceclient.stop()
	source.cleanup()

#my_bot.db 저장하기
async def dbSave():
	global bossData
	global bossNum
	global bossTime
	global bossTimeString
	global bossDateString
	global bossMungCnt

	for i in range(bossNum):
		for j in range(bossNum):
			if bossTimeString[i] and bossTimeString[j] != '99:99:99':
				if bossTimeString[i] == bossTimeString[j] and i != j:
					tmp_time1 = bossTimeString[j][:6]
					tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
					if tmp_time2 < 10 :
						tmp_time22 = '0' + str(tmp_time2)
					elif tmp_time2 == 60 :
						tmp_time22 = '00'
					else :
						tmp_time22 = str(tmp_time2)
					bossTimeString[j] = tmp_time1 + tmp_time22
					
	datelist1 = bossTime
	
	datelist = list(set(datelist1))

	information1 = '----- 보스탐 정보 -----\n'
	for timestring in sorted(datelist):
		for i in range(bossNum):
			if timestring == bossTime[i]:
				if bossTimeString[i] != '99:99:99' :
					if bossData[i][2] == '0' :
						information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][6] + '\n'
					else : 
						information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (멍 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][6] + '\n'
						
	try :
		contents = repo.get_contents("my_bot.db")
		repo.update_file(contents.path, "bossDB", information1, contents.sha)
	except GithubException as e :
		print ('save error!!')
		print(e.args[1]['message']) # output: This repository is empty.
		errortime = datetime.datetime.now()
		print (errortime)
		pass



#my_bot.db 불러오기
async def dbLoad():
	global LoadChk
	
	contents1 = repo.get_contents("my_bot.db")
	file_data = base64.b64decode(contents1.content)
	file_data = file_data.decode('utf-8')
	beforeBossData = file_data.split('\n')
	
	if len(beforeBossData) > 1:	
		for i in range(len(beforeBossData)-1):
			for j in range(bossNum):
				startPos = beforeBossData[i+1].find('-')
				endPos = beforeBossData[i+1].find('(')
				if beforeBossData[i+1][startPos+2:endPos] == bossData[j][0] :
				#if beforeBossData[i+1].find(bossData[j][0]) != -1 :
					tmp_mungcnt = 0
					tmp_len = beforeBossData[i+1].find(':')
					tmp_datelen = beforeBossData[i+1].find('@')
					tmp_msglen = beforeBossData[i+1].find('*')

					
					years1 = beforeBossData[i+1][tmp_datelen+2:tmp_datelen+6]
					months1 = beforeBossData[i+1][tmp_datelen+7:tmp_datelen+9]
					days1 = beforeBossData[i+1][tmp_datelen+10:tmp_datelen+12]
					
					hours1 = beforeBossData[i+1][tmp_len+2:tmp_len+4]
					minutes1 = beforeBossData[i+1][tmp_len+5:tmp_len+7]
					seconds1 = beforeBossData[i+1][tmp_len+8:tmp_len+10]
					
					now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

					tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
					tmp_now = tmp_now.replace(year = int(years1), month = int(months1), day = int(days1), hour=int(hours1), minute=int(minutes1), second = int(seconds1))

					if tmp_now < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[j][1]), minutes = int(bossData[j][5]))
						while now2 > tmp_now :
							tmp_now = tmp_now + deltaTime
							tmp_mungcnt = tmp_mungcnt + 1
					
					now2 = tmp_now

					tmp_bossTime[j] = bossTime[j] = now2
					tmp_bossTimeString[j] = bossTimeString[j] = bossTime[j].strftime('%H:%M:%S')
					tmp_bossDateString[j] = bossDateString[j] = bossTime[j].strftime('%Y-%m-%d')
					
					bossData[j][6] = beforeBossData[i+1][tmp_msglen+2:len(beforeBossData[i+1])]

					if beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3] != 0 and beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] == ' ':
						bossMungCnt[j] = int(beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3]) + tmp_mungcnt
					elif beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] != ' ':
						bossMungCnt[j] = int(beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] + beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3]) + tmp_mungcnt
					else:
						bossMungCnt[j] = 0
		LoadChk = 0
		print ("<불러오기 완료>")
	else:
		#await client.get_channel(channel).send('<보스타임 정보가 없습니다.>', tts=False)
		LoadChk = 1
		print ("보스타임 정보가 없습니다.")

#음성채널 입장
async def JointheVC(VCchannel, TXchannel):
	global chkvoicechannel
	global voice_client1

	if VCchannel is not None:
		if chkvoicechannel == 0:
			voice_client1 = await VCchannel.connect(reconnect=True)
			if voice_client1.is_connected():
				await voice_client1.disconnect()
				voice_client1 = await VCchannel.connect(reconnect=True)
			chkvoicechannel = 1
			await PlaySound(voice_client1, './sound/hello.mp3')
		else :
			await voice_client1.disconnect()
			voice_client1 = await VCchannel.connect(reconnect=True)
			await PlaySound(voice_client1, './sound/hello.mp3')
	else:
		await TXchannel.send('음성채널에 먼저 들어가주세요.', tts=False)

#사다리함수
async def LadderFunc(number, ladderlist, channelVal):
	if number < len(ladderlist):
		result_ladder = random.sample(ladderlist, number)
		result_ladderSTR = ','.join(map(str, result_ladder))
		embed = discord.Embed(
			title = "----- 당첨! -----",
			description= '```' + result_ladderSTR + '```',
			color=0xff00ff
			)
		await channelVal.send(embed=embed, tts=False)
	else:
		await channelVal.send('```추첨인원이 총 인원과 같거나 많습니다. 재입력 해주세요```', tts=False)

## 명치 예외처리	
def handle_exit():
	#print("Handling")
	client.loop.run_until_complete(client.logout())

	for t in asyncio.Task.all_tasks(loop=client.loop):
		if t.done():
		#t.exception()
			try:
			#print ('try :   ', t)
				t.exception()
			except asyncio.CancelledError:
			#print ('cancel :   ', t)
				continue
			continue
		t.cancel()
		try:
			client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
			t.exception()
		except asyncio.InvalidStateError:
			pass
		except asyncio.TimeoutError:
			pass
		except asyncio.CancelledError:
			pass

# 봇이 구동되었을 때 동작되는 코드입니다.
@client.event
async def on_ready():
	global task1
	global channel
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type
	
	global chkvoicechannel
	global chflg
			
	print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
	print(client.user.name)
	print(client.user.id)
	print("===========")

	
	#await joinVoiceChannel()
	all_channels = client.get_all_channels()
	
	for channel1 in all_channels:
		channel_type.append(str(channel1.type))
		channel_info.append(channel1)
	
	for i in range(len(channel_info)):
		if channel_type[i] == "text":
			channel_name.append(str(channel_info[i].name))
			channel_id.append(str(channel_info[i].id))
			
	for i in range(len(channel_info)):
		if channel_type[i] == "voice":
			channel_voice_name.append(str(channel_info[i].name))
			channel_voice_id.append(str(channel_info[i].id))

	await dbLoad()
	
	if basicSetting[6] != "" and basicSetting[7] != "" :
		#print ('join channel')
		await JointheVC(client.get_channel(basicSetting[6]), client.get_channel(basicSetting[7]))
		await client.get_channel(basicSetting[7]).send('< 텍스트채널 [' + client.get_channel(basicSetting[7]).name + '] 접속완료>', tts=False)
		await client.get_channel(basicSetting[7]).send('< 음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>', tts=False)
		await client.get_channel(basicSetting[7]).send('< 보탐봇 재시작 설정시간 ' + basicSetting[4] + '시 ' + basicSetting[5] + '분입니다. >', tts=False)
		channel = basicSetting[7]
		chflg = 1

	# 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
	# 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
	await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="여어!히사시부리!", type=1))

while True:
	# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
	@client.event
	async def on_message(msg):
		if msg.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
			return None #동작하지 않고 무시합니다.

		global channel
		
		global basicSetting
		global bossData
		global fixed_bossData

		global bossNum
		global fixed_bossNum
		global chkvoicechannel
		global chkrelogin

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		
		global voice_client1
			
		global task1
		
		global channel_info
		global channel_name
		global channel_id
		global channel_voice_name
		global channel_voice_id
		global channel_type
		
		global chflg
		global LoadChk
		
		id = msg.author.id #id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
		
		if chflg == 0 :
			channel = int(msg.channel.id) #channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다
			if basicSetting[7] == "":
				inidata_textCH = repo.get_contents("test_setting.ini")
				file_data_textCH = base64.b64decode(inidata_textCH.content)
				file_data_textCH = file_data_textCH.decode('utf-8')
				inputData_textCH = file_data_textCH.split('\n')
				
				for i in range(len(inputData_textCH)):
					if inputData_textCH[i] == 'textchannel = \r':
						inputData_textCH[i] = 'textchannel = ' + str(channel) + '\r'
						basicSetting[7] = channel
						#print ('======', inputData_text[i])
				
				result_textCH = '\n'.join(inputData_textCH)
				
				#print (result_textCH)
				
				contents = repo.get_contents("test_setting.ini")
				repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)

			await client.get_channel(channel).send('< 텍스트채널 [' + client.get_channel(channel).name + '] 접속완료>', tts=False)
				
			if basicSetting[6] != "":
				#print ('join channel')
				await JointheVC(client.get_channel(basicSetting[6]), channel)
				await client.get_channel(channel).send('< 음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>', tts=False)

			await client.get_channel(channel).send('< 보탐봇 재시작 설정시간 ' + basicSetting[4] + '시 ' + basicSetting[5] + '분입니다. >', tts=False)
			chflg = 1
			
		if client.get_channel(channel) != msg.channel :
			##### 사다리 채널바꾸기
			if basicSetting[8] != "":
				if msg.channel.id == int(basicSetting[8]): #### 사다리 채널ID 값넣으면 됨
					message = await msg.channel.fetch_message(msg.id)
					##################################

					if message.content.startswith('!사다리'):
						ladder = []
						ladder = message.content[5:].split(" ")
						num_cong = int(ladder[0])
						del(ladder[0])
						await LadderFunc(num_cong, ladder, msg.channel)
				else :
					return None
			else :
				return None
			#return None
		else :
			message = await client.get_channel(channel).fetch_message(msg.id)
			
			##################################

			if message.content == '!채널확인' :
				ch_information = ''
				for i in range(len(channel_name)):
					ch_information += '[' + channel_id[i] + '] ' + channel_name[i] + '\n'

				ch_voice_information = ''
				for i in range(len(channel_voice_name)):
					ch_voice_information += '[' + channel_voice_id[i] + '] ' + channel_voice_name[i] + '\n'
				print (ch_information)
				print (ch_voice_information)
				embed = discord.Embed(
					title = "----- 채널 정보 -----",
					description= '',
					color=0xff00ff
					)
				embed.add_field(
					name="< 택스트 채널 >",
					value= '```' + ch_information + '```',
					inline = False
					)
				embed.add_field(
					name="< 보이스 채널 >",
					value= '```' + ch_voice_information + '```',
					inline = False
					)
				await client.get_channel(channel).send( embed=embed, tts=False)

			##################################

			if message.content.startswith('!채널이동'):
				tmp_sayMessage1 = message.content
				
				for i in range(len(channel_name)):
					if  channel_name[i] == str(tmp_sayMessage1[6:]):
						channel = int(channel_id[i])
						
				inidata_textCH = repo.get_contents("test_setting.ini")
				file_data_textCH = base64.b64decode(inidata_textCH.content)
				file_data_textCH = file_data_textCH.decode('utf-8')
				inputData_textCH = file_data_textCH.split('\n')
				
				for i in range(len(inputData_textCH)):
					if inputData_textCH[i] == 'textchannel = ' + str(basicSetting[7]) + '\r':
						inputData_textCH[i] = 'textchannel = ' + str(channel) + '\r'
						basicSetting[7] = int(channel)
				
				result_textCH = '\n'.join(inputData_textCH)

				contents = repo.get_contents("test_setting.ini")
				repo.update_file(contents.path, "test_setting", result_textCH, contents.sha)
					
				await client.get_channel(channel).send('< ' + client.get_channel(channel).name + ' 이동완료>', tts=False)
			
			hello = message.content

			##################################

			for i in range(bossNum):
				if message.content.startswith(bossData[i][0] +' 컷'):
					if hello.find('  ') != -1 :
						bossData[i][6] = hello[hello.find('  ')+2:]
						hello = hello[:hello.find('  ')]
					else:
						bossData[i][6] = ''
						
					tmp_msg = bossData[i][0] +' 컷'
					if len(hello) > len(tmp_msg) + 3 :
						if hello.find(':') != -1 :
							chkpos = hello.find(':')
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos+1:chkpos+3]
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							chkpos = len(hello)-2
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos:chkpos+2]
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = now2

					bossFlag[i] = False
					bossFlag0[i] = False
					bossMungFlag[i] = False
					bossMungCnt[i] = 0

					if tmp_now > now2 :
						tmp_now = tmp_now + datetime.timedelta(days=int(-1))
						
					if tmp_now < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
						while now2 > tmp_now :
							tmp_now = tmp_now + deltaTime
							bossMungCnt[i] = bossMungCnt[i] + 1
						now2 = tmp_now
						bossMungCnt[i] = bossMungCnt[i] - 1
					else :
						now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
								
					tmp_bossTime[i] = bossTime[i] = nextTime = now2
					tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
					tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
					embed = discord.Embed(
							description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
							color=0xff0000
							)
					await client.get_channel(channel).send(embed=embed, tts=False)

			##################################

				if message.content.startswith(bossData[i][0] +'멍'):
					if hello.find('  ') != -1 :
						bossData[i][6] = hello[hello.find('  ')+2:]
						hello = hello[:hello.find('  ')]
					else:
						bossData[i][6] = ''
						
					tmp_msg = bossData[i][0] +'멍'
					tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))

					if len(hello) > len(tmp_msg) + 3 :
						if hello.find(':') != -1 :
							chkpos = hello.find(':')
							hours1 = hello[chkpos-2:chkpos] 
							minutes1 = hello[chkpos+1:chkpos+3]					
							temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							chkpos = len(hello)-2
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos:chkpos+2]					
							temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						
						nextTime = temptime + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
						
						bossMungCnt[i] = 0
						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = bossMungCnt[i] + 1

						if nextTime > tmp_now :
							nextTime = nextTime + datetime.timedelta(days=int(-1))

						if nextTime < tmp_now :
							deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							while tmp_now > nextTime :
								nextTime = nextTime + deltaTime
								bossMungCnt[i] = bossMungCnt[i] + 1
						else :
							nextTime = nextTime

						tmp_bossTime[i] = bossTime[i] = nextTime				

						tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
						tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
						embed = discord.Embed(
								description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
								color=0xff0000
								)
						await client.get_channel(channel).send(embed=embed, tts=False)
					else:
						if tmp_bossTime[i] < tmp_now :

							nextTime = tmp_bossTime[i] + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))

							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False
							bossMungCnt[i] = bossMungCnt[i] + 1

							tmp_bossTime[i] = bossTime[i] = nextTime				

							tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
							embed = discord.Embed(
									description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
									color=0xff0000
									)
							await client.get_channel(channel).send(embed=embed, tts=False)
						else:
							await client.get_channel(channel).send('```' + bossData[i][0] + '탐이 아직 안됐습니다. 다음 ' + bossData[i][0] + '탐 [' + tmp_bossTimeString[i] + '] 입니다```', tts=False)

					
##################################

			for i in range(bossNum):
				if message.content.startswith(bossData[i][0], 4, 8):
					if hello.find('  ') != -1 :
						bossData[i][6] = hello[hello.find('  ')+2:]
						hello = hello[:hello.find('  ')]
						hello = filter(str.isdigit,hello))
					else:
						bossData[i][6] = ''
						
					tmp_msg = bossData[i][0]
					if len(hello) > len(tmp_msg) + 3 :
						if hello.find(':') != -1 :
							chkpos = hello.find(':')
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos+1:chkpos+3]
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							i = filter(str.isdigit,hello))
							chkpos = len(i)-2
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos:chkpos+2]
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						
						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = 0

						if tmp_now < now2 :
							tmp_now = tmp_now + datetime.timedelta(days=int(1))

						tmp_bossTime[i] = bossTime[i] = nextTime = tmp_now
						tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
						tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
						embed = discord.Embed(
								description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
								color=0xff0000
								)
						await client.get_channel(channel).send(embed=embed, tts=False)
					else:
						await client.get_channel(channel).send(bossData[i][0] +' 예상 시간을 입력해주세요.', tts=False)
						
			##################################

					
				if message.content == bossData[i][0] +'삭제':
					bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
					tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365, hours = int(basicSetting[0]))
					bossTimeString[i] = '99:99:99'
					bossDateString[i] = '9999-99-99'
					tmp_bossTimeString[i] = '99:99:99'
					tmp_bossDateString[i] = '9999-99-99'
					bossFlag[i] = (False)
					bossFlag0[i] = (False)
					bossMungFlag[i] = (False)
					bossMungCnt[i] = 0
					await client.get_channel(channel).send('<' + bossData[i][0] + ' 삭제완료>', tts=False)
					await dbSave()
					print ('<' + bossData[i][0] + ' 삭제완료>')
				
			if message.content == '!오빠':
				await PlaySound(voice_client1, './sound/오빠.mp3')
			if message.content == '!언니':
				await PlaySound(voice_client1, './sound/언니.mp3')
			if message.content == '!형':
				await PlaySound(voice_client1, './sound/형.mp3')

			##################################

			if message.content.startswith('!분배'):
				separate_money = []
				separate_money = message.content[4:].split(" ")
				num_sep = int(separate_money[0])
				cal_tax1 = math.ceil(float(separate_money[1])*0.05)
				real_money = int(int(separate_money[1]) - cal_tax1)
				cal_tax2 = int(real_money/num_sep) - math.ceil(float(int(real_money/num_sep))*0.95)
				if num_sep == 0 :
					await client.get_channel(channel).send('```분배 인원이 0입니다. 재입력 해주세요.```', tts=False)
				else :
					await client.get_channel(channel).send('```1차세금 : ' + str(cal_tax1) + '\n1차 수령액 : ' + str(real_money) + '\n분배자 거래소등록금액 : ' + str(int(real_money/num_sep)) + '\n2차세금 : ' + str(cal_tax2) + '\n인당 실수령액 : ' + str(int(float(int(real_money/num_sep))*0.95)) + '```', tts=False)

			##################################

			if message.content.startswith('!사다리'):
				ladder = []
				ladder = message.content[5:].split(" ")
				num_cong = int(ladder[0])
				del(ladder[0])
				await LadderFunc(num_cong, ladder, client.get_channel(channel))
				
			##################################
			
			if message.content == '!메뉴' :
				embed = discord.Embed(
						title = "----- 메뉴 -----",
						description= '```!현재시간\n!채널확인\n!채널이동 [채널명]\n!소환\n!불러오기\n!초기화\n!재시작\n!명치\n!미예약\n!분배 [인원] [금액]\n!사다리 [뽑을인원수] [아이디1] [아이디2] ...\n!보스일괄 00:00 또는 !보스일괄 0000\n!ㅂ,ㅃ,q\n\n[보스명]컷\n[보스명]컷 00:00 또는 [보스명]컷 0000\n[보스명]멍\n[보스명]멍 00:00 또는 [보스명]멍 0000\n[보스명]예상 00:00 또는 [보스명]예상 0000\n[보스명]삭제\n보스탐\n!보스탐\n!리젠```',
						color=0xff00ff
						)
				embed.add_field(
						name="----- 추가기능 -----",
						value= '(보스명)컷/멍/예상  (할말) : 보스시간 입력 후 빈칸 두번!! 메모 가능'
						)
				await client.get_channel(channel).send(embed=embed, tts=False)

			##################################

			if message.content == '!미예약':
				temp_bossTime2 = []
				for i in range(bossNum):
					if bossTimeString[i] == '99:99:99' :
						temp_bossTime2.append(bossData[i][0])

				if len(temp_bossTime2) != 0:
					temp_bossTimeSTR1 = ','.join(map(str, temp_bossTime2))
					temp_bossTimeSTR1 = '```fix\n' + temp_bossTimeSTR1 + '\n```'
				else:
					temp_bossTimeSTR1 = '``` ```'
						
				embed = discord.Embed(
						title = "----- 미예약보스 -----",
						description= temp_bossTimeSTR1,
						color=0x0000ff
						)
				await client.get_channel(channel).send( embed=embed, tts=False)

			##################################		
				
			if message.content.startswith('!v') or message.content.startswith('!ㅍ') or message.content.startswith('!V'):
				tmp_sayMessage = message.content
				sayMessage = tmp_sayMessage[3:]
				await MakeSound(message.author.display_name +'님이.' + sayMessage, './sound/say')
				await client.get_channel(channel).send("```< " + msg.author.display_name + " >님이 \"" + sayMessage + "\"```", tts=False)
				await PlaySound(voice_client1, './sound/say.mp3')

			##################################

			if message.content == '!재시작':
				for i in range(bossNum):
					if bossMungFlag[i] == True:
						bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
						bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
				await dbSave()
				await client.get_channel(channel).send('<보탐봇 재시작 중... 갑자기 인사해도 놀라지마세요!>', tts=False)
				await asyncio.sleep(2)

				inidata_restart = repo_restart.get_contents("restart.txt")
				file_data_restart = base64.b64decode(inidata_restart.content)
				file_data_restart = file_data_restart.decode('utf-8')
				inputData_restart = file_data_restart.split('\n')

				if len(inputData_restart) < 3:	
					contents12 = repo_restart.get_contents("restart.txt")
					repo_restart.update_file(contents12.path, "restart_0", "restart\nrestart\nrestrat\n", contents12.sha)
				else:
					contents12 = repo_restart.get_contents("restart.txt")
					repo_restart.update_file(contents12.path, "restart_1", "", contents12.sha)
				
			#############################

			if message.content =='!소환':
				if message.author.voice == None:
					await client.get_channel(channel).send('음성채널에 먼저 들어가주세요.', tts=False)
				else:
					voice_channel = message.author.voice.channel

					if basicSetting[6] == "":
						inidata_voiceCH = repo.get_contents("test_setting.ini")
						file_data_voiceCH = base64.b64decode(inidata_voiceCH.content)
						file_data_voiceCH = file_data_voiceCH.decode('utf-8')
						inputData_voiceCH = file_data_voiceCH.split('\n')

						for i in range(len(inputData_voiceCH)):
							if inputData_voiceCH[i] == 'voicechannel = \r':
								inputData_voiceCH[i] = 'voicechannel = ' + str(voice_channel.id) + '\r'
								basicSetting[6] = int(voice_channel.id)

						result_voiceCH = '\n'.join(inputData_voiceCH)

						contents = repo.get_contents("test_setting.ini")
						repo.update_file(contents.path, "test_setting", result_voiceCH, contents.sha)

					elif basicSetting[6] != int(voice_channel.id):
						inidata_voiceCH = repo.get_contents("test_setting.ini")
						file_data_voiceCH = base64.b64decode(inidata_voiceCH.content)
						file_data_voiceCH = file_data_voiceCH.decode('utf-8')
						inputData_voiceCH = file_data_voiceCH.split('\n')

						for i in range(len(inputData_voiceCH)):
							if inputData_voiceCH[i] == 'voicechannel = ' + str(basicSetting[6]) + '\r':
								inputData_voiceCH[i] = 'voicechannel = ' + str(voice_channel.id) + '\r'
								basicSetting[6] = int(voice_channel.id)

						result_voiceCH = '\n'.join(inputData_voiceCH)

						contents = repo.get_contents("test_setting.ini")
						repo.update_file(contents.path, "test_setting", result_voiceCH, contents.sha)


					await JointheVC(voice_channel, channel)
					await client.get_channel(channel).send('< 음성채널 [' + client.get_channel(voice_channel.id).name + '] 접속완료>', tts=False)
			
			##################################
						
			if message.content == '!초기화':
				basicSetting = []
				bossData = []

				bossTime = []
				tmp_bossTime = []

				fixed_bossTime = []

				bossTimeString = []
				bossDateString = []
				tmp_bossTimeString = []
				tmp_bossDateString = []

				bossFlag = []
				bossFlag0 = []
				fixed_bossFlag = []
				fixed_bossFlag0 = []
				bossMungFlag = []
				bossMungCnt = []
				
				init()

				await dbSave()

				await client.get_channel(channel).send('<초기화 완료>', tts=False)
				print ("<초기화 완료>")

			##################################
			
			if message.content.startswith('!보스일괄'):
				for i in range(bossNum):
					tmp_msg = '!보스일괄'
					if len(hello) > len(tmp_msg) + 3 :
						if hello.find(':') != -1 :
							chkpos = hello.find(':')
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos+1:chkpos+3]
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							chkpos = len(hello)-2
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos:chkpos+2]
							now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						now2 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
						tmp_now = now2
						
					bossFlag[i] = False
					bossFlag0[i] = False
					bossMungFlag[i] = False
					bossMungCnt[i] = 1

					if tmp_now > now2 :
						tmp_now = tmp_now + datetime.timedelta(days=int(-1))
						
					if tmp_now < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
						while now2 > tmp_now :
							tmp_now = tmp_now + deltaTime
							bossMungCnt[i] = bossMungCnt[i] + 1
						now2 = tmp_now
						bossMungCnt[i] = bossMungCnt[i] - 1
					else :
						now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
								
					tmp_bossTime[i] = bossTime[i] = nextTime = now2
					tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
					tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

				await dbSave()
				await dbLoad()
				await dbSave()
				
				await client.get_channel(channel).send('<보스 일괄 입력 완료>', tts=False)
				print ("<보스 일괄 입력 완료>")

			##################################


			if message.content == '!설정확인':			
				setting_val = '보탐봇 재시작 설정시간 : ' + basicSetting[4] + '시 ' + basicSetting[5] + '분\n' + '보스젠알림시간1 : ' + basicSetting[1] + ' 분 전\n' + '보스젠알림시간2 : ' + basicSetting[3] + ' 분 전\n' + '보스멍확인시간 : ' + basicSetting[2] + ' 분 후\n'
				embed = discord.Embed(
						title = "----- 설정내용 -----",
						description= '```' + setting_val + '```',
						color=0xff00ff
						)
				await client.get_channel(channel).send(embed=embed, tts=False)
				print ('보스젠알림시간1 : ', basicSetting[1])
				print ('보스젠알림시간2 : ', basicSetting[3])
				print ('보스멍확인시간 : ', basicSetting[2])

			##################################

			if message.content == '!불러오기' :
				await dbLoad()

				if LoadChk == 0:
					await client.get_channel(channel).send('<불러오기 완료>', tts=False)
				else:
					await client.get_channel(channel).send('<보스타임 정보가 없습니다.>', tts=False)
			
			##################################
			
			if message.content == '!ㅂ' or message.content == '!q' or message.content == '!ㅃ' or message.content == '!Q':
				
				checkTime = datetime.datetime.now() + datetime.timedelta(days=1)

				sorted_datelist = []

				datelist = bossTime
				
				tmp_sorted_datelist = sorted(datelist)

				for i in range(len(tmp_sorted_datelist)):
					if checkTime > tmp_sorted_datelist[i]:
						sorted_datelist.append(tmp_sorted_datelist[i])
					
				if len(sorted_datelist) == 0:
					await client.get_channel(channel).send( '<보스타임 정보가 없습니다.>', tts=False)
				else : 
					result_lefttime = ''
					
					
					if len(sorted_datelist) > int(basicSetting[9]):
						for j in range(int(basicSetting[9])):
							for i in range(bossNum):
								if sorted_datelist[j] == bossTime[i]:
									leftTime = bossTime[i] - (datetime.datetime.now()  + datetime.timedelta(hours = int(basicSetting[0])))

									total_seconds = int(leftTime.total_seconds())
									hours, remainder = divmod(total_seconds,60*60)
									minutes, seconds = divmod(remainder,60)

									result_lefttime += '다음 ' + bossData[i][0] + '탐까지 %02d:%02d:%02d 남았습니다. ' % (hours,minutes,seconds) + '[' +  bossTimeString[i] + ']\n'
					else :
						for j in range(len(sorted_datelist)):
							for i in range(bossNum):						
								if sorted_datelist[j] == bossTime[i]:
									leftTime = bossTime[i] - (datetime.datetime.now()  + datetime.timedelta(hours = int(basicSetting[0])))

									total_seconds = int(leftTime.total_seconds())
									hours, remainder = divmod(total_seconds,60*60)
									minutes, seconds = divmod(remainder,60)

									result_lefttime += '다음 ' + bossData[i][0] + '탐까지 %02d:%02d:%02d 남았습니다. ' % (hours,minutes,seconds) + '[' +  bossTimeString[i] + ']\n'
									#result_lefttime += bossData[i][0] + '탐[' +  bossTimeString[i] + ']까지 ' + '%02d:%02d:%02d 남았습니다.\n' % (hours,minutes,seconds)

					embed = discord.Embed(
						description= result_lefttime,
						color=0xff0000
						)
					await client.get_channel(channel).send( embed=embed, tts=False)

			################ 보스타임 출력 ################ 

			if message.content == '보스탐' or message.content == '/1' or message.content == '/보스':
				
				datelist = []
				datelist2 = []
				temp_bossTime1 = []
				ouput_bossData = []
				aa = []
				
				for i in range(bossNum):
					if bossMungFlag[i] == True :
						datelist2.append(tmp_bossTime[i])
					else :
						datelist2.append(bossTime[i])

				for i in range(fixed_bossNum):
					if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours=int(basicSetting[0])+3):
						datelist2.append(fixed_bossTime[i])

				datelist = list(set(datelist2))

				for i in range(bossNum):
					if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
						temp_bossTime1.append(bossData[i][0])
					else :
						aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
						if bossMungFlag[i] == True :
							aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
							aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00)  *초 제거 희망시 '%H:%M:%S' -> '%H:%M'
							aa.append('-')	                                 #output_bossData[3] : -
						else :
							aa.append(bossTime[i])                           #output_bossData[1] : 시간            *초 제거 희망시 '%H:%M:%S' -> '%H:%M'
							aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00)
							aa.append('+')	                                 #output_bossData[3] : +
						aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
						aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
						aa.append(bossData[i][6])	                         #output_bossData[6] : 메세지
						ouput_bossData.append(aa)
						aa = []

				for i in range(fixed_bossNum):
					aa.append(fixed_bossData[i][0])                      #output_bossData[0] : 보스명
					aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
					aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : 시간(00:00:00)      *초 제거 희망시 '%H:%M:%S' -> '%H:%M'
					aa.append('@')                                       #output_bossData[3] : @
					aa.append(0)                                         #output_bossData[4] : 멍/미입력 보스
					aa.append(0)                                         #output_bossData[5] : 멍/미입력횟수
					aa.append("")                                        #output_bossData[6] : 메세지
					ouput_bossData.append(aa)
					aa = []

				if len(temp_bossTime1) != 0:
					temp_bossTimeSTR1 = ','.join(map(str, temp_bossTime1))
					temp_bossTimeSTR1 = '```fix\n' + temp_bossTimeSTR1 + '\n```'
				else:
					temp_bossTimeSTR1 = '``` ```'
							
				information = ''
				for timestring in sorted(datelist):
					for i in range(len(ouput_bossData)):
						if timestring == ouput_bossData[i][1]:
							if ouput_bossData[i][4] == '0' :
								if ouput_bossData[i][5] == 0 :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
								else :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
							else : 
								if ouput_bossData[i][5] == 0 :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
								else :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
			
				if len(information) != 0:
					information = "```diff\n" + information + "\n```"
				else :
					information = '``` ```'

				embed = discord.Embed(
						title = "----- 보스탐 정보 -----",
						description= information,
						color=0x0000ff
						)
				embed.add_field(
						name="----- 미예약보스 -----",
						value= temp_bossTimeSTR1,
						inline = False
						)
				
				await client.get_channel(channel).send( embed=embed, tts=False)

				await dbSave()

			################ 보스타임 출력(고정보스포함) ################ 

			if message.content == '!보스탐':

				datelist = []
				datelist2 = []
				temp_bossTime1 = []
				ouput_bossData = []
				aa = []
				
				for i in range(bossNum):
					if bossMungFlag[i] == True :
						datelist2.append(tmp_bossTime[i])
					else :
						datelist2.append(bossTime[i])

				datelist = list(set(datelist2))

				for i in range(bossNum):
					if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
						temp_bossTime1.append(bossData[i][0])
					else :
						aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
						if bossMungFlag[i] == True :
							aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
							aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00)   *초 제거 희망시 *초 제거 희망시 '%H:%M:%S' -> '%H:%M'
							aa.append('-')	                                 #output_bossData[3] : -
						else :
							aa.append(bossTime[i])                           #output_bossData[1] : 시간
							aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00)   *초 제거 희망시 *초 제거 희망시 '%H:%M:%S' -> '%H:%M'
							aa.append('+')	                                 #output_bossData[3] : +
						aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
						aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
						aa.append(bossData[i][6])	                         #output_bossData[6] : 메세지
						ouput_bossData.append(aa)
						aa = []

				fixed_information = ''
				for i in range(fixed_bossNum):
						tmp_timeSTR = fixed_bossTime[i].strftime('%H:%M:%S')  #*초 제거 희망시 '%H:%M:%S' -> '%H:%M'
						fixed_information += tmp_timeSTR + ' : ' + fixed_bossData[i][0] + '\n'

				if len(fixed_information) != 0:
					fixed_information = "```" + fixed_information + "```"
				else :
					fixed_information = '``` ```'

				temp_bossTime1 = []
				for i in range(bossNum):
					if bossTimeString[i] == '99:99:99' :
						temp_bossTime1.append(bossData[i][0])

				if len(temp_bossTime1) != 0:
					temp_bossTimeSTR1 = ','.join(map(str, temp_bossTime1))
					temp_bossTimeSTR1 = '```fix\n' + temp_bossTimeSTR1 + '\n```'
				else:
					temp_bossTimeSTR1 = '``` ```'
							
				information = ''
				for timestring in sorted(datelist):
					for i in range(len(ouput_bossData)):
						if timestring == ouput_bossData[i][1]:
							if ouput_bossData[i][4] == '0' :
								if ouput_bossData[i][5] == 0 :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
								else :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
							else : 
								if ouput_bossData[i][5] == 0 :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
								else :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
			
				if len(information) != 0:
					information = "```diff\n" + information + "\n```"
				else :
					information = '``` ```'

				embed = discord.Embed(
						title = "----- 고 정 보 스 -----",
						description= fixed_information,
						color=0x0000ff
						)
				embed.add_field(
						name="----- 보스탐 정보 -----",
						value=information,
						inline = False
						)
				embed.add_field(
						name="----- 미예약보스 -----",
						value= temp_bossTimeSTR1,
						inline = False
						)
				
				await client.get_channel(channel).send( embed=embed, tts=False)

				await dbSave()

			##################################

			if message.content == '!현재시간':
				now3 = datetime.datetime.now() + datetime.timedelta(hours = int(basicSetting[0]))
				await client.get_channel(channel).send(now3.strftime('%Y-%m-%d') + '   ' + now3.strftime('%H:%M:%S'), tts=False)

			##################################
			
			if message.content == '!리젠':
				embed = discord.Embed(
						title='----- 리스폰 보스 -----',
						description= ' ')
				embed.add_field(name='1시간', value='기감', inline=False)
				embed.add_field(name='2시간', value='서드,북드,카파,질풍,광풍,이프,자웜,개미', inline=False)
				embed.add_field(name='3시간', value='중드,동드,거드,마요,산적,자크,스피,가스트,대흑장로', inline=False)
				embed.add_field(name='4시간', value='아르,도펠', inline=False)
				embed.add_field(name='5시간', value='에자', inline=False)
				embed.add_field(name='6시간', value='감시자 데몬', inline=False)
				embed.add_field(name='6시간 53분', value='피닉스', inline=False)
				embed.add_field(name='7시간', value='데스나이트', inline=False)
				embed.add_field(name='10시간', value='리칸트, 커츠', inline=False)
				await client.get_channel(channel).send(embed=embed, tts=False)

			################ 명존쎄 ################ 

			if message.content == '!명치':
				await client.get_channel(channel).send( '<보탐봇 명치 맞고 숨 고르기 중! 잠시만요!>', tts=False)
				print("명치!")
				for i in range(bossNum):
					if bossMungFlag[i] == True:
						bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
						bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
				await dbSave()
				await voice_client1.disconnect()
				#client.clear()
				raise SystemExit

	client.loop.create_task(task())
	try:
		client.loop.run_until_complete(client.start(access_token))
	except SystemExit:
		handle_exit()
	except KeyboardInterrupt:
		handle_exit()
	#client.loop.close()
	#print("Program ended")
	#break

	print("Bot restarting")
	client = discord.Client(loop=client.loop)
