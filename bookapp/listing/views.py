from django.shortcuts import render
from .forms import ProductForm
# Create your views here.
from django.contrib.auth.decorators import login_required

from .models import Category, Product

@login_required(login_url='/login') # Check login
def addlisting(request):
    form = ProductForm()
    context={   
             'form':form,        
            }
    return render(request,'listing/addlisting.html') 



def listing(request):
    categories = Category.objects.all()
    books = Product.objects.all()
    num_books = Product.objects.count()
    context={   
             'books':books,        
             'num_books':num_books,
             'categories':categories
            }
    return render(request,'listing/listing.html',context)     

def listing_search(request):
    return render(request,'listing/listing_search.html')    

