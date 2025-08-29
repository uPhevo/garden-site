from django.urls import path
from main.views import home, about
from flowers.views import (
    personals,
    catalog,
    catalog_data,
    flower_detail,
    add_to_cart,
    cart_view,
    submit_order,
    toggle_cart,
    clear_cart,
    submit_consultation,
    contacts_view,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contacts/', contacts_view, name='contacts'),
    path('personals/', personals, name='personals'),

    # Маршруты из flowers
    path('catalog/<int:pk>/', flower_detail, name='flower_detail'),
    path('add-to-cart/<int:flower_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('toggle-cart/<int:flower_id>/', toggle_cart, name='toggle_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('submit-order/', submit_order, name='submit_order'),
    path('submit-consultation/', submit_consultation, name='submit_consultation'),

    # Фильтр и каталог
    path('catalog-data/', catalog_data, name='catalog_data'),
    path('catalog/', catalog, name='catalog'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
