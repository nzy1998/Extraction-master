import json
import re
#from pyhanlp import *
import os
from pyltp import Segmentor
LTP_DATA_DIR='./data/model'
cws_model_path=os.path.join(LTP_DATA_DIR,'cws.model')
segmentor=Segmentor()
segmentor.load(cws_model_path)
#words=segmentor.segment('被告人陈杰在本市东城区磁器口光明日报社门前')
count1=0
count_easy=0
count_complex=0

file1 = open('case.txt', encoding='utf-8')
file2 = open('result.txt', 'w', encoding='utf-8')
file3 = open('result_complex.txt', 'w', encoding='utf-8')
file4 = open('result1.txt', 'w', encoding='utf-8')
file5 = open('result_easy.txt', 'w', encoding='utf-8')

def find_date(str):
    arr = re.findall(
        r"(\d{4}年\d{1,2}月\d{1,2}日|\d{4}年\d{1,2}月中旬|\d{4}年\d{1,2}月上旬|\d{4}年\d{1,2}月下旬|"
        r"\d{4}年\d{1,2}月|\d{1,2}月\d{1,2}日|\d{4}年|\d{1,2}月|\d{1,2}日|当日|次日|当天|\d{1,2}时\d{1,2}分|"
        r"某年某月某日|\d{1,2}时许|\d{1,2}时多|\d{1,2}时左右|同年|同月|同日|期间|随后)", str)

    return arr



def find_thing(str):
    cnt=0
    arr = re.findall(r"(阿普唑仑|毒品|白色晶体|MDMA|N-异丙基苄胺|新型毒品|氟硝西泮|糖浆|5-MeO-DiPT|5-MeO-DIPT|AB-CHMINACA|美沙酮|磷酸可待因|麦角酰二乙胺|苄基异丙胺|麻黄碱|止咳水|G点液|苯丙胺|鸦片|海洛因|甲基苯丙胺|冰毒|吗啡|大麻|可卡因|杜冷丁|古柯|摇头丸|K粉|咖啡因|三唑仑|三唑伦|-羟基丁酸安纳咖|氟硝安定|麦角乙二胺（LSD）|安眠酮|丁丙诺啡|地西泮|氯胺酮|麻古|麻果)",str)
#     if len(arr) != 0:
#         for i in arr:
#             print(i,end=' ')
#         print('\n')
#         return 1
#     else:
#         print("没有找到"+str)
#         print('\n')
    #return arr
    return list(set(arr))


def find_person(str):
    flag=0
    words=segmentor.segment(str)
    can=('被告人','被告','罪犯')
    person=[]
    for i in words:
        if any(a in i for a in can):
            flag=1  #找到触发词了，开始提取
        elif flag==1:
            if i not in person:
                if len(i)==1:
                    i=i+'某'
                i=i.split('犯')[0]
                person.append(i)
            flag=2  #提取到1个被告,看下一个是不是连词，如果是，继续提取
        elif flag==2:
            if i == '、' or i == '和':
                flag=1
            else:
                flag=0
    return person


def findAddress(name2):
    a = name2
    if "内" in name2:
        if "内蒙古" not in name2:
            name3 = name2.split("内")
            a= name3[0]
        else:
            name2=name2.replace("内蒙古","")
            name3 = name2.split("内")
            a = "内蒙古"+name3[0]
    if "处" in name2:
        name3 = name2.split("处")
        a = name3[0]+'处'
    if "中" in name2:
        name3 = name2.split("中")
        a = name3[0]
    if "与" in name2:
        name3 = name2.split("与")
        a = name3[0]
    if "将" in name2:
        name3 = name2.split("将")
        a = name3[0]
    if "和" in name2:
        name3 = name2.split("和")
        a = name3[0]
    if "时" in name2:
        name3 = name2.split("时")
        a = name3[0]
    if "向" in name2:
        name3 = name2.split("向")
        a = name3[0]
    if "借用" in name2:
        name3 = name2.split("借用")
        a = name3[0]
    if "交易" in name2:
        name3 = name2.split("交易")
        a = name3[0]
    if "购买" in name2:
        name3 = name2.split("购买")
        a = name3[0]
    if "贩卖" in name2:
        name3 = name2.split("贩卖")
        a = name3[0]
    if "通过" in name2:
        name3 = name2.split("通过")
        a = name3[0]
    if "进行" in name2:
        name3 = name2.split("进行")
        a = name3[0]
    if "等地" in name2:
        name3 = name2.split("等地")
        a = name3[0]+"等地"
    if "期间" in name2:
        name3 = name2.split("期间")
        a = name3[0]
    if "山上" in name2:          # 在xx山上
        name3 = name2.split("上")
        a = name3[0]
    if "的被" in name2:           # 在某地的被害人
        name3 = name2.split("的被")
        a = name3[0]
    if "采用" in name2:            # 在某地采用某方式
        name3 = name2.split("采用")
        a = name3[0]
    if "以" in name2:            # 在某地以某方式
        name3 = name2.split("以")
        a = name3[0]
    if "扒窃" in name2:            # 在某地扒窃某物
        name3 = name2.split("扒窃")
        a = name3[0]
    if "实施盗窃" in name2:         # 在某地实施盗窃
        name3 = name2.split("实施盗窃")
        a = name3[0]
    if "盗窃" in name2:             # 在某地盗窃某物
        name3 = name2.split("盗窃")
        a = name3[0]
    if "窃取" in name2:             # 在某地盗窃某物
        name3 = name2.split("窃取")
        a = name3[0]
    if "的电表" in name2:            # 位于某地的电表
        name3 = name2.split("的电表")
        a = name3[0]
    if "被害人" in name2:            # 位于某地的电表
        name3 = name2.split("被害人")
        a = name3[0]
    if "的住所" in name2:            # 位于某地的电表
        name3 = name2.split("的住所")
        a = name3[0]
    if "附近" in name2:            # 位于某地的电表
        name3 = name2.split("附近")
        a = name3[0]
    return a
# 如果仍未匹配到地点，就采用字典匹配和正则匹配
def findAddress2(str):

    add1=re.findall(r"(?<=作为|经营).*(?=的服务员|期间)", str)
    add2 = re.findall(r"[\u4e00-\u9fa5]{2}市.*?区", str)
    add3 = re.findall(r"本市.*?街", str)
    add4 = re.findall(r"本区.*?镇", str)
    add5 = re.findall(r"本市.*?路", str)
    add6=re.findall(r"[\u4e00-\u9fa5]{2}市",str)
    add7 = re.findall(r"[\u4e00-\u9fa5]{2}区.*?镇", str)
    add8 = re.findall(r"本区.*?连", str)
    add9 = re.findall(r"本区.*?路", str)
    if add1!=[]:
        return add1[0]
    elif add2!=[]:
        return add2[0]
    elif add3!=[]:
        return add3[0]
    elif add4!=[]:
        return add4[0]
    elif add5!=[]:
        return add5[0]
    elif add6!=[]:
        return add6[0]
    elif add7!=[]:
        return add7[0]
    elif add8!=[]:
        return add8[0]
    elif add9!=[]:
        return add9[0]
    else:
        return None


def find_address(str):
    str = str.replace("提现至", "")
    str = str.replace("至当日", "")
    str = str.replace("从被害人", "")

    if "到达" in str:
        add = str.split("到达")
        return findAddress(add[1])
    elif "到" in str and "到案" not in str and '收到' not in str and '联系' not in str and '联络' not in str:
        add = str.split("到")
        return findAddress(add[1])
    elif "前往" in str:
        add = str.split("前往")
        return findAddress(add[1])
    elif "送往" in str:
        add = str.split("送往")
        return findAddress(add[1])
    elif "途经" in str:
        add = str.split("途经")
        return findAddress(add[1])
    elif "位于" in str:
        add = str.split("位于")
        return findAddress(add[1])
    elif "至" in str:
        add = str.split("至")
        return findAddress(add[1])
    elif "在" in str:
        if "期间" not in str and "授意" not in str and '在押' not in str and '联络' not in str and '促成' not in str:       # 在XXX期间
            add = str.split("在")
            return findAddress(add[1])
    elif "进入" in str:
        add = str.split("进入")
        return findAddress(add[1])
    elif "潜入" in str:
        add = str.split("潜入")
        return findAddress(add[1])
    elif "前往" in str:
        add = str.split("前往")
        return findAddress(add[1])
    elif "送往" in str:
        add = str.split("送往")
        return findAddress(add[1])
    elif "位于" in str:
        add = str.split("位于")
        return findAddress(add[1])
    else:
        return ''

def extract(line):
    global count_complex
    global count_easy
    global count1
    count=0
    flag_valid=0
    result=[]
    time=''
    person=[]
    thing=find_thing(line)
    cnt = 0
    cnt_thing = 0
    cnt_person = 0
    cnt_add = 0
    cnt_time = 0
    alternatives = ('减刑', '二审', '假释', '裁定书', '判决书','罪','诉讼','犯','一案','毒案','投案','案件','服刑','监狱')

    #     if '指控：'in line:
    #         line= line.split("指控：",1)[1]#公诉机关指控之后的才是犯罪事实
    #     elif'指控，'in line:
    #         line= line.split("指控，",1)[1]#公诉机关指控之后的才是犯罪事实
    # name=find_person(line)
    # thing=find_thing(line)
    # date=find_date(line)

    if '指控' in line:
        line = line.split('指控', 1)[1]
    if '上述事实' in line:
        line = line.split('上述事实', 1)[0]
    if '抓获' in line:
        line = line.split('抓获', 1)[0]
    if '查获' in line:
        line = line.split('查获', 1)[0]
    if '民警' in line:
        line = line.split('民警', 1)[0]
    #括号内容清除
    line = re.sub('\\（.*?\\）', '', line)
    line = re.sub('\\(.*?\\)', '', line)


    for sen in re.split(r'[；。]', line):


        #如果被抓了就不属于犯罪事实
        if '上述指控' in sen:
            break
        else:
            flag_person = 0
            flag_add = 0
            flag_time = 0
            flag_thing = 0
            text_dict = {}
            text_dict["时间"] = ''
            text_dict["地点"] = ''
            text_dict["人物"] = []
            text_dict["物品"] = []

            # 因为抽取物品不大可能太长，所以放在一句话里即可
            # thing = find_thing(sen)
            # text_dict['物品'] = thing
            # if text_dict['物品'] == []:
            #     continue

            # 如果这句话里有物品，再抽取其他
            flag_valid = 1

            # 抽取人物

            if find_person(sen) != []:
                text_dict['人物']=find_person(sen)
                person.extend(text_dict['人物'])
                flag_person = 1

            elif person!=[]:
                for _p in person:
                    if _p in sen:
                        text_dict['人物'].append(_p)




            #子句只用来提取时间和地点，细化毒品
            for sub_sen in re.split(r'[，：]', sen):
                # 如果这句话来自于开头，不用去考虑
                if any(a in sub_sen for a in alternatives):
                    continue


                # 抽取时间
                dateArray = find_date(sub_sen)
                if len(dateArray) != 0:
                    flag_time = 1
                    if len(dateArray) > 1:  # 时间区间，多个时间
                        start = sub_sen.find(dateArray[0])
                        end = sub_sen.find(dateArray[len(dateArray) - 1]) + len(dateArray[len(dateArray) - 1])
                        text_dict["时间"] = sub_sen[start:end]
                    else:  # 单个时间
                        text_dict["时间"] = dateArray[0]

                    sub_sen=sub_sen.split(text_dict["时间"])[1]  # 把时间去掉，防止影响抽取结果
                elif re.match(r'后.*',sub_sen):
                    text_dict['时间']='后'

                # 抽取地点
                address = find_address(sub_sen)
                if address != '':
                    flag_add = 1
                    text_dict['地点'] = address
                elif '微信' in sub_sen:
                    text_dict['地点'] = '微信'
                elif '电话' in sub_sen:
                    text_dict['地点'] = '电话'

                #细化毒品
                if find_thing(sub_sen) !=[]:
                    #以贩卖行为为准
                    _w = re.findall(r"将(.*?)贩卖给", sub_sen)
                    if _w != []:
                        text_dict['物品'].extend(_w)
                        # print(text_dict['物品'])
                    elif '贩卖' in sub_sen and find_thing(sub_sen.split('贩卖')[1].split('给',1)[0])!=[]:
                        text_dict['物品'].append(sub_sen.split('贩卖')[1].split('给',1)[0])
                    elif '购买' in sub_sen and find_thing(sub_sen.split('购买')[1].split('给', 1)[0]) != []:
                        text_dict['物品'].append(sub_sen.split('购买')[1].split('给', 1)[0])
                    elif '交易' in sub_sen and find_thing(sub_sen.split('交易')[1].split('给', 1)[0]) != []:
                        text_dict['物品'].append(sub_sen.split('交易')[1].split('给', 1)[0])
                    else:
                        text_dict['物品']=find_thing(sub_sen)



        # 替换"次日"的时间
        if text_dict["时间"].startswith("次日") and len(time) != 0:
            text_dict["时间"] = re.findall(r"(\d{4}年\d{1,2}月)", time)[0] + str(
                int(re.findall(r"(\d{1,2}日)", time)[0].split("日")[0]) + 1) + "日" + text_dict["时间"].split("次日")[1]
        # 替换"同年"的时间
        if text_dict["时间"].startswith("同年") and len(time) != 0:
            text_dict["时间"] = re.findall(r"(\d{4}年)", time)[0]+text_dict["时间"].split("同年")[1]
        # 替换"同月"的时间
        if text_dict["时间"].startswith("同月") and len(time) != 0:
            text_dict["时间"] = re.findall(r"(\d{4}年\d{1,2}月)", time)[0] + text_dict["时间"].split("同月")[1]
        # 替换"同日"的时间
        if text_dict["时间"].startswith("同日") and len(time) != 0:
            text_dict["时间"] = re.findall(r"(\d{4}年\d{1,2}月\d{1,2}日)", time)[0] + text_dict["时间"].split("同日")[1]
        # 替换"当日"的时间
        if text_dict["时间"].startswith("当日") and len(time) != 0:
            text_dict["时间"] = re.findall(r"(\d{4}年\d{1,2}月\d{1,2}日)", time)[0] + text_dict["时间"].split("当日")[1]
        # 替换"当天"的时间
        if text_dict["时间"].startswith("当天") and len(time) != 0:
            text_dict["时间"] = re.findall(r"(\d{4}年\d{1,2}月\d{1,2}日)", time)[0] + text_dict["时间"].split("当天")[1]
        # 替换"期间"的时间
        if text_dict["时间"].startswith("期间") and len(time) != 0:
            text_dict["时间"] = time

        _t = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", text_dict['时间'])
        if _t is not None:
            time = text_dict['时间']

        if text_dict['物品']==[] and thing !=[] and text_dict['时间']!='' and text_dict['地点']!='' and text_dict['人物']!=[]:
            text_dict['物品']=thing

        if text_dict['人物']==[] and person !=[] and text_dict['时间']!='' and text_dict['地点']!='' and text_dict['物品']!=[]:
            text_dict['人物']=person

        # 筛选数据，如果事件缺少要素，则删除该事件，不添加进最终的结果中
        if text_dict["时间"] == ''or text_dict['物品'] ==[] or text_dict['人物']==[]:
            continue


        else:
            # 去重
            text_dict['物品']=list(set(text_dict['物品']))
            text_dict['人物'] = list(set(text_dict['人物']))
            person=list(set(person))
            result.append(text_dict)
            count=count+1
    if result!=[]:
        dic = {}
        dic['result'] = result
        dicJson = json.dumps(dic, ensure_ascii=False)
        file2.write(dicJson)
        file2.write('\n')
        # print(dicJson)
        # print(' 时间：', text_dict['时间'], ' 地点：', text_dict['地点'], ' 人物：', text_dict['人物'], ' 物品：', text_dict['物品'],
        #   end=' ')
    if count == 0:
        count1 = count1 + 1
        file4.write(line)
        file4.write('\n')
    elif count == 1 or len(person)==1:
        count_easy = count_easy + 1
        if count==1:
            file5.write(dicJson)
            file5.write('\n')
    #多人物多事件称为复杂案件
    elif count>1 and len(person)>1:
        count_complex = count_complex + 1
        file3.write(dicJson)
        file3.write('\n')

def main():
    global count_complex
    global count_easy
    global count1

    for line in file1:
       if len(line)<10:
           count1=count1+1
           continue
       else:
           extract(line)

    print('无效事件 ',count1)
    print('简单事件 ',count_easy)
    print('复杂事件 ',count_complex)

    file1.close()
    file2.close()
    file3.close()
    file4.close()
    file5.close()


if __name__=='__main__':
    main()