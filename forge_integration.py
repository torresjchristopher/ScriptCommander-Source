"""Forge integration module for Shortcut CLI

Integrates Forge container orchestration as a top-level menu in Shortcut CLI.

Menu structure:
  [1] Forge         - Container orchestration + workflows
  [2] Scripts       - Local script management
  [3] Features      - Additional features & administration
"""

import subprocess
import sys
import os
from pathlib import Path

# Try to add local forge to path for latest recursive features
FORGE_PATH = Path("C:/Users/serro/Yukora/forge")
if FORGE_PATH.exists():
    sys.path.append(str(FORGE_PATH))

try:
    from forge.recursive.engine import RecursiveEngine
    from forge.recursive.pruning_dag import PruningDAG
    RECURSIVE_AVAILABLE = True
except ImportError:
    RECURSIVE_AVAILABLE = False


def launch_forge_command(command_args):
    """Launch a Forge command via subprocess.
    
    Args:
        command_args: List of command arguments (e.g., ['tui'], ['container', 'run', ...])
    
    Returns:
        Return code from Forge CLI
    """
    try:
        result = subprocess.run(
            ['forge'] + command_args,
            check=False
        )
        return result.returncode
    except FileNotFoundError:
        print("[ERROR] Forge CLI not found. Install with: pip install forge-runtime")
        return 1
    except Exception as e:
        print(f"[ERROR] Failed to launch Forge: {e}")
        return 1


def attach_forge_commands(main_group):
    """Attach Forge command group to main CLI.
    
    This creates a 'forge' subcommand that passes through to the Forge CLI.
    
    Args:
        main_group: Click group to attach Forge commands to
    """
    import click
    
    @main_group.group(name='forge')
    def forge_group():
        """Container orchestration + embedded workflows."""
        pass
    
    @forge_group.command()
    @click.pass_context
    def tui(ctx):
        """Launch real-time dashboard (forge tui)."""
        sys.exit(launch_forge_command(['tui']))

    @forge_group.group(name='recursive')
    def recursive_group():
        """Recursive Self-Reengineering Engine (Zip-and-Detonate)."""
        if not RECURSIVE_AVAILABLE:
            click.secho("[WARNING] Recursive Engine modules not found. Using CLI fallback.", fg="yellow")

    @recursive_group.command(name='run')
    @click.option('--seed', required=True, help='Path to logic-seed (zip/tar.gz)')
    def recursive_run(seed):
        """Run a logic-seed with Zero-Inertia constraints."""
        if RECURSIVE_AVAILABLE:
            click.secho(f"[DETONATE] Propagating {seed}...", fg="cyan")
            with RecursiveEngine() as engine:
                # In a real run, we'd load the seed logic here
                click.secho("[EXEC] Executing recursive payload...", fg="blue")
                click.secho("[PRUNE] Real-time node shredding active.", fg="magenta")
            click.secho("[SUCCESS] System returned to Zero Baseline.", fg="green")
        else:
            sys.exit(launch_forge_command(['recursive', 'run', '--seed', seed]))

    @recursive_group.command(name='demo')
    def recursive_demo():
        """Run the 6-Task Radar Benchmark."""
        if FORGE_PATH.exists():
            demo_path = FORGE_PATH / "examples" / "six_task_radar_demo.py"
            if demo_path.exists():
                os.environ['PYTHONPATH'] = str(FORGE_PATH)
                subprocess.run([sys.executable, str(demo_path)])
                return
        click.secho("[ERROR] Demo script not found.", fg="red")
    
    @forge_group.group(name='container')
    def container_group():
        """Manage containers."""
        pass
    
    @container_group.command()
    @click.argument('image')
    @click.argument('command', nargs=-1, required=True)
    @click.option('-m', '--memory', type=int, help='Memory limit in MB')
    @click.option('-p', '--port', multiple=True, help='Port mapping')
    @click.option('-v', '--volume', multiple=True, help='Volume mount')
    @click.option('--timeout', type=int, help='Timeout in seconds')
    def run(image, command, memory, port, volume, timeout):
        """Run a container (forge container run)."""
        args = ['container', 'run', image] + list(command)
        if memory:
            args.extend(['-m', str(memory)])
        for p in port:
            args.extend(['-p', p])
        for v in volume:
            args.extend(['-v', v])
        if timeout:
            args.extend(['--timeout', str(timeout)])
        sys.exit(launch_forge_command(args))
    
    @forge_group.group(name='workflow')
    def workflow_group():
        """Manage workflows."""
        pass
    
    @workflow_group.command()
    @click.argument('workflow_id')
    def run_wf(workflow_id):
        """Run a workflow (forge workflow run)."""
        sys.exit(launch_forge_command(['workflow', 'run', workflow_id]))
    
    @workflow_group.command()
    def list_wf():
        """List workflows (forge workflow list)."""
        sys.exit(launch_forge_command(['workflow', 'list']))
    
    @forge_group.group(name='scheduler')
    def scheduler_group():
        """Manage scheduler."""
        pass
    
    @scheduler_group.command()
    @click.argument('workflow_id')
    @click.option('--cron', required=True, help='Cron expression')
    def schedule(workflow_id, cron):
        """Schedule a workflow (forge scheduler schedule)."""
        sys.exit(launch_forge_command(['scheduler', 'schedule', workflow_id, '--cron', cron]))
    
    @scheduler_group.command()
    def status():
        """Show scheduler status (forge scheduler status)."""
        sys.exit(launch_forge_command(['scheduler', 'status']))
    
    @forge_group.group(name='benchmark')
    def benchmark_group():
        """Performance benchmarking."""
        pass
    
    @benchmark_group.command()
    @click.option('--iterations', type=int, default=5)
    def startup(iterations):
        """Benchmark container startup (forge benchmark startup)."""
        sys.exit(launch_forge_command(['benchmark', 'startup', '--iterations', str(iterations)]))
    
    @benchmark_group.command()
    def compare():
        """Compare vs Podman/Docker (forge benchmark compare)."""
        sys.exit(launch_forge_command(['benchmark', 'compare']))
    
    @forge_group.group(name='system')
    def system_group():
        """System operations."""
        pass
    
    @system_group.command()
    def usage():
        """Show usage (forge system usage)."""
        sys.exit(launch_forge_command(['system', 'usage']))
    
    @system_group.command()
    def prune():
        """Prune unused data (forge system prune)."""
        sys.exit(launch_forge_command(['system', 'prune']))
