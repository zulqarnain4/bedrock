/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function (Mozilla) {
    'use strict';

    var syncTimeout = setTimeout(showMobilePromo, 1500); // fallback for if UITour should fail.

    function showAccountsForm() {
        document.querySelector('.main-content').classList.add('signed-out');

        Mozilla.Client.getFirefoxDetails(function(data) {
            Mozilla.FxaIframe.init({
                distribution: data.distribution,
                gaEventName: 'whatsnew-fxa'
            });
        });
    }

    function showMobilePromo() {
        document.querySelector('.main-content').classList.add('signed-in');
    }

    Mozilla.UITour.getConfiguration('sync', function(config) {
        clearTimeout(syncTimeout); // clear UITour fallback timeout.

        if (config.setup) {
            showMobilePromo();
        } else {
            showAccountsForm();
        }
    });

})(window.Mozilla);
