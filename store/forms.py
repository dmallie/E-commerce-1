from django import forms
from category.models import Category
from .models import Product, Variation 

class CategoryForm(forms.ModelForm):
       class Meta:
              model = Category
              fields = ["category_name", "slug", "description"]
       def __init__(self, *args, **kwargs):
              super(CategoryForm, self).__init__(*args, **kwargs)
              
              self.fields['category_name'].widget.attrs['placeholder'] = 'Category'
              self.fields['slug'].widget.attrs['placeholder'] = 'Slug'
              self.fields['description'].widget.attrs['placeholder'] = 'Brief description about the category'

              for field in self.fields:
                     self.fields[field].widget.attrs['class'] = 'form-control'
"""
       def clean(self):
              cleaned_data = super(CategoryForm, self).clean()
              print("forms.py clean()")
              category_name = cleaned_data.get('category_name')
              slug = cleaned_data.get('slug')
              description = cleaned_data.get('description')
              picture = cleaned_data.get('cat_image')
"""
       
class ProductForm(forms.ModelForm):
       class Meta:
              model = Product
              fields = ["product_name", "slug", "description", "price", "image", "stock", "category"]

       def __init__(self, *args, **kwargs):
              super(ProductForm, self).__init__(*args, **kwargs)

              for field in self.fields:
                     self.fields[field].widget.attrs['class'] = 'form-controla'

class NavbarForm(forms.ModelForm):
       class Meta:
              model = Category
              fields = ["category_name",]
       def __init__(self, *args, **kwargs):
              super(NavbarForm, self).__init__(*args, **kwargs)

class VariationForm(forms.ModelForm):
       class Meta:
              model = Variation
              fields = ["product", "variation_category", "variation_value", "is_active"]

       def __init__(self, *args, **kwargs):
              super(VariationForm, self).__init__(*args, **kwargs)
              
              