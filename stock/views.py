import json

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Eth_transaction.settings import web3, action
from stock.models import IPO


def ipo_index(request):
    name = request.session.get('address')

    return render(request, 'ipo/ipo.html', {
        'euser': {
            'name': name
        }
    })


def get_list(request):
    """获取单页的ipo信息"""
    rows = request.GET.get('rows', 2)
    page = request.GET.get('page', 1)
    st_list = list(IPO.objects.all().order_by('stock_id'))
    paginator = Paginator(st_list, int(rows))
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

    def mydefault(u):
        if isinstance(u, IPO):
            return {
                'stock_id': u.stock_id,
                'company_name': u.company_name,
                'ipo_price': str(u.ipo_price),
                'ipo_count': u.ipo_count,
                'ipo_date': u.ipo_date.strftime("%Y-%m-%d"),
            }

    data = json.dumps(page_data, default=mydefault)
    print(data)
    return HttpResponse(data)


@csrf_exempt
def ipo_submit(request):
    company_name = request.POST.get('company_name')
    ipo_price = request.POST.get('ipo_price')
    ipo_count = request.POST.get('ipo_count')
    print(company_name, ipo_count, ipo_price)
    try:
        with transaction.atomic():
            ipo = IPO.objects.create(company_name=company_name, ipo_price=ipo_price, ipo_count=ipo_count)

        nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(request.session.get('address')))
        txn_dict = action.functions.add_ipo(int(ipo.stock_id), int(ipo.ipo_count), int(ipo.ipo_price)).buildTransaction(
            {
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


def get_ipo_info(request):
    try:
        stock_id = request.GET.get('stock_id')
        ipo = IPO.objects.get(stock_id=stock_id)
        print(ipo.content, ipo.content2)
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1, 'content': ipo.content, 'content2': ipo.content2})
