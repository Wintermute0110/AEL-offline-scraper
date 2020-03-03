## TODO

 * Nothing at the moment.

## Launchbox database
 
See [LaunchBox API access](https://bitbucket.org/jasondavidcarr/launchbox/issues/902/api-access-to-launchbox)

The LaunchBox database ZIP file is updated daily. Download it from
[LaunchBox metadata ZIP file](http://gamesdb.launchbox-app.com/Metadata.zip).

Do not use the LaunchBox database to build an offline scraper for now. I think it is better to have
one good offline scraper than several options.

## Include Python modules

To include an arbitrary directory in Python the directory must be added to the Python search path.

```
if __name__ == "__main__" and __package__ is None:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './AEL/resources')))
from scrap import *
```

However, by placing `__init__.py` functions in directories then they are converted into
packages and this syntax is valid.

```
# ./AEL/__init__.py exists
# ./AEL/resources/__init__.py exists
# ./AEL/resources/scrap.py is the module to include
#
from AEL.resources.scrap import *
```

It seems that having a `__init__.py` file in Kodi addon root is OK.
