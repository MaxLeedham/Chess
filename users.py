from __future__ import annotations


class User:
    def __init__(
        self,
        user_id: int | None,
        username: str | None,
        playing_as: str | None = None,
        guest: bool = False,
    ) -> None:
        self.user_id = user_id
        self.username = username or "Guest"
        self.playing_as = playing_as
        self.guest = guest

    def __repr__(self):
        return f"{self.user_id} ({self.username})"
