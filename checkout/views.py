from . import config
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView
from django.forms import modelformset_factory
from django.contrib import messages
from django.core.urlresolvers import reverse

from catalog.models import Product

from .models import CartItem, Order


class CreateCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])

        if self.request.session.session_key is None:
            self.request.session.save()

        cart_item, created = CartItem.objects.add_item(
            self.request.session.session_key, product
        )
        if created:
            messages.success(self.request, config.MESSAGE_ADDED_PRODUCT)
        else:
            messages.success(self.request, config.MESSAGE_UPDATED_PRODUCT)
        return reverse('checkout:cartitem')


class CartItemView(TemplateView):

    template_name = 'checkout/cart.html'

    def get_formset(self, clear=False):
        cart_item_formset = modelformset_factory(
            CartItem, fields=('quantity',), can_delete=True, extra=0
        )
        session_key = self.request.session.session_key
        if session_key:
            if clear:
                formset = cart_item_formset(queryset=CartItem.objects.none())
            else:
                formset = cart_item_formset(
                    queryset=CartItem.objects.filter(cartkey=session_key),
                    data=self.request.POST or None
                )
        else:
            formset = cart_item_formset(queryset=CartItem.objects.none())
        return formset

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            formset.save()
            messages.success(request, config.MESSAGE_UPDATED_CART)
            context['formset'] = self.get_formset(clear=True)
        return self.render_to_response(context)


class CheckoutView(LoginRequiredMixin, TemplateView):

    template_name = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            cart_items = CartItem.objects.filter(cart_key=session_key)
            order = Order.objects.create_order(
                user=request.user, cart_items=cart_items
            )
        else:
            messages.info(request, config.MESSAGE_NO_ITEMS_IN_THE_CART)
            return redirect('checkout:cart_item')
        return super(CheckoutView, self).get(request, *args, **kwargs)


create_cartitem = CreateCartItemView.as_view()
cart_item = CartItemView.as_view()
checkout = CheckoutView.as_view()
