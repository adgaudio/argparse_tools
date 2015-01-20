from argparse_tools import (
    build_arg_parser, add_argument, group, mutually_exclusive, lazy_kwargs,
    DefaultFromEnv
)


def opt1(parser):
    parser.add_argument('--shared_option1', default=12345)


def optgroup1(parser):
    group(
        'optgroup1: a group of options',
        add_argument('--some_setting', action='store_true'),
        add_argument('--another_setting', default=5),
    )(parser)


@lazy_kwargs
def opt2(parser, **kwargs):
    """This shared option sets a default but lets developers using this code
    modify other attributes to this parser option as they please"""
    parser.add_argument('--opt2', default='cannot override this', **kwargs)
