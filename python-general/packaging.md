To create a python package out of a repo and upload it to pypi:

1. create the python source code
1. add a setup.py file in the repo root (above source code)
1. install setuptools, wheel, twine
1. run `$python setup.py sdist bdist_wheel`
1. run `$twine upload dist/*`
    - Enter your credentials to upload to PyPi

