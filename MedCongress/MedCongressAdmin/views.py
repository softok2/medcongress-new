from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, View)
from django.contrib.auth.decorators import user_passes_test


class Home(UserPassesTestMixin,TemplateView):
    template_name= 'MedCongressAdmin/base.html' 
    def test_func(self):
        print(self.request.user.is_staff) 
        return self.request.user.is_staff