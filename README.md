# sandsoftime

Simple script to run any arbitrary command at regular intervals (Only for didactic purposes)

# Command line options


Run a command at a given interval (output buffer is not clear every time)
```
sds-watch <interval_time> "<command>"
```


Run all scheduled commands
```
sds-dgtime
```


Schedule a command to run at a given interval (in minutes)
```
sds-dgtime <interval_time> "<command>"
```

List all schedule commands
```
sds-dgtime -l
```

Commands are saved in a JSON file indicated by macro SANDSOFTIME_DATAFILE