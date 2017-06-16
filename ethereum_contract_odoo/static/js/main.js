odoo.define('ethereum_contract_odoo', function(require) {
    "use strict";

    var base = require('web_editor.base');
    var ajax = require('web.ajax');
    var utils = require('web.utils');
    var core = require('web.core');
    var _t = core._t;

    var contract = window.contract; //truffle-contract
    var web3 = window.web3; //web3

    function fetchJSONFile(path, callback) {
        var httpRequest = new XMLHttpRequest();
        httpRequest.onreadystatechange = function() {
            if(httpRequest.readyState === 4) {
                if(httpRequest.status === 200) {
                    var data = JSON.parse(httpRequest.responseText);
                    if(callback) callback(data);
                }
            }
        };
        httpRequest.open('GET', path);
        httpRequest.send();
    }

    fetchJSONFile('/ethereum_contract_odoo/static/json/Will.json', function(will_artifact) {
        var Will = contract(will_artifact);
        Will.setProvider(web3.currentProvider);

        Will.deployed().then()
    });

});