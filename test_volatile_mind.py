import sys
import os

# Set paths
NEMO_PATH = "C:/Users/serro/Yukora/nemo"
CLI_PATH = "C:/Users/serro/Yukora/shortcut-cli"
sys.path.extend([NEMO_PATH, CLI_PATH])

from nexus_shell import NexusShell
from ephemeral_mind import EphemeralMind

print("=== SOVEREIGN INTELLIGENCE TEST ===")

# 1. Test Command (Observation)
print("\n[STEP 1] Running Echo Command...")
with EphemeralMind() as mind:
    mind.observe("echo Volatile_Intelligence_Test")
    # Simulate execution
    os.system("echo Volatile_Intelligence_Test")

# 2. Test Query (Thinking)
print("\n[STEP 2] Running Compounded Query...")
with EphemeralMind() as mind:
    response = mind.think("Explain Nemo and Time")
    print(f"RESPONSE: {response}")

print("\n=== TEST COMPLETE ===")
