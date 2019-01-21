#!/bin/bash -x
EXAMPLE_DIR=`dirname $0`
if [[ ! $EXAMPLE_DIR =~ ^/ ]]; then
  EXAMPLE_DIR="$PWD/$EXAMPLE_DIR"
fi

python $EXAMPLE_DIR/burnin.py --config-file $EXAMPLE_DIR/burnin.yaml
