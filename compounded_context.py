"""
Compounded Context Protocol (CCP) - Logic Filter Engine.

This engine implements a communication protocol based on the intersection
of two distinct context factors. It highlights two objects in the request
and uses them as simultaneous filters to generate a precise response.
"""

import re
from typing import Tuple, Optional

class ContextCompounder:
    def __init__(self):
        # Knowledge Graph for Compounded Intersections
        self.knowledge_matrix = {
            ("forge", "speed"): "Forge achieves 10.5x velocity via Recursive DAG Pruning, eliminating daemon overhead.",
            ("forge", "security"): "Detonation containers are ephemeral. Memory is shredded post-execution, leaving zero forensic trace.",
            ("nemo", "security"): "Nemo uses self-supervised DINOv2 to process telemetry locally. No data leaves the silicon.",
            ("nemo", "time"): "Nemo Code allows for bi-directional traversal, scrubbing both authentic history and synthetic futures.",
            ("nexus", "forge"): "The Nexus Shell wraps every user command in a Forge Detonation loop for sovereign execution.",
            ("nexus", "nemo"): "Nexus provides the event stream (User Actions) that Nemo tokenizes into the Instruction Stack.",
            ("forge", "nemo"): "Forge handles the 'Lightning' (Compute), while Nemo handles the 'Memory' (State Reversal).",
        }
        
        # Keywords to scan for
        self.factors = ["forge", "nemo", "nexus", "speed", "security", "time"]

    def process_query(self, query: str) -> str:
        """
        Analyzes the query to find two compounding factors and returns
        the intersection context.
        """
        found_factors = self._extract_factors(query)
        
        if len(found_factors) < 2:
            return "[CCP] Error: Need exactly two factors to compound context. (e.g., 'Forge speed', 'Nemo security')"
        
        # Sort to match dictionary keys regardless of order
        f1, f2 = sorted(list(found_factors))[:2]
        
        response = self.knowledge_matrix.get((f1, f2))
        
        if response:
            return f"[CCP] Compounding ({f1.upper()} + {f2.upper()}) :: {response}"
        else:
            return f"[CCP] No intersection data found for {f1.upper()} and {f2.upper()}."

    def _extract_factors(self, query: str) -> set:
        """Identify known factors in the user string."""
        normalized = query.lower()
        found = set()
        for factor in self.factors:
            if factor in normalized:
                found.add(factor)
        return found

if __name__ == "__main__":
    ccp = ContextCompounder()
    print(ccp.process_query("Tell me about Forge and its speed."))
    print(ccp.process_query("How does Nemo handle security?"))
    print(ccp.process_query("What is the relationship between Nexus and Forge?"))
