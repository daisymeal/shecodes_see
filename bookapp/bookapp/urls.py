"""bookapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from home import views as HomeViews
from user import views as UserViews
from listing import views as ListingViews
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeViews.home, name='home'),
   
    path('about', HomeViews.about, name='about'),
    path('contact', HomeViews.contact, name='contact'),


    path('login', UserViews.login_form, name='login'),
    path('register', UserViews.register, name='register'),
    path('logout/', UserViews.logout_func, name='logout'),
    path('sent/', UserViews.activation_sent, name="activation_sent"),
    path('activated/', UserViews.activated, name="activated"),
    path('activate/<slug:uidb64>/<slug:token>/', UserViews.activate, name='activate'),
    path('password_reset/', PasswordResetView.as_view(
            from_email = "tramszone@gmail.com",template_name = 'user/forgot-password.html'
        ), name='password_reset'),    
    path('password_reset/done', PasswordResetDoneView.as_view(template_name = 'user/password_reset_sent.html'), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name = 'user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name = 'user/password_reset_complete.html'), name='password_reset_complete'),
    path('userprofile',UserViews.userprofile,name='user_profile'),
    path('/change_password', UserViews.change_password, name='change_password'),



    path('addlisting', ListingViews.addlisting, name='addlisting'),
    path('listing', ListingViews.listing, name='listing'),
    path('listing-search', ListingViews.listing_search, name='listing_search'),


    path('listing/<int:id>/<slug:slug>/', HomeViews.listing_detail, name='listing_detail'),
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)