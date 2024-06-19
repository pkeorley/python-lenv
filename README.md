
# python-lenv

Welcome to the **lenv** package page!
This package allows you to quickly, efficiently and conveniently load environment variables into a *class*!




## Features
 
- [x] Loading variables into a class by variable name
- [x] Loading variables into a class by variable value
- [x] Configurability using `metadata` 
- [ ] Documentation

## Installation

To install/update the `lenv` package, you need to use `pip`

```bash
python3 -m pip install -U python-lenv
```

    
## Usage/Examples

First, we'll look at the structure of your project, which should look like this
```bash
my-awesome-project
├── .env
└── main.py
```


Let's go to the file where the variables will be loaded into your class. We will name it `.env` and put the following content inside

```dotenv
NAME='John Doe'
AGE=21
API_KEYS='["01f95ec3-ab56-4272-a1fc-71cd6b94b720", "6d70c8a7-90f...", "..."]'
```


Let's move on to the most important thing, namely our python script where environment variables will be loaded from the `.env` file we created earlier

```python
# main.py
from lenv import MetaEnvironmentVariablesLoader


class Environ(metaclass=MetaEnvironmentVariablesLoader):
    # Metadata allows you to configure the settings for loading environment variables.
    metadata = {
        # To see the available configurable options, you can view the `load_dotenv` function signature
        # https://github.com/theskumar/python-dotenv/blob/main/src/dotenv/main.py#L321-L328
        "load_dotenv": {
            "dotenv_path": "./venv/.env",
            ...: ...
        },
        # Let's look at these parameters later...
        "filters": {
            "includes": [],
            "excludes": [],
        },
        # If you enable this option, then if the variable is not found in the .env,
        # it will throw an 'AttributeError' error instead of the usual warning
        "raise_when_not_found": False,
    }

    # Normal retrieval of a value. We can get the value of an environment variable
    # using the name of the variable, this is the most common use case
    NAME: str

    # Also, we can get the environment variable not by the variable name, but by the value of the variable
    WE_CAN_PUT_THERE_WHAT_YOU_WANT: int = "NAME"  # <- This is the key by which the value of the environment variable will be sufficient

    # We can use typehints as below to convert the received
    # environment variable to a Python data type
    AGE: int

    # We can also use other types, such as list
    API_KEYS: list


print(Environ.NAME)         # "John Doe"
print(Environ.AGE)          # 21
print(Environ.API_KEYS[0])     # "01f95ec3-ab56-4272-a1fc-71cd6b94b720"
```

In addition, we can load into the class only those variables that we have selected, for example, only those ending in `api_keys`

```py
import os
os.environ["NAME"] = "John Doe"
os.environ["OPENAI_API_KEYS"] = '["...", "...", "..."]'
os.environ["SOMEONE_ELSE_API_KEYS"] = '["..."]'

from lenv import MetaEnvironmentVariablesLoader


class ApiKeys(metaclass=MetaEnvironmentVariablesLoader):
    metadata = {
        # There are two filters, one by `includes` and the other by `excludes`. 
        # For filtering, the regex language is used
        "filters": {
            "includes": [r"\w*_API_KEYS"],
            "excludes": [],
        }
    }

    OPENAI_API_KEYS: list
    SOMEONE_ELSE_API_KEYS: list
    NAME: str

assert ApiKeys.OPENAI_API_KEYS is not None          # Correct
assert ApiKeys.SOMEONE_ELSE_API_KEYS is not None    # Correct
assert ApiKeys.NAME is not None                     # Error. And although the name exists in the environment variables, it will not load
```

## License

`lenv` is distributed under the terms of the [MIT](https://choosealicense.com/licenses/mit/) license.

