import phrasal
from phrasal import *

if __name__ == '__main__':

    import sys
    import inspect

    if len(sys.argv) < 2:
        print('Missing requirement argument: <ClassName>')
        sys.exit(1)

    clsname = sys.argv[1]
    if clsname in ['-h', '--help', 'help', '?']:
        print('Call one of the tools from the commandline. Usage: ')
        print('   classname [other arguments specific to classname]|[-h]')
        print('\nAllowed classname arguments:')
        for k, v in phrasal.__dict__.items():
            if k[0].isupper():
                if getattr(inspect.getmodule(v), 'main', None) is not None:
                    print(' -', v.__name__)
        exit(0)

    if clsname not in globals():
        print(f'Class "{clsname}" could not be loaded. Maybe a typo or error in casing ?')
        exit(1)

    cls = globals()[clsname]
    main_func = getattr(inspect.getmodule(cls), 'main', None)
    if main_func is None:
        print(f'Class "{clsname}" does not define a main() method.')
        exit(1)

    sys.argv.pop(0)
    main_func()
