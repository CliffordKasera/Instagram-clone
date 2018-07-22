from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now=True)
    likes = models.BooleanField(default=False)
    caption = models.CharField(max_length=250)
    tags = models.IntegerField(default=0)


    class Meta:

        ordering = ('-upload_date')

    def delete_images(self):

        return self.delete()   

    def save_image(self):

        return self.save()
    
    @classmethod
    def get_image_id(cls, id):

        image = Image.objects.get(pk=id)
        return image
    
    @classmethod
    def get_all_images(cls):

        images = Image.objects.all()
        return images


class Profile(models.Model):
    profile_pic = models.ImageField(upload_to='profile/'blank=True)
    bio = models.CharField(max_length=255)
    user = models.ForeignKey(User)

    def save_profile(self):
        self.save()
    
    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains = name)
        return profile
    
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

    @classmethod
    def filter_by_id(cls, id):
        profile = Profile.objects.filter(user = id).first()
        return profile