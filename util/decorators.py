from ..types.anki.qt import AqtVars


def require_vars(*required_vars: AqtVars):
    def decorator(func):
        def wrapper(*args, **kwargs):
            assert mw and mw.col
            for var in required_vars:
                if var.get() is None:
                    raise ValueError(
                        f"Required variable '{var.name}' is not available. Ensure Anki is fully initialized."
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator
