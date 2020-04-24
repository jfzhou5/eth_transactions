from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from eth_account import Account

from Eth_transaction.settings import web3, action
from stock.models import IPO
from user.models import Euser
from util.md5_password import encode_md5


def user_stock(request):
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
    # action.functions.get_stockers_all_stocks(web3.toChecksumAddress(address)).call()
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
    return render(request, 'user/register.html')


@csrf_exempt
def register_form(request):
    try:
        name = request.POST.get('name')
        password = request.POST.get('password')
        ac = Account.create()
        with transaction.atomic():
            Euser.objects.create(private_key=str(ac._key_obj), address=ac.address, name=name,
                                 password=encode_md5(password))
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})


def login(request):
    return render(request, 'user/login.html')


def check_user(request):
    return HttpResponse()


@csrf_exempt
def login_form(request):
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
    stock_id = request.POST.get('sell_stock_id')
    stock_count = request.POST.get('sell_stock_count')
    stock_price = request.POST.get('sell_stock_price')
    print(stock_id,stock_count,stock_price)
    try:
        nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(request.session.get('address')))
        txn_dict = action.functions.sell(int(stock_id), int(stock_count), int(stock_price)).buildTransaction({
            'nonce': nonce,
            "from": web3.toChecksumAddress(request.session.get('address')),
        })
        signed_txn = web3.eth.account.signTransaction(txn_dict,private_key=request.session.get('private_key'))
        result_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})
