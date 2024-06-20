from lenv import MetaEnvironmentVariablesLoader


class Config(metaclass=MetaEnvironmentVariablesLoader):
    metadata = {
        "filters": {
            "includes": [r"\w*_API_KEYS"],
        },
        "raise_when_not_found": False
    }

    NAGA_API_KEYS: str
    USERNAME: str


print(Config.NAGA_API_KEYS, Config.USERNAME)



from lenv import Metadata


print(Metadata.default())
