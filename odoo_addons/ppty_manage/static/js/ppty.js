odoo.define('ppty_manage_odoo', function(require) {
    "use strict";

    var base = require('web_editor.base');
    var ajax = require('web.ajax');
    var utils = require('web.utils');
    var core = require('web.core');
    var _t = core._t;

    //Only if snippet is here
    if(!$('.snippet_app_ppty'))
        return;

    // Google maps Javascript is loaded when document id ready, to avoid timing problems
    if (odoo.google_maps_api_key) {
        odoo.ajax = ajax;

        var google_maps_script = document.createElement('script');
        google_maps_script.setAttribute('src','https://maps.googleapis.com/maps/api/js?libraries=places&callback=initGmap&key=' + odoo.google_maps_api_key);
        google_maps_script.setAttribute('async','async');
        google_maps_script.setAttribute('defer','defer');
        document.head.appendChild(google_maps_script);
    }

});

// Initialize to google maps autocomplete input
function initGmap() {
    var map = new google.maps.Map(document.getElementById('gmap'), {
        zoom: 11,
        center: {lat: 50.51, lng: 4.20}
    }), mk;
    var bouncing = false;
    map.addListener('bounds_changed', function() {
        if(!bouncing) {
            setTimeout(function() {
                bouncing = false;
                loadPoints(map, mk).then(function(nmk) { mk = nmk; });
            }, 1000);
        }
        bouncing = true;
    })
    setTimeout(function() {
        loadPoints(map, mk).then(function(nmk) { mk = nmk; });
    }, 1000);
}

function loadPoints(map, mk) {
    if(mk)
        mk.setMap(null);

    return new Promise(function(resolve) {
        var bounds = map.getBounds();
        odoo.ajax.jsonRpc('/map/get', 'call', {
            point_from: [bounds.getNorthEast().lat(), bounds.getNorthEast().lng()],
            point_to: [bounds.getSouthWest().lat(), bounds.getSouthWest().lng()]
        }, function(points) {
            var markers = points.map(function(point, i) {
                var marker = new google.maps.Marker({
                    position: point.location,
                    label: point.label
                });
                if(marker.odoo_id) {
                    marker.addListener('click', function() {
                        window.open('/web#return_label=Website&model=casalta.belonging&id=' + marker.odoo_id + '&view_type=form', '_blank');
                    });
                }
            });
            resolve(new MarkerClusterer(map, markers, {imagePath: '/ppty_manage/static/images/m'}));
        });
    });
}
