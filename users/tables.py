import django_tables2 as tables
from .models import Radpostauth,Radacct
class AuthLogTable(tables.Table):
    class Meta:
        model = Radpostauth
        template_name = 'django_tables2/table.html'
        fields = ('username','reply','authdate')
        attrs = {'class': 'paleblue'}

class AccLogTable(tables.Table):
    class Meta:
        model = Radacct
        template_name = 'django_tables2/table.html'
        fields = ('username','acctsessiontime','connectinfo_start','acctinputoctets','acctoutputoctets','acctterminatecause','framedipaddress')
        attrs = {'class': 'paleblue'}