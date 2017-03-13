/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var nav = document.getElementById('moz-universal-nav');
    var page = document.getElementsByTagName('html')[0];

    function cutsTheMustard() {
        return 'querySelector' in document &&
               'querySelectorAll' in document &&
               'addEventListener' in window;
    }

    function toggleFlyOutMenu() {
        page.classList.toggle('moz-nav-open');
    }

    function toggleSecondaryMenuItem(id) {
        var link = document.querySelector('.nav-menu-primary-links > li > .summary > a[data-id="'+ id +'"]');
        var heading = link.parentNode;

        if (link && heading && heading.classList.contains('summary')) {
            link.focus();

            if (!heading.classList.contains('selected')) {
                closeSecondaryMenuItems();
            }

            heading.classList.toggle('selected');
        }
    }

    function closeSecondaryMenuItems() {
        var menuLinks = document.querySelectorAll('.nav-menu-primary-links > li > .summary');

        for (var i = 0; i < menuLinks.length; i++) {
            menuLinks[i].classList.remove('selected');
        }
    }

    function handleMenuLinkClick(e) {
        e.preventDefault();
        var target = e.target.getAttribute('data-id');

        if (target) {
            toggleSecondaryMenuItem(target);
        }
    }

    function handleNavLinkClick(e) {
        e.preventDefault();

        var target = e.target.getAttribute('data-id');

        if (target) {
            toggleSecondaryMenuItem(target);

            if (!page.classList.toggle('moz-nav-open')) {
                toggleFlyOutMenu();
            }
        }
    }

    function bindEvents() {
        var menuLinks = document.querySelectorAll('.nav-menu-primary-links > li > .summary > a');

        for (var i = 0; i < menuLinks.length; i++) {
            menuLinks[i].addEventListener('click', handleMenuLinkClick, false);
        }

        var navLinks = document.querySelectorAll('.nav-primary-links > li > a');

        for (var j = 0; j < navLinks.length; j++) {
            navLinks[j].addEventListener('click', handleNavLinkClick, false);
        }

        var closeButton = document.getElementById('nav-flyout-close-button');
        closeButton.addEventListener('click', toggleFlyOutMenu, false);
    }

    if (nav && cutsTheMustard()) {
        var menuButton = document.getElementById('nav-button-more');

        // Show the secondary menu button
        menuButton.classList.remove('hidden');
        menuButton.addEventListener('click', toggleFlyOutMenu, false);

        bindEvents();
    }
})();
