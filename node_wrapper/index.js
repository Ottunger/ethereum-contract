/**
 * Node entry point.
 * @module index
 * @author Mate It Right
 */

var express = require('express');
var helmet = require('helmet');
var body = require('body-parser');
var http = require('http');
var https = require('https');
var pass = require('passport');
var fs = require('fs');
var pki = require('node-forge').pki;

var utils = require('./utils');
var all = require('./all');
var will = require('./will');
var rpem;

//Set the running configuration
//Launch as ">$ node index.js localhost" for instance
var configs = require('./configs.json');
var config = configs[process.argv[2]];
var httpport = config.port;
var localhost = config.localhost;
utils.DEBUG = config.debug;
if(utils.DEBUG)
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

/**
 * Sets the API to connect to the database.
 * @function connect
 * @public
 * @param {Function} callback Callback.
 */
function connect(callback) {
    all.managerInit(config);
    will.managerInit(config);
    utils.prepareRL();
    callback(false);
}

/**
 * Closes connection to the database.
 * @function close
 * @public
 */
function close() {
    process.exit(0);
}

/**
 * Chunks the string.
 * @fucntion chunk
 * @public
 * @param {String} str Input.
 * @param {Number} n Break.
 * @return {String[]} Chunks.
 */
function chunk(str, n) {
    var ret = [], i, len;
    for(i = 0, len = str.length; i < len; i += n) {
        ret.push(str.substr(i, n))
    }
    return ret
};

/**
 * Is the first middleware for passport.
 * @function pauth
 * @public
 * @param {Request} req Request.
 * @param {Response} res Response.
 * @param {Function} next Middleware.
 */
function pauth(req, res, next) {
    var cert;
    if(!!req.get('X-SSL-CERT')) {
        var t = '-----BEGIN CERTIFICATE-----\n' + chunk(req.get('X-SSL-CERT'), 64).join('\n') + '\n-----END CERTIFICATE-----';
    } else if(config.https) {
        var t = '-----BEGIN CERTIFICATE-----\n' + chunk((req.socket.getPeerCertificate().raw || '').toString('base64'), 64).join('\n') + '\n-----END CERTIFICATE-----';
    }
    try {
        cert = pki.certificateFromPem(t);
    } catch(e) {}
    if(cert) {
        var ok = false;
        try {
            ok = rpem.verify(cert);
        } catch(e) {}
        if(!ok) {
            res.type('application/json').status(401).json({error: utils.i18n('client.auth', req)});
        } else {
            var id = cert.subject.getField('CN').value;
            req.user = id;
            next();
        }
    } else {
        res.type('application/json').status(401).json({error: utils.i18n('client.auth', req)});
    }
}

//Now connect to DB then start serving requests
connect(function(e) {
    if(e) {
        console.log('Bootstrap could not be completed.');
        process.exit();
    }

    //Create the express application
    var app = express();
    if(utils.DEBUG == false) {
        app.use(helmet());
    } else {
        app.use(function(req, res, next) {
            res.set('Access-Control-Allow-Origin', '*');
            res.set('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With');
            next();
        });
    }
    app.use(function(req, res, next) {
        if(!!req.body)
            req.bodylength = Buffer.byteLength(req.body, 'utf8');
        next();
    });
    app.use(body.json({limit: '5000mb'}));

    //API AUTH DECLARATIONS
    app.post('/api/v:version/create_account', pauth);
    app.post('/api/v:version/will/execute', pauth);
    //API POST CHECKS
    app.post('/api/v:version/create_account', utils.checkBody([]));
    app.post('/api/v:version/will/execute', utils.checkBody(['contract', 'contract_address', 'method', 'arg_array', 'transform']));
    //API ROUTES
    app.post('/api/v:version/create_account', all.createAccount);
    app.post('/api/v:version/will/execute', will.executor);

    //Error route
    app.use(function(req, res) {
        res.type('application/json').status(404).json({error: utils.i18n('client.notFound', req)});
    });

    process.on('SIGTERM', close);
    process.on('SIGINT', close);
    if(utils.DEBUG == false) {
        process.on('uncaughtException', function(err) {
            console.log(err, err.stack);
        });
    }

    if(config.https) {
        var servers = https.createServer({
            key: fs.readFileSync(config.keypem),
            cert: fs.readFileSync(config.certpem),
            ca: fs.readFileSync(__dirname + '/ca-cert.pem'),
            requestCert: true,
            rejectUnauthorized: false
        }, app);
        servers.listen(httpport);
    } else {
        var server = http.createServer(app);
        server.listen(httpport);
    }
    console.log('Booststrap finished.');
});