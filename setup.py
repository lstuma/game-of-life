import setuptools

with open('README.md', 'r') as fh:
    long_desc = fh.read()

setuptools.setup(
    name='Game Of Life',
    version='0.1',
    author='Lukas Stockmann',
    author_email='g.lstuma@gmail.com',
    description='A clone of the popular \'Game Of Life\'',
    long_description=long_desc,
    url='',
    packages=setuptools.find_packages(),
    install_requires=['setuptools,'
                      'pygame',
                      'numpy'
                      ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'game_of_life=game_of_life.game_of_life:main',
        ]
    }
)
