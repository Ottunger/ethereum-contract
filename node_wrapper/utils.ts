/**
 * API to have utilities.
 * @module utils
 * @author Mathonet Grégoire
 */

'use strict';
declare var require: any
declare var Buffer: any
declare var __dirname: any
var fs = require('fs');
var path = require('path');
var querystring = require('querystring');
var https = require('https');
var hash = require('js-sha256');
var pki = require('node-forge').pki;
var RL = require('limiter').RateLimiter;
var constants = require('constants');
export var strings = {
    en: require('./i18n/en.json'),
    fr: require('./i18n/fr.json')
};
export var DEBUG = true;
var rl;

/**
 * Prepare the rate limiting.
 * @function prepareRL
 * @public
 */
export function prepareRL() {
    rl = new RL(30 * 1024 * 1024, 'second', true);
}

/**
 * Verifies that the client has generated an OK solution. Anyways, generate a new challenge.
 * @function checkPuzzle
 * @public
 * @param {Request} req The request.
 * @param {Response} res The response.
 * @param {Function} next Handler middleware.
 */
export function checkPuzzle(req, res, next) {
    if(!('puzzle' in req.query)) {
        req.user.puzzle = generateRandomString(16);
        req.user.persist();
        res.type('application/json').status(412).json({error: i18n('client.puzzle', req), puzzle: req.user.puzzle});
    } else {
        var complete = hash.sha256(req.user.puzzle + req.query.puzzle);
        if(complete.charAt(0) == '0' && complete.charAt(1) == '0' && complete.charAt(2) == '0') {
            req.user.puzzle = generateRandomString(16);
            req.user.persist();
            rl.removeTokens(((req.user._id.indexOf('wiuser') == 0)? 5 : 1) * req.bodylength, function(e, r) {
                if(r < 0) {
                    res.type('application/json').status(429).json({error: i18n('client.burst', req), puzzle: req.user.puzzle});
                } else {
                    next();
                }
            });
        } else {
            req.user.puzzle = generateRandomString(16);
            req.user.persist();
            res.type('application/json').status(412).json({error: i18n('client.puzzle', req), puzzle: req.user.puzzle});
        }
    }
}

/**
 * Creates a function suitable for use in express app that checks that the request has some fields in it.
 * @function checkBody
 * @public
 * @param {Array} arr The required top-level fields.
 * @return {Function} An express middleware.
 */
export function checkBody(arr: string[]): Function {
    return function(req, res, next) {
        if(!req.body) {
            res.type('application/json').status(400).json({puzzle: !!req.user? req.user.puzzle : null, error: i18n('client.missing', req)});
        } else {
            for(var i = 0; i < arr.length; i++) {
                if(!(arr[i] in req.body)) {
                    res.type('application/json').status(400).json({puzzle: !!req.user? req.user.puzzle : null, error: i18n('client.missing', req)});
                    return;
                }
            }
            next();
        }
    }
}

/**
 * Checks if a signature is OK.
 * @function eidSig
 * @public
 * @param {Object} load Payload.
 * @return {Boolean} If signature OK.
 */
export function eidSig(load: any): boolean {
    var signed = load['openid.signed'];
    if(!signed)
        return false;
    signed = signed.split(',');
    var check = {};
    for(var i = 0; i < signed.length; i++) {
        check[signed[i]] = load['openid.' + signed[i]];
    }
    check = querystring.stringify(check);

    var hmac = crypto.createHmac('sha256', '???');
    hmac.update(check);
    return hmac.digest('base64') == load['openid.sig'];
}

/**
 * Returns the decoded version of a string incoded as binary base64.
 * @function atob
 * @private
 * @param {String} str Encoded string.
 * @return {String} Decoded string.
 */
export function atob(str: string): string {
    return new Buffer(str, 'base64').toString('binary');
}

/**
 * Returns the encoded version of a string as binary base64.
 * @function btoa
 * @private
 * @param {String} str Decoded string.
 * @return {String} Encoded string.
 */
export function btoa(str: string): string {
    return new Buffer(str).toString('base64');
}

/**
 * Generates a random string.
 * @function generateRandomString
 * @public
 * @param {Number} length The length.
 * @param {Boolean} l Only letters.
 * @return {String} The string.
 */
export function generateRandomString(length: number, l?: boolean): string {
    var characters = (l !== false)? 'abcdefghijklmnopqrstuvwxyz' : '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    var randomString = '';
    for (var i = 0; i < length; i++) {
        randomString += characters[Math.floor(Math.random() * characters.length)];
    }
    return randomString;
}

/**
 * Generates a random ID.
 * @function genID
 * @public
 * @param {String} prefixes Forbidden prefixes.
 * @param {String} prefix A prefix
 * @return {String} The string.
 */
export function genID(prefixes: string[], prefix: string = ''): string {
    var more = 128 - prefix.length, newid = prefixes[0], can = false;
    if(more == 128) {
        while(!can) {
            can = true;
            for(var i = 0; i < prefixes.length; i++) {
                if(newid.indexOf(prefixes[i]) == 0) {
                    newid = generateRandomString(128);
                    can = false;
                    break;
                }
            }
        }
        return newid;
    } else
        return prefix + generateRandomString(more);
}

/**
 * Array forEach with callback if asynchronous.
 * @function loopOn
 * @public
 * @param {Array} array The array.
 * @param {Function} apply The function to apply to each element.
 * @param {Function} callin A function that runs as a callback to each asynchrnous "apply" call.
 * @param {Function} callback Global callback.
 */
export function loopOn(array: any[], apply: Function, callin: Function, callback: Function) {
    var ct = 0;
    array.forEach(function(item, i) {
        apply(item, function(a, b, c) {
            callin(item, a, b, c);
            ct++;
            if(ct == array.length)
                callback();
        });
    });
}

/**
 * Solves the server puzzle, then return a string for it.
 * @function regPuzzle
 * @private
 * @param {String} puzzle Challenge.
 * @return {String} Puzzle solution.
 */
export function regPuzzle(puzzle: string): string {
    var i = 0, complete;
    do {
        complete = hash.sha256(puzzle + i);
        i++;
    } while(complete.charAt(0) != '0' || complete.charAt(1) != '0' || complete.charAt(2) != '0');
    return '?puzzle=' + (i - 1);
}

/**
 * Tries to translate a string into the given language.
 * @function i18n
 * @public
 * @param {String} str The string to translate.
 * @param {Request} req The language as a IANA code.
 * @param {User} userin A user object whose lang should be used rather than ours.
 * @param {Object} more Dictionary to prefer to use before fallback dictionary.
 * @return {String} The translated string or itself if no match.
 */
export function i18n(str: string, req: any, userin?: any, more?: {[id: string]: {[id: string]: string}}) {
    userin = userin || req.user;
    var lang = (!!userin && !!userin.lang)? userin.lang : undefined;
    if(lang == undefined && !!req.get)
        lang = req.get('Accept-Language');
    if(lang == undefined)
        lang = 'en';
    else {
        lang = lang.trim().substring(0, 2);
        if(!(lang in strings))
            lang = 'en';
    }
    
    if(!!more && !!more[lang] && !!more[lang][str])
        return more[lang][str];
    else if(str in strings[lang])
        return strings[lang][str];
    return str;
}

/**
 * Parses a template.
 * @function parser
 * @public
 * @param {String} file File to load.
 * @param {Request} req For i18n.
 * @param {Object} context More context.
 * @param {User} userin For i18n.
 * @param {Boolean} html Already HTML.
 * @return {String} Parsed HTML.
 */
export function parser(file: string, req: any, context?: {[id: string]: any}, userin?: any, html?: boolean): string {
    var template: string = !!html? file : fs.readFileSync(file, 'utf8'), parsed = template;
    var rgx = /[{$]{2}\s*([^$}]*)\s*[$}]{2}/g;
    var match = rgx.exec(template);
    var shift = 0, by;
    while(match != null) {
        match[1] = match[1].trim();
        if(/^['"].*['"]$/.test(match[1]))
            by = i18n(match[1].substr(1, match[1].length - 2), req, userin, context['i18n']);
        else
            by = ('' + context[match[1]]) || '???';
        parsed = parsed.substr(0, match.index + shift) + by + parsed.substr(match.index + match[0].length + shift);
        shift += by.length - match[0].length;
        match = rgx.exec(template);
    }
    return parsed;
}

/**
 * Turns an array of nums to a string.
 * @function arr2str
 * @public
 * @param {Number[]} arr Array.
 * @return {String} String.
 */
export function arr2str(arr: number[]): string {
    var result = '';
    for (var i = 0; i < arr.length; i++) {
        result += String.fromCharCode(arr[i]);
    }
    return result;
}

/**
 * Turns a string to an array of numbers.
 * @function str2arr
 * @public
 * @param {String} str String.
 * @return {Number[]} Array.
 */
export function str2arr(str: string): number[] {
    var result: number[] = [];
    for (var i = 0; i < str.length; i++) {
        result.push(parseInt(str.charCodeAt(i).toString(10)));
    }
    return result;
}

/**
 * Checks the captcha and returns whether ko or not to callback.
 * @function checkCaptcha
 * @public
 * @param {String} c Challenge.
 * @param {Function} callback Callback.
 */
export function checkCaptcha(c: string, callback: Function) {
    var data = querystring.stringify({
        secret: '6LfleigTAAAAAG_-AGX7NOMgfchlIbzuBtdD5qmw',
        response: c
    });
    var options = {
        host: 'www.google.com',
        port: 443,
        path: '/recaptcha/api/siteverify',
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Content-Length': Buffer.byteLength(data)
        }
    };
    var ht = https.request(options, function(res) {
        var r = '';
        res.on('data', function(chunk) {
            r += chunk;
        });
        res.on('end', function() {
            var obj = JSON.parse(r);
            if('success' in obj && obj.success == true)
                callback(true);
            else
                callback(false);
        });
    }).on('error', function(err) {
        callback(false);
    });
    ht.write(data);
    ht.end();
}

/**
 * Returns a certificate.
 * @function genCert
 * @public
 * @param {String} pubPem Public PEM.
 * @param {String} priPemLoc Private PEM location.
 * @param {Object} params Remote params.
 * @return {String} Certificate PEM.
 */
export function genCert(pubPem: string, priPemLoc: string, params: any): string {
    var cert = pki.createCertificate();
    cert.publicKey = pki.publicKeyFromPem(pubPem);
    cert.serialNumber = '01';
    cert.validity.notBefore = new Date();
    cert.validity.notAfter = new Date();
    cert.validity.notAfter.setFullYear(cert.validity.notBefore.getFullYear() + 1000);
    var localAttrs = [
        {
            name: 'commonName',
            value: 'auth_node'
        }, {
            name: 'countryName',
            value: 'BE'
        }, {
            shortName: 'ST',
            value: 'some_state'
        }, {
            name: 'localityName',
            value: 'some_city'
        }, {
            name: 'organizationName',
            value: 'auth_node'
        }
    ], remoteAttrs = [
        {
            name: 'commonName',
            value: params.commonName
        }, {
            name: 'countryName',
            value: params.countryName
        }, {
            name: 'localityName',
            value: params.localityName
        }, {
            name: 'organizationName',
            value: params.organizationName
        }
    ];
    cert.setSubject(remoteAttrs);
    cert.setIssuer(localAttrs);
    cert.setExtensions([
        {
            name: 'keyUsage',
            keyCertSign: true,
            digitalSignature: true,
            nonRepudiation: false,
            keyEncipherment: true,
            dataEncipherment: true
        }, {
            name: 'extKeyUsage',
            serverAuth: true,
            clientAuth: true,
            codeSigning: true,
            emailProtection: true,
            timeStamping: true
        }, {
            name: 'nsCertType',
            client: true,
            server: false,
            email: true,
            objsign: true,
            sslCA: false,
            emailCA: false,
            objCA: false
        }
    ]);
    cert.sign(pki.privateKeyFromPem(fs.readFileSync(priPemLoc)));
    return pki.certificateToPem(cert);
}
