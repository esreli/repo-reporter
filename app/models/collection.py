from app import static

class Collection(object):

    __name = None

    @staticmethod
    def name():
        if Collection.__name is None: Collection.__build_from_yaml()
        return Collection.__name

    __accent_color = None

    @staticmethod
    def accent_color():
        if Collection.__accent_color is None: Collection.__build_from_yaml()
        return Collection.__accent_color

    @staticmethod
    def __build_from_yaml():
        Collection.__name = static.collection()["collection-name"]
        Collection.__accent_color = static.collection()["collection-accent-color"]
