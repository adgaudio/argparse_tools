import argparse_tools as at
from argparse import Namespace
import nose.tools as nt


def test_add_subparsers():
    p = at.build_arg_parser([
        at.add_argument('--opt1'),
        at.add_subparsers({
            'subparserA': [at.add_argument('--in_a_only')],
            'subparserB': [at.add_argument('--in_b_only')]})
    ])()
    # subparser options are appropriately constrained to their location
    ns = p.parse_args(['--opt1', '1', 'subparserA', '--in_a_only', 'AAA'])
    nt.assert_equal(ns, Namespace(opt1='1', in_a_only='AAA'))
    with nt.assert_raises(SystemExit):
        p.parse_args(['--opt1', '1', 'subparserA', '--in_b_only'])

    # subparsers are required
    with nt.assert_raises(SystemExit):
        ns = p.parse_args(['--opt1', '1'])
