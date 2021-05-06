"""
Reup google drive files to photos
--------------
Second project in 2019
"""
from setuptools import setup, find_packages

setup(
    name='r',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'Flask-SQLAlchemy==2.3.2',
        'PyMySQL',
        'requests',
        'flask-praetorian==0.5.3',
        'flask-cors==3.0.9',
        'Flask-Migrate==2.5.1',
        'flask-request-id-header==0.1.1'
    ],
)
