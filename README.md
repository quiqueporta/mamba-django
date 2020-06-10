# mamba-django

A Django test runner for [mamba](https://github.com/nestorsalceda/mamba).


## How to use

Go to your Django test settings and add this line.

```
TEST_RUNNER = '<your_module>.mamba_runner.MambaRunner'
```

## How to execute

```
./manage.py test --settings=project.settings.test --keepdb
```

You can pass all the mamba options to the Django test command.

For example:

```
./manage.py test --settings=project.settings.test --keepdb -f documentation -s 1
```
