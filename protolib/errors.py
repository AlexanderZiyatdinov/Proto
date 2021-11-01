class ProtoLibraryError(Exception):
    pass


class BadExtension(ProtoLibraryError):
    def __str__(self):
        return "You need to use the extension .proto for deserialization"
