from distutils.core import setup

setup(
    name='SubFixer',
    version='0.2',
    py_modules = ['subfixer'],
    license='GPL 3.0',
    author='Mohammad Reza Kamalifard',
    install_requires=[
        'click'
    ],
    author_email='mrkamalifard@gmail.com',
    description='',
    entry_points = '''
        [console_scripts]
        subfixer=subfixer:cli
    '''
)
