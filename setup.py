import setuptools

setuptools.setup(
    name="nires-display-tools",
    version="0.1.0",
    author="AUTHORS",
    packages=setuptools.find_packages(),
    include_package_data=True,
    namespace_packages=["nires"],
    url="https://github.com/Smarter-Sorting/smarter-spiders",
    license="LICENSE",
    description="Smarter Spiders UPC scraping Repo",
    long_description=open("README.md").read(),
    install_requires=[
        "scrapy==1.5.0",
        "scrapy_crawlera==1.3.0",
        "pika==0.11.2",
        "simplejson==3.13.2",
        "cryptography==2.1.4",
        "pyasn1==0.4.2",
        "pyasn1_modules==0.2.1",
        "requests==2.18.4"
    ]
)
