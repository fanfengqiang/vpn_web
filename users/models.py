from django.db import models

# Create your models here.


class User(models.Model):

    name = models.CharField('用户名',max_length=64, unique=True)
    password = models.CharField('密码',max_length=64)
    email = models.EmailField('邮件地址',unique=True)
    c_time = models.DateTimeField('创建时间',auto_now_add=True)
    has_confirmed = models.BooleanField('是否邮件确认',default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"



class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"




class Nas(models.Model):
    nasname = models.CharField(max_length=128)
    shortname = models.CharField(max_length=32, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    ports = models.IntegerField(blank=True, null=True)
    secret = models.CharField(max_length=60)
    server = models.CharField(max_length=64, blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nas'


class Radacct(models.Model):
    radacctid = models.AutoField('RADIUS 计费 ID',primary_key=True, blank=True)
    acctsessionid = models.CharField('ACCT会话ID',max_length=64)
    acctuniqueid = models.CharField('记账编号',unique=True, max_length=32)
    username = models.CharField('用户名',max_length=64)
    groupname = models.CharField('组名',max_length=64)
    realm = models.CharField('组',max_length=64, blank=True, null=True)
    nasipaddress = models.CharField('NAS的IP地址',max_length=15)
    nasportid = models.CharField('NAS端口ID',max_length=15, blank=True, null=True)
    nasporttype = models.CharField('NAS端口类型',max_length=32, blank=True, null=True)
    acctstarttime = models.DateTimeField('记账开始时间',blank=True, null=True)
    acctupdatetime = models.DateTimeField(blank=True, null=True)
    acctstoptime = models.DateTimeField('记账停止时间',blank=True, null=True)
    acctinterval = models.IntegerField(blank=True, null=True)
    acctsessiontime = models.IntegerField('用户会话时间',blank=True, null=True)
    acctauthentic = models.CharField('用户的认证方式',max_length=32, blank=True, null=True)
    connectinfo_start = models.CharField(max_length=50, blank=True, null=True)
    connectinfo_stop = models.CharField(max_length=50, blank=True, null=True)
    acctinputoctets = models.BigIntegerField('下载流量',blank=True, null=True)
    acctoutputoctets = models.BigIntegerField('上传流量',blank=True, null=True)
    calledstationid = models.CharField('NAS端MAC地址',max_length=50)
    callingstationid = models.CharField('用户IP地址',max_length=50)
    acctterminatecause = models.CharField('终止类型',max_length=32)
    servicetype = models.CharField('客户端类型',max_length=32, blank=True, null=True)
    framedprotocol = models.CharField('认证协议',max_length=32, blank=True, null=True)
    framedipaddress = models.CharField('服务端IP地址',max_length=15)

    class Meta:
        managed = False
        db_table = 'radacct'
        verbose_name_plural = "VPN计费表"


class Radcheck(models.Model):
    username = models.CharField('用户名',max_length=64)
    attribute = models.CharField('密码类型',max_length=64)
    op = models.CharField('操作符',max_length=2)
    value = models.CharField('密码值',max_length=253)

    def __str__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'radcheck'
        verbose_name = "VPN用户名"
        verbose_name_plural = "VPN账户表"


class Radgroupcheck(models.Model):
    groupname = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)



    class Meta:
        managed = False
        db_table = 'radgroupcheck'



class Radgroupreply(models.Model):
    groupname = models.CharField('组名',max_length=64)
    attribute = models.CharField('属性',max_length=64)
    op = models.CharField('操作符',max_length=2)
    value = models.CharField('值',max_length=253)

    def __str__(self):
        return self.groupname

    class Meta:
        managed = False
        db_table = 'radgroupreply'
        verbose_name = "VPN组"
        verbose_name_plural = "VPN组授权表"


class Radpostauth(models.Model):
    username = models.CharField('用户名',max_length=64)
    pass_field = models.CharField('密码',db_column='pass', max_length=64)  # Field renamed because it was a Python reserved word.
    reply = models.CharField('用户状态',max_length=32)
    authdate = models.TextField('记录连接时间')  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'radpostauth'
        verbose_name_plural = "VPN登录记录表"


class Radreply(models.Model):
    username = models.CharField(max_length=64)
    attribute = models.CharField(max_length=64)
    op = models.CharField(max_length=2)
    value = models.CharField(max_length=253)

    class Meta:
        managed = False
        db_table = 'radreply'


class Radusergroup(models.Model):
    username = models.CharField('用户名',max_length=64)
    groupname = models.CharField('组名',max_length=64)
    priority = models.IntegerField('权重')

    def __str__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'radusergroup'
        verbose_name = "VPN用户名"
        verbose_name_plural = "VPN账户&组对应表"
