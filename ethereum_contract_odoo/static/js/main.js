odoo.define('ethereum_contract_odoo', function(require) {
    "use strict";

    var base = require('web_editor.base');
    var ajax = require('web.ajax');
    var utils = require('web.utils');
    var core = require('web.core');
    var _t = core._t;

    var contract = window.contract; //truffle-contract
    var Web3 = window.Web3; //web3
    var account;
    var wills = [];

    if(typeof web3 !== 'undefined') {
        console.warn('Using web3 detected from external source. If you find that your accounts don\'t appear or you have 0 MetaCoin, ensure you\'ve configured that source properly. If using MetaMask, see the following link. Feel free to delete this warning. :) http://truffleframework.com/tutorials/truffle-and-metamask');
        // Use Mist/MetaMask's provider
        window.web3 = new Web3(web3.currentProvider);
    } else {
        console.warn('No web3 detected. Falling back to http://localhost:8545. You should remove this fallback when you deploy live, as it\'s inherently insecure. Consider switching to Metamask for development. More info here: http://truffleframework.com/tutorials/truffle-and-metamask');
        // fallback - use your fallback strategy (local node / hosted node + in-dapp id mgmt / fail)
        window.web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));
    }
    web3.eth.getCoinbase(function (err, data) {
        if(err == null) {
            account = data;
        }
    });

    for(var i = 0; i < odoo.ethereum_contracts_json.length; i++) {
        wills.append(contract(JSON.parse(odoo.ethereum_contracts_json[i])));
    }
    for(var i = 0; i < wills.length; i++) {
        wills[i].setProvider(web3.currentProvider);
        wills[i].deployed().then(function(instance) {
            instance.getAllInfo().then(function(info) { //Array(...)
                $button = '';
                if(info[10]) {
                    //Can sign
                    $button = '<button id="' + instance.address + '">Sign</button>';
                } else {
                    //Can propose
                    $button = '<button id="' + instance.address + '">Propose</button>';
                }
                $('.wills_body').append('<tr><td>' + info[8] + '</td><td>' + info[9] + '</td>'
                    + '<td>' + info[0] +  '</td><td>' + info[1] +  '</td><td>' + info[2] +  '</td><td>' + info[3] +  '</td></tr>')
                $('.wills_body').append('<tr><td>' + new Date(info[11]).toLocaleString() + '</td><td>' + $button + '</td>'
                    + '<td><input type="date" value="' + new Date(info[4]).toISOString().split('T')[0] +  '"/></td>'
                    + '<td><input type="date" value="' + new Date(info[5]).toISOString().split('T')[0] +  '"/></td>'
                    + '<td><input type="number" min="0" value="' + info[6] +  '"/></td>'
                    + '<td><input type="number" min="0" value="' + info[7] +  '"/></td></tr>')
                if(info[10]) {
                    //Can sign
                    $('#' + instance.address).on('click', function() {
                        instance.sign({from: account, gas: 500000});
                    });
                } else {
                    //Can propose
                    $('#' + instance.address).on('click', function() {
                        instance.propose({from: account, gas: 500000});
                    });
                }
            });
            instance.onSigned({}, {fromBlock: 0; toBlock: 'latest'}).watch(function(err, event) {
                alert(event);
            });
        });
    }

});