
alias sds-watch="python3 $SANDSOFTIME_DIR/python/sandsoftime/watch.py"


sds_dgtime() {
  screen -dmS sds-dgtime bash -lc \
    "source ~/.bashrc && python3 \"$SANDSOFTIME_DIR/python/sandsoftime/dgtime.py\""
}
alias sds-dgtime=sds_dgtime
