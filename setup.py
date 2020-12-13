import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setuptools.setup(
        name='cha',
        url='https://github.com/ayuz999/cha',
        py_modules=['cha'],
        entry_points={
            'console_scripts': [
                'cha=cha:main',
            ],
        },
        packages=setuptools.find_packages(),
        install_requires=['lxml'],
        long_description=long_description,
        long_description_content_type="text/markdown",
    )
