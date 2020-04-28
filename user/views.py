from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from eth_account import Account

from Eth_transaction.settings import web3, action
from stock.models import IPO
from user.models import Euser
from util.md5_password import encode_md5


def user_stock(request):
    """
    获取单个用户的地址、私钥、余额，所持证券的信息
    """
    private_key = request.session.get('private_key')
    address = request.session.get('address')
    name = request.session.get('address')
    balance = web3.fromWei(web3.eth.getBalance(address, 'latest'), 'ether')
    return render(request, 'user/user_stock.html', {
        'euser': {
            'private_key': private_key,
            'address': address,
            'balance': balance,
            'name': name
        }
    })


def get_list(request):
    """
    获取jqgrid的信息：用户所持股票的详情信息
    """
    address = request.session.get('address')
    private_key = request.session.get('private_key')
    data = []
    print(address)
    nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(address))
    txn_dict = action.functions.get_stockers_all_stocks(web3.toChecksumAddress(address)).buildTransaction({
        'nonce': nonce,
        "from": web3.toChecksumAddress(address),
    })
    signed_txn = web3.eth.account.signTransaction(txn_dict, private_key=private_key)
    result_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    id_count = action.functions.get_id_counts().call()
    stocks = list(zip(id_count[0], id_count[1]))
    print(stocks)
    for i in stocks:
        company_name = IPO.objects.get(stock_id=str(i[0])).company_name
        data.append({
            'stock_id': i[0],
            'company_name': company_name,
            'stock_count': i[1],
            'status': '持有'
        })

    rows = request.GET.get('rows', 4)
    page = request.GET.get('page', 1)
    paginator = Paginator(data, int(rows))
    try:
        rows = list(paginator.page(page).object_list)
    except Exception as tips:
        print(tips)
        rows = list(paginator.page(int(page) - 1).object_list)
        page = int(page) - 1

    page_data = {
        'page': page,
        'total': paginator.num_pages,
        'records': paginator.count,
        'rows': rows
    }
    return JsonResponse(page_data, safe=False)


@csrf_exempt
def register(request):
    """
    渲染注册界面
    """
    return render(request, 'user/register.html')


@csrf_exempt
def register_form(request):
    """
    注册逻辑的实现
    """
    try:
        name = request.POST.get('name')
        password = request.POST.get('password')
        ac = Account.create()
        with transaction.atomic():
            Euser.objects.create(private_key=str(ac._key_obj),
                                 address=ac.address,
                                 name=name,
                                 password=encode_md5(password))
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})


def login(request):
    """渲染登录界面"""
    return render(request, 'user/login.html')


def check_user(request):
    """注册时，检查用户名是否重复"""
    return HttpResponse()


@csrf_exempt
def login_form(request):
    """
    登录逻辑的实现
    登录成功时，将私钥，地址，用户id，用户名，存入session中
    """
    name = request.POST.get('name')
    password = request.POST.get('password')
    euser = Euser.objects.filter(name=name, password=encode_md5(password))
    if euser:
        request.session['private_key'] = euser[0].private_key
        request.session['address'] = euser[0].address
        request.session['euser_id'] = euser[0].id
        request.session['name'] = name
        print(request.session.get('private_key'))
        return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})


@csrf_exempt
def sell(request):
    """
    抛售股票的逻辑
    """
    stock_id = request.POST.get('sell_stock_id')
    stock_count = request.POST.get('sell_stock_count')
    stock_price = request.POST.get('sell_stock_price')
    print(stock_id, stock_count, stock_price)


    try:
        nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(request.session.get('address')))
        txn_dict = action.functions.sell(int(stock_id), int(stock_count), int(stock_price)).buildTransaction({
            'nonce': nonce,
            "from": web3.toChecksumAddress(request.session.get('address')),
        })
        signed_txn = web3.eth.account.signTransaction(txn_dict, private_key=request.session.get('private_key'))
        result_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})

    address = request.session.get('address')
    balance = web3.fromWei(web3.eth.getBalance(address, 'latest'), 'ether')
    return JsonResponse({'status': 1, 'balance': str(balance)})


def logout(request):
    """注销逻辑"""
    print('logout')
    try:
        request.session.flush()
        print(request.session.get('address'))
    except Exception or BaseException as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})
