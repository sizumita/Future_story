from django.core.management.base import BaseCommand
from story.models import AuthUser, Story, Write_Entry


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Write_Entry.objects.all().delete()
        user = list(AuthUser.objects.all())
        story = list(Story.objects.all())
        for x in range(len(story)):
            try:
                if user[0].age < 18:
                    if story[0].tag1 == 6 or story[0].tag2 == 6 or story[0].tag3 == 6:
                        Write_Entry(user=user[0], story=story[1]).save()
                        del user[0]
                        del story[1]
                        continue
                Write_Entry(user=user[0], story=story[0]).save()
                del user[0]
                del story[0]
            except IndexError:
                break


