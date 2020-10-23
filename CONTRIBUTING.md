# Contributing to COVID19 data toolset

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Welcome! I'm very happy if you are willing to make the project better.

You can contribute in the following ways:

* implement features
* fix bugs
* add tests
* give suggestions, share ideas etc...
* write documentation

## <a name="codestyle"></a> Code style

Please use black as code formatter

`pip install black`

`black .`

## <a name="commit"></a> Commit format

Please format commit message using following structure:

`<type>:<summary>`

**Type**

Must be one of the following:

* feat: a new feature

* fix: a bug fix

* test: adding missing tests or correcting existing tests

* refactor: a code change that neither fixes a bug nor adds a feature

* docs: documentation only changes

**Summary**

Provide succinct description of the change

## Pull Request process

Make your changes in a new git branch

`git checkout -b my-fix-branch master`

Before submitting a pull request please run unit tests.

`pytest --cov=ia tests/ --cov-config=.coveragerc`

Commit your changes using a descriptive commit message that follows [Commit format](#commit)

`git commit --all`

Push your branch to GitHub

`git push origin my-fix-branch`

In GitHub, send a pull request
