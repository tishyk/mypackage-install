### THis is a demo for a python package creation
mypackage-name
### build
```bash
python -m build 
python setup.py  bdist_wheel --universal
```

### install
```bash
pip install [-e] .
pip install dist/... --force-reinstall
```
