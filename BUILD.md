# BUILD

Minimal instructions...

## Setup
`npm create anywidget@latest`

`npm install`

Uses: [`hpcc-systems/hpcc-js-wasm`](https://github.com/hpcc-systems/hpcc-js-wasm): `npm install --save @hpcc-js/wasm-graphviz`

## Build

Install node packages: `npm install`

Build / package Typescript/JS: `npm run build`

Build Python package (into `dist/`): `hatch build`

Install package: `pip install --upgrade --force-reinstall --no-deps dist/jupyter_anywidget_graphviz-0.0.0-py2.py3-none-any.whl`

Push to PyPi: `twine upload  dist/*0.0.0*` etc.
