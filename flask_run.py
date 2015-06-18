"""Flask-based web application runner."""

from __future__ import print_function

__all__ = 'run'.split()
__version__ = '0.1.3'

def run(create_app, config, description=None, args=None, namespace=None, options=None):
    """Parses commandline options, updates config, creates and runs the application.

    Supports listing and selecting environment configurations if `Flask-Config`_ configuration class is used.

    .. _Flask-Config: http://pypi.python.org/pypi/Flask-Config
    """
    import argparse

    class HelpFormatter(
        # argparse.RawTextHelpFormatter,
        argparse.RawDescriptionHelpFormatter,
        # argparse.ArgumentDefaultsHelpFormatter,
        # argparse.HelpFormatter,
        ):
        pass

    # Get configurations data if
    envName = getattr(config, 'ENV', None)
    envMap = getattr(config, 'envMap', None)
    envHelp = getattr(config, 'envHelp', {})
    envSelectVar = getattr(config, 'envSelectVar', None)
    configurations = getattr(config, 'configurations', None)
    envSelectable = callable(getattr(config, 'select', None))
    envPrintable = config.__str__ is not object.__str__

    parser = argparse.ArgumentParser(
        description = description or getattr(config, 'description',
            'runs Flask-based web application using Python WSGI reference server'),
        epilog = ''.join((
            '\n\noptional environment variables:\n{}'.format(
                '\n'.join(sorted('  {:<20}  {}'.format(envMap[key], envHelp.get(key, ''))
                for key in envMap))) if envMap else '',
            '\n\navailable environment configurations (*: active):\n{}'.format(
                '\n'.join('{} {}'.format(
                    '*' if envName in c.names else ' ',
                    ' | '.join(c.names)
                ) for c in configurations)) if configurations else '',
        )),
        formatter_class = HelpFormatter)

    parser.add_argument('-b', '--bind', metavar='[HOST|:PORT]', default='127.0.0.1:5000',
        help = 'bind to HOST:PORT (default: 127.0.0.1:5000)')

    debug = config.DEBUG
    debugMsg = ' (default in {})'.format(config.ENV)
    debugTrueMsg = debugMsg if debug else ''
    debugFalseMsg = debugMsg if not debug else ''

    parser.add_argument('-r', '--reload', action='store_true', default=debug,
        help = 'reload server on code change' + debugTrueMsg)
    parser.add_argument('-R', '--no-reload', action='store_false', dest='reload',
        help = 'do not reload server on code change' + debugFalseMsg)

    parser.add_argument('-d', '--debug', action='store_true', default=debug,
        help = 'show debugger on exception' + debugTrueMsg)
    parser.add_argument('-D', '--no-debug', action='store_false', dest='debug',
        help = 'do not show debugger on exception' + debugFalseMsg)

    if envSelectable:
        parser.add_argument('-e', '--env', default=config.ENV,
            help = 'select environment config (default: {})'.format(config.ENV))

    if envPrintable:
        if envSelectable:
            parser.add_argument('-E', '--show-env', nargs='?', const=True,
                help = 'show environment config and exit ({}default: {})'
                    .format('*: all, ' if configurations else '', config.ENV))
        else:
            parser.add_argument('-E', '--show-env', action='store_true',
                help = 'show environment config and exit')

    parser.add_argument('-g', '--gen-key', action='store_true',
        help = 'generate a good secret key and exit')


    args = parser.parse_args(args, namespace)

    if args.gen_key:
        # See http://flask.pocoo.org/docs/0.10/quickstart/#sessions
        import os
        key = os.urandom(24)
        return print(key)
        # return print('{0}\n{0!r}'.format(key))

    if envSelectable and args.env:
        config = config.select(args.env)

    if envPrintable and args.show_env:
        if configurations and args.show_env == '*':
            print('\n\n'.join('# {}\n{}'.format(' | '.join(c.names), c) for c in configurations))
        elif args.show_env is True:
            print(config)
        else:
            print(config.select(args.show_env))

        return

    host, port = (args.bind + ':').split(':')[:2]
    host = host or '127.0.0.1'
    port = int(port) if port else 5000

    return create_app(config).run(host, port, args.debug, use_reloader=args.reload, **(options or {}))
