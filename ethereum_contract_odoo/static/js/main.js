odoo.define('ethereum_contract_odoo', function(require) {
    "use strict";

    var base = require('web_editor.base');
    var ajax = require('web.ajax');
    var utils = require('web.utils');
    var core = require('web.core');
    var _t = core._t;

    var contract = window.TruffleContract; //truffle-contract
    var Web3 = window.Web3; //web3
    var account;
    var wills = [];

    /*
    if(typeof web3 != 'undefined') {
        console.warn('Using web3 detected from external source. If you find that your accounts don\'t appear or you have 0 MetaCoin, ensure you\'ve configured that source properly. If using MetaMask, see the following link. Feel free to delete this warning. :) http://truffleframework.com/tutorials/truffle-and-metamask');
        window.web3 = new Web3(web3.currentProvider);
    }
    if(typeof web3 == 'undefined') {
        console.warn('No web3 detected. Falling back to http://localhost:8545. You should remove this fallback when you deploy live, as it\'s inherently insecure. Consider switching to Metamask for development. More info here: http://truffleframework.com/tutorials/truffle-and-metamask');
        window.web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));
    }
    */
    window.web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));
    web3.eth.getCoinbase(function (err, data) {
        if(err == null) {
            account = data;
            odoo.eth_account = data;
        }
    });

    for(var i = 0; i < odoo.ethereum_contracts_json.length; i++) {
        wills.push(contract(JSON.parse(odoo.ethereum_contracts_json[i])));
    }
    for(var i = 0; i < wills.length; i++) {
        wills[i].setProvider(web3.currentProvider);
        var addrs = odoo.ethereum_contracts_addr[i].split(',');
        for(var j = 0; j < addrs.length ; j++) {
            wills[i].at(addrs[j]).then(function(instance) {
                instance.getAllInfo().then(function(info) {
                    var $button = '';
                    info = formatInfo(info);
                    if(info[10]) {
                        //Can sign
                        $button = '<button class="btn" id="' + instance.address + '">Sign</button>';
                    } else {
                        //Can propose
                        $button = '<button class="btn" id="' + instance.address + '">Propose</button>';
                    }
                    $('#wills_body').append('<tr><td>' + info[8] + '</td><td>' + info[9] + '</td>'
                        + '<td>' + new Date(info[0]).toLocaleString() +  '</td><td>' + new Date(info[1]).toLocaleString() +  '</td>'
                        + '<td>' + info[2] +  '</td><td>' + info[3] +  '</td></tr>')
                    $('#wills_body').append('<tr><td>Last offer: ' + new Date(info[11]).toLocaleString() + '</td><td>Mode: ' + $button + '</td>'
                        + '<td><input type="date" value="' + new Date(info[4]).toISOString().split('T')[0] +  '"/></td>'
                        + '<td><input type="date" value="' + new Date(info[5]).toISOString().split('T')[0] +  '"/></td>'
                        + '<td><input type="number" min="0" value="' + info[6] +  '"/></td>'
                        + '<td><input type="number" min="0" value="' + info[7] +  '"/></td></tr>')
                    if(info[10]) {
                        //Can sign
                        $('#' + instance.address).on('click', function() {
                            instance.sign({from: account, gas: 500000});
                            $(this).remove();
                        });
                    } else {
                        //Can propose
                        $('#' + instance.address).on('click', function() {
                            $tr = $(this).closest('tr');
                            instance.propose(
                                new Date($tr.find('input')[0].val()).getTime(),
                                new Date($tr.find('input')[1].val()).getTime(),
                                $tr.find('input')[2].val(),
                                $tr.find('input')[3].val(),
                                {from: account, gas: 500000});
                            $(this).remove();
                        });
                    }
                });
                instance.onSigned({}, {fromBlock: 0, toBlock: 'latest'}).watch(function(err, event) {
                    alert(event);
                });
            });
        }
    }

    $('#creator_btn').on('click', function() {
        if(wills.length == 0) {
            alert($('#error_len').text());
            return;
        }
        wills[0].new(true, $('#subject').val(), $('#ong').val(), new Date($('#from_date')).getTime(),
                new Date($('#end_date').val()).getTime(), $('#amt_hour').val(), $('#hour_week').val(),
                0, [], {from: account, gas: 20000000}).then(function(instance) {
            ajax.jsonRpc('/will/new', 'call', {
                id: parseInt(odoo.ethereum_contracts_id[0]),
                address: instance.address
            }).then(function(data) {
                window.location.reload();
            });
        });
    });

    function formatInfo(info) {
        //Use web3.toAscii for strings
        return [
            Number(info[0]),
            Number(info[1]),
            Number(info[2]),
            Number(info[3]),
            Number(info[4]),
            Number(info[5]),
            Number(info[6]),
            Number(info[7]),
            info[8],
            info[9],
            info[10],
            Number(info[11])
        ];
    }

});