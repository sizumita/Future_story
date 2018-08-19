from django import template
from future_story.settings import STATIC_URL
from story.models import Write_Entry, AuthUser, Entry, Story, Evaluation
register = template.Library()


@register.filter(name='get_id')
def get_id(value):
    sid = None
    for x in Write_Entry.objects.filter(user_id=value):
        sid = x.story_id
    if not sid:
        sid = False
    return sid


@register.filter(name='get_story')
def get_story(value):
    if not Write_Entry.objects.filter(user_id=value).exists():
        return ""
    story = Write_Entry.objects.filter(user_id=value)[0].story
    entrys = [entry.text for entry in Entry.objects.filter(story=story)]
    text = story.first_text + "\n"
    text += "\n".join(entrys)
    return text


@register.filter(name='get_story_name')
def get_story_name(value):
    if not Write_Entry.objects.filter(user_id=value).exists():
        return ""
    story = Write_Entry.objects.filter(user_id=value)[0].story
    return story.name


@register.filter(name='can_write_entry')
def can_write_entry(value):
    if not Write_Entry.objects.filter(user_id=value).exists():
        return False
    else:
        return True


@register.filter(name='already_vote')
def already_vote(value, arg):
    try:
        if Evaluation.objects.filter(story_id=arg).exists():
            evaluation = Evaluation.objects.filter(story_id=arg)[0]
            if AuthUser.objects.filter(id=value)[0] in evaluation.nice_users.all():
                return 'images/good_already.png'
            else:
                return 'images/good.png'
    except IndexError:
        return 'images/good.png'
