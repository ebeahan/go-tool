# go
Uses a menu driven interface to open SSH sessions

**Basic Usage:**

```console
$ go.py
```
This will print all entries in the current configdb and prompt for an entry.

**Config Database**

```console
$ go.py -db /path/to/configdb
```

Saves a .configdb in ~/.go/ by default. A specific sqlite DB can be specified with the -db flag.
