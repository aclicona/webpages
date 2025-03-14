from django.conf import settings
from django.contrib.sites.models import Site


def append_site():
    sites = settings.SITES
    for site in sites:
        try:
            site_ = Site.objects.get(pk=site['pk'])
            site_.name = site['name']
            site_.domain = site['domain']
            site_.save()
        except Site.DoesNotExist:
            Site.objects.create(name=site['name'], domain=site['domain'])
        except:
            pass
