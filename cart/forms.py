from django import forms

DISTRICT = (
    ('', 'Choose...'),
    ('dwd', 'Dharwad'),
    ('belgaum', 'Belgaum'),
    ('RJ', 'Bangalore')
)
 

class AddressForm(forms.Form):
    billingname=forms.CharField(label='billingname')
    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    city = forms.CharField()
    district = forms.ChoiceField(choices=DISTRICT)
    zip_code = forms.CharField(label='Zip')
    phone_number=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '+91:'}))
    check_me_out = forms.BooleanField(required=True)


 