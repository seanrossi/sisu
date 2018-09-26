from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment, Category, AppPreferrence, PostPreferrence, ReplyToComment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, ContactForm, SearchForm, ReplyToCommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from ipware import get_client_ip
from django.template import Context
import re
from django.db.models import Q
from django.contrib import messages

# Create your views here.

#
# Global variables across all templates
# 
def category(request):
  categories = Category.__members__.items()
  return {'categories' : categories}

#
# For About us page
#
def about_sisu(request):
    return render(request, 'blog/about.html')
    
def about_us(request):
    return render(request, 'blog/about_us.html')
    
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})
    
# Post.objects.get(pk=pk)

def post_list_by_category(request, category_name):
    posts = Post.objects.filter(category_name=category_name).order_by('-published_date')
    cat = Category.get_label(category_name)
    return render(request, 'blog/post_list.html', {'posts':posts, 'cat':cat })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_name = auth.get_user(request)
    ip = request.session['ip']
      
    if request.user.is_authenticated:
        if PostPreferrence.objects.filter(username=user_name, ip_address=ip, postpk=pk, vote_value=1).exists():   
            voted = True
        else:
            voted = False
        
    else:
        if PostPreferrence.objects.filter(ip_address=ip, postpk=pk, vote_value=1).exists(): 
            voted = True
        else:
            voted = False   
    try:
        total_yes = PostPreferrence.objects.filter(vote_value=1, postpk=pk).count()
    except PostPreferrence.DoesNotExist:
        total_yes = 0;
    
    summary = ({
      'voted':voted,
      'total_yes': total_yes,
    }) 
    
    return render(request, 'blog/post_detail_index.html', {'post': post, 'summary': summary})
    
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required   
def post_draft_list(request):
  posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
  return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required  
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish_post()
    return redirect('post_detail', pk=pk)

@login_required    
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required     
def post_edit(request, pk):

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required     
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.info(request, 'Thank you for your comment! It will be posted after censoring.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
    
@login_required     
def add_reply_to_comment(request, pk, cpk):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, post=post, pk=cpk)
    if request.method == "POST":
        form = ReplyToCommentForm(request.POST)
        if form.is_valid():
            replyToComment = form.save(commit=False)
            replyToComment.post = post
            replyToComment.comment = comment
            replyToComment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
    
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
#
# For contact us page
#
def contact_us(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            sender = "From " + form.cleaned_data['your_name']
            if request.user.is_authenticated:
              sender = sender + "_(REG_User)_" + auth.get_user(request).username
            else:
              sender = sender + "_(PUB_User)_"
              
            subject = sender + form.cleaned_data['subject']
            from_email = form.cleaned_data['your_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'blog/contact_us_success.html')
    return render(request, "blog/contact_us.html", {'form': form})
    
#
# For User Settings
#
@login_required
def user_settings(request):
    return render(request, 'blog/user_settings.html')
       
#
# For voting app
#
# check if the user / ip_address has voted 
def check_voted(request):
  voted = False;
  user_ip = get_client_ip(request)
  user_name = auth.get_user(request)
  ip = user_ip[0]
  
  request.session['ip'] = ip
  
  total_yes = AppPreferrence.objects.filter(vote_yes=1).count()
  total_no = AppPreferrence.objects.filter(vote_no=1).count()
  
   
  if request.user.is_authenticated:
     if AppPreferrence.objects.filter(username=user_name).exists() or AppPreferrence.objects.filter(ip_address=ip).exists():   
        voted = True
        
  else:
     if AppPreferrence.objects.filter(ip_address=ip).exists(): 
        voted = True
  
  summary = ({
      'voted':voted,
      'total_yes': total_yes,
      'total_no': total_no,
    })     
  return ({'summary': summary}) 

# save the vote if never voted
def vote_for_app(request, voted_value):
   
   if request.method == "POST":     
      user_preference = int(voted_value)
      #user_ip = get_client_ip(request)
      user_name = auth.get_user(request)
      ip = request.session['ip']
  
      app_voted = AppPreferrence() 
      app_voted.ip_address = ip
      
      if user_preference == 1:
          app_voted.vote_yes += 1
      elif user_preference == 2:
          app_voted.vote_no +=1
      
      if request.user.is_authenticated:
         #print("===================================" + str(user_preference) + str(ip) + str(user_name))
         app_voted.username = user_name
              
   app_voted.save()
     
   return render(request, "blog/about.html")
  
def on_off_star(request, postid, on_off_value):
   
   if request.method == "POST":     
          
      post_preference = int(on_off_value)
      user_name = auth.get_user(request)
      ip = request.session['ip']
      
      post = get_object_or_404(Post, pk=postid)   
      
      try:
        postpreferrence_obj = PostPreferrence.objects.get(username=request.user, postpk=post, ip_address=ip)     
        postpreferrence_obj.vote_value = post_preference
        postpreferrence_obj.save()       
        
        if post_preference == 2:
            voted = False
        else:
            voted = True
      
      except PostPreferrence.DoesNotExist:
        post_voted = PostPreferrence()
        post_voted.ip_address = ip
        post_voted.postpk = post
        post_voted.vote_value = post_preference 
      
        if request.user.is_authenticated:
          #print("===================================" + str(user_preference) + str(ip) + str(user_name))
          post_voted.username = user_name
                 
        post_voted.save()   
        voted = True
   
      summary = ({
         'voted':voted,
         'total_yes': PostPreferrence.objects.filter(vote_value=1, postpk=postid).count(),
      })
      
   return render(request, 'blog/post_detail_index.html', {'post':post, 'summary':summary})
 
# Search Functionality
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
 
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
    
def search(request):
    query_string = ''
    found_entries = None
    
    if request.method == "POST":
       search_form = SearchForm(request.POST)
      
       if search_form.is_valid():
          query_string = search_form.cleaned_data['search_string']
          post_query = get_query(query_string, ['title', 'text', 'category_name'])
          found_entries = Post.objects.filter(post_query).order_by('-published_date')
            
    else:
       search_form = SearchForm()
    
    return render(request, 'blog/post_search_res.html',{ 'query_string': query_string, 'found_entries': found_entries })
