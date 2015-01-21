This package wraps argparse to facilitate sharing a standardized set of
arguments across various scripts and applications that may use argparse.

For example, assume you have two scripts, "runthis.py" and "runthat.py," both
of which share common arguments.  It may make sense to share the argument logic
between runthis and runthat.  See the examples directory for an
implementation of runthis and runthat.


Features:

- Share common arguments between scripts
    - ability to override specific argument options via @lazy_kwargs decorator
- Set default values directly from environment variables by
setting action=DefaultFromEnv in the argument's options.
- I think it's slightly cleaner than default argparse
- Used at Sailthru in production
- Actually, I use this everywhere I write Python code!

```
$ cat argparse_tools/examples/runthat.py
$ python argparse_tools/examples/runthat.py

$ cat argparse_tools/examples/runthis.py
$ python argparse_tools/examples/runthis.py --opt2 isrequired

$ MYVAR_FENV=111 python argparse_tools/examples/runthis.py --opt2 isrequired
```
