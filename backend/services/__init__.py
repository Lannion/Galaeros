"""Business-logic layer: authorization decisions that need domain context,
orchestration across multiple repositories, and translation between
Pydantic input schemas and ORM models. Routers depend on these modules,
never on `repositories/` directly."""
