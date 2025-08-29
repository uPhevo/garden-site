from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    delivery = forms.ChoiceField(choices=[('cdek', 'СДЕК'), ('post', 'Почта России')])
    email = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea)