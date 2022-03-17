# python-jyutping

Python library for Jyutping: conversion, validation and more

## Install

```sh
pip install jyutping
```

## APIs

Conversion (WIP):

```python
>>> import jyutping
>>> jyutping.get('广东话')
['gwong2', 'dung1', 'waa6']
```

Validation (WIP):

```python
>>> from jyutping import validate, ValidationStatus
>>> assert validate('jyut6') == ValidationStatus.VALID
>>> assert validate('gwek6') == ValidationStatus.UNCOMMON
>>> assert validate('nguk1') == ValidationStatus.INVALID
```
