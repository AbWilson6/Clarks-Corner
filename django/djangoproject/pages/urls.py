from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('templates/pages/textbooks.html', views.textbooks, name='textbooks'),
    path('templates/pages/electronics.html', views.electronics, name='electronics'),
    path('templates/pages/housing.html', views.housing, name='housing'),
    path('templates/pages/fashion.html', views.fashion, name='fashion'),
    path('templates/pages/stationary.html', views.stationary, name='stationary'),
    path('templates/pages/collectibles.html', views.collectibles, name='collectibles'),
    path('templates/pages/product/<int:product_id>/', views.product, name='product'),
    path('templates/pages/login.html', views.login, name='login'),
    path('templates/pages/signup.html', views.signup, name='signup'),
    path('templates/pages/login/', views.login_view, name='login_view'),
    path('templates/pages/signup/', views.signup_view, name='signup_view'),
    path('add_review/<int:seller_id>/', views.add_review, name='add_review'),
    path('templates/pages/profile/<int:seller_id>/', views.profile, name='profile'),
    path('templates/pages/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('add_product/', views.add_product, name='add_product'),
    path('orders/', views.orders, name='orders'),
    path('submit_product/', views.submit_product, name='submit_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('templates/pages/cart.html', views.cart, name='cart'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('templates/pages/checkout/', views.checkout, name='checkout'),
    path('templates/pages/thank_you.html', views.thank_you, name='thank_you'),
    path('search/', views.search, name='search'),
    path('search_results/', views.search_results, name='search_results'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
