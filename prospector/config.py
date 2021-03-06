import setoptconf as soc

from prospector.__pkginfo__ import get_version
from prospector.adaptor import LIBRARY_ADAPTORS
from prospector.formatters import FORMATTERS
from prospector.tools import TOOLS, DEFAULT_TOOLS


__all__ = (
    'build_manager',
)


def build_manager():
    manager = soc.ConfigurationManager('prospector')

    manager.add(soc.BooleanSetting('zero_exit', default=False))

    manager.add(soc.BooleanSetting('autodetect', default=True))
    manager.add(soc.ListSetting('uses', soc.String, default=[]))

    manager.add(soc.BooleanSetting('blending', default=True))
    manager.add(soc.BooleanSetting('common_plugin', default=True))

    manager.add(soc.BooleanSetting('doc_warnings', default=False))
    manager.add(soc.BooleanSetting('test_warnings', default=False))
    manager.add(soc.BooleanSetting('style_warnings', default=True))
    manager.add(soc.BooleanSetting('full_pep8', default=False))
    manager.add(soc.IntegerSetting('max_line_length', default=None))

    manager.add(soc.BooleanSetting('messages_only', default=False))
    manager.add(soc.BooleanSetting('summary_only', default=False))
    manager.add(soc.ChoiceSetting(
        'output_format',
        sorted(FORMATTERS.keys()),
        default=None,
    ))
    manager.add(soc.BooleanSetting('absolute_paths', default=False))

    manager.add(soc.ListSetting(
        'tools',
        soc.Choice(sorted(TOOLS.keys())),
        default=None,
    ))
    manager.add(soc.ListSetting('with_tools', soc.String, default=[]))
    manager.add(soc.ListSetting('without_tools', soc.String, default=[]))
    manager.add(soc.ListSetting('profiles', soc.String, default=[]))
    manager.add(soc.ListSetting('profile_path', soc.String, default=[]))
    manager.add(soc.ChoiceSetting(
        'strictness',
        ['veryhigh', 'high', 'medium', 'low', 'verylow'],
        default='medium',
    ))
    manager.add(soc.ChoiceSetting(
        'external_config',
        ['none', 'merge', 'only'],
        default='only',
    ))

    manager.add(soc.StringSetting('path', default=None))

    manager.add(soc.ListSetting('ignore_patterns', soc.String, default=[]))
    manager.add(soc.ListSetting('ignore_paths', soc.String, default=[]))

    manager.add(soc.BooleanSetting('die_on_tool_error', default=False))

    return manager


def build_default_sources():
    sources = [
        build_command_line_source(),
        soc.EnvironmentVariableSource(),
        soc.ConfigFileSource((
            '.prospectorrc',
            'setup.cfg',
            'tox.ini',
        )),
        soc.ConfigFileSource((
            soc.ConfigDirectory('.prospectorrc'),
            soc.HomeDirectory('.prospectorrc'),
        ))
    ]

    return sources


def build_command_line_source(prog=None, description='Performs static analysis of Python code'):
    parser_options = {}
    if prog is not None:
        parser_options['prog'] = prog
    if description is not None:
        parser_options['description'] = description

    options = {
        'zero_exit': {
            'flags': ['-0', '--zero-exit'],
            'help': 'Prospector will exit with a code of 1 (one) if any messages'
                    ' are found. This makes automation easier; if there are any'
                    ' problems at all, the exit code is non-zero. However this behaviour'
                    ' is not always desirable, so if this flag is set, prospector will'
                    ' exit with a code of 0 if it ran successfully, and non-zero if'
                    ' it failed to run.'
        },
        'autodetect': {
            'flags': ['-A', '--no-autodetect'],
            'help': 'Turn off auto-detection of frameworks and libraries used.'
                    ' By default, autodetection will be used. To specify'
                    ' manually, see the --uses option.',
        },
        'uses': {
            'flags': ['-u', '--uses'],
            'help': 'A list of one or more libraries or frameworks that the'
                    ' project uses. Possible values are: %s. This will be'
                    ' autodetected by default, but if autodetection doesn\'t'
                    ' work, manually specify them using this flag.' % (
                        ', '.join(sorted(LIBRARY_ADAPTORS.keys())),
                    )
        },
        'blending': {
            'flags': ['-B', '--no-blending'],
            'help': 'Turn off blending of messages. Prospector will merge'
                    ' together messages from different tools if they represent'
                    ' the same error. Use this option to see all unmerged'
                    ' messages.',
        },
        'common_plugin': {
            'flags': ['--no-common-plugin'],
        },
        'doc_warnings': {
            'flags': ['-D', '--doc-warnings'],
            'help': 'Include warnings about documentation.',
        },
        'test_warnings': {
            'flags': ['-T', '--test-warnings'],
            'help': 'Also check test modules and packages.',
        },
        'style_warnings': {
            'flags': ['-8', '--no-style-warnings'],
            'help': 'Don\'t create any warnings about style. This disables the'
                    ' PEP8 tool and similar checks for formatting.',
        },
        'full_pep8': {
            'flags': ['-F', '--full-pep8'],
            'help': 'Enables every PEP8 warning, so that all PEP8 style'
                    ' violations will be reported.',
        },
        'max_line_length': {
            'flags': ['--max-line-length'],
            'help': 'The maximum line length allowed. This will be set by the strictness if no'
                    ' value is explicitly specified'

        },
        'messages_only': {
            'flags': ['-M', '--messages-only'],
            'help': 'Only output message information (don\'t output summary'
                    ' information about the checks)',
        },
        'summary_only': {
            'flags': ['-S', '--summary-only'],
            'help': 'Only output summary information about the checks (don\'t'
                    'output message information)',
        },
        'output_format': {
            'flags': ['-o', '--output-format'],
            'help': 'The output format. Valid values are: %s' % (
                ', '.join(sorted(FORMATTERS.keys())),
            ),
        },
        'absolute_paths': {
            'help': 'Whether to output absolute paths when referencing files'
                    'in messages. By default, paths will be relative to the'
                    'project path',
        },
        'tools': {
            'flags': ['-t', '--tool'],
            'help': 'A list of tools to run. This lets you set exactly which '
                    'tools to run. To add extra tools to the defaults, see '
                    '--extra-tool. Possible values are: %s. By '
                    'default, the following tools will be run: %s' % (
                        ', '.join(sorted(TOOLS.keys())),
                        ', '.join(sorted(DEFAULT_TOOLS)),
                    ),
        },
        'with_tools': {
            'flags': ['-w', '--with-tool'],
            'help': 'A list of tools to run in addition to the default tools. '
                    'To specify all tools explicitly, use the --tool argument. '
                    'Possible values are %s.' % (
                        ', '.join(sorted(TOOLS.keys()))
                    ),

        },
        'without_tools': {
            'flags': ['-W', '--without-tool'],
            'help': 'A list of tools that should not be run. Useful to turn off '
                    'only a single tool from the defaults. '
                    'To specify all tools explicitly, use the --tool argument. '
                    'Possible values are %s.' % (
                        ', '.join(sorted(TOOLS.keys()))
                    ),

        },
        'profiles': {
            'flags': ['-P', '--profile'],
            'help': 'The list of profiles to load. A profile is a certain'
                    ' \'type\' of behaviour for prospector, and is represented'
                    ' by a YAML configuration file. Either a full path to the YAML'
                    ' file describing the profile must be provided, or it must be'
                    ' on the profile path (see --profile-path)',
        },
        'profile_path': {
            'flags': ['--profile-path'],
            'help': 'Additional paths to search for profile files. By default this'
                    ' is the path that prospector will check, and a directory '
                    ' called ".prospector" in the path that prospector will check.',
        },
        'strictness': {
            'flags': ['-s', '--strictness'],
            'help': 'How strict the checker should be. This affects how'
                    ' harshly the checker will enforce coding guidelines. The'
                    ' default value is "medium", possible values are'
                    ' "veryhigh", "high", "medium", "low" and "verylow".',
        },
        'external_config': {
            'flags': ['-e', '--external-config'],
            'help': 'Determines how prospector should behave when'
                    ' configuration already exists for a tool. By default,'
                    ' prospector will use existing configuration. A value of'
                    ' "merge" will cause prospector to merge existing config'
                    ' and its own config, and "none" means that prospector'
                    ' will use only its own config.',
        },
        'ignore_patterns': {
            'flags': ['-I', '--ignore-patterns'],
            'help': 'A list of paths to ignore, as a list of regular'
                    ' expressions. Files and folders will be ignored if their'
                    ' full path contains any of these patterns.',
        },
        'ignore_paths': {
            'flags': ['-i', '--ignore-paths'],
            'help': 'A list of file or directory names to ignore. If the'
                    ' complete name matches any of the items in this list, the'
                    ' file or directory (and all subdirectories) will be'
                    ' ignored.',
        },
        'die_on_tool_error': {
            'flags': ['-X', '--die-on-tool-error'],
            'help': 'If a tool fails to run, prospector will try to carry on.'
                    ' Use this flag to cause prospector to die and raise the'
                    ' exception the tool generated. Mostly useful for'
                    ' development on prospector.',
        },
        'path': {
            'flags': ['-p', '--path'],
            'help': 'The path to a Python project to inspect. Defaults to PWD'
                    ' if not specified. Note: This command line argument is'
                    ' deprecated and will be removed in a future update. Please'
                    ' use the positional PATH argument instead.'
        }
    }

    positional = (
        ('checkpath', {
            'help': 'The path to a Python project to inspect. Defaults to PWD'
                    '  if not specified.',
            'metavar': 'PATH',
            'nargs': '*',
        }),
    )

    return soc.CommandLineSource(
        options=options,
        version=get_version(),
        parser_options=parser_options,
        positional=positional,
    )
