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
var utils = require('./utils');
var config, web3;

/**
 * Sets up the mailer before use.
 * @function managerInit
 * @public
 * @param {Object} c Config.
 */
export function managerInit(c: any) {
    config = c;
    web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));
}

/**
 * Forges the response to create an account.
 * @function createAccount
 * @public
 * @param {Request} req The request.
 * @param {Response} res The response.
 */
export function createAccount(req, res) {

}
