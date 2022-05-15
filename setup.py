import setuptools

with open('README.md', 'r') as fh:
    long_desc = fh.read()

setuptools.setup(
    name='Game Of Life',
    version='0.2',
    author='Lukas Stockmann',
    author_email='g.lstuma@gmail.com',
    description='A clone of the popular \'Game Of Life\'',
    long_description=long_desc,
    url='',
    packages=setuptools.find_packages(),
    install_requires=['setuptools',
                      'wheel',
                      'pygame',
                      'numpy'
                      ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'game-of-life=game_of_life.game_of_life:main',
        ]
    }
)
