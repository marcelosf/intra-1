from django.core.paginator import Paginator


class PaginatorMixin():
    model = None
    per_page = None
    filterset = None
    request = None

    def __init__(self, model, filterset, request):
        """Initialization"""
        self.model = model
        self.filterset = filterset
        self.request = request

    def set_per_page(self, per_page):
        """Set the number of rows per page"""
        self.per_page = per_page

    def get_queryset(self):
        """Get the filtered queryset"""
        return self.filterset(self.request.GET, queryset=self.model.objects.all())

    def get_page(self):
        """Get the page number from request and remove the page
            query string"""
        page = self.request.GET.get('page')
        request_without_page = self.request.GET.copy()
        if page:
            request_without_page.pop('page')
            self.request.GET = request_without_page        
        return page

    def get_paginator(self):
        """Get the filtered list and paginator resources"""
        object_list = self.get_queryset()
        paginator = Paginator(object_list.qs, self.per_page)
        page = self.get_page()

        object_list._qs = paginator.get_page(page)

        page_range = range(1, paginator.num_pages +1)
        page_list = list(page_range)

        return {'object_list': object_list, 'page_list': page_list, 'request': self.request}