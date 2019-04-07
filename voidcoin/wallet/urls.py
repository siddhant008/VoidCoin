from django.urls import path
from wallet.views import *

app_name='wallet'

urlpatterns = [
    path('new_wallet/', new_wallet,name='new_wallet'),
    path('new_wallet_form/', new_wallet_form,name='new_wallet_form'),
    path('make_transaction/',make_transaction,name='make_transaction'),
    path('check_balance/', check_balance,name='check_balance'),
]
