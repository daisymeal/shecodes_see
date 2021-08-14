from django.shortcuts import render
from listing.models import Category, Product, Images, Comment, Variants
# Create your views here.
def home(request):
    books = Product.objects.all()[:4]
    categories = Category.objects.filter()
    context={   
             'categories':categories,   
             'books':books,    
            }
    return render(request,'index.html',context)



def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')  


#user
def userprofile(request):
    return render(request,'userprofile.html') 

def userprofile_edit(request):
    return render(request,'userprofile_edit.html')

def login(request):
    return render(request,'login.html')

def wishlist(request):
    return render(request,'wishlist.html') 

def orders(request):
    return render(request,'orders.html') 



#listing
def listing_detail(request,id,slug):
    query = request.GET.get('q')
    categories = Category.objects.all()
    book = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    context = {'book': book,'categories': categories,
               'images': images, 'comments': comments,
               }
    return render(request,'listing/listing_detail.html',context)