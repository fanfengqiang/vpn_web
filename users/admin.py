from django.contrib import admin
from users import models

class UserAdmin(admin.ModelAdmin):

    '''设置列表可显示的字段'''
    list_display = ('name', 'password', 'email','has_confirmed','c_time')

    '''设置过滤选项'''
    list_filter = ('has_confirmed',)

    '''每页显示条目数'''
    list_per_page = 20
    ordering = ('-c_time',)
    date_hierarchy = 'c_time'
    search_fields = ['name', 'password', 'email']

    # # 列表顶部，设置为False不在顶部显示，默认为True。
    # actions_on_top = True
    #
    # # 列表底部，设置为False不在底部显示，默认为False。
    # actions_on_bottom = False

class ConfirmStringAdmin(admin.ModelAdmin):

    '''设置列表可显示的字段'''
    list_display = ('user', 'code','c_time')


    '''每页显示条目数'''
    list_per_page = 20
    ordering = ('-c_time',)
    date_hierarchy = 'c_time'

class RadcheckAdmin(admin.ModelAdmin):

    '''设置列表可显示的字段'''
    list_display = ('username', 'attribute','op','value')


    '''每页显示条目数'''
    list_per_page = 20
    search_fields = ['username', 'value']

class RadgroupreplyAdmin(admin.ModelAdmin):

    '''设置列表可显示的字段'''
    list_display = ('groupname', 'attribute','op','value')


    '''每页显示条目数'''
    list_per_page = 20
    search_fields = ['groupname', 'value']

    '''设置过滤选项'''
    list_filter = ('groupname',)

class RadusergroupAdmin(admin.ModelAdmin):

    '''设置列表可显示的字段'''
    list_display = ('username','groupname', 'priority')


    '''每页显示条目数'''
    list_per_page = 20
    search_fields = ['groupname', 'username']

    '''设置过滤选项'''
    list_filter = ('groupname','username')

class RadacctAdmin(admin.ModelAdmin):

    '''设置列表可显示的字段'''
    list_display = ('radacctid','acctsessionid','acctuniqueid','username','groupname','realm','nasipaddress','nasportid','nasporttype','acctstarttime','acctupdatetime','acctstoptime','acctinterval','acctsessiontime','acctauthentic','connectinfo_start','connectinfo_stop','acctinputoctets','acctoutputoctets','calledstationid','callingstationid','acctterminatecause','servicetype','framedprotocol','framedipaddress')


    '''每页显示条目数'''
    list_per_page = 10
    search_fields = ['groupname', 'username']

class RadpostauthAdmin(admin.ModelAdmin):

    '''设置列表可显示的字段'''
    list_display = ('username','pass_field','reply','authdate')

    '''每页显示条目数'''
    list_per_page = 10
    search_fields = ['username','pass_field']

    '''设置过滤选项'''
    list_filter = ('reply',)


# Register your models here.
admin.site.register(models.User,UserAdmin)
admin.site.register(models.ConfirmString,ConfirmStringAdmin)
admin.site.register(models.Radcheck,RadcheckAdmin)
admin.site.register(models.Radgroupreply,RadgroupreplyAdmin)
admin.site.register(models.Radusergroup,RadusergroupAdmin)
admin.site.register(models.Radacct,RadacctAdmin)
admin.site.register(models.Radpostauth,RadpostauthAdmin)
