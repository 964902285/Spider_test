# 爬取熊猫TV绝地求生版块直播中各主播人气排名

import re
from urllib import request


# *匹配0次或者无限多次
# ?非贪婪模式
# ()元组去除多余的标签
# 断点调试
class Spider():
    url = 'https://www.panda.tv/cate/pubg?pdt=1.24.psbar-re.0.7c79cspu5od'
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<span class="video-number">([\s\S]*?)</span>'

    # __表示私有方法
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        # bytes
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    def __analysis(self, htmls):
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)
        # print(anchors[1])
        return anchors

# 精炼数据

    def __refine(self, anchors):
        l = lambda anchor: {
            'name': anchor['name'][0].strip(),
            'number': anchor['number'][0]
            }
        return map(l, anchors)

# 排序数据
# reverse表示是否降序,默认升序

    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)

        return anchors
# 种子函数：按关键字即数字大小排列

    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

# 展现数据

    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print('排名' + str(rank + 1) + ' : ' + anchors[rank]['name'] +
                  '   ' + anchors[rank]['number'])


# 入口方法

    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)


spider = Spider()
spider.go()
