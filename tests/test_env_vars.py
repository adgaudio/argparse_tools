import argparse_tools as at
import nose.tools as nt
import argparse
import os

def test_default_from_env():
    ns = at.build_arg_parser([
        at.add_argument('--opt1', action=at.DefaultFromEnv, default=123)
    ])().parse_args()
    expected = argparse.Namespace(opt1=123)
    nt.assert_equal(ns, expected)

    with nt.assert_raises(SystemExit):
        # required option not defined
        ns = at.build_arg_parser([
            at.add_argument(
                '--opt1', action=at.DefaultFromEnv, default=123, required=True)
        ])().parse_args()

    os.environ['TEST_DEFAULT_REQUIRED_OPT1'] = '444'
    with nt.assert_raises(at.TooManyDefaultsDefined):
        ns = at.build_arg_parser([
            at.add_argument(
                '--test_default_required_opt1', action=at.DefaultFromEnv,
                default=123)
        ])()

    ns = at.build_arg_parser([at.add_argument(
        '--opt1', action=at.DefaultFromEnv, env_prefix='test_default_required_')
    ])().parse_args()
    nt.assert_equal(ns, argparse.Namespace(opt1='444'))

    ns = at.build_arg_parser([at.add_argument(
        '--opt1', action=at.DefaultFromEnv, env_prefix='test_default_required_',
        required=True  # if var is set in the environment, don't fail
    )
    ])().parse_args()
    nt.assert_equal(ns, argparse.Namespace(opt1='444'))


def test_default_bool():
    # This test shows what happens if you wanted both
    # action='store_true'  and  action=at.DefaultFromEnv

    # where env variable is defined, set the var to True
    os.environ['TEST_DEFAULT_BOOL_OPT1'] = '444'
    val = at.build_arg_parser([at.add_argument(
        '--opt1', action=at.DefaultFromEnv, env_prefix='test_default_bool_',
        type=bool),
    ])().parse_args().opt1
    nt.assert_is(val, True)
    # where env var is undefined, set the var to None
    val = at.build_arg_parser([at.add_argument(
        '--opt1', action=at.DefaultFromEnv, type=bool),
    ])().parse_args().opt1
    # where the env var is defined but empty, set the var to False
    os.environ['TEST_DEFAULT_BOOL_OPT2'] = ''
    nt.assert_is(val, None)
    val = at.build_arg_parser([at.add_argument(
        '--opt2', action=at.DefaultFromEnv,
        type=bool, env_prefix='test_default_bool_'),
    ])().parse_args().opt2
    nt.assert_is(val, False)
