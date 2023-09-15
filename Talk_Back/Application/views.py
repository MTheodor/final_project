from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
#from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    all_posts = Post.objects.all()
    post_links = ""

    for post in all_posts:
        post_links += f"""
        <div class = 'uploads'>
            <a href='/post/{post.id}'>{post.title}</a>
            <p>{post.text}</p>
        </div>"""
    
    context = {
        'post_links': post_links,
    }

    return render(request, 'home.html', context)

class RemoveUser(forms.Form):
    username = forms.CharField()

def account(request):
    if request.user.is_authenticated:
        user = request.user
        confirm_delete = False
        form = None

        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'update_profile':
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = request.POST.get('email')
                user.save()
                messages.success(request, 'Profile details updated successfully.')
                return redirect('account')

            elif action == 'change_password':
                form = PasswordChangeForm(user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Password changed successfully.')
                    return redirect('account')
                else:
                    messages.error(request, 'Please correct the error below.')

            elif action == 'delete_account':
                if request.POST.get('confirm_delete') == 'on':
                    user_posts = Post.objects.filter(by_user=user)
                    user_posts.delete()

                    logout(request)
                    user.delete()
                    messages.success(request, 'Account and associated posts have been deleted.')
                    return redirect('/')
                else:
                    messages.error(request, 'Please check the confirmation checkbox.')

        else:
            form = PasswordChangeForm(request.user)

        return render(request, 'account.html', {'form': form, 'user': user, 'confirm_delete': confirm_delete})
    else:
        return HttpResponse("You are not logged in. Please log in to access your account.")
    
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs.pop('maxlength', None)

        self.fields['password2'].label = 'Confirm password'

    class Meta(UserCreationForm.Meta):
         fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('/')

def settings(request):
    return HttpResponse("Testing...")

def subscriptions(request):
    return HttpResponse("Testing...")

def liked(request):
    return HttpResponse("Testing...")

def post(request, post_id):
    try:
        my_post = get_object_or_404(Post, id=post_id)
        if my_post.by_user:
            user_name = my_post.by_user.username
        else:
            user_name = "Deleted User"
            
        return render(request, 'post.html', {'my_post': my_post, 'user_name': user_name})
    except Post.DoesNotExist:
        return HttpResponse("Error 404", status=404)
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'images']
        
def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.by_user = request.user
                post.save()
                return redirect('/')
        else:
            form = PostForm()
        return render(request, 'create_post.html', {'form': form})
    else:
        return HttpResponse("You are not logged in. Please log in to access your account.")

