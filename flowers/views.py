from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from flowers.models import Flower, Category, WorkCondition, About, Contacts
from django.db import models
from asgiref.sync import sync_to_async
import json


# --- Страницы ---
def contacts_view(request):
    contacts = Contacts.objects.first()
    return render(request, "main/contacts.html", {"contacts": contacts})


def about_view(request):
    about = About.objects.first()
    return render(request, "about.html", {"about": about})


def personals(request):
    conditions = WorkCondition.objects.first()
    return render(request, "main/personals.html", {"conditions": conditions})


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
                'id': f.id,
                'name': f.name,
                'price': str(f.price),
                'in_stock': getattr(f, 'in_stock', True),
                'image_url': f.image.url if f.image else '',
            }
            for f in flowers
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
            'id': f.id,
            'name': f.name,
            'price': str(f.price),
            'image': f.image.url if f.image else '',
        }
        for f in flowers
    ]
    return JsonResponse({'flowers': data})


# --- Асинхронная отправка почты для консультации ---
@csrf_exempt
@require_POST
async def submit_consultation(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    mail = request.POST.get('mail')
    message = request.POST.get('message')

    if not all([name, phone, mail, message]):
        return JsonResponse({'success': False, 'error': 'Пожалуйста, заполните все поля.'})

    email_body = f"Новая заявка на консультацию:\n\nИмя: {name}\nТелефон: {phone}\nПочта: {mail}\nСообщение:\n{message}"

    try:
        await sync_to_async(send_mail)(
            subject="📝 Запрос на консультацию — Сказочный сад",
            message=email_body,
            from_email="skazochniysad@mail.ru",
            recipient_list=["skazochniysad@mail.ru"],
            fail_silently=False,
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# --- Корзина ---
def get_cart_items(request):
    cart = request.session.get('cart', {})
    flowers = Flower.objects.filter(id__in=cart.keys())
    items = []
    for flower in flowers:
        qty = cart.get(str(flower.id), 0)
        subtotal = qty * flower.price
        items.append({'flower': flower, 'quantity': qty, 'subtotal': subtotal})
    return items


def get_cart_total(items):
    return sum(item['subtotal'] for item in items)


def cart_view(request):
    items = get_cart_items(request)
    total = get_cart_total(items)
    return render(request, 'flowers/cart.html', {'items': items, 'total': total})


def add_to_cart(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        cart[str(flower_id)] = cart.get(str(flower_id), 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True
        return JsonResponse({'success': True, 'quantity': cart[str(flower_id)]})
    return JsonResponse({'success': False})


def flower_detail(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    cart = request.session.get('cart', {})
    cart_ids = [int(k) for k in cart.keys()]
    return render(request, 'flowers/detail.html', {'flower': flower, 'cart_ids': cart_ids})


# --- Асинхронная отправка почты для заказа ---
@require_POST
async def submit_order(request):
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
    total = 0
    message = f"Новый заказ от {name}\nEmail: {email}\nТелефон: {phone}\nДоставка: {delivery}\n\nЗаказ:\n"
    for flower in flowers:
        qty = cart.get(str(flower.id), 0)
        subtotal = qty * flower.price
        total += subtotal
        message += f"- {flower.name} x{qty} = {subtotal} ₽\n"
    message += f"\nИтого: {total} ₽"

    try:
        await sync_to_async(send_mail)(
            subject="🌸 Новый заказ — Сказочный сад",
            message=message,
            from_email="skazochniysad@mail.ru",
            recipient_list=["skazochniysad@mail.ru"],
            fail_silently=False,
        )
        # очищаем корзину
        request.session['cart'] = {}
        request.session.modified = True
        return JsonResponse({'success': True, 'message': 'Заказ отправлен! Спасибо! 😊'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Ошибка при отправке: {e}'})


# --- Очистка и управление корзиной ---
@require_POST
def clear_cart(request):
    if 'cart' in request.session:
        request.session['cart'] = {}
        request.session.modified = True
    return JsonResponse({'success': True})


@require_POST
def toggle_cart(request, flower_id):
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'error': 'Неверное количество'}, status=400)

    cart = request.session.get('cart', {})
    flower_id_str = str(flower_id)

    if flower_id_str in cart:
        del cart[flower_id_str]
        added = False
    else:
        cart[flower_id_str] = quantity
        added = True

    request.session['cart'] = cart
    request.session.modified = True
    return JsonResponse({'added': added, 'quantity': cart.get(flower_id_str, 0)})
