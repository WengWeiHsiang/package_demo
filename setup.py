from setuptools import setup

setup(
    # Needed to silence warnings
    name='testR4',
    url='https://github.com/WengWeiHsiang/package_demo',
    author='weng',
    author_email='weng@ares.com.tw',
    # Needed to actually package something
    packages=['testR4', 'measure', 'closed_form'],
    # Needed for dependencies
    install_requires=['numpy'],
    # *strongly* suggested for sharing
    version='0.5',
    license='MIT',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.rst').read(),
    # if there are any scripts
    scripts=['scripts/hello.py'],
)