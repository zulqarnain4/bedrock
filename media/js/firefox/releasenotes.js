/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla, Waypoint) {
    'use strict';

    var $nav = $('#nav');

    $(window).scroll(function(){ // scroll event  

        var stickyNav = new Waypoint.Sticky({
            element: $nav,
            handler: function(direction){
                if(direction == 'down'){
                    $nav.addClass('fixedNav');
                } else{
                    $nav.removeClass('fixedNav');
                }
            }
        });
 
    });

})(window.jQuery, window.Mozilla, window.Waypoint);
