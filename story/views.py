from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from .forms import LoginForm, RegisterForm, ProfileForm, StoryForm, EntryForm, CommentForm
from .models import Story, AuthUser, Entry, Profile, Write_Entry, Comment, Evaluation
from django.db.models import Q
from django.contrib.auth.decorators import login_required


class Top(generic.TemplateView):
    template_name = 'index.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'user/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'index.html'


class CreateUserView(generic.CreateView):
    template_name = 'user/create.html'
    form_class = RegisterForm
    success_url = reverse_lazy('story:top')


@login_required
def user_profile_view(request):
    template_name = 'user/profile.html'
    try:
        profile = Profile.objects.get(user=request.user)
        return render(request, template_name, {'profile': profile})
    except:
        template_name = 'user/profile_not_created.html'
        return render(request, template_name, {})


@login_required
def edit_profile(request):
    if Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.get(user=request.user)
    else:
        profile = Profile()

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():  # フォームのバリデーション
            profile = form.save(commit=False)
            profile.user = request.user
            profile.can_add_entry = None
            profile.can_add_entry_id = 0
            profile.save()
            return redirect('story:profile')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user/edit_profile.html', dict(form=form))


@login_required
def write_entry(request, story_id=None):
    if not Write_Entry.objects.filter(user=request.user).exists():
        return render(request, 'not_found.html', dict(title="あなたが今書ける小説はありません！ 。・゜゜・(>_<)・゜゜・。",
                                                      message="0 / 6 / 12 / 18時になるまで待ってみよう！"))
    entry = Entry()

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():  # フォームのバリデーション
            story = Write_Entry.objects.filter(user=request.user)
            _story_id = None
            for x in story:
                _story_id = x.story.id
            if str(_story_id) != story_id:
                return render(request, 'not_found.html', dict(title="時間が経ち過ぎました！ 。・゜゜・(>_<)・゜゜・。",
                                                              message="次の小説を書いてみよう！"
                                                              )
                              )
            entry = form.save(commit=False)
            entry.user = request.user
            entry.story = story[0].story
            entry.save()
            Write_Entry.objects.filter(user=request.user).delete()
            change_story = Story.objects.filter(story_id=story[0].story.id)[0]
            change_story.last_added = entry.create_datetime
            change_story.last_added_user = request.user.username
            change_story.save()
            return redirect('story:top')

    else:
        form = EntryForm(instance=entry)

    return render(request, 'add_entry.html', dict(form=form))


def story_list(request):
    if request.user.age < 18:
        storys = Story.objects.filter(~Q(tag1=6), ~Q(tag2=6), ~Q(tag3=6)).order_by('last_added')

    else:
        storys = Story.objects.all().order_by('last_added')

    return render(request,
                  'story_list.html',  # 使用するテンプレート
                  dict(storys=storys))


def show_story(request, story_id=None):
    story = get_object_or_404(Story, id=story_id)
    entrys = Entry.objects.filter(story=story)
    vote_num = 0
    if Evaluation.objects.filter(story=story).exists():
        evaluation = Evaluation.objects.filter(story=story)[0]
        vote_num = evaluation.nice
    comments = Comment.objects.filter(story=story)[0:4]
    comment = Comment()

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.story = story
            comment.save()
            return redirect('story:show_story', story_id)

    else:
        form = CommentForm(instance=comment)

    return render(request, 'show_story.html', dict(story=story, entrys=entrys,
                                                   form=form, comments=comments, vote=vote_num
                                                   )
                  )


@login_required
def start_story(request):
    if request.user.already_start_story:
        return redirect('story:top')
    else:
        story = Story()

    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():  # フォームのバリデーション
            story = form.save(commit=False)
            story.starter = request.user
            story.last_added_user = request.user.username
            story.save()
            user = AuthUser.objects.get(id=request.user.id)
            user.already_start_story = True
            user.save()
            return redirect('story:profile')

    else:
        form = StoryForm(instance=story)

    return render(request, 'create_story.html', dict(form=form))


def error_404(request):
    contexts = {
        'request_path': request.path,
    }

    return render(request, '404.html', contexts, status=404)


def comment_page(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    comments = Comment.objects.filter(story=story)

    return render(request, 'comment.html', dict(comments=comments, story=story))


def entry_list(request, page):
    entrys = Entry.objects.all().order_by('create_datetime')[int(page) * 20 - 20: int(page) * 20]

    return render(request, 'entry_list.html', dict(entrys=entrys, page=page))


@login_required
def add_nice(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    if Evaluation.objects.filter(story=story).exists():
        evaluation = Evaluation.objects.filter(story=story)[0]
        if request.user in evaluation.nice_users.all():
            evaluation.nice_users.remove(request.user)
            evaluation.nice -= 1
            evaluation.save()
            return redirect('story:show_story', story_id)
        evaluation.nice_users.add(request.user)
        evaluation.nice += 1
        evaluation.save()
        return redirect('story:show_story', story_id)

    else:
        evaluation = Evaluation(story=story, nice=1)
        evaluation.save()
        evaluation.nice_users.add(request.user)
        return redirect('story:show_story', story_id)

