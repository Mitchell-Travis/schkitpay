from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User, VerifyConfirmation, ConfirmationCode
from django.core.paginator import Paginator
from urllib.parse import urlparse
from itertools import chain
from friends.models import (
	FriendsList,
	FriendRequest
)
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import F
from django.core.mail import send_mail
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from django.db import transaction


from wellet.models import (
	BankCard, 
	CardHolder, 
	CardPassCode,
	VerifiedPassCode,
	Record

)

from wellet.forms import (
	CardHolderDetailForm,
	BankCardForm,
	CardPassCodeForm,
	TopUpBalanceForm,
	WithdrewBalanceForm,
	VerifiedPassCodeForm,
)


@login_required
def card_holder_detail(request, *args, **kwargs):
	context = {}
	card_holder = CardHolder.objects.filter(user=request.user)
	confired_code = ConfirmationCode.objects.filter(user=request.user)
	verified_code = VerifyConfirmation.objects.filter(user=request.user)
	form = CardHolderDetailForm(
		request.POST
		or None
	)
	if form.is_valid():
		holder = form.save(commit=False)
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']
		holder.user = request.user
		holder.save()
		return render(request, 'wallet/balance.html', {'card_holder':card_holder})
	context = {
		'form':form,
		'card_holder':card_holder,
		'confired_code':confired_code,
		'verified_code':verified_code
	}
	return render(request, 'wallet/card_holder_detail.html', context)

@login_required
def balance(request):
    # Retrieve data from the database
    verified_code = VerifyConfirmation.objects.filter(user=request.user)
    confirmed_code = ConfirmationCode.objects.filter(user=request.user)
    bank_card = BankCard.objects.filter(user=request.user)
    card_holder = CardHolder.objects.filter(user=request.user)
    card_pass_code = CardPassCode.objects.filter(user=request.user)
    verified_pass_code = VerifiedPassCode.objects.filter(user=request.user)

    # Calculate the new balance
    new_balance = calculate_new_balance(request.user)

    context = {
        'verified_code': verified_code,
        'confirmed_code': confirmed_code,
        'bank_card': bank_card,
        'card_holder': card_holder,
        'card_pass_code': card_pass_code,
        'verified_pass_code': verified_pass_code,
        'total_balance': new_balance,
    }

    return render(request, 'wallet/balance.html', context)


@login_required
def handle_qr_code(request):
    if request.method == 'POST':
        # Extract the decoded code from the request
        decoded_code = request.POST.get('code')

        # Validate the decoded code (if needed)
        # For example, check if the decoded code exists and is valid
        if not decoded_code:
            return JsonResponse({'error': 'Invalid QR code'}, status=400)

        # Parse the decoded code as a URL
        parsed_url = urlparse(decoded_code)

        # Check if the decoded code is a valid URL
        if parsed_url.scheme and parsed_url.netloc:
            # Redirect the user to the URL from the decoded code
            return redirect(decoded_code)
        else:
            # If the decoded code is not a valid URL, return an error response
            return JsonResponse({'error': 'Invalid URL in QR code'}, status=400)

    else:
        # Handle non-POST requests
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def calculate_new_balance(user):
    # Retrieve the card holder's balance from the database
    card_holder = CardHolder.objects.filter(user=user).first()  # Assuming each user has only one card holder entry
    if card_holder:
        new_balance = card_holder.balance
    else:
        new_balance = 0  # Default balance if no card holder entry found for the user
    return new_balance


@login_required
def add_bank_card(request):
	context = {}
	card_holder = CardHolder.objects.filter(user=request.user)
	bank_card = BankCard.objects.filter(user=request.user)
	form = BankCardForm(
		request.POST
		or None
	)
	if form.is_valid():
		card = form.save(commit=False)
		card_number = form.cleaned_data['card_number']
		expiration_date = form.cleaned_data['expiration_date']
		cvv_number = form.cleaned_data['cvv_number']
		card.user = request.user
		card.save()
		return redirect('pay-code')
	context = {
		'form':form,
		'bank_card':bank_card,
		'card_holder':card_holder
	}

	return render(request , 'wallet/bank_card.html', context)


@login_required
def add_payment_pass_code(request):
	context = {}
	bank_card = BankCard.objects.filter(user=request.user)
	card_holder = CardHolder.objects.filter(user=request.user)
	form = CardPassCodeForm(
		request.POST
		or None
	)
	if form.is_valid():
		code = form.save(commit=False)
		pass_code = form.cleaned_data['pass_code']
		code.user = request.user
		code.save()
		return redirect('balance')
	context = {
		'form':form,
		'card_holder':card_holder,
		'bank_card':bank_card
	}
	return render(request, 'wallet/payment_pass_code.html', context)


@login_required
def top_up_balance(request, *args, **kwargs):
	context = {}
	confirmed_code = ConfirmationCode.objects.filter(user=request.user)
	bank_card = BankCard.objects.filter(user=request.user)
	card_holder = CardHolder.objects.filter(user=request.user)
	form = TopUpBalanceForm(
		request.POST
		or None
	)
	if form.is_valid():
		top_up = form.save(commit=False)
		top_up_amount = form.cleaned_data['top_up_amount']

		for card in bank_card:
			amount_on_card = card.card_amount # default amaount 10,000 USD

		if amount_on_card >= top_up_amount:
			BankCard.objects.filter(id__in=bank_card).update(
				card_amount=F('card_amount') - top_up_amount
			)
			CardHolder.objects.filter(id__in=card_holder).update(
				balance=F('balance') + top_up_amount
			)
			top_up.user = request.user
			top_up.save()
			return render(request, 'wallet/top_up_success.html', {'card_holder':card_holder, 'bank_card':bank_card, 'confirmed_code':confirmed_code, 'top_up_amount':top_up_amount})
		else:
			messages.error(request, f'Amount exceeds available card amount')
			return redirect('top-up')
	context = {
		'form':form,
		'card_holder':card_holder,
		'bank_card':bank_card
	}
	return render(request, 'wallet/top_up.html', context)





@login_required
def withdrew_balance(request, *args, **kwargs):
	context = {}
	confirmed_code = ConfirmationCode.objects.filter(user=request.user)
	card_holder = CardHolder.objects.filter(user=request.user)
	bank_card = BankCard.objects.filter(user=request.user)
	form = WithdrewBalanceForm(
		request.POST
		or None
	)
	if form.is_valid():
		withdrew = form.save(commit=False)
		withdrew_amount = form.cleaned_data['withdrew_amount']
		for holder in card_holder:
			holder_balance = holder.balance
		if holder_balance >= withdrew_amount:
			CardHolder.objects.filter(id__in=card_holder).update(
				balance=F('balance') -  withdrew_amount
			)
			BankCard.objects.filter(id__in=bank_card).update(
				card_amount=F('card_amount') + withdrew_amount
			)
			withdrew.user = request.user
			withdrew.save()
			return render(request, 'wallet/withdrew_success.html', {'withdrew_amount':withdrew_amount, 'bank_card':bank_card, 'card_holder':card_holder})
		else:
			messages.error(request, f'Amount entered exceeds available Balance')
			return redirect('withdrew')
	context = {
		'form':form,
		'bank_card':bank_card,
		'card_holder':card_holder
	}

	return render(request, 'wallet/withdrew.html', context)



@login_required
def transfer(request, *args, **kwargs):
    context = {}
    confirmed_code = ConfirmationCode.objects.filter(user=request.user)
    bank_card = BankCard.objects.filter(user=request.user)
    card_holder = CardHolder.objects.filter(user=request.user)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            username = request.POST['username']
            amount = request.POST['amount']

            sendName = request.user  # Sender
            try:
                receiverName = User.objects.get(username=username)  # Receiver
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Receiver does not exist'})

            if receiverName == sendName:
                return JsonResponse({'success': False, 'error': 'Unable to transfer to yourself'})

            try:
                amount = Decimal(amount)
                if amount <= 0:
                    return JsonResponse({'success': False, 'error': 'Enter a valid amount'})
            except InvalidOperation:
                return JsonResponse({'success': False, 'error': 'Enter a valid amount'})

            # Ensure receiver has card holders
            receivers = CardHolder.objects.filter(user=receiverName)
            if not receivers.exists():
                return JsonResponse({'success': False, 'error': 'Receiver has no card holders'})

            holder_balance = card_holder.first().balance
            if holder_balance < amount:
                return JsonResponse({'success': False, 'error': 'Amount entered exceeds available balance'})

            with transaction.atomic():
                # Deduct from sender
                CardHolder.objects.filter(user=request.user).update(
                    balance=F('balance') - amount
                )
                # Add to receiver
                CardHolder.objects.filter(user=receiverName).update(
                    balance=F('balance') + amount
                )

                # Record the transaction for sender
                Record.objects.create(
                    user=request.user,
                    transfer_amount=amount,
                    recevier_name=receiverName.username
                )

                # Record the transaction for receiver
                Record.objects.create(
                    user=receiverName,
                    amount_recevied=amount,
                    recevier_name=sendName.username
                )

                # Send email to receiver (uncomment if needed)
                # receiverEmail = receiverName.email
                # send_mail(
                #     'You Have Received ' + str(amount) + '¥ In Your Schkit Pay',
                #     'Hello, ' + str(receiverName) + '!\n' + str(sendName) + ' has sent $' + str(amount) +
                #     ' to your Schkit Pay\nUpdated Wallet Balance :$' + str(receiverBalance) + '\n\n\nContact us: schkit01@gmail.com\n',
                #     "(Schkit Pay) Schkit pay mitchellsherman01@gmail.com",
                #     [receiverEmail]
                # )

                return JsonResponse({'success': True, 'redirect_url': '/wallet/verify_passcode/'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An error occurred: ' + str(e)})

    context = {
        'bank_card': bank_card,
        'card_holder': card_holder,
    }
    return render(request, 'wallet/transfer.html', context)



@login_required
def passcode_verification(request):
    form = VerifiedPassCodeForm(request.POST or None)

    # Fetch necessary data related to the user
    bank_card = BankCard.objects.filter(user=request.user).first()
    card_holder = CardHolder.objects.filter(user=request.user).first()

    recipient_username = request.session.get('recipient_username', 'N/A')
    amount = request.session.get('amount', '0.00')

    if request.method == 'POST':
        if form.is_valid():
            verified_pass_code = form.cleaned_data['verified_pass_code']
            card_pass_code = CardPassCode.objects.filter(user=request.user).first()

            if card_pass_code and verified_pass_code == card_pass_code.pass_code:
                # Passcode verified successfully
                VerifiedPassCode.objects.create(user=request.user, verified_pass_code=verified_pass_code)
                
                amount = Decimal(amount)  # Use the amount from the session
                return render(request, 'wallet/passcode_success.html', {'bank_card': bank_card, 'card_holder': card_holder, 'amount': amount})
            else:
                messages.error(request, 'Invalid passcode. Please try again.')
                return redirect('verify-passcode')

    context = {
        'form': form,
        'recipient_username': recipient_username,
        'amount': amount,
        'card_holder': card_holder,
    }
    return render(request, 'wallet/passcode_verification.html', context)



