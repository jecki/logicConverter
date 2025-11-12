#!/usr/bin/env python3

"""tst_principia_grammar.py - runs the unit tests for the logi-grammar
"""

import os
import sys

LOGGING = 'LOGS'
DEBUG = True
TEST_DIRNAME = 'tests_grammar'

scriptpath = os.path.dirname(__file__)
if scriptpath not in sys.path:
    sys.path.append(scriptpath)

try:
    from DHParser.configuration import access_presets, set_preset_value, \
        finalize_presets, read_local_config
    from DHParser import dsl
    import DHParser.log
    from DHParser import testing
    from DHParser.toolkit import re
    from DHParser import versionnumber
    print(versionnumber.__version__)
except ModuleNotFoundError:
    print('Could not import DHParser. Please adjust sys.path in file '
          '"%s" manually' % __file__)
    sys.exit(1)


def recompile_grammar(grammar_src, force):
    grammar_tests_dir = os.path.join(scriptpath, TEST_DIRNAME)
    testing.create_test_templates(grammar_src, grammar_tests_dir)
    # recompiles Grammar only if it has changed
    if not dsl.recompile_grammar(grammar_src, force=force,
            notify=lambda: print('recompiling ' + grammar_src)):
        print('\nErrors while recompiling "%s":' % grammar_src +
              '\n--------------------------------------\n\n')
        error_path = os.path.join(grammar_src[:-5] + '_ebnf_MESSAGES.txt')
        with open(error_path, 'r', encoding='utf-8') as f:
            print(f.read())
        sys.exit(1)
    dsl.create_scripts(grammar_src)


mathjax_head = '''
<!DOCTYPE html>
<html lang="de" xml:lang="de">
<head>
<title>TITLE</title>
<meta charset="UTF-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
'''

mathjax_tail = '''
</body>
</html>
'''


def gen_html():
    try:
        import markdown2
        grammar_tests_dir = os.path.join(scriptpath, TEST_DIRNAME)
        report_dir = os.path.join(grammar_tests_dir, 'REPORT')
        for fname in os.listdir(report_dir):
            fpath = os.path.join(report_dir, fname)
            html = markdown2.markdown_path(fpath)
            html = re.sub(r'<pre><code>\s*\\\[', r'\[', html)
            html = re.sub(r'\\\]\s*</code></pre>', r'\]', html)
            html_name = fpath[:fpath.rfind('.')] + '.html'
            with open(html_name, 'w', encoding='utf-8') as f:
                head = mathjax_head.replace('TITLE', fname)
                f.write('\n'.join([head, html, mathjax_tail]))
    except ImportError:
        print('WARNING: Could not import markdown2. No HTML-report will be generated.')


def run_grammar_tests(fn_pattern, get_grammar, get_transformer):
    if fn_pattern.find('/') >= 0 or fn_pattern.find('\\') >= 0:
        testdir, fn_pattern = os.path.split(fn_pattern)
        if not testdir.startswith('/') or not testdir[1:2] == ':':
            testdir = os.path.abspath(testdir)
    else:
        testdir = os.path.join(scriptpath, TEST_DIRNAME)
    DHParser.log.start_logging(os.path.join(testdir, LOGGING))
    error_report = testing.grammar_suite(
        testdir, get_grammar, get_transformer,
        fn_patterns=[fn_pattern], report='REPORT', verbose=True,
        junctions={compiling, modern_junction, principia_tex_junction,
                   modern_tex_junction},
        show={'ast', 'LST', 'modern', 'pm.tex', 'modern.tex'})
    gen_html()
    return error_report


if __name__ == '__main__':
    read_local_config('dhparser.ini')
    argv = sys.argv[:]
    if len(argv) > 1 and sys.argv[1] == "--debug":
        DEBUG = True
        del argv[1]

    access_presets()
    # set_preset_value('test_parallelization', True)
    if DEBUG:  set_preset_value('history_tracking', True)
    finalize_presets()

    if (len(argv) >= 2 and (argv[1].endswith('.ebnf') or
        os.path.splitext(argv[1])[1].lower() in testing.TEST_READERS.keys())):
        # if called with a single filename that is either an EBNF file or a known
        # test file type then use the given argument
        arg = argv[1]
    else:
        # otherwise run all tests in the test directory
        arg = '*_test_*.ini'
    if arg.endswith('.ebnf'):
        recompile_grammar(arg, force=True)
    else:
        recompile_grammar(os.path.join(scriptpath, 'principia.ebnf'),
                          force=False)
        sys.path.append('.')
        from principiaParser import get_grammar, get_transformer, compiling, \
            modern_junction, principia_tex_junction, modern_tex_junction
        error_report = run_grammar_tests(arg, get_grammar, get_transformer)
        if error_report:
            print('\n')
            print(error_report)
            sys.exit(1)
        print('ready.\n')
