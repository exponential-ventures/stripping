from setuptools import setup, find_packages

setup(
    name='stripping',
    version='0.2.4',
    description='An easy to use pipeline solution for AI/ML experiments',
    author='Adriano Marques, Nathan Martins, Thales Ribeiro',
    author_email='adriano@xnv.io, nathan@xnv.io, thales@xnv.io',
    python_requires='>=3.7.0',
    install_requires=['aurum', 'numpy'],
    include_package_data=True,
    license="GNU LGPLv3",
    url='https://github.com/exponential-ventures/stripping',
    packages=find_packages(exclude=['*tests*', 'test*']),
    platforms=['any'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

)
