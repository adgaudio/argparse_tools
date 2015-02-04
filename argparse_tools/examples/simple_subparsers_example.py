from argparse_tools.examples import shared as at


def main(ns):
    print('hello world from subparser example! %s' % ns.__dict__)


build_arg_parser = at.build_arg_parser([
    at.opt1,
    at.add_subparsers({
        "optionA": [at.opt2],
        "optionB": [at.optgroup1]})
])


if __name__ == '__main__':
    NS = build_arg_parser().parse_args()
    main(NS)
