"""
NEXUS Ephemeral Mind - Volatile Intelligence Engine.

The Mind is a detonatable artifact. It wakes up, inhabits RAM, 
processes context, and implodes back to zero-inertia.
"""

import sys
import os
from typing import Optional

# Path configuration for the Sovereign Trinity
FORGE_PATH = "C:/Users/serro/Yukora/forge"
NEMO_PATH = "C:/Users/serro/Yukora/nemo"

for path in [FORGE_PATH, NEMO_PATH]:
    if path not in sys.path:
        sys.path.append(path)

try:
    from forge.recursive.engine import RecursiveEngine
    FORGE_CORE_AVAILABLE = True
except ImportError:
    FORGE_CORE_AVAILABLE = False

class EphemeralMind:
    """
    A context manager that summons the Sovereign AI for a single operation.
    """
    def __init__(self, action_type: str = "query"):
        self.action_type = action_type
        self.engine = None
        self.nemo = None
        self.ccp = None

    def __enter__(self):
        # 1. IGNITION: Initialize Recursive Engine (Volatile RAM context)
        if FORGE_CORE_AVAILABLE:
            self.engine = RecursiveEngine()
            self.engine.__enter__()
        
        print(f"[MIND] Waking... (Hydrating in RAM context)")

        # 2. PROPAGATION: Load logic into the volatile space
        try:
            from nemo.core.nemo_code import NemoCodeStack
            from compounded_context import ContextCompounder
            self.nemo = NemoCodeStack()
            self.ccp = ContextCompounder()
        except ImportError as e:
            print(f"[MIND] Warning: Limited hydration. Missing modules: {e}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 3. IMPLOSION: Shred the memory and return to dormant state
        print(f"[MIND] Imploding... (Returning to Zero Baseline)")
        
        # Explicitly delete the logic objects to free memory
        del self.nemo
        del self.ccp
        
        if self.engine:
            self.engine.__exit__(exc_type, exc_val, exc_tb)
        
        # Signal garbage collection
        import gc
        gc.collect()

    def think(self, query: str) -> str:
        """Process a query while the Mind is awake."""
        if not self.ccp:
            return "[MIND] Error: Logic hydration incomplete."
        return self.ccp.process_query(query)

    def observe(self, command: str):
        """Record an action while the Mind is awake."""
        if self.nemo:
            self.nemo.push("detonate", command)
