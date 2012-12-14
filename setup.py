from setuptools import setup

setup(
    name='scrapy-proxynova',
    version='0.1.0',
    description='Allows scrapy to use proxy list from proxynova.com',
    keywords='scrapy proxy',
    url='http://github.com/svetlyak40wt/scrapy-proxynova/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    #packages=find_packages(),
    packages=[
        'scrapy_proxynova',
    ]
)
