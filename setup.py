try:
    from distutils.core import setup
    from setuptools import find_packages
except ImportError:
    print ("Please install Distutils and setuptools"
           " before installing this package")
    raise

setup(
    name='argparse_tools',
    version='1.0.0',
    description=(
        'Share a standardized set of argparse arguments within your codebase'),
    long_description=open('README.md').read(),
    keywords=['argparse', ],

    author='Alex Gaudio',
    author_email='adgaudio@gmail.com',
    url='https://github.com/adgaudio/argparse_tools',

    packages=find_packages(),
    data_files=[('README.md', ['README.md'])],
    install_requires = ['argparse'],
    tests_require=['nose'],
    test_suite="nose.main",
)
