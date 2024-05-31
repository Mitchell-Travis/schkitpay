from django.contrib import admin
from wellet.models import (
BankCard,
CardHolder,
CardPassCode,
VerifiedPassCode,
QRCODE,
Record
)

class RecordAdmin(admin.ModelAdmin):
	# fields = (
	# 	'course_title',
	# 	'course_benefit'
	# )

	list_display = ['user', 'top_up_amount', 'withdrew_amount', 'transfer_amount']

# Register your models here.
admin.site.register(BankCard)
admin.site.register(CardHolder)
admin.site.register(CardPassCode)
admin.site.register(VerifiedPassCode)
admin.site.register(QRCODE)
admin.site.register(Record, RecordAdmin)






