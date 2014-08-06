# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mock import patch

from bedrock.mozorg.tests import TestCase
from bedrock.security.models import ProductVersion
from bedrock.security.views import ProductView, ProductVersionView
from product_details.version_compare import Version


class TestViews(TestCase):
    def setUp(self):
        pvnames = [
            'Firefox 3.6',
            'Firefox 4.0',
            'Firefox 4.0.1',
            'Firefox 4.2',
            'Firefox 4.2.3',
            'Firefox 24.0',
        ]
        self.pvs = [ProductVersion.objects.create(name=pv) for pv in pvnames]

    def test_product_view_min_version(self):
        """Should not include versions below minimum."""
        pview = ProductView()
        pview.kwargs = {'slug': 'firefox'}
        with patch.dict(pview.minimum_versions, {'firefox': Version('4.2')}):
            self.assertListEqual(pview.get_queryset(),
                                 [self.pvs[5], self.pvs[4], self.pvs[3]])

        with patch.dict(pview.minimum_versions, {'firefox': Version('22.0')}):
            self.assertListEqual(pview.get_queryset(), [self.pvs[5]])

    def test_product_version_view_filter_major(self):
        """Given a major version should return all minor versions."""
        pview = ProductVersionView()
        pview.kwargs = {'slug': 'firefox-4'}
        self.assertListEqual(pview.get_queryset(),
                             [self.pvs[4], self.pvs[3], self.pvs[2], self.pvs[1]])

    def test_product_version_view_filter_minor(self):
        """Given a minor version should return all point versions."""
        pview = ProductVersionView()
        pview.kwargs = {'slug': 'firefox-4.2'}
        self.assertListEqual(pview.get_queryset(), [self.pvs[4], self.pvs[3]])
