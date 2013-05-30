// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

;(function($) {
    'use strict';

    var $tabZilla = $('#tabzilla');
    var $outerWrapper = $('#outer-wrapper');
    var tabZillaOpened = false;

    $tabZilla.on('mouseover focus', function () {
        $outerWrapper.addClass('highlight');
        $(this).addClass('highlight');
    });

    $tabZilla.on('mouseout blur', function () {
        if (!tabZillaOpened) {
            $outerWrapper.removeClass('highlight');
            $(this).removeClass('highlight');
        }
    });

    //preserve tabzilla opacity state on open/close
    $tabZilla.on('click', function () {
        tabZillaOpened = !tabZillaOpened;
        if (tabZillaOpened) {
            $outerWrapper.addClass('highlight');
            $(this).addClass('highlight');
        } else {
            $outerWrapper.removeClass('highlight');
            $(this).removeClass('highlight');
        }
    });

    /*
     * Set geolocation specific page information
     * Shows the correct partner logo (if applicable)
     * Then auto selects country field in newsletter form
     */
    function configGeoLocation() {
        var COUNTRY_CODE = '';
        var DICT = {
            'pl': 'T-Mobile',
            'co': 'Movistar',
            've': 'Movistar',
            'es': 'Movistar'
        };

        try {
            //http://geo.mozilla.org/country.js
            COUNTRY_CODE = geoip_country_code().toLowerCase();
        } catch (e) {
            COUNTRY_CODE = "";
        }

        //add cc class to coming soon section
        $('.coming-soon').addClass(COUNTRY_CODE);

        //set the correct partner logo text
        if (DICT[COUNTRY_CODE]) {
            $('.partner-logo').text(DICT[COUNTRY_CODE]);
        }

        //auto select country option based on cc
        $('#id_country option[value="' + COUNTRY_CODE + '"]').attr('selected', 'selected');

        //auto select lang option based on cc
        $('#id_lang option[value="' + COUNTRY_CODE + '"]').attr('selected', 'selected');
    }

    //reallly primative validation e.g a@a
    //matches built-in validation in Firefox
    function validateEmail(elementValue) {
        var emailPattern = /\S+@\S+/;
        return emailPattern.test(elementValue);
    }

    function validateForm() {
        var $form = $('#footer-email-form');
        var email = $form.find('#id_email').val();
        var $privacy = $form.find('#id_privacy');

        if ('checkValidity' in $form) {
            //do native form validation
            return $form.checkValidity();
        }
        return validateEmail(email) && $privacy.is(':checked');
    }

    $('#footer_email_submit').on('click', function (e) {
        // if form is valid, delay submission to wait for GA tracking
        if (validateForm()) {

            e.preventDefault();

            if (_gaq) {
                _gaq.push(['_trackEvent', 'Newsletter Registrations', 'click', 'Firefox OS Teaser Registration']);
            }

            //delay form submission so GA has time to kick in
            setTimeout(function() {
                $('#footer-email-form').submit();
            }, 500);
        }
    });

    $script('//geo.mozilla.org/country.js', function() {
        configGeoLocation();
    });

})(jQuery);
