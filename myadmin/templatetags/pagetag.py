from django import template
from django.utils.html import format_html

# 实例化标签对象
register = template.Library()

# # 自定义过滤器
# @register.filter
# def kong_upper(val):
#     # print ('val from template:',val)
#     return val.upper()

# 自定义标签
@register.simple_tag
def pageshow_mine(count,p):
    '''
        count 总页数
        p  当前页
        begin 开始页
        end 结束页
    '''
    # 开始页
    begin = p-4
    # 结束页
    end = p+5
    # 判断如果当前页 小于5
    if p < 5:
        # 则开始页为1
        begin = 1
        # 结束页为10
        end = 10
    # 判断如果当前页 大于 总页数-5
    if count<10:
        begin=1
        end = count
    # 当前页如果大于总页数-5
    if p > count-5:
        # 则开始页为总页数-9
        begin = count - 9
        # 结束页为总页数
        end = count
    # 判断如果开始页 小于等于 0,则开始页为1
    if begin <= 0:
        begin = 1

    for x in range(begin,end+1):
        print(x)

@register.simple_tag
def pageshow(count,request):
    '''
        count 总页数
        p  当前页
        begin 开始页
        end 结束页
    '''
    # 注意请求的数据是字符串类型
    p = int(request.GET.get('p',1))
    # count = int(count)
    print('当前页: ', p, type(p))  #
    print('总页数: ', count,type(count))
    begin = p - 4
    end = p + 5

    # ==================  去掉分页的边界问题  ========================

    # 判断如果当前p 小于5
    if p < 5:
        begin = 1
        end = 10
    # 判断当前页 如果大于 总页数-5
    if p > (count - 5):
        begin = count - 9
        end = count
    # 如果 总页数小于10
    if count < 10:
        begin = 1
        end = count
    # =================  获取表单提交的数据  =========================
    select = request.GET.get('types')
    keyword = request.GET.get('keyword')
    print('types : ', select)
    print('keyword: ', keyword)

    # ====  拼接  template/myadmin/user/index.html 中的标签 pageshow 所需的内容
    res = ''
    print('begin' , begin)
    print('end', end)
    for i in range(begin, end+1):
        if i == p:
            res += '<li class="am-active"><a href="?p=' + str(p)   + '">' + str(p) + ' </a></li>'
        else:
            res += '<li ><a href="?p=' + str(i) + '">' + str(i) + ' </a></li>'
    return format_html(res)

@register.simple_tag
def ShowPages(count, request):
    '''
    count  总页数      100
    p      当前页码     1

    begin 开始页
    end  结束页

    return 10个页码数
    '''
    p = int(request.GET.get('p', 1))

    begin = p - 4
    end = p + 5
    # 判断如果当前p 小于5
    if p < 5:
        begin = 1
        end = 10
    # 判断当前页 如果大于 总页数-5
    if p > (count - 5):
        begin = count - 9
        end = count
    # 如果 总页数小于10
    if count < 10:
        begin = 1
        end = count

    # 获取页面上的其它搜索条件 &types=username&keywords=da
    data = request.GET.dict()
    data.pop('p', None)
    res = ''
    for k, v in data.items():
        res += '&' + k + '=' + v

    # {'types': 'username', 'keywords': 'da'}
    #  &types=username&keywords=da


    ps = ''
    # 上一页
    if p > 1:
        ps += '<li><a href="?p=' + str(p - 1) + res + '">«</a></li>'

    for x in range(begin, end + 1):
        # 判断是否为当前页
        if p == x:
            ps += '<li class="am-active"><a href="?p=' + str(x) + res + '">' + str(x) + '</a></li>'
        else:
            ps += '<li><a href="?p=' + str(x) + res + '">' + str(x) + '</a></li>'
    if p < count:
        ps += '<li><a href="?p=' + str(p + 1) + res + '">»</a></li>'

    return format_html(ps)

# 实现缩进效果
@register.simple_tag
def ind(path): # '0,'
    # var = 'a,d,s,gsdad,sg'.split(',')
    # print(var,type(var)) # ['a', 'd', 's', 'gsdad', 'sg'] <class 'list'>
    res = path.split(',')
    # print(res) # ['0', '']　＃　ength = 2
    res = len(res) - 2
    # print(res)
    res = res * "--->"

    return res

# 列表页的分类
@register.simple_tag
def ShowPagesHome(count, request):
    '''
    count  总页数      100
    p      当前页码     1
    begin 开始页
    end  结束页
    return 10个页码数
    '''
    p = int(request.GET.get('p', 1))
    sorttype = request.GET.get('sorttype', 'index')
    catetype = request.GET.get('catetype', '')
    goodtype = request.GET.get('goodtype', '')


    begin = p - 4
    end = p + 5
    # 判断如果当前p 小于5
    if p < 5:
        begin = 1
        end = 10
    # 判断当前页 如果大于 总页数-5
    if p > (count - 5):
        begin = count - 9
        end = count
    # 如果 总页数小于10
    if count < 10:
        begin = 1
        end = count

    # 获取页面上的其它搜索条件 &types=username&keywords=da
    data = request.GET.dict()
    data.pop('p', None)
    res = ''
    for k, v in data.items():
        res += '&' + k + '=' + v

    # {'types': 'username', 'keywords': 'da'}
    #  &types=username&keywords=da

    ps = ''
    # 上一页
    if p > 1:
        ps += '<li><a href="?sorttype=' + sorttype + '&catetype=' + catetype + '&goodtype=' + goodtype + '&p=' + str(p - 1) + res + '"> << </a></li>'

    for x in range(begin, end + 1):
        # 判断是否为当前页
        if p == x:
            ps += '<li class="am-active"><a href="?sorttype=' + sorttype + '&catetype=' + catetype + '&goodtype=' + goodtype + '&p=' + str(x) + res + '">' + str(x) + '</a></li>'
        else:
            ps += '<li><a href="?sorttype=' + sorttype + '&catetype=' + catetype + '&goodtype=' + goodtype + '&p=' + str(x) + res + '">' + str(x) + '</a></li>'
    if p < count:
        ps += '<li><a href="?sorttype=' + sorttype + '&catetype=' + catetype + '&goodtype=' + goodtype + '&p=' + str(p + 1) + res + '"> >> </a></li>'

    return format_html(ps)
