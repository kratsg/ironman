from setuptools import setup

extras_require = {}
extras_require['docs'] = ['repoze.sphinx.autointerface']
extras_require['lint'] = sorted({'flake8', 'black'})
extras_require['test'] = [
    'pytest~=6.0',
    'pytest-cov>=2.5.1',
]
extras_require['develop'] = sorted(
    set(
        extras_require['docs']
        + extras_require['lint']
        + extras_require['test']
        + [
            'bump2version',
            'pre-commit',
            'check-manifest',
            'twine',
        ]
    )
)
extras_require['complete'] = sorted(set(sum(extras_require.values(), [])))

setup(extras_require=extras_require)
