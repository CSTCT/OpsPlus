from django.db import models
import uuid
from django.utils import timezone
from saltapi.models import Salt
from accounts.models import User

class ISP(models.Model):

  name = models.CharField(unique=True,max_length=64, verbose_name=u'运营商')

  def __str__(self): 
      return self.name

class IDC(models.Model):

    uuid = models.UUIDField(blank=True,primary_key=True, auto_created=True, default=uuid.uuid4)
    name = models.CharField(unique=True,max_length=64, verbose_name=u'机房名称')
    isp = models.ForeignKey(ISP,null=True,on_delete=models.SET_NULL,verbose_name=u'运营商名称')
    address = models.CharField(max_length=64, verbose_name=u'机房地址')
    contact = models.CharField(max_length=32, verbose_name=u'联系人')
    phone = models.CharField(max_length=32, verbose_name=u'联系电话')
    network = models.TextField(blank=True,null=True, verbose_name=u'IP地址段')
    comment = models.TextField(blank=True,null=True, verbose_name=u'备注')
    update_time = models.DateTimeField(blank=True,default=timezone.now, verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self): 
        return self.name

    class Meta:
      verbose_name = u'机房管理'
      verbose_name_plural = verbose_name 

class ServerAsset(models.Model):

    operation_status = (
      (1,'运营中'),
      (2,'未上线'),
      (3,'故障中'),
      (4,'维修中'),
      (5,'开发机'),
      (6,'测试机'),
      (7,'下线'),
      )
    minion_status = (
      (1,'正常'),
      (2,'未安装'),
      )
    
    uuid = models.UUIDField(blank=True,primary_key=True, auto_created=True, default=uuid.uuid4)

    hostname = models.CharField(max_length=50,verbose_name=u'主机名')
    ip = models.GenericIPAddressField(unique=True, verbose_name=u'IP')
    idc = models.ForeignKey(IDC, blank=True, null=True,on_delete=models.SET_NULL,verbose_name=u'机房')
    salt = models.ForeignKey(Salt,blank=True, null=True,on_delete=models.SET_NULL,verbose_name=u'Salt-Master')
    status = models.IntegerField(choices=operation_status,verbose_name=u'状态',default=1)
    ops = models.ForeignKey(User, blank=True, null=True,on_delete=models.SET_NULL,related_name='ops',verbose_name=u'运维负责人')
    dev = models.ForeignKey(User, blank=True, null=True,on_delete=models.SET_NULL,related_name='dev',verbose_name=u'开发负责人')
    manufacturer = models.CharField(max_length=20, blank=True, verbose_name=u'厂商')
    productname = models.CharField(max_length=100, blank=True, verbose_name=u'型号')
    sn = models.CharField(max_length=100, blank=True, verbose_name=u'序列号')
    cpu_model = models.CharField(max_length=100, blank=True, verbose_name=u'CPU型号')
    cpu_nums = models.PositiveSmallIntegerField(blank=True,verbose_name=u'CPU线程', default=0)
    memory = models.CharField(max_length=20,blank=True, verbose_name=u'内存')
    disk = models.TextField(blank=True, verbose_name=u'硬盘')

    os = models.CharField(max_length=200, blank=True, verbose_name=u'操作系统')
    virtual = models.CharField(max_length=20, blank=True, verbose_name=u'虚拟化')
    kernel = models.CharField(max_length=200, blank=True, verbose_name=u'内核')
    shell = models.CharField(max_length=10, blank=True, verbose_name=u'Shell')
    selinux = models.CharField(max_length=50, blank=True, verbose_name=u'Selinux')
    locale = models.CharField(max_length=200, blank=True, verbose_name=u'编码')

    saltversion = models.CharField(max_length=10, blank=True, verbose_name=u'Salt版本')
    minion_status = models.IntegerField(choices=minion_status,verbose_name=u'Minion状态',default=2)

    update_time = models.DateTimeField(blank=True,default=timezone.now, verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __unicode__(self):
        return self.hostname
    
    class Meta:
        # default_permissions = ()
        # permissions = (
        #     ("view_asset", u"查看资产"),
        #     ("edit_asset", u"管理资产"),
        # )
        verbose_name = u'主机资产信息'
        verbose_name_plural = u'主机资产信息管理'


class NetworkInterface(models.Model):

    name = models.CharField(max_length=15, verbose_name=u'网卡名称')
    address = models.CharField(max_length=15,verbose_name=u'IP地址')
    mac = models.CharField(max_length=17,verbose_name=u'Mac地址')
    server = models.ForeignKey(ServerAsset, null=True, on_delete=models.SET_NULL, verbose_name=u'主机' )

    def __str__(self):
        return self.name

    class Meta:

      unique_together = (('name', 'server'),)
      verbose_name = u'网卡管理'
      verbose_name_plural = verbose_name 
