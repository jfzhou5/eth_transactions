import json

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from redis import Redis

from Eth_transaction.settings import action, web3
from stock.models import IPO

red = Redis(host='127.0.0.1', port=6379)


def index(request):
    name = request.session.get('address')

    return render(request, 'index/index.html', {
        'euser': {
            'name': name
        }
    })


def get_buys(request):
    """获取单页的买入队列信息"""
    buys_index = action.functions.get_buys_index().call()
    print(f"buys_index:{buys_index}")

    buys = []
    red.delete('buys')
    for i in range(buys_index):
        one = action.functions.get_buys(i).call()
        if one[1]:
            a = {
                'trans_addr': one[0],
                'stock_id': one[1],
                'stock_count': one[2],
                'stock_price': one[3],
                'category': '待抛售',
                'buys_index': i,
                'company_name': IPO.objects.get(stock_id=one[1]).company_name
            }
            buys.append(a)
            red.lpush('buys', json.dumps(a))

    rows = request.GET.get('rows', 4)
    page = request.GET.get('page', 1)
    paginator = Paginator(buys, int(rows))
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


def get_sells(request):
    sells_index = action.functions.get_sells_index().call()
    sells = []
    red.delete('sells')
    for i in range(sells_index):
        one = action.functions.get_sells(i).call()
        if one[1]:
            a = {
                'trans_addr': one[0],
                'stock_id': one[1],
                'stock_count': one[2],
                'stock_price': one[3],
                'category': '待买入',
                'sells_index': i,
                'company_name': IPO.objects.get(stock_id=one[1]).company_name
            }
            sells.append(a)
            red.lpush('sells', json.dumps(a))

    rows = request.GET.get('rows', 4)
    page = request.GET.get('page', 1)
    paginator = Paginator(sells, int(rows))
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
    print(sells)
    return JsonResponse(page_data, safe=False)


def buy(request):
    """抛出队列  购买逻辑"""
    sell_index = request.GET.get('sells_index')
    sells = [json.loads(i) for i in red.lrange('sells', 0, -1)]
    print('index.buy()', sell_index, sells)


    for i in sells:
        if i.get('sells_index') == int(sell_index):
            stock_id = i.get('stock_id')
            stock_count = i.get('stock_count')
            stock_price = i.get('stock_price')
    try:
        nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(request.session.get('address')))
        txn_dict = action.functions.buy(int(stock_id), int(stock_count), int(stock_price)).buildTransaction({
            'value': stock_price * stock_count * 10 ** 18,
            'nonce': nonce,
            "from": web3.toChecksumAddress(request.session.get('address')),
        })
        signed_txn = web3.eth.account.signTransaction(txn_dict,
                                                      private_key=request.session.get('private_key'))
        result_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})


def sell(request):
    """买入队列 抛出逻辑"""
    buy_index = request.GET.get('buys_index')
    buys = [json.loads(i) for i in red.lrange('buys', 0, -1)]
    print('index.sell()', buy_index, buys)
    for i in buys:
        if i.get('buys_index') == int(buy_index):
            stock_id = i.get('stock_id')
            stock_count = i.get('stock_count')
            stock_price = i.get('stock_price')
    try:
        nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(request.session.get('address')))
        txn_dict = action.functions.sell(int(stock_id), int(stock_count), int(stock_price)).buildTransaction({
            'nonce': nonce,
            "from": web3.toChecksumAddress(request.session.get('address')),
        })
        signed_txn = web3.eth.account.signTransaction(txn_dict,
                                                      private_key=request.session.get('private_key'))
        result_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})


def transactions(request):
    name = request.session.get('address')

    return render(request, 'index/transactions.html', {
        'euser': {
            'name': name
        }
    })


def get_transactions(request):
    ipos = IPO.objects.all().values_list('stock_id').distinct()
    ipos = [i[0] for i in list(ipos)]
    print(ipos)
    data = []
    try:
        for i in ipos:
            ipo = action.functions.get_ipo_from_id(i).call()
            data.append({
                'stock_id': i,
                'company_name': IPO.objects.get(stock_id=str(i)).company_name,
                'ipo_price': ipo[1],
                'ipo_count': ipo[0],
                'status': '募股中',
                'newest_price': ipo[2],
            })
    except Exception as tips:
        print(tips)
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
def transactions_buy(request):
    stock_id = request.POST.get('buy_stock_id')
    stock_count = request.POST.get('buy_stock_count')
    stock_price = request.POST.get('buy_stock_price')
    print(stock_id, stock_count, stock_price)

    try:
        nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(request.session.get('address')))
        txn_dict = action.functions.buy(int(stock_id), int(stock_count), int(stock_price)).buildTransaction({
            'value': int(stock_price) * int(stock_count) * 10 ** 18,
            'nonce': nonce,
            "from": web3.toChecksumAddress(request.session.get('address')),
        })
        signed_txn = web3.eth.account.signTransaction(txn_dict,
                                                      private_key=request.session.get('private_key'))
        result_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})
