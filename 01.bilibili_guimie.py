import time
import csv
import requests
import json

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}#伪装成浏览器，绕过反爬
url='https://api.bilibili.com/pgc/review/short/list?media_id=22718131&ps=20&sort=0'
# 发送get请求
w = requests.get(url, headers=headers).text
json_comment=json.loads(w)
total=json_comment['data']['list']#url中list中存储的内容
num=json_comment['data']['total']#total中的内容，一共有多少个url
#用下面的话 太麻烦了 虽然变量多了 可读性变高了 但是再次循环的时候 会遇到一些小问题  需要再次写一遍 所以直接用 “total”比较舒服
# uname = json_comment['data']['list']#用户名
# utime = json_comment['data']['list']#时间
# user_grade =json_comment['data']['list']#分数
# s=json_comment['data']#url中的所有内容
j = 0
header = ['用户名','发表时间','分数','评论',"点赞数","不喜欢"]#为CSV创建第一行（头
with open('test.csv','a+',newline='',encoding='utf-8') as f:#写入CSV
    writer = csv.DictWriter(f,fieldnames=header)
    writer.writeheader()
    while j < 1:
        total = json_comment['data']['list']
        for i in range(len(total)):
            # uname = total[i]['uname']
            comment = total[i]['content']  # 获取url中的评论
            uame = total[i]['author']['uname'] #用户的名称
            ctime = total[i]['ctime']#获得评论的时间戳
            xtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ctime)))#时间戳转换为 %Y-%m-%d %H:%M:%S
            score = total[i]['score'] #分数
            #喜欢 不喜欢
            star_disliked = total[i]['stat']['disliked']
            # star_like = total[i]['stat']['liked']
            star_likes = total[i]['stat']['likes']
            outdata = [{"用户名": uame, "发表时间": xtime, "分数": score, "评论": comment,"点赞数":star_likes,"不喜欢":star_disliked}]
            # print(outdata)
            writer.writerows(outdata)#写入CSV
        j += 1
        next = json_comment['data']['next']  # 获取next中的内容
        # print(next)   #79714616963704
        next1 = str(next)#获取下一页评论的index
        url1 = url + '&cursor=' + next1  # 这时候 url更新了   用户名 发表时间 分数 评论 都更新了
        response = requests.get(url1, headers=headers).text  # 再次获得初始数据
        json_comment = json.loads(response) #当前循环结束 这里的值作为下一个循环的初始值

