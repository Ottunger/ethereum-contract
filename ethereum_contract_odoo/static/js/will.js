odoo.define('ethereum_contract_odoo', function(require) {
    "use strict";

    var base = require('web_editor.base');
    var ajax = require('web.ajax');
    var utils = require('web.utils');
    var core = require('web.core');
    var _t = core._t;

    for(var i = 0; i < odoo.ethereum_contracts_types.length; i++) {
        if(odoo.ethereum_contracts_types[i] != 'will')
            continue;
        ajax.jsonRpc('/will/get', 'call', {
            instance_id: parseInt(odoo.ethereum_contracts_ids[i])
        }).then(function(data) {
            $('#wills_body').append(data.html);
            if(data.signing) {
                //Can sign
                $('.' + data.classname).on('click', function() {
                    ajax.jsonRpc('/will/sign', 'call', {
                        instance_id: parseInt($(this).attr('data-id'))
                    }).then(function(data) {
                        window.location.reload();
                    });
                    $(this).attr('disabled', 'disabled');
                    setTimeout(function() {$(this).attr('disabled', false);}.bind(this), 500);
                });
            } else {
                //Can propose
                $('.' + data.classname).on('click', function() {
                    $tr = $(this).closest('tr');
                    ajax.jsonRpc('/will/propose', 'call', {
                        instance_id: parseInt($(this).attr('data-id')),
                        arg_array: [
                            new Date($tr.find('input')[0].val()).getTime(),
                            new Date($tr.find('input')[1].val()).getTime(),
                            parseInt($tr.find('input')[2].val()),
                            parseInt($tr.find('input')[3].val())
                            //Controller will append from account
                        ]
                    }).then(function(data) {
                        window.location.reload();
                    });
                    $(this).attr('disabled', 'disabled');
                    setTimeout(function() {$(this).attr('disabled', false);}.bind(this), 500);
                });
            }
        });
    }

    $('#creator_btn').on('click', function() {
        if(odoo.ethereum_types.indexOf('will') < 0) {
            alert($('#error_len').text());
            return;
        }
        ajax.jsonRpc('/will/new', 'call', {
            arg_array: [
                true,
                $('#subject').val(),
                0,
                []
                //Controller will append from account
            ],
            arg_array_2: [
                new Date($('#from_date').val()).getTime(),
                new Date($('#end_date').val()).getTime(),
                parseInt($('#amt_hour').val()),
                parseInt($('#hour_week').val())
                //Controller will append from account
            ]
        }).then(function(data) {
            window.location.reload();
        });
        $(this).attr('disabled', 'disabled');
        setTimeout(function() {$(this).attr('disabled', false);}.bind(this), 500);
    });

});