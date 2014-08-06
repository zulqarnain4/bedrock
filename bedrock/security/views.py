# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db.models import Q
from django.views.generic import DetailView, ListView, RedirectView

from funfactory.urlresolvers import reverse
from product_details.version_compare import Version

from bedrock.security.models import ProductVersion, SecurityAdvisory


class AdvisoriesView(ListView):
    template_name = 'security/advisories.html'
    queryset = SecurityAdvisory.objects.only('id', 'impact', 'title', 'announced')
    context_object_name = 'advisories'


class AdvisoryView(DetailView):
    model = SecurityAdvisory
    template_name = 'security/advisory.html'
    context_object_name = 'advisory'


class ProductView(ListView):
    template_name = 'security/product-advisories.html'
    context_object_name = 'product_versions'
    allow_empty = False
    minimum_versions = {
        'firefox': Version('4.0'),
        'thunderbird': Version('6.0'),
        'seamonkey': Version('2.3'),
    }

    def get_queryset(self):
        product_slug = self.kwargs.get('slug')
        versions = ProductVersion.objects.filter(product_slug=product_slug)
        min_version = self.minimum_versions.get(product_slug)
        if min_version:
            versions = [vers for vers in versions if vers.version >= min_version]
        return sorted(versions, reverse=True)


class ProductVersionView(ListView):
    template_name = 'security/product-advisories.html'
    context_object_name = 'product_versions'
    allow_empty = False

    def get_queryset(self):
        slug = self.kwargs['slug']
        qfilter = Q(slug__startswith=slug + '.')
        dots = slug.count('.')
        if dots == 1:
            # minor version. add exact match.
            qfilter |= Q(slug__exact=slug)
        versions = ProductVersion.objects.filter(qfilter)
        return sorted(versions, reverse=True)


class OldAdvisoriesView(RedirectView):
    def get_redirect_url(self, **kwargs):
        return reverse('security.advisory', kwargs=kwargs)
