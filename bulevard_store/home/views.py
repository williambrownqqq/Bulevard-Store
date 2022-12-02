from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Category, Item, Cart


class CategoryListView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = ''
        return context


class ItemListView(ListView):
    model = Item
    template_name = 'home/item_list.html'

    def get(self, request, **kwargs):
        category = kwargs['category']
        item_list = self.model.objects.filter(category=category)
        ctx = {'item_list': item_list, 'next': f'item_list/{category}'}
        return render(request, self.template_name, ctx)


class ItemDetailView(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = f"item_detail/{context['item'].id}"
        return context


class CartListView(LoginRequiredMixin, ListView):
    model = Cart

    def get_queryset(self):
        print('update get_queryset called')
        """ Limit a User to only modifying their own data. """
        qs = super(CartListView, self).get_queryset()
        return qs.filter(user=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class AddToCartView(LoginRequiredMixin, View):

    def post(self, request, pk):
        item = get_object_or_404(Item, id=pk)
        cart = Cart(user=request.user, item=item, count=1)
        try:
            if item.count > 0:
                item.count -= 1
                cart.save()  # In case of duplicate key
                item.save(update_fields=["count"])
        except IntegrityError:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class RemoveFromCartView(LoginRequiredMixin, View):

    def post(self, request, pk):
        cart_item = get_object_or_404(Cart, id=pk)
        item = cart_item.item
        try:
            if item.count > 0:
                item.count += cart_item.count
                cart_item.delete()  # In case of duplicate key
                item.save(update_fields=["count"])
        except IntegrityError:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class IncItemView(LoginRequiredMixin, View):

    def post(self, request, pk):
        cart_item = get_object_or_404(Cart, id=pk)
        item = cart_item.item
        try:
            if item.count > 0:
                cart_item.count += 1
                item.count -= 1
                cart_item.save(update_fields=["count"])
                item.save(update_fields=["count"])
        except IntegrityError:
            print(3)
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DecItemView(LoginRequiredMixin, View):

    def post(self, request, pk):
        cart_item = get_object_or_404(Cart, id=pk)
        item = cart_item.item
        try:
            if cart_item.count > 1:
                cart_item.count -= 1
                item.count += 1
                cart_item.save(update_fields=["count"])
                item.save(update_fields=["count"])
        except IntegrityError:
            pass
        return HttpResponse()


def register_request(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {'form': form, "next": request.GET.get('next')}
        return render(request, 'registration/register.html', context)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        next_url = request.POST.get('next') if 'next' in request.POST else "home:category_list"
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form, "next": next_url}
            return render(request, 'registration/register.html', context)

    return render(request, 'registration/register.html', {})
