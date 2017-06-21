/**
 * API of a contract.
 * @module _
 * @author Mate It Right
 */

'use strict';
declare var require: any
declare var Buffer: any
declare var __dirname: any
var Web3 = require('web3');
var exec = require('child_process').exec;
var fs = require('fs');
var utils = require('./utils');
export var web3;
var config;

/**
 * Sets up the mailer before use.
 * @function managerInit
 * @public
 * @param {Object} c Config.
 */
export function managerInit(c: any) {
    config = c;
    web3 = new Web3(new Web3.providers.HttpProvider(config.web3));
}

/**
 * Transforms an input.
 * @function transform
 * @param {Object} arg To transform.
 * @param {String} method Method.
 * @return {Object} Result.
 */
export function transform(arg: any, method: string) {
    switch(method) {
        case 'number':
            return Number(arg);
        case 'none':
            return arg;
        case 'string':
            return web3.toAscii(arg);
        case 'date_number':
            return new Date(Number(arg)).toLocaleString();
        case 'iso_date_number':
            return new Date(Number(arg)).toISOString().split('T')[0]
    }
}

/**
 * Forges the response to create an account.
 * @function createAccount
 * @public
 * @param {Request} req The request.
 * @param {Response} res The response.
 */
export function createAccount(req, res) {
    if(config.web3.indexOf('localhost') < 0) {
        res.type('application/json').status(600).json({error: utils.i18n('external.down', req)});
        return;
    }
    var rnd = utils.generateRandomString(12);
    fs.writeFileSync('/tmp/' + rnd, (req.body.password || config.default_password) + '\n')
    exec(`
        geth --datadir ` + config.chain_path + ` account new --password /tmp/` + rnd + `
    `, function(err, stdout, stderr) {
        fs.unlink('/tmp/' + rnd);
        var address = /.*{(.*)}.*/.exec(stdout);
        if(address)
            res.type('application/json').status(200).json({address: address[1]});
        else
            res.type('application/json').status(500).json({error: utils.i18n('internal.db', req)});
    });
}
