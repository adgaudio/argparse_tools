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
        kwargs['metavar'] = "%s%s" % (
            env_prefix, kwargs.get('metavar') or kwargs['dest'].upper())
        super(DefaultFromEnv, self).__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def add_argument_default_from_env_factory(env_prefix=""):
    """Return an add_argument(...) function that gets defaults from an
    environment variable (using the DefaultFromEnv action), but also lets
    users use some specifically supported actions like
    'store_true' and 'store_false'

    >>> add_argument = add_argument_default_from_env_factory("PREFIX_")
    >>> p = build_arg_parser([\
        add_argument('--blah', action='store_true'),\
        add_argument('--bloo', action='store_false'),\
    ])()

    >>> p.print_help()
    usage: nosetests [-h] [--blah [PREFIX_BLAH]] [--bloo [PREFIX_BLOO]]
    <BLANKLINE>
    optional arguments:
      -h, --help            show this help message and exit
      --blah [PREFIX_BLAH]
      --bloo [PREFIX_BLOO]

    >>> p.parse_args(['--blah', '--bloo'])
    Namespace(blah=True, bloo=False)

    """
    @functools.wraps(add_argument)
    def _add_argument(*args, **kwargs):
        """Wraps argparse.ArgumentParser.add_argument to guarantee that all
        defined options are available from environment variables.

        Use as you would add_argument, but be warned that most actions will
        not work.  Acceptable actions are 'store_true' and 'store_false'.
        """
        if 'action' in kwargs:
            val = kwargs.pop('action')
            if val == 'store_true':
                kwargs['const'] = True
                kwargs['nargs'] = '?'
            elif val == 'store_false':
                kwargs['const'] = False
                kwargs['nargs'] = '?'
            else:
                raise NotImplemented(
                    "Not sure how to deal with this argparse argument option."
                    " add_argument() applies a custom action to get defaults"
                    " from"
                    " the environment.  You cannot specify action=%s for the"
                    " argument identified by: %s" % (val, str(args[:2])))
        return add_argument(
            *args, action=DefaultFromEnv, env_prefix=env_prefix, **kwargs)
    return _add_argument


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


def add_subparsers(dct, **kwargs):
    """
    Declarative way to define subparsers.
    Returns a closure that accepts a parent parser and adds subparsers to it.

    `dct` - a dict like
        {"subparserA": [add_argument('--in_a_only'), ...],
         "subparserB": [add_argument('--in_b_only'), ...]
        }

    Meant to be used like this:
        build_arg_parser([
            add_argument('--opt1'),
            add_subparsers({
                'subparserA': [add_argument('--in_a_only')],
                'subparserB': [add_argument('--in_b_only')]})
        ])
    """
    def _add_subparsers(parser):
        factory = parser.add_subparsers(**kwargs)
        # hack: bypass bug in python3 argparse
        # http://stackoverflow.com/questions/22990977/why-does-this-argparse-code-behave-differently-between-python-2-and-3
        factory.required = True
        for name in sorted(dct.keys()):
            funcs = dct[name]
            _subparser = factory.add_parser(name)
            build_arg_parser(funcs, _subparser)
    return _add_subparsers


def build_arg_parser(funcs=None, parser=None, **argument_parser_kwargs):
    """Returns an argparse.ArgumentParser that applies each func in funcs to
    the parser.

    funcs - None or a list of funcs that accept an argparse.ArgumentParser,
    parser - None or an instance of an argparse.ArgumentParser.  If not given,
        create our own.

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
    if not parser:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            **argument_parser_kwargs)
    for func in funcs:
        if func:
            func(parser)
    if _closure:
        def _I_return_an_ArgumentParser():
            return parser
        return _I_return_an_ArgumentParser
    return parser
