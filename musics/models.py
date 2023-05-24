from django.db import models

# Create your models here.
class Room(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    playlists = models.ManyToManyField('playlist', related_name='rooms')


class Playlist(models.Model):
    title = models.CharField(max_length=200)
    room = models.ForeignKey(Room, null=True, on_delete=models.CASCADE)
    video_key = models.CharField(max_length=12)
    # 플레이리스트를 큐 형식으로 관리하기 위해 순서 부여하는 필드
    queue_order = models.IntegerField(default=0)


    @classmethod
    def add_to_queue(cls, title, video_key, room):
        last_order = cls.objects.filter(rooms=room).aggregate(models.Max('queue_order'))['queue_order__max'] or 0
        cls.objects.create(title=title, video_key=video_key, queue_order=last_order + 1)


    def get_next_song(cls, room):
        # 큐에서 가장 먼저 들어온 음악 가져오기
        next_song = cls.objects.filter(rooms=room).order_by('queue_order').first()
        if next_song:
            return next_song