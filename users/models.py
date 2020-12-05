from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()





class Follow(models.Model):
    '''Subcribe to user recipse'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower", null=True)  # сам юзер
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", null=True, blank=True)  # на кого подписан



