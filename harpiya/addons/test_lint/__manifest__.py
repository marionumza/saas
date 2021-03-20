# -*- coding: utf-8 -*-
{
    'name': 'test-lint',
    'version': '0.1',
    'category': 'Tests',
    'description': """A module to test Harpiya code with various linters.""",
    'maintainer': 'Harpiya SA',
    'depends': ['base'],
    'installable': True,
    'auto_install': False,
    'pre_init_hook': 'uninstall_test_pylint'
}
