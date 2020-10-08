from django.shortcuts import render
from .models import IconModel
from .forms import IconSearchForm
from django.views import generic

import os
import re
import mimetypes
from django.http import StreamingHttpResponse, HttpResponse
from wsgiref.util import FileWrapper

# Create your views here.

class IconList(generic.ListView):

    model = IconModel
    template_name = 'iconmaker/icon_list.html'

    def get_queryset(self):

        queryset = super().get_queryset()
        self.form = form = IconSearchForm(self.request.POST or None)

        if form.is_valid():

            keywords = form.cleaned_data.get('keyword')
            if keywords:
                for word in keywords.split():
                    queryset = queryset.filter(name_icontains=word)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        return context

