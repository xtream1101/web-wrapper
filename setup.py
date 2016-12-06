from setuptools import setup


setup(
    name='web_wrapper',
    packages=['web_wrapper'],
    version='0.0.1',
    description='Web wrapper for Selenium/requests',
    author='Eddy Hintze',
    author_email="eddy.hintze@gmail.com",
    url="https://github.com/xtream1101/web-wrapper",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
    ],
    install_requires=[
        'cutil',
        'bs4',
        'pillow',
        'requests',
        'selenium',
        'fake_useragent',
    ],
)
