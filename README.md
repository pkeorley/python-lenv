
# lenv

Welcome to the **lenv** package page!
This package allows you to quickly, efficiently and conveniently load environment variables into a *class*!




## Features
 
- [x] Loading variables into a class by variable name
- [x] Loading variables into a class by variable value
- [ ] Configurability 

## Installation

To install/update the `lenv` package, you need to use `pip`

```bash
python3 -m pip install -U python-lenv
```

    
## Usage/Examples

First, we'll look at the structure of your project, which should look like this
```
my-awesome-project
├── .env
└── main.py
```


Let's go to the file where the variables will be loaded into your class. We will name it `.env` and put the following content inside
```
/* .env */
KEY=value
```


Let's move on to the most important thing, namely our python script where environment variables will be loaded from the `.env` file we created earlier
```python
# main.py
from lenv import Meta


class Config(metaclass=Meta):
    KEY: str


print(Config.KEY) # value
```

## License

`lenv` is distributed under the terms of the [MIT](https://choosealicense.com/licenses/mit/) license.

