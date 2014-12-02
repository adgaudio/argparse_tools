from argparse_tools.examples import shared as at


def main(ns):
    print('hello world from runthis! %s' % ns.__dict__)


build_arg_parser = at.build_arg_parser([
    at.opt1,
    at.optgroup1,
    at.add_argument('--custom_arg', default=1),
    at.group(
        'my custom argument group',
        at.add_argument('--a'),
        at.add_argument('--b'),
    ),
    at.opt2(required=True),
], description=(
    'An example implementation of argparse_tools that uses shared arguments'))


if __name__ == '__main__':
    NS = build_arg_parser().parse_args()
    main(NS)
