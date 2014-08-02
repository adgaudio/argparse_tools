This package wraps argparse to facilitate sharing a standardized set of
arguments across various scripts and applications that may use argparse.

For example, assume you have two scripts, "runthis.py" and "runthat.py," both
of which share common arguments.  It may make sense to share the argument logic
between runthis and runthat.  See the examples directory for an
implementation of runthis and runthat.

This tool lets you specify default argparse arguments and also lets
applications override the defaults via the @lazy_kwargs decorator.  See
examples/shared.py for an example.
