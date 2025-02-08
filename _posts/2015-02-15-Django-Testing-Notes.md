---
layout: post
title: "Django Testing Notes"
tagline : "Django Testing Notes"
description: "Django Testing Notes"
category: "Language"
tags: [python, django, testing]
---
{% include JB/setup %}

Django is equipped with powerful testing framework, but there may be some issues one may encounter in real work. I noted down mines.

### How test cases are run

We usually subclass django.test.TestCase and django.test.TransactionTestCase to begin our test cases. When the test cases are run

```
python manage.py test [--settings=test_settings] [app1 app2] [module-full-name ...] [-v 2]
```

Django do as follows:

  * Create an empty db
  * What you do by `python manage.py syncdb`
  * What you do by `python manage.py migrate`
  * For each test_xxx function in each test case
  	* Load db dataset from fixtures, i.e. `python manage.py loaddata <fixture-name>`
  	* Run your test_xxx function
  	* Reset you modifications on db

### Use fixtures

I copy our dev db to a fixture, then load the fixture in our test cases. This works as a fast way in which we can run our test cases on a copied dev db.

```
# copy dev db to fixtures
python manage.py dumpdata --indent=4 --natural --exclude contenttypes --exclude south.migrationhistory --exclude auth --exclude sessions --exclude <a-bunch-of-history-tables> > db/fixtures/test_data.json

# run our tests afterwards
python manage.py test [--settings=test_settings] [app1 app2] [module-full-name ...] [-v 2]
```

You should load the fixture in each test case

```
class TestXXX(TestCase):
    # sepcify the database dataset for testing.
    # it will be loaded before setUp
    fixtures = ['test_data.json']
 
    def setUp(self):
        pass
 
    def test_xxx(self):
        pass
```

The fixtures are loaded on every test_xxx function in every test case. So it is slow. The best recommendations are not to use fixtures at all, and always set up your test data in TestCase.setUp method. The [django-dynamic-fixture](http://django-dynamic-fixture.readthedocs.org/en/latest/overview.html) library can make this easier.

Another solution is to load fixtures at module level or whole test level, rather than on each test_xxx function. See [1](http://stackoverflow.com/questions/979434/how-to-load-fixtures-only-once-in-django-unit-tests), [2](http://stackoverflow.com/questions/979434/how-to-load-fixtures-only-once-in-django-unit-tests).

### Use sqlite as test database

Use in-memory sqlite database to speed up test. Create a test_settings.py as below

```
from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}
```

Run test by below will switch to use above sqlite db

```
python manage.py test --settings=test_settings
```

The `default` db without `NAME` attribute will make sqlite in-memory.

### Sqlite with threading problem

If you use above sqlite in-memory db, and you are also use multi-threading (i.e. the threading lib). If your test case launches new thread and the thread access db, you may encounter `No such table: xxx` error. This is because python sqlite hardly support multi-user access.

To fix this, use sqlite on-disk db. Change test_settings.py as below and the sqlite will now run on disk.

```
from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'test.db'),
        'TEST_NAME': os.path.join(os.path.dirname(__file__), 'test.db'),
    }
}
```

### Transaction with threading problem

If your test case launches new thread (i.e. the threading lib), and the thread accesses db, and you are subclassing django.test.TestCase, the thread may hang forever. This is because django.test.TestCase, your base case, wraps each test_xxx function in a db transaction (so that it can rollback after the test_xxx function are run). Your threads are blocked because of the transaction.

To fix this, subclass django.test.TransactionTestCase instead

```
from django.test import TransactionTestCase

class TestXXX(TransactionTestCase):
	pass
```

TestCase and TransactionTestCase [differences](https://docs.djangoproject.com/en/1.7/topics/testing/tools/#transactiontestcase) as follows:

  * TestCase wraps each test_xxx function in a db transaction, and rollback after a test_xxx function is run. So that you cannot operate db transaction by yourself. Other threads who need db access may block.
  * TransactionTestCase, doesn't like its name, let you handle transaction by yourself. It truncates all tables after each test_xxx function is run, but not by db transaction rollback.

It looks like that django test framework doesn't take threading much into consideration.

### Fast way to run test

Use `python manage.py test` to run test cases each time is slow, because it needs to set up a blank db and do schema migration. 

To run a test case directly, on your dev db (not the test db). First enter `python manage.py shell`:

```
from tests import TestXXX
from unittest import TestResult

fn = 'test_xxx'

# run the test_xxx function and capture results
t = TestXXX(fn)
r = TestResult()
t.run(r)

# print the test results
for e in (r.errors+r.failures):
    for token in e:
        print token
```

Django shell is interactive but hard for using pdb and debug with threading. To write a fast_test.py script

```
# to set up django settings, so that we won't need 'python manage.py shell'
import sys, os
sys.path.append('/path/to/your/django/app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmc.settings'
from django.conf import settings

# paste the above code to run test cases
...
```

The above sets up django settings for your app and avoids the 'ImproperlyConfigured' error.

Note that in this way the test cases are run on your dev db (be carefull not to lose data). Without django running the test cases, the common test case set up and tear down won't be run, yet it won't reset or rollback your database after each test_xxx function.

### Patching tool

Python [mock](https://docs.python.org/3/library/unittest.mock.html) lib is a famous tool in testing to mock and patch things. However it cannot satisfy my needs to patch a class method and intercept its calling arguments. I want to take these arguments out and examine them in test cases.

See is my [patch](https://github.com/accelazh/pyacc/blob/master/common/patch.py) tool on github. See its [test cases](https://github.com/accelazh/pyacc/blob/master/tests/patch/test_patch.py) about how to use. Here is another example

```
import time

# Patch your specified class method. You will be able to get calling arguments from 'trace', i.e. the handle to the patched method.
# With 'deocrate=True' the patched method will still be executed. 'decorate=False' only captures arguments but won't execute the 
# method. 'return_value=xxx' specifies what to return when 'decorate=False', as the faked returns of the patched method.
with utils.Patch('<module>.<class>.<method>', decorate=True, return_value=None) as trace:
    # Execute something, where an object of <module>.<class> will be instantiated and <method> invoked.
    # The above can be executed in another thread (python threading lib), but not another process.
    ...

    # Wait until the <method> is invoked, if it should be invoked in another thread
    while trace['run'] < 1:
        time.sleep(1)

    # Examine what calling arguments are passed into <method>. Object method's 'self' will also be included
    print trace['args']
    print trace['kwargs']
```

You can set an upper waiting limit to the time.sleep(1) part.

### Squash db migrations

Each time your run `python manage.py test`, the db schema migration will be run. If you have many migration versions, it costs a lot of time. A solution is to squash the db migrations. Django 1.7 supports it by [squashmigrations](https://docs.djangoproject.com/en/1.7/topics/migrations/#squashing-migrations). But for django 1.6 you have to do it by your own. Below is for schema migration

  1. Migrate your db to the version you want to start from
  2. Delete all your db schema migrations files after that version
  3. Create the migration file by `python manage.py schemamigration <app> --auto`

Note that the squash can only squash from your selected version to the latest version.

