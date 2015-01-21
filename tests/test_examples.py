import argparse
from argparse_tools.examples import runthis, runthat
import nose.tools as nt
from subprocess import check_output


def test_doctest_examples_help():
    """
    >>> runthis.build_arg_parser().print_help()
    usage: nosetests [-h] [--shared_option1 SHARED_OPTION1] [--some_setting]
                     [--another_setting ANOTHER_SETTING] [--custom_arg CUSTOM_ARG]
                     [--a A] [--b B] --opt2 OPT2 [--fenv FENV]
    <BLANKLINE>
    An example implementation of argparse_tools that uses shared arguments
    <BLANKLINE>
    optional arguments:
      -h, --help            show this help message and exit
      --shared_option1 SHARED_OPTION1
      --custom_arg CUSTOM_ARG
      --opt2 OPT2
      --fenv FENV
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


def test_runthis_parseargs():
    ns = runthis.build_arg_parser().parse_args(['--opt2', 'a'])
    ns2 = argparse.Namespace(
        a=None, another_setting=5, b=None, custom_arg=1, fenv=None,
        opt2='a', shared_option1=12345, some_setting=False)
    nt.assert_equal(ns, ns2)

    ns = runthis.build_arg_parser().parse_args(['--opt2', 'b', '--fenv', '123'])
    ns2 = argparse.Namespace(
        a=None, another_setting=5, b=None, custom_arg=1, fenv='123',
        opt2='b', shared_option1=12345, some_setting=False)
    nt.assert_equal(ns, ns2)


def test_runthat_parseargs():
    ns = runthat.build_arg_parser().parse_args()
    ns2 = argparse.Namespace(
        another_setting=5, custom_arg=99999, shared_option1=12345,
        some_setting=False)
    nt.assert_equal(ns, ns2)


def test_doctest_env_vars():
    # this test is very brittle
    cmd = 'MYVAR_FENV=11 python -m argparse_tools.examples.runthis --opt2 2'
    rv = check_output(cmd, shell=True)
    expected = (
        "hello world from runthis! {'a': None, 'b': None,"
        " 'shared_option1': 12345, 'some_setting': False, 'custom_arg': 1,"
        " 'fenv': '11', 'opt2': '2', 'another_setting': 5}\n")
    nt.assert_equal(rv, expected)
