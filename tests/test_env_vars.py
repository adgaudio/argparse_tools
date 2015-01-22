import argparse_tools as at
import nose.tools as nt
import argparse
import os


def test_default_from_env():
    # if no hardcoded default and no env var defined, default value is None
    nt.assert_not_in('OPT1', os.environ)
    val = at.build_arg_parser([
        at.add_argument('--opt1', action=at.DefaultFromEnv)
    ])().parse_args().opt1
    nt.assert_is(val, None)

    # hardcoded default used if env var default is not defined
    ns = at.build_arg_parser([
        at.add_argument('--opt1', action=at.DefaultFromEnv, default=123)
    ])().parse_args()
    expected = argparse.Namespace(opt1=123)
    nt.assert_equal(ns, expected)

    os.environ['TEST_DEFAULT_FROM_ENV_OPT1'] = '444'

    # check that the env var is actually used
    ns = at.build_arg_parser([at.add_argument(
        '--opt1', action=at.DefaultFromEnv, env_prefix='test_default_from_env_')
    ])().parse_args()
    nt.assert_equal(ns, argparse.Namespace(opt1='444'))

    # env var default overrides hardcoded default
    val = at.build_arg_parser([
        at.add_argument(
            '--test_default_from_env_opt1', action=at.DefaultFromEnv,
            default=123)
    ])().parse_args().test_default_from_env_opt1
    nt.assert_equal(val, '444')

    # required and default= means option must be defined
    # this is argparse's standard way of dealing with this... not ideal
    with nt.assert_raises(SystemExit):
        ns = at.build_arg_parser([
            at.add_argument(
                '--opt1', action=at.DefaultFromEnv, default=123, required=True)
        ])().parse_args()

    # if var is set in the environment, don't fail on required=True
    ns = at.build_arg_parser([at.add_argument(
        '--opt1', action=at.DefaultFromEnv, env_prefix='test_default_from_env_',
        required=True)
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
