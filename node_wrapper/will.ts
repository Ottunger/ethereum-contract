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
 * Creator on will.
 * @function creator
 * @public
 * @param {Request} req The request.
 * @param {Response} res The response.
 */
export function creator(req, res) {
    var will = TC(req.body.contract);
    will.setProvider(all.web3.currentProvider);
    will.new(req.body.arg_array[req.body.arg_array.length - 1]).then(function(response) {
        response.construct(...req.body.arg_array).then(function() {
            res.type('application/json').status(200).json({
                address: response.address,
                transactionHash: response.transactionHash
            });
            //Do one more task?
            if(!req.body.arg_array_2 || !req.body.method)
                return;
            req.body.arg_array = req.body.arg_array_2;
            req.body.contract_address = response.address;
            executor(req, undefined);
        }, function(error) {
            res.type('application/json').status(600).json(error);
        });
    }, function(error) {
        res.type('application/json').status(600).json(error);
    });
}

/**
 * Executor on will.
 * @function executor
 * @public
 * @param {Request} req The request.
 * @param {Response} res The response.
 */
export function executor(req, res) {
    var will = TC(req.body.contract);
    will.setProvider(all.web3.currentProvider);
    will.at(req.body.contract_address).then(function(instance) {
        instance[req.body.method](...req.body.arg_array).then(function(response) {
            if(!res)
                return;
            res.type('application/json').status(200).json(response.tx?
                {transactionHash : response.tx} : response.map(function(arg, index) {
                    return all.transform(arg, req.body.transform[index]);
            }));
        }, function(error) {
            if(!res)
                return;
            res.type('application/json').status(600).json(error);
        });

        /* Pool of followed
        instance.onSigned({}, {fromBlock: 0, toBlock: 'latest'}).watch(function(err, event) {
            alert(event);
        });
        */
    }, function(error) {
        if(!res)
            return;
        res.type('application/json').status(600).json(error);
    });
}
