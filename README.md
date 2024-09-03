![python-lenv-logo](./docs/python-lenv-logo.png)

----

<center>Welcome to the <b>lenv</b> package page!</center>
<center>Load environment variables into a class <b>quickly</b>, <b>efficiently</b> and<b>conveniently</b>!</center>

## Features
 
- [x] Loading environment variables into class variables by variable name
- [x] Configuring the package as you want

## Installation

You can use your favorite package manager to install/update the `lenv` package. For example, `pip`, as in this example:

```bash
python3 -m pip install -U python-lenv
```

    
## Usage/Examples

### dotenv

First of all, let's define our `.env` file, which will be located in the startup directory of the main file.

I put the `TOKEN` and `API_KEY` there, in the future we will be able to get them through class variables

```dotenv
TOKEN=FOlCLYqcM.ZRgpwq.IrUyWYwjwSvFmCITCbmOBqvbqpZLWNrufvQKsrawplHMAwICSjBJvSlkJFaeENCrYkdOUeqSwmwQoMbTEJLLFLIGDLXaWF.HsNqciQnXitjhzXO
API_KEY=a3edffac-f4cc-4e68-9fd3-11e942fc7ea6
```

### python

Finally, we come to our first example. We can use class variables to get environment variables directly through the class.

```python
import lenv


class Config(lenv.EnvironmentLoader):
    # This configuration is not important, the default is used `lenv.DefaultMetadata` 
    # which has a file path like .env in it (You can change it with lenv.Config.DEFAULT_DOTENV_FILE_PATH). But for example, let's leave it
    meta = lenv.ConfigurableMetadata(dotenv_path=".env")
    
    # These class variables will be used directly to access environment variables －O－
    TOKEN: str
    API_KEY: str


assert Config.TOKEN == 'FOlCLYqcM.ZRgpwq.IrUyWYwjwSvFmCITCbmOBqvbqpZLWNrufvQKsrawplHMAwICSjBJvSlkJFaeENCrYkdOUeqSwmwQoMbTEJLLFLIGDLXaWF.HsNqciQnXitjhzXO'
assert Config.API_KEY == 'a3edffac-f4cc-4e68-9fd3-11e942fc7ea6'
```
## License

`lenv` is distributed under the terms of the [MIT](https://choosealicense.com/licenses/mit/) license.

 