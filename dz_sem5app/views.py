from django.shortcuts import render
from django.utils import timezone
import logging
import random
from .models import Client, Product, Order
from . import forms

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'dz_sem5app/index.html')


def add_product(request):
    if request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES)
        message = 'Ошибка данных'
        if form.is_valid():
            image = form.cleaned_data['product_image']
            product_name = form.cleaned_data['product_name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            # работа БД
            logger.debug(f'result: {product_name=}, {description=}, {price=}, {quantity=}')
            product = Product(product_name=product_name,
                              description=description,
                              price=price,
                              quantity=quantity,
                              date_ordered=timezone.now(),
                              product_image=image)
            product.save()
            message = "Товар добавлен !"
            logger.debug(f'PRODUCT SAVE: {product}')
    else:
        form = forms.ProductForm()
        message = "Заполните форму:"
    return render(request, 'dz_sem5app/product_add.html', {'form': form, 'message': message, 'title': 'Добавить продукт'})


def update_product(request):
    if request.method == 'POST':
        form = forms.ProductUpdateForm(request.POST, request.FILES)
        message = 'Ошибка данных'
        if form.is_valid():
            pk = form.cleaned_data['product_update'].pk
            image = form.cleaned_data['product_image']
            product_name = form.cleaned_data['product_name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            # работа БД
            logger.debug(f'result: {product_name=}, {description=}, {price=}, {quantity=}, {pk=}')
            product_update = Product.objects.filter(pk=pk).first()
            product_update.product_name = product_name
            product_update.description = description
            product_update.price = price
            product_update.quantity = quantity
            product_update.date_ordered = timezone.now()
            product_update.product_image = image
            product_update.save()
            message = "Товар обновлен !"
            logger.debug(f'PRODUCT UPDATE: {product_update}')
    else:
        form = forms.ProductUpdateForm
        message = "Заполните форму для для редактирования товара:"
    return render(request, 'dz_sem5app/product_add.html', {'form': form, 'message': message, 'title': 'Обновить продукт'})


def show_products(request):
    products = Product.objects.all()
    return render(request, 'dz_sem5app/index.html', {'products': products})


def show_clients(request):
    clients = Client.objects.all()
    return render(request, 'dz_sem5app/index.html', {'clients': clients})
