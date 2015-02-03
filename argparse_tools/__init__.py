import argparse
import functools
import os


class TooManyDefaultsDefined(Exception):
    pass


class EnvironmentVarRequired(Exception):
    pass


class DefaultFromEnv(argparse.Action):
    """Define argument options that fetch defaults from environment variables

        add_argument("--optA", action=DefaultFromEnv)
            --> fetches default from the environment var, OPTA

        add_argument("--optB", action=DefaultFromEnv, required=True)
            --> ensures that optB is defined
                either in command-line, env var, or hardcoded default=

        add_argument("--optC", action=DefaultFromEnv, default=1)
            --> first tries to get val from environment,
                otherwise uses default=

        add_argument("--optD", action=DefaultFromEnv, envrequired=True)
        add_argument("--optD2", action=DefaultFromEnv, envrequired=True,
                     default=1)
            --> both fail if OPTD is not an environment variable
            --> hardcoded 'default=...' is always ignored
    """
    def __init__(self, env_prefix="", envrequired=False, **kwargs):
        kwargs = kwargs.copy()
        key = ("%s%s" % (env_prefix, kwargs['dest'])).upper()
        if key in os.environ:
            if 'default' in kwargs:
                # the environment default overrides the code default
                pass
            if kwargs.get('required'):
                kwargs['required'] = False
        elif envrequired:
            raise EnvironmentVarRequired(key)
        kwargs['default'] = os.getenv(key, kwargs.get('default'))
        super(DefaultFromEnv, self).__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def lazy_kwargs(f):
    """
    A decorator that won't execute the wrapped func until you pass in args.
    If you pass in kwargs, it will save those as a functools.partial and delay
    execution until the partial receives args.
    """

    @functools.wraps(f)
    def _lazy_kwargs(*args, **kwargs):
        if args:
            return f(*args, **kwargs)
        else:
            return functools.partial(f, **kwargs)
    return _lazy_kwargs


def add_argument(*args, **kwargs):
    """wraps argparse.ArgumentParser.add_argument
    meant to be used like this:

        build_arg_parser([add_argument('blah')])
    """
    def _add_argument(parser):
        parser.add_argument(*args, **kwargs)
    return _add_argument


def group(description, *funcs, **kwargs):
    """
    A convenience wrapper for grouping argparse options

    Receive a list of funcs that receive a parser and add arguments
    to the parser.

    `mutually_exclusive` - (bool) if True, then
                           each func is mutually exclusive of the other funcs

    Return a function that receives an argparse.ArgumentParser instance and
    adds the group to it

    EXAMPLE:

        >>> p = argparse.ArgumentParser()
        >>> group(
        ...     "My argument group",
        ...      lambda x: x.add_argument('--this_option'),
        ...      lambda x: x.add_argument('--and_this'),
        ... )(p)

        >>> p.print_help()
        usage: nosetests [-h] [--this_option THIS_OPTION] [--and_this AND_THIS]
        <BLANKLINE>
        optional arguments:
          -h, --help            show this help message and exit
        <BLANKLINE>
        My argument group:
          --this_option THIS_OPTION
          --and_this AND_THIS

    """
    def _argument_group(parser):
        if kwargs.get('mutually_exclusive'):
            kwargs.pop('mutually_exclusive')
            g = parser.add_mutually_exclusive_group(**kwargs)
        elif kwargs:
            raise UserWarning(
                "Unrecognized kwargs: %s" % str(list(kwargs.keys())))
        else:
            g = parser.add_argument_group(description)
        for f in funcs:
            f(g)
    return _argument_group


def mutually_exclusive(*funcs, **kwargs):
    """
    A convenience wrapper for creating an
    argparse mutually exclusive argument group

    `kwargs` are params passed to
    argparse.ArgumentParser.add_mutually_exclusive_group

    EXAMPLE:

        >>> p = argparse.ArgumentParser()
        >>> mutually_exclusive(
        ... lambda x: x.add_argument('--only_this'),
        ... lambda x: x.add_argument('--xor_this'),
        ... )(p)

        >>> p.print_help()
        usage: nosetests [-h] [--only_this ONLY_THIS | --xor_this XOR_THIS]
        <BLANKLINE>
        optional arguments:
          -h, --help            show this help message and exit
          --only_this ONLY_THIS
          --xor_this XOR_THIS
    """
    # in argparse, mutually exclusive groups ignore the description
    return group(None, *funcs, mutually_exclusive=True, **kwargs)


def build_arg_parser(funcs=None, **argument_parser_kwargs):
    """Returns an argparse.ArgumentParser that applies each func in funcs to
    the parser.

    funcs - None or a list of funcs that accept an argparse.ArgumentParser,

    If funcs is not None, return a closure.

    Example usage:

    >>> parser = build_arg_parser([lambda p: p.add_argument('--a')])()

    >>> parser.parse_args(['--a', '1'])
    Namespace(a='1')

    """
    if funcs is None:
        _closure = False
        funcs = []
    else:
        _closure = True
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        **argument_parser_kwargs)
    for func in funcs:
        if func:
            func(parser)
    if _closure:
        return (lambda: parser)
    return parser
