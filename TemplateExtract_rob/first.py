# -*- coding: UTF-8 -*-
import json
import re
# from pyhanlp import *
import os
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

LTP_DATA_DIR = './TemplateExtract_rob/ltp_data_v3.4.0'  # ltp模型目录的路径
user_dict = './TemplateExtract_rob/ltp_data_v3.4.0/lexicon.txt'
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
segmentor = Segmentor()  # 初始化实例
segmentor.load_with_lexicon(cws_model_path, user_dict)
postagger = Postagger()  # 初始化实例
postagger.load_with_lexicon(pos_model_path, user_dict)
recognizer = NamedEntityRecognizer()  # 初始化实例
recognizer.load(ner_model_path)  # 加载模型
data = []
text_dict = {}
file4 = open('file4.txt', 'w', encoding='utf-8')
file5 = open('file5.txt', 'w', encoding='utf-8')
file6 = open('file6.txt', 'w', encoding='utf-8')
count1 = 0

aa = bb = cc = dd = 0
tx  = txx = non = unsuc = 0

def findDate():
    file1 = open('file1.txt', encoding='utf-8')
    file2 = open('file2.txt', 'w', encoding='utf-8')
    for line in file1:
        mat = re.findall(r"(\d{4}年\d{1,2}月\d{1,2}日)", line)
        if len(mat) != 0:
            for i in mat:
                file2.write(i + " ")
            file2.write('\n')
        else:
            file2.write("没有日期" + '\n')


# 非盗窃开头的句子
def findThing(str):
    if "未盗得" in str or "未窃得"  in str:
        return None
    str = str.replace("扒窃作案", "")
    str = str.replace("的方式", "")
    str = str.replace("盗窃行迹", "")
    str = str.replace("秘密窃取他人财物的行为", "")
    str = str.replace("盗窃事实：", "")
    str = str.replace("盗窃后", "")
    str = str.replace("盗窃所得的", "")
    str = str.replace("实施盗窃犯罪", "")
    str = str.replace("扒窃未果", "")
    str = str.replace("偷扫其微信付款码", "")
    str = str.replace("盗窃一起", "")
    str = str.replace("盗窃两起", "")
    str = str.replace("盗窃三起", "")
    str = str.replace("盗窃四起", "")
    str = str.replace("盗窃五起", "")
    #print("thing--str:",str)
    thing = []
    # 匹配"发现...未上锁"
    temp0 = re.findall(r"(?<=发现).*(?=未上锁)", str)
    # 匹配"将...拿走"
    temp = re.findall(
        r"(?<=将|见|把).*(?=拿走|抢走|脱下|盗出|盗转|剪断|盗走|拿入|装入|窃走|搬到|窃回|窃取|分多次转至|未锁好|未上锁|带走|带至|带入|藏匿|转走|带进|装在|转入|提现|以人民币|开锁骑走|放出卖于|运回|偷了出来)",
        str)
    # 匹配"试图剪断...的环形锁"
    temp1 = re.findall(r"(?<=剪断|撬开|取走|少交|购买|换出|转出).*(?=的环形锁|车头锁|后逃逸|费|1部|予以贩卖|至自己支付宝账户|并盗走)", str)
    # 匹配"价值...的电动自行车"
    temp2 = re.findall(r"(?<=一辆|此的).*(?=自行车)", str)
    # 匹配"套现获取..."
    temp3 = re.findall(r"(?<=套现获取).*", str)
    # 匹配"被害人的...失窃"
    temp4 = re.findall(r"(?<=被害人的).*(?=失窃)", str)
    # 匹配"贷款人民币...元"
    temp5 = re.findall(r"(?<=贷款人民币).*(?=元)", str)
    if len(temp0) == 0 and len(temp) == 0 and len(temp1) == 0 and len(temp2) == 0 and len(temp3) == 0 and len(
            temp4) == 0 and len(temp5) == 0:
        if "抢走" in str:
            if len(re.findall(r"(?<=将).*(?=抢走)", str)) != 0:
                if len(re.findall(r"(?<=的).*?(?=抢走)", str)) != 0:
                    thing = re.findall(r"(?<=的).*?(?=抢走)", str)
                    print("thing:", thing)
                else:
                    thing = re.findall(r"(?<=将).*(?=抢走)", str)
            elif len(re.findall(r"(?<=把).*(?=抢走)", str)) != 0:
                if len(re.findall(r"(?<=的).*?(?=抢走)", str)) != 0:
                    thing = re.findall(r"(?<=的).*?(?=抢走)", str)
                else:
                    thing = re.findall(r"(?<=把).*(?=抢走)", str)
            else:
                thing = str.split("抢走")
        elif "劫取" in str:
            if len(re.findall(r"(?<=劫取).*", str)) != 0:
                thing = re.findall(r"(?<=劫取).*", str)
                thing = re.sub(r".*?(?<=的)","",thing[0])
                print("thing:", thing)
                if(len(thing)>1):
                    return thing
            else:
                thing = str.split("劫取")
        elif "窃" in str:
            if "窃得" in str:
                if len(re.findall(r"(?<=窃得).*(?=后离开|后藏匿)", str)) > 0:
                    return re.findall(r"(?<=窃得).*(?=后离开|后藏匿)", str)[0]
                else:
                    thing = str.split("窃得")
            elif "盗窃" in str and "盗窃之念" not in str:
                if "盗窃罪" not in str and "盗窃案" not in str:
                    thing = str.split("盗窃")
                    if "后被北京市公安局丰台分局大红门商城派出所民警抓获" in thing[1]:
                        thing[1] = thing[1].replace("后被北京市公安局丰台分局大红门商城派出所民警抓获", "")  # 盗窃xxx后
            elif "窃取" in str:

                if len(re.findall(r"(?<=窃取).*(?=过程中|被发现|后逃离|时被其发现|未得逞|后准备)", str)) > 0:
                    return re.findall(r"(?<=窃取).*(?=过程中|被发现|后逃离|时被其发现|未得逞|后准备)", str)[0]
                else:
                    thing = str.split("窃取")
            elif "窃走" in str:
                thing = str.split("窃走")
            elif "所窃的" not in str and "盗窃之念" not in str:
                thing = str.split("窃")
        elif "盗走" in str:
            thing = str.split("盗走")
        elif "盗用" in str:
            thing = str.split("盗用")
        elif "盗充" in str:
            thing = str.split("盗充")
        elif "盗割" in str:
            thing = str.split("盗割")
        elif "盗取" in str:
            thing = str.split("盗取")
        elif "盗刷" in str:
            thing = str.split("盗刷")
        elif "盗挖" in str:
            thing = str.split("盗挖")
        elif "抢得" in str:
            thing = str.split("抢得")
        elif "偷" in str and "偷东西" not in str:
            if "偷逃" in str:
                thing = str.split("偷逃")
            else:
                thing = str.split("偷")
                if "挣钱" in thing[1]:
                    thing[1] = thing[1].replace("挣钱", "")  # 窃取xxx过程中
                if "使用" in thing[1]:
                    thing[1] = thing[1].replace("使用", "")  # 窃取xxx被发现后逃离
        elif "缴获" in str:
            thing = str.split("缴获")
        elif "骗取" in str:
            if "信任" not in str:
                thing = str.split("骗取")
        elif "撬下" in str:
            thing = str.split("撬下")
        if len(thing) > 1:
            thing[1] = thing[1].replace("后逃逸", "")
            return thing[1]
        else:
            return None
    elif len(temp0) != 0:
        thing=temp0[0]
        return thing
    elif len(temp) != 0:
        thing = temp[0]
        '''file6.write("before:")
        file6.write(thing)
        file6.write('\n')'''
        thing=re.sub(r".*?(?<=的)","",thing)
        '''file6.write("thing:")
        file6.write(thing)
        file6.write('\n')'''
        return thing
    elif len(temp2) != 0:
        thing = "一辆" + temp2[0] + "自行车"
        return thing
    elif len(temp3) != 0:
        thing = temp3[0]
        return thing
    elif len(temp4) != 0:
        thing = temp4[0]
        return thing
    elif len(temp5) != 0:
        thing = "贷款人民币" + temp5[0] + "元"
        return thing
    else:
        thing = temp1[0]
        return thing


def findAddress(name2):
    a = name2
    if "内" in name2:
        if "内蒙古" not in name2:
            name3 = name2.split("内")
            a = name3[0]
        else:
            name2 = name2.replace("内蒙古", "")
            name3 = name2.split("内")
            a = "内蒙古" + name3[0]
    elif "处" in name2:
        name3 = name2.split("处")
        a = name3[0]
    elif "借用" in name2:
        name3 = name2.split("借用")
        a = name3[0]
    elif "等地" in name2:
        name3 = name2.split("等地")
        a = name3[0] + "等地"
    elif "期间" in name2:
        name3 = name2.split("期间")
        a = name3[0]
    elif "山上" in name2:  # 在xx山上
        name3 = name2.split("上")
        a = name3[0]
    elif "的被" in name2:  # 在某地的被害人
        name3 = name2.split("的被")
        a = name3[0]
    elif "采用" in name2:  # 在某地采用某方式
        name3 = name2.split("采用")
        a = name3[0]
    elif "以" in name2:  # 在某地以某方式
        name3 = name2.split("以")
        a = name3[0]
    elif "扒窃" in name2:  # 在某地扒窃某物
        name3 = name2.split("扒窃")
        a = name3[0]
    elif "实施盗窃" in name2:  # 在某地实施盗窃
        name3 = name2.split("实施盗窃")
        a = name3[0]
    elif "盗窃" in name2:  # 在某地盗窃某物
        name3 = name2.split("盗窃")
        a = name3[0]
    elif "窃取" in name2:  # 在某地盗窃某物
        name3 = name2.split("窃取")
        a = name3[0]
    elif "的电表" in name2:  # 位于某地的电表
        name3 = name2.split("的电表")
        a = name3[0]
    elif "被害人" in name2:  # 位于某地的电表
        name3 = name2.split("被害人")
        a = name3[0]
    elif "的住所" in name2:  # 位于某地的电表
        name3 = name2.split("的住所")
        a = name3[0]
    elif "附近" in name2:  # 位于某地的电表
        name3 = name2.split("附近")
        a = name3[0]
    return a


# 被告人XXX在某地  | 被告人在XXX期间
def findAddress2(str, str1):
    array = []
    str = str.replace("提现至", "")
    str1 = str1.replace("提现至", "")
    str = str.replace("捡到", "")
    str1 = str1.replace("捡到", "")
    if "到" in str:
        add = str1.split("到")
        array.append(add[0])  # 人物
        if (len(add) > 1): array.append(findAddress(add[1]))  # 地点
        return array
    elif "位于" in str:
        add = str1.split("位于")
        array.append(add[0])  # 人物
        if (len(add) > 1): array.append(findAddress(add[1]))  # 地点
        return array
    elif "至" in str:
        if "窜至" in str:
            add = str1.split("窜至")
            array.append(add[0])
            if (len(add) > 1): array.append(findAddress(add[1]))
            return array
        else:
            add = str1.split("至")
            array.append(add[0])
            if (len(add) > 1): array.append(findAddress(add[1]))
            return array

    elif "在" in str:
        if "工作期间" in str or "公司期间" in str:
            add = str1.split("在")  # 被告人xx在XXX期间，只能提取出被告人的名字
            array.append(add[0])
            if (len(add) > 1): array.append(findAddress(add[1]))
            return array
        elif "期间" not in str and "授意" not in str:
            add = str1.split("在")
            array.append(add[0])
            if (len(add) > 1): array.append(findAddress(add[1]))
            return array
        else:
            add = str1.split("在")  # 被告人xx在XXX期间，只能提取出被告人的名字
            array.append(add[0])
            array.append(None)
            return array
    elif "途经" in str:
        add = str.split("途经")
        array.append(add[0])
        if (len(add) > 1): array.append(findAddress(add[1]))
        return array
    elif "途径" in str:
        add = str.split("途径")
        array.append(add[0])
        if (len(add) > 1): array.append(findAddress(add[1]))
        return array
    elif "路过" in str:
        add = str.split("路过")
        array.append(add[0])
        if (len(add) > 1): array.append(findAddress(add[1]))
        return array
    elif "从" in str:
        add = str.split("从")
        array.append(add[0])
        if (len(add) > 1): array.append(findAddress(add[1]))
        return array
    elif "进入" in str:
        add = str1.split("进入")
        array.append(add[0])
        if (len(add) > 1): array.append(findAddress(add[1]))
        return array
    elif "潜入" in str:
        add = str.split("潜入")
        array.append(add[0])
        array.append(findAddress(add[1]))
    elif "前往" in str:
        add = str1.split("前往")
        array.append(add[0])
        if (len(add) > 1): array.append(findAddress(add[1]))
        return array

    elif "乘坐" in str:
        add = str1.split("乘坐")
        array.append(add[0])
        if (len(add) > 1): array.append(findAddress(add[1]))
        return array

    elif "驾驶" in str:
        add = str1.split("驾驶")  # 被告人xx驾驶
        array.append(add[0])
        array.append(None)
        return array
    elif "以手机验证码" in str:
        add = str1.split("以手机验证码")  # 被告人xx以手机验证码的方式，只能提取出被告人的名字
        array.append(add[0])
        array.append(None)
        return array


# 在某地，，不包括被告人的情况
def findAddress3(str):
    str = str.replace("提现至", "")
    str = str.replace("至当日", "")
    str = str.replace("从被害人", "")
    if "到" in str and "到案" not in str:
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
    elif "从" in str:
        add = str.split("从")
        return findAddress(add[1])
    elif "在" in str:
        if "期间" not in str and "授意" not in str:  # 在XXX期间
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


# 如果仍未匹配到地点，就采用字典匹配和正则匹配
def findAddress4(str):
    add1 = re.findall(r"(?<=作为|经营).*(?=的服务员|期间)", str)
    add2 = re.findall(r"[\u4e00-\u9fa5]{2}市.*?区", str)
    add3 = re.findall(r"本市.*?街", str)
    add4 = re.findall(r"本区.*?镇", str)
    add5 = re.findall(r"本市.*?路", str)
    add6 = re.findall(r"[\u4e00-\u9fa5]{2}市", str)
    add7 = re.findall(r"[\u4e00-\u9fa5]{2}区.*?镇", str)
    add8 = re.findall(r"本区.*?连", str)
    add9 = re.findall(r"本区.*?路", str)
    if add1 != []:
        return add1[0]
    elif add2 != []:
        return add2[0]
    elif add3 != []:
        return add3[0]
    elif add4 != []:
        return add4[0]
    elif add5 != []:
        return add5[0]
    elif add6 != []:
        return add6[0]
    elif add7 != []:
        return add7[0]
    elif add8 != []:
        return add8[0]
    elif add9 != []:
        return add9[0]
    else:
        return None


def processPerson(str):
    str = re.sub('(先后|使用|未经|来到|趁|通过|持票|三次|两次|酒后|游荡|采取|结伙|谎称|尾随|明知|见|'
                 '连续|多次|再次|将|为|动手|采用|携带|因经|独自|骑|撬锁|经事|搭|乘|爬|翻|以|单独'
                 '|至|一同|分别|作为|发现|利用|共同|商议|进入|窃取|盗窃|在|相识|窃得|盗刷|到|攀|行|均系|让|原系|化名|遂|应聘|自|从|步|佯装|面带|手持).*', '',
                 str)  # 去除掉句子里的"在xxx授意下"
    str=str.replace("当时",'')

    final = []
    strlist = re.split(r'[、]', str)
    for j in strlist:
        person = []
        if "伙同" in j:
            pp = j.split("伙同")
            person.append(pp[0])
            person.append(pp[1])
        elif "纠集" in j:
            pp = j.split("纠集")
            person.append(pp[0])
            person.append(pp[1])
        elif "与" in j:
            pp = j.split("与")
            person.append(pp[0])
            person.append(pp[1])
        elif "介绍" in j:
            pp = j.split("介绍")
            person.append(pp[0])
            person.append(pp[1])
        elif "和" in j:
            pp = j.split("和")
            person.append(pp[0])
            person.append(pp[1])
        else:
            person.append(j)
        for i in person:
            a = re.sub('(经|驾驶|预谋|途径|又|示意|的|驾|安装).*', '', i)  # 去除掉句子里的"在xxx授意下"
            if len(a) == 1:
                a = a + "某"
            final.append(a)
    return final


def NER(str):
    start = 0
    end = 0
    flag = 0
    result = ""
    words = segmentor.segment(str)
    # segmentor.release()  # 释放模型

    postags = postagger.postag(words)  # 词性标注
    # postagger.release()  # 释放模型

    length = len(words)

    for i in range(0, length):
        if postags[i] == 'o':
            start = i
            for j in range(i, length):
                if postags[j] == 'm':
                    if j != length - 1 and postags[j + 1] == 'q':
                        flag = 1  # 既找到专有名词，又找到量词
                        end = j + 1
                        break
            if flag == 0:
                return words[i]  # 只有专有名词，没有量词
            break
        if postags[i] == 'm' and i < length - 1:
            if postags[i + 1] == 'q':
                start = i
                for j in range(i + 1, length):
                    if postags[j] == 'o':
                        flag = 1
                        end = j
                        break

            if flag == 1:
                break
    if flag == 1:  # 检查到了专有名词
        for i in range(start, end + 1):
            result = result + words[i]
        return result
    else:
        return None


def NER2(str):
    start = 0
    end = 0
    flag = 0
    result = ""
    words = segmentor.segment(str)
    # segmentor.release()  # 释放模型
    postags = postagger.postag(words)  # 词性标注

    # postagger.release()  # 释放模型

    length = len(words)
    for i in range(0, length):
        if words[i] == "狗" or words[i] == "鹅" or words[i] == "Iphone6S" or words[i] == "Iphone7PLUS" or words[
            i] == "VIVO" or words[i] == "OPPO" or words[i] == "OPPOA5":
            postags[i] = "o"
        print(words[i] + '/' + postags[i], end=" ")
    for i in range(0, length):
        if postags[i] == 'o':
            start = i
            for j in range(i, length):
                if postags[j] == 'm':
                    if j != length - 1 and postags[j + 1] == 'q':
                        flag = 1  # 既找到专有名词，又找到量词
                        end = j + 1
                        break
            if flag == 0:
                return words[i]  # 只有专有名词，没有量词
            break
        if postags[i] == 'm' and i < length - 1:
            if postags[i + 1] == 'q':
                start = i
                for j in range(i + 1, length):
                    if postags[j] == 'o':
                        flag = 1
                        end = j
                        break

            if flag == 1:
                break
        if postags[i] == 'z':  # 只有人民币的情况
            start = i
            for j in range(i + 1, length):
                if postags[j] == 'z':
                    flag = 1
                    end = j
                    break
            break
    if flag == 1:  # 检查到了专有名词
        for i in range(start, end + 1):
            result = result + words[i]
        return result
    else:
        return str


def extract(line):
    global aa, bb, cc, dd,tx,txx,non,unsuc
    text = []
    result = []
    place = ''
    # line = re.sub('', '', line)
    line = re.sub('并报案', '', line)  # 去除掉句子里"盗窃罪"，因为影响抽取结果
    line = re.sub('(?<=在).*(?=授意下)', '', line)  # 去除掉句子里的"在xxx授意下"
    line = re.sub('\\(.*?\\)', '', line)  # 英文括号
    line = re.sub('\\（.*?\\）', '', line)  # 去除掉句子里的中文括号及括号内容，因为里面一些标点符号影响抽取结果
    line = re.sub('\\(.*?\\）', '', line)
    # line = re.sub('^.*(?=人民检察院)','',line)

    mm = re.findall("\d,\d", line)  # 将金额里的英文逗号去掉，即将1,000改为1000
    if mm:
        for i in mm:
            line = line.replace(i, i.replace(",", ""))

    line = re.sub(',', '，', line)  # 将句子里的英文标点符号变成中文标点符号
    sen_count = 0
    '''if len(re.findall(r".*人民检察院",line))!=0:
        place=re.findall(r".*人民检察院",line)[0]
        place=place.replace("人民检察院", "")
    elif len(re.findall(r".*铁路运输检察院",line))!=0:
        place=re.findall(r".*铁路运输检察院",line)[0]
        place=place.replace("铁路运输检察院", "")'''
    if len(re.findall("刑事判决书(.*?)人民法院刑事判决书", line)) != 0 and len(re.findall("刑事判决书(.*?)人民法院刑事判决书", line))<30:
        place = re.findall("刑事判决书(.*?)人民法院刑事判决书", line)[0]
        place = place.replace("人民法院刑事判决书", "")
    elif len(re.findall("刑事判决书(.*?)人民检察院刑事判决书", line)) != 0 and len(re.findall("刑事判决书(.*?)人民检察院刑事判决书", line))<30:
        place = re.findall("刑事判决书(.*?)人民检察院刑事判决书", line)[0]
        place = place.replace("人民法院刑事判决书", "")
    elif len(re.findall("刑事裁定书(.*?)人民法院刑事裁定书", line)) != 0 and len(re.findall("刑事裁定书(.*?)人民法院刑事裁定书", line))<30:
        place = re.findall("刑事裁定书(.*?)人民法院刑事裁定书", line)[0]
        place = place.replace("人民法院刑事裁定书", "")
    elif len(re.findall("刑事裁定书(.*?)人民法院刑事裁定书", line)) != 0 and len(re.findall("刑事裁定书(.*?)人民法院刑事裁定书", line))<30:
        place = re.findall("刑事裁定书(.*?)人民检察院刑事裁定书", line)[0]
        place = place.replace("人民检察院刑事裁定书", "")
    print("place:", place)

    strlist = re.split(r'[；。]', line)  # 用句号分割字符串，因为每个句子代表一个事件
    person = []
    address = ''
    time = ''

    for value in strlist:
        print("value:",value)
        sen_count = sen_count + 1
        #if ((len(re.findall(r"(\d{4}年\d{1,2}月\d{1,2}日|\d{4}年\d{1,2}月中旬|\d{4}年\d{1,2}月上旬|\d{4}年\d{1,2}月下旬|\d{4}年\d{1,2}月|\d{4}年|\d{1,2}时\d{2}分|某年某月某日|\d{1,2}时许|同年\d{1,2}月\d{1,2}日|次日)",value)) != 0)) and \

        if "出生" not in value and "日生" not in value and "\n" not in value\
             and ('''"盗" in value or "窃" in value or "拿走" in value or "携赃" in value or "作案" in value or "搬到" in value or "试图剪断" in value or "偷" in value or "装入" in value or "撬开" in value or "电表" in value or "装在" in value or "吸取被害人" in value or "开锁骑走" in value''') \
             and "自首" not in value and "经侦查" not in value and "如实供述" not in value and "补缴" not in value and "报警" not in value  and "查获" not in value and "人赃并获" not in value \
             and "在被公安机关盘问" not in value and "被公安机关依法传唤"not in value and "判处" not in value and "被释放" not in value  and "起获" not in value and "带领民警" not in value and "共计窃得"not in value\
             and "缴获" not in value and "重大作案嫌疑" not in value and "扭获" not in value and "搜查到" not in value and "承认" not in value and "行政拘留" not in value and "反窃电" not in value \
             and "经检定" not in value and "经计算" not in value and "经检测" not in value and "主动供述" not in value and "窃电行为" not in value and "被公安机关抓获" not in value \
             and "被北京市公安局" not in value and "被抓获归案" not in value and "将被盗手机发还给" not in value and "上述被窃" not in value and "被公安民警抓获" not in value and "时被发现抓获"not in value and "有盗窃嫌疑"not in value\
             and "价格卖掉" not in value and "予以否认"not in value and "被公安人员当场人赃俱获" not in value and "执勤民警发现" not in value and "将被盗电动车归还" not in value and "被抓获到案" not in value and "私接线路的窃电量" not in value\
             and "帮助民警" not in value and "民警抓获" not in value and "获得表扬" not in value and "驳回上诉" not in value and "维持原判" not in value \
             and "报送本院审理" not in value and "剥夺政治权利" not in value and "被减刑" not in value and "提起公诉" not in value and "悔改表现" not in value and "服刑" not in value \
             and "审理" not in value and "立案" not in value and "羁押" not in value and "执行刑罚" not in value and "减刑建议" not in value and "报送本院" not in value and "刑期执行至" not in value\
             and "表扬" not in value and "劳动" not in value and "欠产" not in value and "被评为" not in value and "刑事裁定" not in value and "刑事判决" not in value \
             and "审理终结" not in value and "判决生效后" not in value and "遵守法律法规" not in value and "教育改造" not in value and "积极参加" not in value \
             and "法律效力" not in value and "提出上诉" not in value and "交付执行" not in value and "辩护人" not in value and "律师" not in value and "考核期间" not in value and "认罪悔罪" not in value\
            \
            :  # 如果句子中包含时间，则可能为盗窃事件

            value = value.replace("1.", "")
            value = value.replace("2.", "")
            value = value.replace("3.", "")
            value = value.replace("4.", "")
            value = value.replace("5.", "")
            value = value.replace("6.", "")
            value = value.replace("7.", "")
            value = value.replace("8.", "")
            value = value.replace("9.", "")
            value = value.replace("10.", "")
            value = value.replace("11.", "")
            value = value.replace("12.", "")
            value = value.replace("13.", "")
            value = value.replace("14.", "")
            value = value.replace("15.", "")
            value = value.replace("一、", "")
            value = value.replace("二、", "")
            value = value.replace("三、", "")
            value = value.replace("四、", "")
            value = value.replace("五、", "")
            value = value.replace("六、", "")
            value = value.replace("七、", "")
            value = value.replace("八、", "")
            value = value.replace("九、", "")
            value = value.replace("十、", "")

            eventlist = value.split('，')
            sub = []
            subject = []

            for i in eventlist:
                if "被盗" not in i and "到案后被告人" not in i \
                        and "接受调查" not in i and "民警经侦查" not in i:
                    sub.append(i)

            print('sub:', sub)
            file5.write("sub:")
            file5.write(str(sub))
            file5.write('\n')

            flag = 0  # 没有找到地点
            flag_name = 0  # 没有找到被告
            flag_yu = 0  # 被告人姓于

            text_dict = {}

            text_dict["时间"] = ''
            text_dict["地点"] = ''
            text_dict["人物"] = []
            for j in sub:
                dateArray = re.findall(
                    r"(\d{4}年\d{1,2}月\d{1,2}日|\d{4}年\d{1,2}月中旬|\d{4}年\d{1,2}月上旬|\d{4}年\d{1,2}月下旬|\d{4}年\d{1,2}月|\d{1,2}月\d{1,2}日|\d{4}年|\d{1,2}月|\d{1,2}日|次日|\d{1,2}时\d{1,2}分|某年某月某日|\d{1,2}时许|同年\d{1,2}月\d{1,2}日)",
                    j)
                if len(dateArray) != 0:

                    if len(dateArray) > 1:  # 时间区间，多个时间
                        start = j.find(dateArray[0])
                        end = j.find(dateArray[len(dateArray) - 1]) + len(dateArray[len(dateArray) - 1])
                        text_dict["时间"] = j[start:end]
                    else:  # 单个时间
                        text_dict["时间"] = dateArray[0]
                    j = j.replace(text_dict["时间"], "")  # 把时间去掉，防止影响抽取结果

                if "被告" in j and flag_name == 0:  # 尚未找到被告

                    if len(j.split("被告人")) == 1:
                        name = j.split("被告", 1)  # 被告xxx ，只切割第一个出现的被告
                    else:
                        name = j.split("被告人", 1)

                    if name[1].startswith("于"):  # 被告人姓于的情况（被告人于xx于某年某月在某地盗窃某物）
                        name[1] = name[1].replace(name[1][0], '')  # 去掉开头第一个"于"，方便后续提取时间
                        flag_yu = 1

                    if "于" in name[1] and "停放于" not in name[1]:  # 被告人xxx于某年某月在某地盗窃某物,已经提取到时间
                        name1 = name[1].split("于", 1)  # 提取被告人名字

                        if flag_yu == 0:
                            text_dict["人物"] = processPerson(name1[0])
                        else:
                            text_dict["人物"] = processPerson("于" + name1[0])  # 姓于的被告人
                        flag_name = 1  # 找到人物

                        # 在某地
                        if findAddress3(name1[1]) != None and flag == 0:
                            text_dict["地点"] = findAddress3(name1[1])
                            flag = 1  # 找到地点

                    elif flag == 0 and findAddress2(j, name[1]) != None:  # 先前的句子中没有提取到地点，在这个句子中提取到了地点
                        if findAddress2(j, name[1])[0] != None:  # 被告人xxx在某地盗窃某物
                            if flag_yu == 0:
                                text_dict["人物"] = processPerson(findAddress2(j, name[1])[0])
                            else:
                                text_dict["人物"] = processPerson("于" + findAddress2(j, name[1])[0])  # 姓于的被告人
                            flag_name = 1
                        if len(findAddress2(j, name[1])) > 1 and findAddress2(j, name[1])[1] != None:
                            text_dict["地点"] = findAddress2(j, name[1])[1]
                            flag = 1  # 默认第一个找到的地址是作案地址
                    else:
                        text_dict["人物"] = processPerson(name[1])  # "被告人xxxx"单独是一个短句
                        flag_name = 1
                # 没有"被告人"的标志的情况，xxx（伙同xxx）
                if text_dict["人物"] == []:
                    temp = re.findall('[\u4e00-\u9fa5]{3}伙同[\u4e00-\u9fa5]{3}', j)
                    temp1 = re.findall('[\u4e00-\u9fa5]{3}和[\u4e00-\u9fa5]{3}', j)
                    temp2 = re.findall('[\u4e00-\u9fa5]{3}与[\u4e00-\u9fa5]{3}', j)
                    temp3 = re.findall('[\u4e00-\u9fa5]{3}纠集[\u4e00-\u9fa5]{3}', j)
                    temp4 = re.findall('[\u4e00-\u9fa5]{1}某某', j)

                    if len(temp) != 0:
                        text_dict["人物"] = processPerson(temp[0])
                    elif len(temp1) != 0:
                        text_dict["人物"] = processPerson(temp1[0])
                    elif len(temp2) != 0:
                        text_dict["人物"] = processPerson(temp2[0])
                    elif len(temp3) != 0:
                        text_dict["人物"] = processPerson(temp3[0])
                    elif len(temp4) != 0 and j.startswith(temp4[0]):
                        text_dict["人物"] = processPerson(temp4[0])

                if flag == 0 and findAddress3(j) != None:  # 在某地，尚未找到地址，在这个句子中提取到了地点

                    text_dict["地点"] = findAddress3(j)
                    flag = 1

                # 盗窃某物，可能有多个物品，所以要用数组。添加NER技术的
                if findThing(j) != None:
                    j = j.replace("微信、支付宝", "微信支付宝")
                    objects = re.split(r'[、和 以及]', findThing(j))  # 对于顿号隔开的物品要分别处理
                    for obj in objects:
                        subject.append(NER2(obj))
                elif NER(j)!= None:
                    subject.append(NER(j))
                '''if findThing(j) != None and findThing(j) != '':  # 盗窃某物，可能有多个物品，所以要用数组
                    objects = re.split(r'[、和 及]', findThing(j))  # 对于顿号隔开的物品要分别处理
                    for obj in objects:
                        subject.append(obj)'''
                    # subject.append(findThing(j))
                if text_dict["地点"] == '' and findAddress4(j) != None:
                    text_dict["地点"] = findAddress4(j)
                    flag = 1
                if text_dict["地点"] == '' and place != '':
                    # print("aaaa")
                    text_dict["地点"] = place
                    flag = 1

                if person == []:
                    person = text_dict["人物"]  # 把第一个出现的人物赋值给person，缓存下来
                if address == '':
                    address = text_dict["地点"]  # 把第一个出现的地点赋值给place，缓存下来
                if time == '':
                    time = text_dict["时间"]  # 把第一个出现的地点赋值给place，缓存下来

            text_dict["物品"] = subject
            if (text_dict["人物"] == [] or text_dict["人物"] == ['']) and person != []:
                text_dict["人物"] = person
            if (text_dict["地点"] == '' or "上址" in text_dict["地点"]) and address != '':
                text_dict["地点"] = address

            prefix = re.findall(r"(\d{4}年\d{1,2}月\d{1,2}日)", time)  # 以第一次出现的时间年月日作为基准
            t2 = re.findall(r"(\d{1,2}时\d{1,2}分|\d{1,2}时许)", text_dict["时间"])
            t3 = re.findall(r"(同年\d{1,2}月\d{1,2}日)", text_dict["时间"])
            # 替换"次日"的时间
            if text_dict["时间"].startswith("次日") and len(prefix) != 0:
                text_dict["时间"] = re.findall(r"(\d{4}年\d{1,2}月)", time)[0] + str(
                    int(re.findall(r"(\d{1,2}日)", time)[0].split("日")[0]) + 1) + "日" + text_dict["时间"].split("次日")[1]
            if len(t2) != 0 and len(prefix) != 0:
                text_dict["时间"] = prefix[0] + t2[0]
            if len(t3) != 0 and len(prefix) != 0:
                text_dict["时间"] = t3[0].replace("同年", re.findall(r"(\d{4}年)", time)[0])
            text.append(sub)

            # print(text_dict)
            print("text_dict:", text_dict)
            file5.write("text_dict:")
            file5.write(str(text_dict))
            file5.write('\n')
            # 筛选数据，如果事件没有时间|物品|地点，则删除该事件，不添加进最终的结果中
            if text_dict["时间"] == '' or text_dict["地点"] == '' or text_dict["物品"] == '':
                # ttt+=1
                print(1111)
                #result.append(text_dict)
            else:
                result.append(text_dict)
    print("Text:",text)
    file5.write("Text:")
    file5.write(str(text))
    file5.write('\n')
    file6.write("Text:")
    file6.write(str(text))
    file6.write('\n')
    if str(text) != '[]':
        # 复杂案件提不出物品；第一句话提不出人物或地点的（保留第一句话就是为了提取出人物或地点）
        if len(result)>1:
            txx+=1
            flag=0
            for i in range(0,len(result)):
                if result[i]["时间"] == '' and flag!=0:
                    aa += 1
                    flag=1
                    break
                elif result[i]["人物"] == [] and flag!=0:
                    dd += 1
                    flag = 1
                    break
                elif result[i]["地点"] == '' and flag!=0:
                    cc += 1
                    flag = 1
                    break
                elif result[i]["物品"] == [] and flag!=0:
                    bb += 1
                    flag = 1
                    break
        elif len(result)==1:
            tx+=1
            if result[0]["时间"] == '':
                aa += 1
            elif result[0]["人物"] == []:
                dd += 1
            elif result[0]["地点"] == '':
                cc += 1
            elif result[0]["物品"] == []:
                bb += 1
        else:
            unsuc+=1
        if len(result) == 2 and (result[0]["人物"] == [] or result[0]["人物"] == ['']) and result[1]["人物"] != []:
            result[0]["人物"] = result[1]["人物"]
        if len(result) == 0 or (len(result) == 1 and (result[0]["物品"] == [] or result[0]["地点"] == '' or result[0]["人物"] == [] or result[0]["时间"] == '')):
            print()
            '''if len(result)>0 and result[0]["时间"] == '':
                aa += 1
            elif len(result)>0 and result[0]["人物"] == []:
                bb += 1
            elif len(result)>0 and result[0]["地点"] == '':
                cc += 1'''
            #tx+= 1
        else:
            dic = {}
            dic['result'] = result
            dicJson = json.dumps(dic, ensure_ascii=False)
            file4.write(dicJson)
            file4.write('\n')
            #txx+= 1
    else:non+=1
    # print("ttt:",ttt)

def main():
    file1 = open('./TemplateExtract_rob/hard.txt', encoding='utf-8')
    num = 0
    # aa = bb = cc = dd = 0
    # tx  = non = unsuc = 0
    global aa,bb,cc,dd
    global tx,txx,non,unsuc
    for line in file1:
        num += 1
        #if (num == 924 or num == 2412):
            #continue
        print(num, ":")
        if len(line) < 10:
            count1 = count1 + 1
            continue
        else:
            extract(line)
    print("时间为空：",aa,"物品为空：",bb,"地点为空：",cc,"人物为空：",dd)
    print("简单：",tx,"复杂：",txx,"未提取出：",unsuc,"无效：",non)


if __name__=='__main__':
    main()