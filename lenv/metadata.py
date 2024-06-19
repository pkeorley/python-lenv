import typing as t

Dict = t.Dict[t.Hashable, t.Any]


class Metadata:
    def __init__(self, metadata: t.Optional[t.Union['Metadata', Dict]]):
        self._metadata = metadata if isinstance(metadata, dict) else metadata.metadata

    def __getitem__(self, item):
        return self.metadata[item]

    @staticmethod
    def default() -> t.Dict[t.Hashable, t.Any]:
        """
        Returns the default metadata
        :return: Default metadata
        """
        return Metadata.add_required_keys({})

    @staticmethod
    def add_required_keys(d: t.Dict[t.Hashable, t.Any]) -> t.Dict[t.Hashable, t.Any]:
        """
        Adds the required keys to the metadata.
        :param d: Metadata to add the required keys
        :return: Metadata with the required keys
        """
        def add(key: t.Hashable, value: t.Any) -> t.Dict[t.Hashable, t.Any]:
            if key not in d:
                d[key] = value
            return d

        add("load_dotenv", {})
        add("filters", {
            "includes": [],
            "excludes": [],
        })
        add("raise_when_not_found", False)

        return d

    @property
    def metadata(self) -> Dict:
        if self._metadata is None:
            return self.default()
        return Metadata.add_required_keys(self._metadata)

    def __repr__(self) -> str:
        return "Metadata(metadata={0!r})".format(self.metadata)

