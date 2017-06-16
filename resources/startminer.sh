#!/bin/bash

echo "./startminer.sh <networkId> <dataDir>"
geth --identity "miner" --networkid $1 --datadir $2 --nodiscover --rpc --rpccorsdomain "*" --nat "any" --rpcapi eth,web3,personal,net --ipcpath "~/geth.ipc"