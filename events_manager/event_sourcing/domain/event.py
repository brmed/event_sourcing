import attr
from datetime import datetime


@attr.s(auto_attribs=True, cmp=False, repr=False, kw_only=True)
class Event:
    name: str
    user: dict = None
    diff: dict = None
    state: dict = None
    date: datetime = None

    def set_diff(self, previous_event):
        current_state = self.state
        previous_state = previous_event.state

        create_or_remove = not current_state or not previous_state

        self.diff = None if create_or_remove else self._build_diff(
            current_state,
            previous_state,
        )

    def _build_diff(self, current_state, previous_state):
        if len(previous_state) > len(current_state):
            items = set(self._as_tuple(previous_state)) - set(self._as_tuple(current_state))
        else:
            items = set(self._as_tuple(current_state)) - set(self._as_tuple(previous_state))

        diff = {
            field: dict(
                old_value=previous_state.get(field),
                new_value=current_state.get(field),
            ) for field, _ in items
        }

        return diff or None

    def _as_tuple(self, d):
        if isinstance(d, list) or isinstance(d, tuple):
            return tuple([self._as_tuple(item) for item in d])
        elif isinstance(d, dict):
            return tuple([
                (self._as_tuple(k), self._as_tuple(v))
                for k, v in sorted(d.items())
            ])
        return d
