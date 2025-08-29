import json
import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.db import models
from flowers.models import Flower, Category, WorkCondition, About, Contacts

logger = logging.getLogger(__name__)


# ----------------------------
# Основные страницы
# ----------------------------
def contacts_view(request):
    contacts = Contacts.objects.first()
    return render(request, "main/contacts.html", {"contacts": contacts})


def about_view(request):
    about = About.objects.first()
    return render(request, "about.html", {"about": about})


def personals(request):
    conditions = WorkCondition.objects.first()
    return render(request, "main/personals.html", {"conditions": conditions})


# ----------------------------
# Каталог
# ----------------------------
def catalog(request):
    categories = Category.objects.all()
    search_text = request.GET.get('search', '').strip()
    selected_in_stock = request.GET.get('in_stock') == 'on'
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    selected_sort = request.GET.get('sort_by')
    category_id = request.GET.get('category')

    flowers = Flower.objects.all()

    if category_id and category_id.isdigit():
        flowers = flowers.filter(category_id=category_id)

    if search_text:
        flowers = flowers.filter(
            models.Q(name__icontains=search_text) | models.Q(description__icontains=search_text)
        )

    if selected_in_stock:
        flowers = flowers.filter(in_stock=True)

    try:
        if price_min:
            flowers = flowers.filter(price__gte=float(price_min))
        if price_max:
            flowers = flowers.filter(price__lte=float(price_max))
    except ValueError:
        pass

    sort_mapping = {
        'name_asc': 'name',
        'name_desc': '-name',
        'price_asc': 'price',
        'price_desc': '-price',
    }
    if selected_sort in sort_mapping:
        flowers = flowers.order_by(sort_mapping[selected_sort])

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [
            {
                'id': flower.id,
                'name': flower.name,
                'price': str(flower.price),
                'in_stock': getattr(flower, 'in_stock', True),
                'image_url': flower.image.url if flower.image else '',
            }
            for flower in flowers
        ]
        return JsonResponse({'flowers': data})

    context = {
        'categories': categories,
        'flowers': flowers,
        'search_text': search_text,
        'selected_in_stock': selected_in_stock,
        'price_min': price_min or '',
        'price_max': price_max or '',
        'selected_sort': selected_sort or '',
        'selected_category': category_id or '',
    }
    return render(request, 'main/catalog.html', context)


def catalog_data(request):
    category_id = request.GET.get('category')
    flowers = Flower.objects.all()
    if category_id and category_id.isdigit():
        flowers = flowers.filter(category_id=category_id)

    data = [
        {
            'id': flower.id,
            'name': flower.name,
            'price': str(flower.price),
            'image': flower.image.url if flower.image else '',
        }
        for flower in flowers
    ]
    return JsonResponse({'flowers': data})


# ----------------------------
# Консультация
# ----------------------------
@csrf_exempt
@require_POST
def submit_consultation(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    mail = request.POST.get('mail')
    message = request.POST.get('message')

    if not all([name, phone, mail, message]):
        return JsonResponse({'success': False, 'error': 'Пожалуйста, заполните все поля.'})

    email_body = f"Новая заявка на консультацию:\n\nИмя: {name}\nТелефон: {phone}\nПочта: {mail}\nСообщение:\n{message}"

    try:
        send_mail(
            subject="📝 Запрос на консультацию — Сказочный сад",
            message=email_body,
            from_email=None,  # будет использовать DEFAULT_FROM_EMAIL
            recipient_list=[mail, 'skazochniysad@mail.ru'],
            fail_silently=False,
        )
        return JsonResponse({'success': True, 'message': '✅ Заявка отправлена!'})
    except BadHeaderError:
        return JsonResponse({'success': False, 'error': 'Неверный заголовок в письме'})
    except Exception as e:
        logger.error(f"Error sending consultation email: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


# ----------------------------
# Корзина
# ----------------------------
def get_cart_items(request):
    cart = request.session.get('cart', {})
    flowers = Flower.objects.filter(id__in=cart.keys())
    return [
        {'flower': flower, 'quantity': cart.get(str(flower.id), 0), 'subtotal': flower.price * cart.get(str(flower.id), 0)}
        for flower in flowers
    ]


def get_cart_total(items):
    return sum(item['subtotal'] for item in items)


def cart_view(request):
    items = get_cart_items(request)
    total = get_cart_total(items)
    return render(request, 'flowers/cart.html', {'items': items, 'total': total})


def add_to_cart(request, flower_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))
        cart[str(flower_id)] = cart.get(str(flower_id), 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart_view')
    return redirect('flower_detail', pk=flower_id)


def flower_detail(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    cart_ids = list(map(int, request.session.get('cart', {}).keys()))
    return render(request, 'flowers/detail.html', {'flower': flower, 'cart_ids': cart_ids})


@require_POST
def submit_order(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    delivery = request.POST.get('delivery')

    if not all([name, email, phone, delivery]):
        return JsonResponse({'success': False, 'error': 'Пожалуйста, заполните все поля.'})

    cart = request.session.get('cart', {})
    if not cart:
        return JsonResponse({'success': False, 'error': 'Корзина пуста.'})

    flowers = Flower.objects.filter(id__in=cart.keys())
    total = sum(cart[str(flower.id)] * flower.price for flower in flowers)

    message = f"Новый заказ от {name}\nEmail: {email}\nТелефон: {phone}\nДоставка: {delivery}\n\nЗаказ:\n"
    for flower in flowers:
        qty = cart[str(flower.id)]
        subtotal = qty * flower.price
        message += f"- {flower.name} x{qty} = {subtotal} ₽\n"
    message += f"\nИтого: {total} ₽"

    try:
        send_mail(
            subject="🌸 Новый заказ — Сказочный сад",
            message=message,
            from_email=None,
            recipient_list=[email, 'skazochniysad@mail.ru'],
            fail_silently=False,
        )
        request.session['cart'] = {}
        request.session.modified = True
        return JsonResponse({'success': True, 'message': '✅ Заказ отправлен!'})
    except Exception as e:
        logger.error(f"Error sending order email: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@require_POST
def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('cart_view')


@require_POST
def toggle_cart(request, flower_id):
    try:
        data = json.loads(request.body)
        quantity = max(int(data.get('quantity', 1)), 1)
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Неверное количество'}, status=400)

    cart = request.session.get('cart', {})
    flower_id_str = str(flower_id)
    added = False

    if flower_id_str in cart:
        del cart[flower_id_str]
    else:
        cart[flower_id_str] = quantity
        added = True

    request.session['cart'] = cart
    request.session.modified = True
    return JsonResponse({'added': added})
