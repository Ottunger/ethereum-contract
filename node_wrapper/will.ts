/**
 * API of a contract.
 * @module _
 * @author Mate It Right
 */

'use strict';
declare var require: any
declare var Buffer: any
declare var __dirname: any
var utils = require('./utils');
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
