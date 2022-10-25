from django.shortcuts import render
from .models import Blog 
from django.views.generic import View, DetailView, CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
import os 
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone



class PostListView(View):
    template_name = 'blogs/post_list.html'

    def get(self, request, *args, **kwargs):
        articles = Blog.objects.all().order_by('-timestamp')
        paginator = Paginator(articles, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context ={
            'posts':articles
        }
        # return render(request, self.template_name, {'page_obj': page_obj})
        return render(request, self.template_name, context)


class PostDetailView(DetailView):
    model = Blog
    template_name = 'blogs/post_detail.html'


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Blog
    template_name = 'blogs/post-create.html'
    fields = ('title', 'description', 'image', 'body')
    success_url = '/blogs/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        user = User()
        if self.request.user.is_staff:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    template_name = 'blogs/post-update.html'
    fields = ('title', 'image', 'body', 'description')
    success_url = reverse_lazy('blogs')

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.author:
            return True
        return False


class PostDeletView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blogs/post-delete.html'
    success_url = '/blogs/'

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.owner:
            return True
        return False



        
@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "Wrong file format"})

        upload_time = timezone.now()
        path = os.path.join(
            settings.MEDIA_ROOT,
            'tinymce',
            str(upload_time.year),
            str(upload_time.month),
            str(upload_time.day)
        )
        # If there is no such path, create
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, file_obj.name)

        file_url = f'{settings.MEDIA_URL}tinymce/{upload_time.year}/{upload_time.month}/{upload_time.day}/{file_obj.name}'

        if os.path.exists(file_path):
            return JsonResponse({
                "message": "file already exist",
                'location': file_url
            })

        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': file_url
        })
    return JsonResponse({'detail': "Wrong request"})
