# from . import runthis, runthat


def examples_doctest():
    """
    >>> runthis.build_arg_parser().print_help()
    usage: nosetests [-h] [--shared_option1 SHARED_OPTION1] [--some_setting]
                     [--another_setting ANOTHER_SETTING] [--custom_arg CUSTOM_ARG]
                     [--a A] [--b B] --opt2 OPT2
    <BLANKLINE>
    An example implementation of argparse_tools that uses shared arguments
    <BLANKLINE>
    optional arguments:
      -h, --help            show this help message and exit
      --shared_option1 SHARED_OPTION1
      --custom_arg CUSTOM_ARG
      --opt2 OPT2
    <BLANKLINE>
    optgroup1: a group of options:
      --some_setting
      --another_setting ANOTHER_SETTING
    <BLANKLINE>
    my custom argument group:
      --a A
      --b B



    >>> runthat.build_arg_parser().print_help()
    usage: nosetests [-h] [--shared_option1 SHARED_OPTION1] [--some_setting]
                     [--another_setting ANOTHER_SETTING] [--custom_arg CUSTOM_ARG]
    <BLANKLINE>
    An example implementation of argparse_tools that uses shared arguments
    <BLANKLINE>
    optional arguments:
      -h, --help            show this help message and exit
      --shared_option1 SHARED_OPTION1
      --custom_arg CUSTOM_ARG
    <BLANKLINE>
    optgroup1: a group of options:
      --some_setting
      --another_setting ANOTHER_SETTING
    """
    pass
