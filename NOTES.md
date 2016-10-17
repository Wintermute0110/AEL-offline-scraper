# TODO #

 * Nothing at the moment.

 
# Include Python modules #

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
