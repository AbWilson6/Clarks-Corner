from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['p_name', 'p_image', 'price', 'p_description', 'category']  # Adjust fields as needed

        widgets = {
            'p_description': forms.Textarea(attrs={'rows': 4}),  # Adjust widget attributes as needed
        }

class ReviewForm(forms.Form):
    rating_number = forms.IntegerField(label='Rating', min_value=1, max_value=5)
    review_description = forms.CharField(label='Review', widget=forms.Textarea)