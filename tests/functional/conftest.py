# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

VIEWPORT = {
    'desktop': {'width': 1280, 'height': 1024},
    'mobile': {'width': 320, 'height': 480}}


@pytest.fixture
def capabilities(request, capabilities):
    driver = request.config.getoption('driver')
    if capabilities.get('browserName', driver).lower() == 'firefox':
        capabilities['marionette'] = True
    return capabilities


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.log.level = 'trace'
    return firefox_options


# @pytest.fixture
# def firefox_profile(firefox_profile):
#     firefox_profile.set_preference('browser.tabs.remote.autostart', False)
#     firefox_profile.set_preference('browser.tabs.remote.autostart.2', False)
#     firefox_profile.set_preference('browser.tabs.remote.force-enable', False)
#     return firefox_profile


@pytest.fixture(scope='session')
def session_capabilities(session_capabilities):
    session_capabilities.setdefault('tags', []).append('bedrock')
    return session_capabilities


@pytest.fixture
def firefox(selenium):
    return selenium.capabilities.get('browserName').lower() == 'firefox'


@pytest.fixture
def internet_explorer(selenium):
    return selenium.capabilities.get('browserName').lower() == 'internet explorer'


@pytest.fixture(autouse=True)
def filter_capabilities(request):
    marker = None
    if request.node.get_marker('skip_if_firefox') and request.getfuncargvalue('firefox'):
        marker = request.node.get_marker('skip_if_firefox')
    if request.node.get_marker('skip_if_not_firefox') and not request.getfuncargvalue('firefox'):
        marker = request.node.get_marker('skip_if_not_firefox')
    if request.node.get_marker('skip_if_internet_explorer') and request.getfuncargvalue('internet_explorer'):
        marker = request.node.get_marker('skip_if_internet_explorer')

    if marker:
        reason = marker.kwargs.get('reason') or marker.name
        pytest.skip(reason)


@pytest.fixture
def selenium(request, selenium):
    viewport = VIEWPORT['desktop']
    if request.keywords.get('viewport') is not None:
        viewport = VIEWPORT[request.keywords.get('viewport').args[0]]
    selenium.set_window_size(viewport['width'], viewport['height'])
    return selenium
