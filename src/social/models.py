from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class Group(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    group_created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        get_user_model(),
        related_name='members',
        blank=True
        )

    def get_absolute_url(self):
        return reverse('social:group_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Post(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    on_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    context = models.TextField(max_length=500)
    post_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        get_user_model(),
        related_name='likes',
        blank=True
        )

    def get_absolute_url(self):
        return reverse(
            'social:post_detail',
            kwargs={'slug': self.on_group.slug, 'pk': self.pk}
            )

    def __str__(self):
        return self.title
