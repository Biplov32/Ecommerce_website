from base.models import product
from base.models import Category, ShoppingCart
from django.forms import ModelForm

#Create a model form here
class ProductForm(ModelForm):
    class Meta:
        model = product
        fields = ('name','price','category','photo',)

class CatogeryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
    
class CreateAddtoCartForm(ModelForm):
    class Meta:
        model = ShoppingCart
        fields = ('quantity',)

    def __init__(self, *args, **kwargs):
        super(CreateAddtoCartForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].label = "Enter quantity"
