"""Persistence layer: one module per aggregate, raw SQLAlchemy queries only.
No request/response shaping and no authorization checks belong here --
those live in `services/` and `api/`, respectively."""
