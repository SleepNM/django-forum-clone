from . import models
from django.contrib.auth import get_user_model


# For side bar in base.html
def side_bar(request):
    total_users = get_user_model().objects.count()
    total_groups = models.Group.objects.count()
    total_posts = models.Post.objects.count()
    # total_comments = models.Comment.objects.count()
    return {
        'total_users': total_users,
        'total_groups': total_groups,
        'total_posts': total_posts
        }
