#!/usr/bin/env bash

echo "./startminer.sh <genesisFile> <dataDir>"
geth --datadir $2 init $1