from django.forms import ModelForm
from django import forms
from .models import *


class AddtoCartForm(forms.Form):
    quantity = forms.IntegerField()


class ProductsFrom(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude =['fields_name'] #for remove not needed fields
        
        
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        
class OrderFrom(ModelForm):
    class Meta:
        model = Order
        fields = ('staus',)
        # exclude =['fields_name'] #for remove not needed fields
        
        STATUS = (
        ('ORDERED', 'Ordered'),
        ('SHIPPED' , 'Shipped'),
        ('DELIVERED', 'delivered')
    )
        widgets = {
            forms.Select(choices=STATUS, attrs={'class': 'form-control'}),
        }


class CouponForm(forms.Form):
    code = forms.CharField(max_length=20)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            raise forms.ValidationError('Invalid coupon code')
        return coupon
