import swapper
from django.db import models
from netaddr import IPNetwork


class AbstractSection(TimeStampedEditableModel):
    """
    An abstract base class which contains
    """
    name = models.CharField(verbose_name=_('name'),
                            max_length=64)
    description = models.TextField(verbose_name=_('description'))

    class Meta:
        abstract = True

class AbstractSubnet(TimeStampedEditableModel):
    """
    An abstract base class which contains all the subnet details
    """
    name = models.CharField(verbose_name=_('name')
                            max_length=64)
    details = models.CharField(verbose_name=_('details'),
                               max_length=64)
    subnet = models.ForeignKey(swapper.get_model_name('django_ipam','Subnet'),
                               null=True)
    section = models.ForeignKey(swapper.get_model_name('django_ipam',
                                                       'Section'))
    description = models.TextField(verbose_name=_('description'))
    gateway = models.GenericIPAddressField()

    @property
    def subnet_usage(self):
        total_addresses = IPNetwork(self.details).size
        ip_model = swapper.load_model('django_ipam', 'IPAddress')
        used = ip_model.objects.filter(subnet=self, ip_status='used').count()
        free = total_addresses - used
        return "free: {0}, used: {1}, total: {2}".format(free, used, total_addresses)
    
    class Meta:
        abstract = True


class AbstractIPAddress(TimeStampedEditableModel):
    """
    An abstract base class model that provides various details for
    IPAddress management
    """
    ip_address = models.GenericIPAddressField()
    description = models.TextField(null=True, blank=True)
    section = models.ForeignKey(swapper.get_model_name('django_ipam',
                                                       'Section'))
    subnet = models.Foreignkey(swapper.get_model_name('django_ipam',
                                                      'Subnet'))
    ip_status = models.CharField(choices=(('used', 'used'),
                                          ('free', 'free')))
    gateway = models.GenericIPAddressField()
    hostname = models.CharField(verbose_name=_('hostname'),
                                max_length=255)
    netmask = models.GenericIPAddressField()

    class Meta:
        abstract = True
