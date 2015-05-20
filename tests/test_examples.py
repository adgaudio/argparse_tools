import argparse
from argparse_tools.examples import runthis, runthat, simple_subparsers_example
import nose.tools as nt
from subprocess import check_output


def test_doctest_simple_subparsers_example():
    """
    >>> simple_subparsers_example.build_arg_parser().print_help()
    usage: nosetests [-h] [--shared_option1 SHARED_OPTION1] {optionA,optionB} ...
    <BLANKLINE>
    positional arguments:
      {optionA,optionB}
    <BLANKLINE>
    optional arguments:
      -h, --help            show this help message and exit
      --shared_option1 SHARED_OPTION1


    >>> simple_subparsers_example.build_arg_parser().parse_args(['optionB'])
    Namespace(another_setting=5, shared_option1=12345, some_setting=False)
    """

def test_doctest_examples_help():
    """
    >>> runthis.build_arg_parser().print_help()
    usage: nosetests [-h] [--shared_option1 SHARED_OPTION1] [--some_setting]
                     [--another_setting ANOTHER_SETTING] [--custom_arg CUSTOM_ARG]
                     [--a A] [--b B] --opt2 OPT2 [--fenv MYVAR_FENV]
                     [--metavar1 customvarname1] [--metavar2 MYVAR_customvarname2]
    <BLANKLINE>
    An example implementation of argparse_tools that uses shared arguments
    <BLANKLINE>
    optional arguments:
      -h, --help            show this help message and exit
      --shared_option1 SHARED_OPTION1
      --custom_arg CUSTOM_ARG
      --opt2 OPT2
      --fenv MYVAR_FENV
      --metavar1 customvarname1
      --metavar2 MYVAR_customvarname2
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
        opt2='a', shared_option1=12345, some_setting=False,
        metavar1=None, metavar2=None, )
    nt.assert_equal(ns, ns2)

    ns = runthis.build_arg_parser().parse_args(['--opt2', 'b', '--fenv', '123'])
    ns2 = argparse.Namespace(
        a=None, another_setting=5, b=None, custom_arg=1, fenv='123',
        opt2='b', shared_option1=12345, some_setting=False,
        metavar1=None, metavar2=None, )
    nt.assert_equal(ns, ns2)


def test_runthat_parseargs():
    ns = runthat.build_arg_parser().parse_args()
    ns2 = argparse.Namespace(
        another_setting=5, custom_arg=99999, shared_option1=12345,
        some_setting=False)
    nt.assert_equal(ns, ns2)


def test_doctest_env_vars():
    # this test is brittle
    cmd = 'MYVAR_FENV=11 python -m argparse_tools.examples.runthis --opt2 2'
    rv = str(check_output(cmd, shell=True))
    nt.assert_regexp_matches(rv, r'.*hello world from runthis!.*')
    nt.assert_regexp_matches(rv, r"'a': None")
    nt.assert_regexp_matches(rv, r"'b': None")
    nt.assert_regexp_matches(rv, r"'shared_option1': 12345")
    nt.assert_regexp_matches(rv, r"'some_setting': False")
    nt.assert_regexp_matches(rv, r"'custom_arg': 1")
    nt.assert_regexp_matches(rv, r"'fenv': '11'")
    nt.assert_regexp_matches(rv, r"'opt2': '2'")
    nt.assert_regexp_matches(rv, r"'another_setting': 5")
