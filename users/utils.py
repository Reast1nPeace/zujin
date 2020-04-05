from math import *
from .models import DingDanInfo, ZuHao


def get_data(user):
    data = {}
    dindans = DingDanInfo.objects.all().order_by("-add_time")[:2000]
    userdindans = DingDanInfo.objects.filter(zyr=user).order_by("-add_time")[:30]

    for dindan in dindans:
        if dindan.zyr == user:
            continue
        if not dindan.zyr in data.keys():
            data[dindan.zyr] = {dindan.game_name: 1}
        else:
            if not dindan.game_name in data[dindan.zyr].keys():
                data[dindan.zyr][dindan.game_name] = 1
            else:
                data[dindan.zyr][dindan.game_name] = data[dindan.zyr][dindan.game_name] + 1
    for dindan in userdindans:
        if not dindan.zyr in data.keys():
            #print("---1")
            data[dindan.zyr] = {dindan.game_name: 1}
        else:
            #print("---2")
            if not dindan.game_name in data[dindan.zyr].keys():
                data[dindan.zyr][dindan.game_name] = 1
            else:
                data[dindan.zyr][dindan.game_name] = data[dindan.zyr][dindan.game_name] + 1
    return data

def Euclid(user1, user2, data):
	#取出两个人都购买过的游戏
	user1_data = data[user1]
	user2_data = data[user2]
	#默认距离
	distance = 0
	#遍历找出都购买过的
	for key in user1_data.keys():
		if key in user2_data.keys():
			distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)
	return 1/(1+sqrt(distance))

#计算某个用户和其他用户的相似度
def top_similiar(user, data):
	res = []
	for userid in data.keys():
		if not userid == user:
			similiar = Euclid(user, userid, data)
			res.append((userid,similiar))
	res.sort(key=lambda val: val[1])
	return res

def recommend(user):
    recommend_list = []
    res = []
    if DingDanInfo.objects.filter(zyr=user).count():
        data = get_data(user)
        print(data)
        top_user = top_similiar(user, data)[0][0]
        # 购买记录
        items = data[top_user]
        print("topuser:",top_user)
        print(items)
        # 推荐列表
        for item in items.keys():
            if item not in data[user].keys():
                recommend_list.append((item, items[item]))
        # 多个商品按照评分排序
        recommend_list.sort(key=lambda val: val[1], reverse=True)
        last_dindan_game_name = DingDanInfo.objects.filter(zyr=user).order_by("-add_time").first().game_name
        res = list(ZuHao.objects.filter(fb_status=True, yz_status=False, game_name=last_dindan_game_name).order_by('-add_time')[:1])
        print(recommend_list)
    if len(recommend_list) == 0:
        res = ZuHao.objects.filter(fb_status=True, yz_status=False).order_by('-add_time')[:8]
    else:
        for item in recommend_list:
            res.extend(ZuHao.objects.filter(fb_status=True, yz_status=False, game_name=item[0]).order_by('-add_time')[:2])
        res.extend(ZuHao.objects.filter(fb_status=True, yz_status=False).order_by('-add_time')[:8])
    return res[:8]




