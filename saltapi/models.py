from django.db import models
import uuid
from django.utils import timezone

class Salt(models.Model):

  status = (
        (0, u"不在线"),
        (1, u"在线"),
    )
  uuid = models.UUIDField(blank=True,primary_key=True, auto_created=True, default=uuid.uuid4)
  name = models.CharField(unique=True,max_length=64, verbose_name=u'SaltAPI名称')
  host = models.URLField(max_length=64, verbose_name=u'SaltAPI地址')
  username = models.CharField(max_length=64, verbose_name=u'SaltAPI用户名',default='admin')
  password = models.CharField(max_length=64, verbose_name=u'SaltAPI密码')
  status = models.IntegerField(choices=status,verbose_name=u'状态')
  comment = models.CharField(max_length=64, verbose_name=u'注释')
  update_time = models.DateTimeField(blank=True,default=timezone.now, verbose_name='更新时间')
  create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

  def __unicode__(self):
      return  self.name

  def __str__(self): 
      return self.name
      
  class Meta:
    verbose_name = u'SaltAPI信息'
    verbose_name_plural = verbose_name 

class Minions(models.Model):
    minions_status = (
    (0, 'Accepted'),
    (1, 'Unaccepted'),
    (2, 'Rejected'),
    (3, 'Denied'),
    (4, 'Unknown'),
    )
    uuid = models.UUIDField(blank=True,primary_key=True, auto_created=True, default=uuid.uuid4)
    minion = models.CharField(max_length=50,verbose_name=u'客户端',unique=True)
    saltserver = models.ForeignKey(Salt,on_delete=models.SET_NULL,null=True,verbose_name=u'所属Salt服务器')
    status = models.IntegerField(choices=minions_status,default=4,verbose_name=u'Key状态')
    create_date=models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')

    def __unicode__(self):
        return self.minion

    class Meta:
        verbose_name = u'Salt客户端'
        verbose_name_plural = u'Salt客户端列表'