from django.db import models

from pyuploadcare.dj.models import ImageField

from django.contrib.auth.models import User

from friendship.models import Friend,Follow,Block

# Create your models here.

class Profile(models.Model):

    profile_pic = ImageField(blank=True, manual_crop="")

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


class Image(models.Model):

    name = models.CharField(max_length = 70)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    profile_pics = models.ForeignKey(Profile,on_delete=models.CASCADE)

    image = ImageField(null=True, blank=True, manual_crop="")

    caption = models.CharField(max_length=250)


    def __str__(self):
        
        return self.name

    def delete_image(self):

        return self.delete()   

    def save_image(self):

        return self.save()

    @classmethod
    def update_caption(cls,id,value):

        cls.objects.filter(id=id).update(caption=value)
    
    @classmethod
    def get_image_id(cls, id):

        image = Image.objects.get(pk=id)

        return image
    
    @classmethod
    def get_all_images(cls):

        images = Image.objects.all()

        return images

    @classmethod
    def get_profile_images(cls, user):
        images = Image.objects.filter(user__pk = user)
        return images


class Comments(models.Model):

    comment = models.CharField(max_length=140,blank=True,null=True)

    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):

        return self.Comments
    
    def save_comment(self):

        return self.save()

    def delete_comment(self):

        return self.delete()
    
    @classmethod
    def get_comments_by_images(cls, id):

        comments = cls.objects.filter(image__pk = id)

        return comments


class Likes(models.Model):

    imageid = models.ForeignKey(Image)

    liker = models.ForeignKey(User)

        
