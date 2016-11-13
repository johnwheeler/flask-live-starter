from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='mvp-starter',
    version='0.0',
    py_modules='mvp.py',
    install_requires=reqs,
    entry_points='''
        [console_scripts]
        mvp=mvp:cli
    '''
)
