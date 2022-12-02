from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path("accounts/registration", views.register_request, name="registration"),
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('item_list/<int:category>', views.ItemListView.as_view(), name='item_list'),
    path('cart_list', views.CartListView.as_view(), name='cart'),
    path('item_detail/<int:pk>', views.ItemDetailView.as_view(), name='item_detail'),
    path('item_detail/<int:pk>/add_to_cart', views.AddToCartView.as_view(), name='add_to_cart'),
    path('item_detail/<int:pk>/remove_from_cart', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/<int:pk>/inc_item', views.IncItemView.as_view(), name='inc_item'),
    path('cart/<int:pk>/dec_item', views.DecItemView.as_view(), name='dec_item'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
