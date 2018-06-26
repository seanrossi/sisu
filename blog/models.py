from django.db import models
from django.utils import timezone
from enumfields import EnumField
from enumfields import Enum
from django.contrib.auth.models import User

# Create your models here.
class Category(Enum):
  Category_A = 'A';
  Category_B = 'B'; 
  Category_C = 'C';
  Category_D = 'D';

class Post(models.Model):
  author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  text = models.TextField()
  short_desc = models.TextField()
  published_date = models.DateTimeField(blank=True, null=True)
  created_date = models.DateTimeField(default=timezone.now)
  category_name = EnumField(Category, max_length=1, default='A')
  
  def publish_post(self):
    self.published_date = timezone.now()
    self.save()
  
  def __str__(self):
    return self.title
    

    
class Comment(models.Model):
  post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
  author = models.CharField(max_length=200)
  text = models.TextField()
  created_date = models.DateTimeField(default=timezone.now)
  approved_comment = models.BooleanField(default=False)
  
  def approve(self):
    self.approved_comment = True
    self.save()
  
  def approved_comments(self):
    return self.comments.filter(approved_comment=True)
    
  def __str__(self):
    return self.text
    
class AppPreferrence(models.Model):
  username = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
  ip_address = models.CharField(max_length=40)
  vote_yes = models.IntegerField(default=0) #1 = yes, 2 = no
  vote_no = models.IntegerField(default=0)
  vote_date = models.DateTimeField(default=timezone.now)
  
  def __str__(self):
    return str(self.username) + str(self.ip_address) + str(self.vote_date)
  
  