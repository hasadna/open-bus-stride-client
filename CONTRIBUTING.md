## Local Development

```
python3 -m venv venv
. venv/bin/activate
pip install -e '.[all]'
```

## Publishing the PyPi package

Install dependencies

```
python3 -m pip install --upgrade build pip twine
```

Set the version in `VERSION.txt` (without preceding v)

Build

```
python3 -m build
```

Publish

```
python3 -m twine upload dist/open-bus-stride-client-$(cat VERSION.txt).tar.gz
```
