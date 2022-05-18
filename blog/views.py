from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class IndexPageView(View):
    template_name = 'source/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class MarketPageView(View):
    template_name = 'source/market.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class DropsPageView(View):
    template_name = 'source/drops.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class ProfilePageView(View):
    template_name = 'source/profile.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
