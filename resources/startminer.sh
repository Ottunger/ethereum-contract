#!/bin/bash

echo "./startminer.sh <networkId> <dataDir> <account>"
geth --identity "miner" --unlock $3 --networkid $1 --datadir $2 --nodiscover --rpc --rpccorsdomain "*" --nat "any" --rpcapi eth,web3,personal,net --ipcpath "~/geth.ipc" --mine console