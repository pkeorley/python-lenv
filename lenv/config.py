from dataclasses import dataclass


@dataclass
class Config:
    """
    Configuration class that allows you to configure package behavior
    """

    # The name of the variable in the class that contains the metadata
    METADATA_CLASS_VAR_NAME: str = "meta"
