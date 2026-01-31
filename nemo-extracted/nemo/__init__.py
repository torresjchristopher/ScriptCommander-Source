"""Project Nemo - Master Synthesis Engine"""

__version__ = "1.0.0"

# Import core classes and functions so they're accessible from nemo package
try:
    from nemo.core.nemo import (
        IntentCategory,
        KeyboardState,
        IntentionPrediction,
        KeyboardInterceptor,
        LayerComposer,
        get_nemo_composer,
        get_keyboard_interceptor,
    )
    __all__ = [
        "IntentCategory",
        "KeyboardState",
        "IntentionPrediction",
        "KeyboardInterceptor",
        "LayerComposer",
        "get_nemo_composer",
        "get_keyboard_interceptor",
    ]
except ImportError:
    # Allow package to install even if imports fail
    pass

