from django.shortcuts import render

from Buyer.models import *
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponse

import time
from Store.views import *
from alipay import AliPay

def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login/")
    return inner

def register(request):
    if request.method == "POST":
        # 获取前端post请求的数据
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")

        # 将数据存入数据库
        buyer = Buyer()
        buyer.username = username
        buyer.password = set_password(password)
        buyer.email = email
        buyer.save()
        # 跳转到login页面
        return HttpResponseRedirect("/Buyer/login/")
    return render(request,"buyer/register.html")

# def ajax_userValid(request):
#     result = {"status":"error","content":""}
#     username = request.GET.get("username")
#     if username:
#         user = ajax_userValid(username)
#         if user:
#             result["content"] = "用户名已经存在"
#         else:
#             result["content"] = "用户名可以使用"
#             result["status"]="success"
#     else:
#         result["content"] = "用户名不可以为空"
#     return JsonResponse(result)

def login(request):
    if request.method == "POST":
        # 获取数据
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        if username and password:
            # 判断用户是否存在
            user = Buyer.objects.filter(username=username).first()
            if user:
                # 密码加密比对
                web_password = set_password(password)
                if user.password == web_password:
                    response = HttpResponseRedirect("/Buyer/index")
                    # 校验的登陆
                    response.set_cookie("username",user.username)
                    request.session["username"]= user.username
                    # 方便其他查询
                    response.set_cookie("user_id",user.id)

                    return response
    return render(request,"buyer/login.html")

@loginValid
def index(request):
    result_list = [] #定义一个容器用来存放结果
    goods_type_list = GoodsType.objects.all() #查询所有的类型
    for goods_type in goods_type_list: #循环类型
        goods_list = goods_type.goods_set.values()[:4]  #查询前4条
        if goods_list: #如果类型对应的值
            goodsType = {
                "id":goods_type.id,
                "name":goods_type.name,
                "description":goods_type.description,
                "picture":goods_type.picture,
                "goods_list":goods_list
            } #构建输出结果
            # 查询类型当中有数据的数据
            result_list.append(goodsType) #有数据的类型放入result_list
    return render(request,"buyer/index.html",locals())

@loginValid
def goods_list(request):
    """
    前台列表页
    :param reuqest:
    :return:
    """
    goodsList = []
    type_id = request.GET.get("type_id")
    #获取类型
    goods_type = GoodsType.objects.filter(id = type_id).first()
    if goods_type:
        # 查询所有上架的产品
        goodsList = goods_type.goods_set.filter(goods_state = 1)
    return render(request,"buyer/goods_list.html",locals())

def logout(request):
    response = HttpResponseRedirect("/Buyer/login/")
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session["username"]
    return response


def goods_detail(request):
    goods_id = request.GET.get("id")
    if goods_id:
        # goods = Goods.objects.filter(id=int(goods_id)).first()
        goods = Goods.objects.filter(id=goods_id).first()
        if goods:
            return render(request, "buyer/goods_detail.html",locals())
    return HttpResponse("没有您指定的商品")


def setOrderId(user_id,goods_id,store_id):
    """
        设置订单编号
        时间+用户id+商品的id+商铺+id
    """
    strtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
    return strtime+user_id+goods_id+store_id

def place_order(request):
    if request.method == "POST":
        # post数据
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")
        # cookie数据
        user_id = request.COOKIES.get("user_id")
        # 数据库的数据
        goods = Goods.objects.get(id=goods_id)
        store_id = goods.store_id.id
        price = goods.goods_price
        # 保存订单
        order = Order()
        order.order_id = setOrderId(str(user_id),str(goods_id),str(store_id))
        order.goods_count = count
        order.order_user = Buyer.objects.get(id=user_id)
        order.order_price = count * price
        order.order_status = 1
        order.save()
        # 订单详情
        order_detail = OrderDetail()
        order_detail.order_id = order
        order_detail.goods_id = goods_id
        order_detail.goods_name = goods.goods_name
        order_detail.goods_price = goods.goods_price
        order_detail.goods_number = count
        order_detail.goods_total = count*goods.goods_price
        order_detail.goods_store = store_id
        order_detail.goods_image = goods.goods_image
        order_detail.save()

        detail = [order_detail]

        return render(request,"buyer/place_order.html",locals())
    else:
        order_id = Order.objects.get("order_id")
        if order_id:
            order = Order.objects.get(id=order_id)
            detail = order.orderdetail_set.all()
            return render(request,"buyer/place_order.html",locals())
        else:
            return HttpResponse("非法请求")

def pay_result(request):
    """
        支付宝支付成功自动用get请求返回的参数
        #编码
        charset=utf-8
        #订单号
        out_trade_no=10002
        #订单类型
        method=alipay.trade.page.pay.return
        #订单金额
        total_amount=1000.00
        #校验值
        sign=enBOqQsaL641Ssf%2FcIpVMycJTiDaKdE8bx8tH6shBDagaNxNfKvv5iD737ElbRICu1Ox9OuwjR5J92k0x8Xr3mSFYVJG1DiQk3DBOlzIbRG1jpVbAEavrgePBJ2UfQuIlyvAY1fu%2FmdKnCaPtqJLsCFQOWGbPcPRuez4FW0lavIN3UEoNGhL%2BHsBGH5mGFBY7DYllS2kOO5FQvE3XjkD26z1pzWoeZIbz6ZgLtyjz3HRszo%2BQFQmHMX%2BM4EWmyfQD1ZFtZVdDEXhT%2Fy63OZN0%2FoZtYHIpSUF2W0FUi7qDrzfM3y%2B%2BpunFIlNvl49eVjwsiqKF51GJBhMWVXPymjM%2Fg%3D%3D&trade_no=2019072622001422161000050134&auth_app_id=2016093000628355&version=1.0&app_id=2016093000628355
        #订单号
        trade_no=2019072622001422161000050134
        #用户的应用id
        auth_app_id=2016093000628355
        #版本
        version=1.0
        #商家的应用id
        app_id=2016093000628355
        #加密方式
        sign_type=RSA2
        #商家id
        seller_id=2088102177891440
        #时间
        timestamp=2019-07-26
        """
    return render(request,"buyer/pay_result.html",locals())

def pay_order(request):
    money = request.GET.get("money") #获取订单金额
    order_id = request.GET.get("order_id") #获取订单id

    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0bIed2r/KZXSKMahA1srQPlij5Wz6Sm7ro2T2PgD/iBMIIvph6vN2WMBtBzBpUehvK6+MuzELL92FSASEL+ypTLdDhlneo0519BCgOGCmuTBTxDCWHecdn28/ddbNXeFFOPGhbTieW3KcQu3FeJgxCyqxi0RLdPnFLQzy9c+JQPiWUlJDXLKrdO5bi1BD0po3El5gluFK57VOIAh5RdR5WQXw0ikjNAbH55/zjYM7jnJWAzJVUaw5W/DSVYMN8SCTaJC8BnVxwbrhkkR/Jj5ZrkHybUMnZXddD6UJNqQMX7SE+oLzsmHNnh1th6xUcYG+7OdjslAsVQFI6m6skyQsQIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEA0bIed2r/KZXSKMahA1srQPlij5Wz6Sm7ro2T2PgD/iBMIIvph6vN2WMBtBzBpUehvK6+MuzELL92FSASEL+ypTLdDhlneo0519BCgOGCmuTBTxDCWHecdn28/ddbNXeFFOPGhbTieW3KcQu3FeJgxCyqxi0RLdPnFLQzy9c+JQPiWUlJDXLKrdO5bi1BD0po3El5gluFK57VOIAh5RdR5WQXw0ikjNAbH55/zjYM7jnJWAzJVUaw5W/DSVYMN8SCTaJC8BnVxwbrhkkR/Jj5ZrkHybUMnZXddD6UJNqQMX7SE+oLzsmHNnh1th6xUcYG+7OdjslAsVQFI6m6skyQsQIDAQABAoIBADZ4jnF22dFzmaP99NVqWVIHdhLWUGXA8X/mRwGVa3QX766EqaUUe+R8U3T2A1drxBe/TKjt2AfHtGTIb+jp4v4GuGVxM/Ahv2TQNHZGHiceRRjEwbc5WutsvisyRf8djPRgNrGEy0+/tVaoNGb65ygOck4IZu4AnYZDSTEqOHpkj13VKtdqyXlKhOhyrBCsIpvi4t/EnrXSoHSW4rPBG6Zl+rGJL29+eD+Ct7nX3iFCrbtsBYfPefg9KP38fCuFWPfBgyLerb+LrHac9Ku8WlgS+H1GdWRAUH6Lx8On2AaN7eXOEcRkYndWDhmy9jmVGA41ESBbxcOSb2V9ONz1oAECgYEA9C+P17YUO+j4HRay3qk28IWe4QxYGUovSs6VYFSq3FIfVL+3tnGq2oIG7Y2cmU/69rc9LypWSIeO48kFqUPWClx+y6UeZUfVx0yzLHUjzNQBp3zcgHLiQxpCZv3OUEtbusyyQUj53gQEd7fB6ydhanhO+oSuoPqx1KjEd1VVzHkCgYEA29de2JxWXSTMPUJuhut8kEcvbRzgzDRsUYX0/gkl+NSwDbpdbUDzknNSaOusVtlr1JTf8uReGF75ZVlBE28YvzQb1/LlDeB+b0IbBShnm+ewY+fPH7wt/2vYePNTDSf46zEkq3K2DdU2UQE70BUMxGdJN+PlHkeXzILi4cQ0Z/kCgYB3WFOma2CCU4AIv5JWzz+B2NzpQ14/pgltN4C8n0UO/7g+dKF2syF9QHXgXwk9yWBweuiVh8y6ED8fR53Tt8sCL2jtYVt0xuJOUUd1IB+KOchBMv6WbQ/3GfuAWOYgSmSf7PHmhKNTBoWkeZR2uT2ciwaW3Ih5N2348S9s37FaiQKBgQCq4ggpm6xODpJrc73yRg23IH4u9GmQkZc470V2Saoodzq6EQkaKYirZ9TBFaAKikqVHXvOk9DIZNq6+tvovUyhI2IZRAbj+IKO/PV/1t5ig3/KyJ9pbZ7bkfrcWVdPPKjyOGrmke4NZpQn9yuFHTelWxvAw/aOyNun7n1pPFf4EQKBgFic3x8hJ0VPJtQkKsNAODdT7DNBhx4OQ65A3+V3imMV1SUUNmq12jmFdS2lv2n33k4feEg7+xJa5263oedYXZ5GaiLhTwEyv/nWPuMPkFuibaxppgj8/MkX9AjNsum0s7dxmWNHFQPVS71gOsTCWSKrnhP9CJCwBKyZM9EEaQzL
    -----END RSA PRIVATE KEY-----"""

    # 实例化支付应用
    alipay = AliPay(
        appid="2016101000652490",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )

    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 支付金额
        subject="生鲜交易",  # 交易主题
        return_url="http://127.0.0.1:8000/Buyer/pay_result/",
        notify_url="http://127.0.0.1:8000/Buyer/pay_result"
    )
    order = Order.objects.get(order_id=order_id)
    order.order_status = 2
    order.save()

    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)

def add_cart(request):
    result = {"state":"error","data":""}
    if request.method == "POST":
        # request请求
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")
        # 数据库查询
        goods = Goods.objects.get(id = int(goods_id))

        # cookie数据
        user_id = request.COOKIES.get("user_id")

        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_price = goods.goods_price
        cart.goods_total = goods.goods_price*count
        cart.goods_number = count
        cart.goods_picture = goods.goods_image
        cart.goods_id = goods.id
        cart.goods_store = goods.store_id.id
        cart.user_id = user_id
        cart.save()
        result["state"]="success"
        result["data"]="商品添加成功"
    else:
        result["data"]="请求错误"
    return JsonResponse(result)

# def cart(request):
#     user_id = request.COOKIES.get("user_id")
#     goods_list = Cart.objects.filter(user_id=user_id)
#     return render(request,"buyer/cart.html",locals())
def cart(request):
    user_id = request.COOKIES.get("user_id")
    goods_list = Cart.objects.filter(user_id=user_id)
    if request.method == "POST":
        post_data = request.POST
        cart_data = []
        for k,v in post_data.items():
            if k.startwith("goods_"):
                cart_data.append(Cart.objects.get(id=int(v)))
        goods_count = len(cart_data)
        goods_total = sum([int(i.goods_total) for i in cart_data])

        order = Order()
        order.order_id = setOrderId(user_id,goods_count,"2")
        order.goods_count = goods_count
        order.order_user = Buyer.objects.get(id = user_id)
        order.order_price = goods_total
        order.order_status = 1
        order.save()

        for detail in cart_data:
            order_detail = OrderDetail()
            order_detail.order_id = order
            order_detail.goods_id = detail.id
            order_detail.goods_name = detail.goods_name
            order_detail.goods_price = detail.goods_price
            order_detail.goods_number = detail.goods_number
            order_detail.goods_total = detail.goods_total
            order_detail.goods_store = detail.goods_store
            order_detail.goods_image = detail.goods_picture
            order_detail.save()

            url = "Buyer/place_order/?order_id=%s"%order.id

            return HttpResponseRedirect(url)
    return render(request,"buyer/cart.html",locals())

# Create your views here.
def base(request):
    return render(request,"buyer/base.html")