from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('razorpay_order_id', 'membership', 'amount', 'status', 'created_at')
    list_filter = ('status', 'currency')
    search_fields = ('razorpay_order_id', 'razorpay_payment_id', 'receipt_number')
    readonly_fields = (
        'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature',
        'created_at', 'updated_at',
    )
