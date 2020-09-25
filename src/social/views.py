from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView,\
                                DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from . import models


def home_page(request):
    try:
        user = get_user_model().objects.get(
            username=request.user.username
            )
        group_list_user = models.Group.objects.filter(
            members=user.id
            ).order_by('-group_created')
        return render(
            request,
            'social/home_page.html',
            {'group_list_user': group_list_user}
            )
    except ("User is probably not logged in"):
        return render(request, 'social/home_page.html', {})


class GroupListView(ListView):
    model = models.Group
    template_name = 'social/group_list.html'
    ordering = ['-group_created']
    paginate_by = 5


class UserGroupListView(ListView):
    model = models.Group
    template_name = 'social/user_groups.html'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(
            get_user_model(),
            username=self.kwargs.get('username')
            )
        return models.Group.objects.filter(
            creator=user
            ).order_by('-group_created')


class UserGroupFolowingListView(ListView):
    model = models.Group
    template_name = 'social/user_groups_folowing.html'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(
            get_user_model(),
            username=self.kwargs.get('username')
            )
        return models.Group.objects.filter(
            members=user.id
            ).order_by('-group_created')


class UserPostListView(ListView):
    model = models.Post
    template_name = 'social/user_posts.html'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(
            get_user_model(),
            username=self.kwargs.get('username')
            )
        return models.Post.objects.filter(owner=user).order_by('-post_created')


class GroupDetailView(DetailView):
    model = models.Group

    def get_context_data(self, *args, **kwargs):
        context = super(
            GroupDetailView,
            self
            ).get_context_data(*args, **kwargs)

        obj = get_object_or_404(models.Group, slug=self.kwargs['slug'])
        joined = False
        if obj.members.filter(id=self.request.user.id).exists():
            joined = True

        context['joined'] = joined
        return context


class GroupCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Group
    fields = ['name', 'description']
    success_message = 'Group has been created!'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.name)
        form.instance.creator = self.request.user
        return super().form_valid(form)


class GroupDeleteView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        SuccessMessageMixin,
        DeleteView
        ):
    model = models.Group
    success_url = reverse_lazy('social:home')
    success_message = 'Group has been deleted!'
    # SuccessMessageMixin doesn't work in DeleteView!!!

    def test_func(self):
        group = self.get_object()
        if self.request.user.id == group.creator.id:
            return True
        return False


class GroupMembers(DetailView):
    model = models.Group
    template_name = 'social/group_members_list.html'


@login_required
def join_group_view(request, slug):
    group = get_object_or_404(models.Group, id=request.POST.get('group_id'))

    if group.members.filter(id=request.user.id).exists():
        group.members.remove(request.user)
    else:
        group.members.add(request.user)

    return HttpResponseRedirect(reverse(
        'social:group_detail',
        kwargs={'slug': slug}
        ))


class PostList(ListView):
    model = models.Post
    template_name = 'social/post_list.html'
    ordering = ['-post_created']
    paginate_by = 5

    def get_queryset(self):
        group = get_object_or_404(models.Group, slug=self.kwargs.get('slug'))
        return models.Post.objects.filter(
            on_group=group
            ).order_by('-post_created')

    def get_context_data(self, *args, **kwargs):
        context = super(PostList, self).get_context_data(*args, **kwargs)

        obj = get_object_or_404(models.Group, slug=self.kwargs['slug'])
        joined = False
        if obj.members.filter(id=self.request.user.id).exists():
            joined = True

        context['joined'] = joined
        return context


class CreatePostView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Post
    fields = ['title', 'context']
    success_message = 'Post has been created!'

    def form_valid(self, form):
        form.instance.on_group = get_object_or_404(
            models.Group,
            slug=self.kwargs['slug']
            )
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Post
    template_name = 'social/post_delete.html'
    # success_url = reverse_lazy('social:post_list',
    # models.Group.objects.get(creator=request.user.id).slug)

    def get_success_url(self, **kwargs):
        group = get_object_or_404(models.Group, slug=self.kwargs['slug'])
        return reverse_lazy('social:post_list', kwargs={'slug': group.slug})

    def test_func(self):
        post = self.get_object()
        if self.request.user.id == post.owner.id:
            return True
        return False


class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Post
    template_name = 'social/edit_post.html'
    fields = ['title', 'context']

    def test_func(self):
        post = self.get_object()
        if self.request.user.id == post.owner.id:
            return True
        return False


class PostDetailsView(DetailView):
    model = models.Post
    template_name = 'social/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            PostDetailsView,
            self
            ).get_context_data(*args, **kwargs)

        obj = get_object_or_404(models.Post, pk=self.kwargs['pk'])
        liked = False
        if obj.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['liked'] = liked
        return context


@login_required
def like_post_view(request, slug, pk):
    post = get_object_or_404(models.Post, id=request.POST.get('post_id'))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse(
        'social:post_detail',
        kwargs={'slug': slug, 'pk': pk}
        ))
