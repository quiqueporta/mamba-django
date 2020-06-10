# mamba-django

A Django test runner for [mamba](https://github.com/nestorsalceda/mamba).


## How to use

Go to your Django test settings and add this line.

```
TEST_RUNNER = 'myapp.mamba_runner.MambaRunner'
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

## How to execute mamba tests with Django database transactions

```
from expects import (
    equal,
    expect
)

from myapp.mamba_runner import (
    start_django_transactions,
    rollback_django_transactions
)

from myapp.models import Animal


with description("Mamba with Django") as self:

    with before.each:
        self.transactions = start_django_transactions()

    with context("Running atomic tests"):

        with it("creates an animal"):
            Animal.objects.create(name="lion", sound="roar")
            expect(Animal.objects.all().count()).to(equal(1))

        with it("creates another animal"):
            Animal.objects.create(name="lion", sound="roar")
            expect(Animal.objects.all().count()).to(equal(1))

    with after.each:
        rollback_django_transactions(self.transactions)
```
