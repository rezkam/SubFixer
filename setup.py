from distutils.core import setup

setup(
    name='SubFixer',
    version='0.1',
    py_modules = ['subfixer'],
    license='GPL 3.0',
    author='Mohammad Reza Kamalifard',
    author_email='mrkamalifard@gmail.com',
    description='',
    entry_points = '''
        [console_scripts]
        subfixer=subfixer:cli
    '''
)
