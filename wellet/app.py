@login_required
def transfer(request, *args, **kwargs):
	context = {}
	confirmed_code = ConfirmationCode.objects.filter(user=request.user)
	bank_card = BankCard.objects.filter(user=request.user)
	card_holder = CardHolder.objects.filter(user=request.user)


	user=request.user

	# Transfer code logic
	card_pass_code = VerifiedPassCode.objects.filter(user=request.user)
	
	form = VerifiedPassCodeForm(
		request.POST or None

	)

	if form.is_valid():
		pass_code = form.save(commit=False)
		verified_pass_code = form.cleaned_data['verified_pass_code']
		code = CardPassCode.objects.filter(user=request.user)

		for pay_code in code:
			sent = pay_code.pass_code

		if verified_pass_code == sent:
			pass_code.user = request.user
			pass_code.save()
		else:
			messages.error(request, f'Invalid code. Please check pass code')
			return redirect('transfer')
	# End

	if request.method == 'POST':

		try:
			email = request.POST['email']
			amount = request.POST['amount']

			sendName = User.objects.get(username=request.user) # Sender
			receiverName = User.objects.get(email=email) # Receiver
			receivers = CardHolder.objects.filter(user=receiverName) # Receiver
		except:
			messages.error(request, f'Username and Email does not exist')
			return redirect('transfer')


		if receiverName == sendName:
			messages.error(request, f'Unable to transfer to yourself')
			return redirect('transfer')
		

		for receiver in receivers:
			holder_name = receiver.first_name + ' ' + receiver.last_name
			receiverBalance = Decimal(receiver.balance) + Decimal(amount)

		for holder in card_holder:
			holder_balance = holder.balance

		if Decimal(holder_balance) >= Decimal(amount):
			CardHolder.objects.filter(id__in=card_holder).update(
				balance=F('balance') - Decimal(amount)
			)
			CardHolder.objects.filter(id__in=receivers).update(
				balance=F('balance') + Decimal(amount)
			)
			user = User.objects.get(cardholder__in=receivers)
			receiverEmail=user.email

			trans = Record.objects.filter(user=user).create(
				transfer_amount=amount
			)
			trans.user = request.user
			trans.save()

			rec = Record.objects.filter(user=user).create(
				amount_recevied=amount, recevier_name=str(sendName)
			)
			rec.user=user
			rec.save()

			send_mail('You Have Received '+str(amount)+'¥ In Your Schkit Pay','Hello, '+str(receiverName)+'!\n'+str(sendName)+' has sent $'+str(amount)+' to your Schkit Pay\nUpdated Wallet Balance :$'+str(receiverBalance)+'\n\n\nContact us: schkit01@gmail.com\n', "(Schkit Pay) Schkit pay mitchellsherman01@gmail.com", [receiverEmail])
			return render(request, 'wallet/transfer_success.html', {'bank_card':bank_card, 'card_holder':card_holder, 'amount':amount})
		
		else:
			messages.error(request, f'Amount entered exceeds available Balance')
			return redirect('transfer')

   

	context = {
		'form':form,
		'bank_card':bank_card,
		'card_holder':card_holder,
	}

	return render(request, 'wallet/transfer.html',context)