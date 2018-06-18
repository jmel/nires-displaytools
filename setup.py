#import subprocess
import setuptools
#from setuptools.command.install import install


#class PostInstallCommand(install):
#    """Post-installation for installation mode."""
#    def run(self):
#        subprocess.run("scripts/aliases.sh")
#        install.run(self)

setuptools.setup(
    name="nires-displaytools",
    version="0.1.0",
    author="AUTHORS",
    packages=setuptools.find_packages(),
    include_package_data=True,
    namespace_packages=["nires"],
    url="https://github.com/jmel/nires-displaytools",
    description="Tools for better display of nires data",
    long_description=open("README.md").read(),
    install_requires=[
        "numpy==1.14.3",
        "astropy==3.0.1",
        "pyfits==3.5",
        "click==6.7",
        "mock==2.0.0"
    ]
)


