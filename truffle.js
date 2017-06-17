module.exports = {
    networks: {
        development: {
            host: 'localhost',
            port: 8545,
            network_id: '*', //Match any network id
            from: '0x4fdf2ae4bc2a96fa6d6772127b1430583939d5a2', //Use geth account new and copy keystore to chain
            gas: 2000000
        },
        live: {
            host: 'localhost',
            port: 8545,
            network_id: 1, //Ethereum public network
            from: '0x4fdf2ae4bc2a96fa6d6772127b1430583939d5a2', //Own account
            gas: 2000000
            //Optional config values:
            //gas
            //gasPrice
            //from - default address to use for any transaction Truffle makes during migrations
            //provider - web3 provider instance Truffle should use to talk to the Ethereum network.
            //         - if specified, host and port are ignored.
        }
    }
}