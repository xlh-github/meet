from django.db import models

# Create your models here.
class MeetingRoom(models.Model):
    '''会议室'''
    name = models.CharField(max_length=32,verbose_name="会议室名称")
    class Meta:
        verbose_name_plural = "会议室"

    def __str__(self):
        return self.name

class ReserveRecord(models.Model):
    '''预定记录表'''
    data = models.DateField(verbose_name="预定日期")
    user = models.ForeignKey(to="UserInfo",verbose_name="预订人")
    room = models.ForeignKey(to="MeetingRoom",verbose_name="预定房间")
    time1 = (
        (1,"8.00"),
        (2,"9.00"),
        (3,"10.00"),
        (4,"11.00"),
        (5,"12.00"),
        (6,"13.00"),
        (7,"14.00"),
        (8,"15.00"),
        (9,"16.00"),
        (10,"17.00"),
        (11,"18.00"),
        (12,"19.00"),
        (13,"20.00"),
    )
    timeline = models.IntegerField(choices=time1,verbose_name="预定时间")
    class Meta:
        verbose_name_plural = "预订记录表"
        unique_together = (
            ('data', 'timeline', 'room')
        )
    def __str__(self):
        return self.user.username

class UserInfo(models.Model):
    '''用户信息'''
    username = models.CharField(max_length=32,verbose_name="用户名",unique=True)
    password = models.CharField(max_length=64,verbose_name="密码")
    class Meta:
        verbose_name_plural = "用户信息"

    def __str__(self):
        return self.username