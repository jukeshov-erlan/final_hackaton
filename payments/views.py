from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

import stripe


def home(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        price = stripe.Price.create(
            unit_amount=2000,
            currency='KGS',
            recurring={
                'interval': 'month'
            },
            product='prod_Pgt8WmUC5BUkxc'
        )
        return HttpResponseRedirect('https://buy.stripe.com/test_14k2b02OK89RaHu7su')

    return render(request, "home.html")


def success(request):
    return HttpResponseRedirect('https://buy.stripe.com/test_cN2eXM0GC61J3f26or')


def cancel(request):
    return render(request, "cancel.html")
