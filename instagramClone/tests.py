from django.test import TestCase
from .models import Profile, Image, Comments

# Create your tests here.

class ImageTestClass(TestCase):
     
    def setUp(self):
         self.image=Image(user='cliff',image='gallery/',caption="memyselfandi",likes="234",)


    def test_instance(self):
        self.assertTrue(isinstance(self.image,Image))

    def tearDown(self):
        Image.objects.all().delete()

    def test_save_image(self):
        self.image.save_image()
        image=Image.objects.all()
        self.assertTrue(len(image)>0)  

    def test_delete_image(self):
        self.image.save_image()
        images=Image.objects.all()
        self.image.delete_image()
        images=Image.objects.all()
        self.assertTrue(len(images)==0)  

    def test_update_caption(self):
        self.image.save_image()
        self.image.update_caption(self.image.id,'gallery/')
        changed_caption = Image.objects.filter(caption='yolo')
        self.assertTrue(len(changed_caption)>0)

    def test_get_image_by_id(self):
        found_img = self.image.get_image_id(self.image.id)
        img = Image.objects.filter(id=self.image.id)
        self.assertTrue(found_img,img)

    def test_get_all_images(self):
        found_imgs = self.image.get_all_images()
        imgs = Image.objects.all()
        self.assertTrue(found_imgs,imgs)


class ProfileTestClass(TestCase):
    def setUp(self):
        self.profile = Profile(profile_pic='profile',bio='very versatile',user='cliff')
        self.profile.save()

    def tearDown(self):
        Profile.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_save_profile(self):
        Profile.objects.all().delete()
        self.profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)>0)

    def test_search_profile(self):
        name = 'cliff'
        found_profile = self.profile.search_profile(name)
        self.assertTrue(len(found_profile)>1)


class CommentsTestClass(TestCase):
    def setUp(self):
        self.comment = Comments(comment='oh well',image='gallery/',user='cliff')
        self.profile.save()

    def tearDown(self):
        Comments.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.comment,Comment))

    def test_save_comment(self):
        Comments.objects.all().delete()
        self.comment.save_comment()
        comment = Comments.objects.all()
        self.assertTrue(len(comment)>0)

    def test_delete_comment(self):
        self.comment.save_comment()
        comment=Comments.objects.all()
        self.comment.delete_comment()
        comment=Comments.objects.all()
        self.assertTrue(len(comment)==0)  

    def test_get_comments_by_images(self):
        found_comments = self.comment.get_comments_by_images(self.comment.id)
        comments = Comments.objects.filter(id=self.comment.id)
        self.assertTrue(found_comments,comments)