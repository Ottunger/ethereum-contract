/**
 * Miner.
 * @module Miner
 * @author Mate It Right
 */

'use strict';
declare var require: any
declare var Buffer: any
var spawn = require('child_process').spawn;

export class Miner {

    private work: {account: string, password: string, value: number}[];
    private startValue: number;
    private working: boolean;
    private launching: boolean;
    private status: string;
    private process: any;

    constructor(public config: any) {
        var self = this;
        this.process = spawn('/usr/bin/geth', ['--identity', 'miner', '--networkid', config.network_id, '--datadir', config.chain_path,
                '--nodiscover', '--rpc', '--rpccorsdomain', '"*"', '--nat', '"any"', '--rpcapi eth,web3,personal,net', 'console'], {
            shell: true
        });
        this.process.unref();
        setTimeout(function() {
            self.process.stdin.write('personal.unlockAccount(' + config.user_id + ', ' + config.user_id_password + ')\n');
            self.process.stdin.write('miner.start()\n');
        }, 700);
        this.process.on('data', function(data) {
            self.manage(data);
        });
        this.process.stdin.on('error', function(err) {
            console.log(err);
        });

        this.work = [];
        this.working = false;
        this.launching = false;
        setInterval(function() {
            self.checkWork();
        }, 800);
    }

    private manage(data: string) {
        //For the check
        if(this.status == 'wait_balance') {
            if(parseFloat(data) > this.startValue + this.work[0].value) {
                this.process.stdin.write('miner.stop()\n');
                this.status = 'wait_stop1';
                this.work.pop();
                this.working = false;
                this.launching = true;
            }
        }
        //For the launch
        else if(this.status == 'wait_start1') {
            this.process.stdin.write('web3.miner.setEtherbase(' + this.work[0].account + ')\n');
            this.status = 'wait_start2';
        } else if(this.status == 'wait_start2') {
            this.process.stdin.write('eth.getBalance(' + this.work[0].account + ')\n');
            this.status = 'wait_start3';
        } else if(this.status == 'wait_start3') {
            this.startValue = parseFloat(data);
            this.process.stdin.write('miner.start()\n');
            this.status = 'wait_confirm';
            this.launching = false;
        }
        //For the stops
        else if(this.status == 'wait_stop1') {
            this.process.stdin.write('web3.miner.setEtherbase(' + this.config.user_id + ')\n');
            this.status = 'wait_stop2';
        } else if(this.status == 'wait_stop2') {
            this.process.stdin.write('miner.start()\n');
            this.status = 'wait_confirm';
            this.launching = false;
        } else if(this.status == 'wait_confirm') {
            return;
        }
    }

    private checkWork() {
        if(this.working && !this.launching) {
            //Wait for feedback of work
            this.process.stdin.write('eth.getBalance(' + this.work[0].account + ')\n');
            this.status = 'wait_balance';
        } else if(this.work.length > 0 && !this.launching) {
            //Wait for balance...
            this.process.stdin.write('personal.unlockAccount(' + this.work[0].account + ', ' + this.work[0].password + ')\n');
            this.status = 'wait_start1';
            this.working = true;
            this.launching = true;
        }
    }

    registerWork(account: string, password: string, value: number) {
        this.work.push({
            account: account,
            password: password,
            value: value
        });
    }

}