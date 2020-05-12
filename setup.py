from setuptools import find_packages, setup

from config import author, author_email, description, name, release, repo


def readme():
    with open('README.rst') as f:
        return f.read()


# 3rd-party run-time requirements:
install_requires = [
    'colorama==0.4.3',
    'typing-extensions==3.7.4.2',
]

# 1st-party run-time requirements:
install_requires += [
    'frozendict @ git+https://github.com/ominatechnologies/'
    'frozendict.git@1.2.2#egg=frozendict',
]

setup(
    author=author,
    author_email=author_email,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    data_files=[
        ('', ['AUTHORS.rst', 'CHANGELOG.rst', 'LICENSE', 'README.rst'])
    ],
    description=description,
    include_package_data=True,
    install_requires=install_requires,
    keywords=[
        'pretty-printing',
        'python',
        'utilities',
    ],
    license='MIT',
    long_description=readme(),
    name=name,
    package_data={
        name: ['py.typed'],
    },
    packages=find_packages(),
    python_requires='>=3.7',
    url=repo,
    version=release,
    zip_safe=False,
)
