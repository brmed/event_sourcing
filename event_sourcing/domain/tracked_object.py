import attr

from lib.json_utils import SerializableDict


@attr.s(auto_attribs=True, cmp=False, repr=False)
class TrackedObject:
    module: str = None
    signature: str = None
    object_id: int = None

    def __attrs_post_init__(self):
        if not self.module:
            self.module = self.__module__
        if not self.signature:
            self.signature = self.__class__.__name__
        if hasattr(self, 'id') and not self.object_id:
            self.object_id = self.id

    def set_id(self, id):
        self.object_id = id

    def get_state(self):
        state = SerializableDict.serialize(self)
        if hasattr(self, 'UNTRACKED_FIELDS'):
            for field in self.UNTRACKED_FIELDS:
                ref = state
                for depth in field.split('__')[:-1]:
                    ref = ref[depth]
                ref.pop(field.split('__')[-1], None)
        return state
