"""The `api` package holds everything HTTP-facing: versioned routers and
their shared dependencies (`deps.py`). No business logic lives here --
endpoints in `v1/endpoints/` call into the `services` layer and translate
the result to/from Pydantic schemas.
"""
