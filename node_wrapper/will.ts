/**
 * API of a contract.
 * @module _
 * @author Mate It Right
 */

'use strict';
declare var require: any
declare var Buffer: any
declare var __dirname: any
var TC = require('truffle-contract');
var utils = require('./utils');
var all = require('./all');
var config;

/**
 * Sets up the mailer before use.
 * @function managerInit
 * @public
 * @param {Object} c Config.
 */
export function managerInit(c: any) {
    config = c;
}
/**
 * Executor on will.
 * @function executor
 * @public
 * @param {Request} req The request.
 * @param {Response} res The response.
 */
export function executor(req, res) {
    var will = TC(req.contract);
    will.setProvider(all.web3.currentProvider);
    will.at(req.contract_address).then(function(instance) {
        instance[req.method](...req.arg_array).then(function(response) {
            res.type('application/json').status(200).json(response.map(function(arg, index) {
                all.transform(arg, req.transform[index]);
            }));
        }, function(error) {
            res.type('application/json').status(600).json(error);
        });

        /* Pool of followed
        instance.onSigned({}, {fromBlock: 0, toBlock: 'latest'}).watch(function(err, event) {
            alert(event);
        });
        */
    }, function(error) {
        res.type('application/json').status(600).json(error);
    });
}

