from django.urls import path
from . import views as pay_views
from .utils import (
	cardholder_update, 
	bankcard_update,
	delete_bank_card,
	delete_transactions,
	scan_to_transfer,
	# payee,
	transactions	
)


urlpatterns = [
	path('bank-card/', pay_views.add_bank_card, name='bank-card'),
	path('bank-card-update/<str:pk>', bankcard_update, name='card-update'),
	path('card-holder-update/<str:pk>', cardholder_update, name='holder-update'),
	path('delete-bank-card/<str:pk>',delete_bank_card, name='delete-card'),
	path('delete-transactions/<str:pk>',delete_transactions, name='delete-transactions'),
	path('holder-detail/', pay_views.card_holder_detail, name='card-holder-detail'),
	path('balance/', pay_views.balance, name='balance'),
	path('handle-qr-code/', pay_views.handle_qr_code, name='handle_qr_code'),
	path('withdrew/', pay_views.withdrew_balance, name='withdrew'),
	# path('payee/<str:pk>', payee, name='payee'),
	path('payment-code/',pay_views.add_payment_pass_code, name='pay-code'),
	path('scan/', scan_to_transfer, name='scan'),
	path('top-up/', pay_views.top_up_balance, name='top-up'),
	path('transfer/', pay_views.transfer, name='transfer'),
	path('transactions/', transactions, name='transactions'),
	path('verify_passcode/', pay_views.passcode_verification, name='verify-passcode')

]

