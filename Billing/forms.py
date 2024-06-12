from django import forms

from Billing.models import Promotion, Coupon


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['image', 'title', 'description', 'discount_code']

    discount_code = forms.ModelChoiceField(
        queryset=Coupon.objects.filter(active=True),
        label="discount_code"
    )

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['discount_code', 'discount_percentage']