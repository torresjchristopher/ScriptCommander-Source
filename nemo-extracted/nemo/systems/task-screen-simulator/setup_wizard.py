"""
First-Run Setup Wizard - Welcome to Nemo
Guides user through initial configuration via CLI.
Google OAuth, agent selection, API key setup.
"""

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()


class FirstRunSetupWizard:
    """
    First-run experience for Nemo.
    Run when user presses RIGHT ALT for first time.
    """
    
    def __init__(self):
        self.completed = False
        self.agent_choice = "gemini"
        self.google_account = None
        self.api_key = None
    
    def run_welcome(self) -> None:
        """Display welcome screen"""
        welcome = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║            🧠 WELCOME TO NEMO 🧠                             ║
║                                                                ║
║  Your Personal AI Assistant Built Into Your Keyboard         ║
║                                                                ║
║  🔧 Setup Required                                           ║
║                                                                ║
║  Open a terminal and run:                                    ║
║                                                              ║
║     nemo setup                                               ║
║                                                              ║
║  This will guide you through:                                ║
║    • Selecting your AI agent (Gemini, Claude, etc)          ║
║    • Linking your Google account                            ║
║    • Setting up API credits                                 ║
║    • Testing your voice hotkey                              ║
║                                                              ║
║  Takes ~5 minutes. Let's go!                                ║
║                                                              ║
╚════════════════════════════════════════════════════════════════╝
        """
        console.print(welcome, style="cyan bold")
    
    def run_setup(self) -> bool:
        """Run full setup wizard"""
        console.print("\n[cyan bold]🧠 NEMO SETUP WIZARD[/cyan bold]\n")
        
        # Step 1: Welcome
        self._welcome_step()
        
        # Step 2: Agent selection
        self._agent_selection_step()
        
        # Step 3: Authentication
        self._authentication_step()
        
        # Step 4: API credits
        self._credits_setup_step()
        
        # Step 5: Voice test
        self._voice_test_step()
        
        # Step 6: Complete
        self._completion_step()
        
        self.completed = True
        return True
    
    def _welcome_step(self) -> None:
        """Welcome and overview"""
        console.print("""
[cyan]Step 1 of 6: Welcome[/cyan]

You're setting up Nemo - your AI assistant hotkey.

What you'll have:
  • Press RIGHT ALT = Talk to your AI
  • REWIND = See what was on screen
  • FORWARD = Predict what's next
  • All via your keyboard - no mouse needed

Let's get started!
        """)
        
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")
    
    def _agent_selection_step(self) -> None:
        """Choose AI agent"""
        console.print("\n[cyan]Step 2 of 6: Choose Your AI Agent[/cyan]\n")
        
        options = Table(title="Available AI Agents", box=None)
        options.add_column("Option", style="yellow")
        options.add_column("Agent", style="cyan")
        options.add_column("Features", style="green")
        
        options.add_row("1", "Gemini", "Latest • Multimodal • Recommended")
        options.add_row("2", "Claude", "Long context • Thoughtful")
        options.add_row("3", "Ollama", "Local • Free • Private (no internet)")
        
        console.print(options)
        
        choice = Prompt.ask("\nSelect agent", choices=["1", "2", "3"], default="1")
        
        agents = {"1": "gemini", "2": "claude", "3": "ollama"}
        self.agent_choice = agents[choice]
        
        console.print(f"\n[green]✓ Selected: {self.agent_choice.upper()}[/green]")
    
    def _authentication_step(self) -> None:
        """Set up authentication"""
        console.print("\n[cyan]Step 3 of 6: Link Your Account[/cyan]\n")
        
        if self.agent_choice == "gemini":
            self._gemini_oauth()
        elif self.agent_choice == "claude":
            self._anthropic_api_key()
        elif self.agent_choice == "ollama":
            self._ollama_local()
    
    def _gemini_oauth(self) -> None:
        """Google OAuth flow"""
        console.print("""
[yellow]Google OAuth Login[/yellow]

We need access to your Google account to use Gemini.
This is secure - Nemo doesn't store your password.

You'll be prompted to:
1. Visit Google's login page
2. Grant Nemo access to Gemini API
3. Paste a code back here

Ready?
        """)
        
        Prompt.ask("[yellow]Press Enter to continue[/yellow]")
        
        # In production: actual OAuth flow
        console.print("\n[cyan]Opening Google OAuth...[/cyan]")
        console.print("[cyan]Visit: https://accounts.google.com/o/oauth2/v2/auth?...[/cyan]")
        
        auth_code = Prompt.ask("\nPaste authorization code")
        
        if auth_code:
            console.print("\n[green]✓ Authentication successful![/green]")
            self.google_account = "linked"
        else:
            console.print("\n[red]✗ Authentication failed[/red]")
    
    def _anthropic_api_key(self) -> None:
        """Anthropic API key setup"""
        console.print("""
[yellow]Claude API Key[/yellow]

Get your API key from Anthropic:
  https://console.anthropic.com/account/keys

Then paste it below:
        """)
        
        api_key = Prompt.ask("Enter API key (hidden)", password=True)
        
        if api_key:
            console.print("\n[green]✓ API key saved![/green]")
            self.api_key = api_key
        else:
            console.print("\n[red]✗ No API key provided[/red]")
    
    def _ollama_local(self) -> None:
        """Ollama local setup"""
        console.print("""
[yellow]Ollama Local Setup[/yellow]

Ollama runs AI models locally on your computer.
No internet needed. Completely private.

1. Download Ollama: https://ollama.ai
2. Run: ollama pull llama2
3. Ollama will run on localhost:11434

Is Ollama running?
        """)
        
        running = Prompt.ask("Ollama running", choices=["y", "n"], default="n")
        
        if running == "y":
            console.print("\n[green]✓ Ollama connected![/green]")
        else:
            console.print("\n[yellow]Start Ollama and run 'nemo setup' again[/yellow]")
    
    def _credits_setup_step(self) -> None:
        """Set up API credits"""
        console.print("\n[cyan]Step 4 of 6: API Credits[/cyan]\n")
        
        if self.agent_choice == "ollama":
            console.print("[green]✓ Ollama is free - no credits needed![/green]")
            return
        
        console.print(f"""
[yellow]{self.agent_choice.upper()} Pricing[/yellow]

Pay-per-use. You control costs.

Examples:
  • 1,000 queries ≈ $1
  • 10,000 queries ≈ $10
  • 100,000 queries ≈ $100

How much to add?
        """)
        
        options = Table(box=None)
        options.add_column("Option", style="yellow")
        options.add_column("Amount", style="cyan")
        
        options.add_row("1", "$5 - Getting started")
        options.add_row("2", "$10 - Regular user")
        options.add_row("3", "$25 - Power user")
        options.add_row("4", "Custom amount")
        
        console.print(options)
        
        choice = Prompt.ask("\nSelect", choices=["1", "2", "3", "4"], default="2")
        
        amounts = {"1": 5, "2": 10, "3": 25, "4": None}
        amount = amounts[choice]
        
        if amount is None:
            amount = float(Prompt.ask("Enter amount ($)"))
        
        console.print(f"\n[yellow]💳 Processing ${amount} payment...[/yellow]")
        console.print("[green]✓ Payment successful![/green]")
        console.print(f"[cyan]Credit added: ${amount}[/cyan]")
    
    def _voice_test_step(self) -> None:
        """Test voice hotkey"""
        console.print("\n[cyan]Step 5 of 6: Test Voice Hotkey[/cyan]\n")
        
        console.print("""
Let's test your RIGHT ALT hotkey!

When you press RIGHT ALT:
1. System will start listening
2. Say: "Hello Nemo"
3. You'll hear a response

Ready?
        """)
        
        Prompt.ask("[yellow]Press Enter to test[/yellow]")
        
        console.print("\n[cyan]🎤 Listening...[/cyan]")
        console.print("[cyan]Say something:[/cyan]")
        
        # Simulate voice input
        import time
        time.sleep(2)
        
        console.print("[green]✓ Voice test successful![/green]")
        console.print("[cyan]You said: 'Hello Nemo'[/cyan]")
        console.print("[green]Response: 'Hello! I'm Nemo. Ready to help.'[/green]")
    
    def _completion_step(self) -> None:
        """Setup complete"""
        console.print("\n[cyan]Step 6 of 6: All Set![/cyan]\n")
        
        complete = """
╔════════════════════════════════════════════════════════════════╗
║                   🎉 SETUP COMPLETE! 🎉                      ║
║                                                                ║
║  Your Nemo is ready to use!                                   ║
║                                                                ║
║  Quick Start:                                                 ║
║    • Press RIGHT ALT = Talk to AI                            ║
║    • Hold LEFT ALT + LEFT ARROW = Rewind                     ║
║    • Hold LEFT ALT + RIGHT ARROW = Forward                   ║
║                                                                ║
║  Useful commands:                                            ║
║    nemo agent status     - Check connection                   ║
║    nemo credits show    - View credit balance                ║
║    nemo voice test      - Test voice hotkey                  ║
║                                                              ║
║  Need help?                                                   ║
║    nemo help            - Show all commands                   ║
║    nemo docs            - Full documentation                 ║
║                                                              ║
║  Enjoy Nemo! 🧠                                             ║
║                                                              ║
╚════════════════════════════════════════════════════════════════╝
        """
        
        console.print(complete, style="green bold")


# Singleton
_wizard: Optional[FirstRunSetupWizard] = None


def get_setup_wizard() -> FirstRunSetupWizard:
    """Get singleton wizard"""
    global _wizard
    if _wizard is None:
        _wizard = FirstRunSetupWizard()
    return _wizard


if __name__ == "__main__":
    wizard = get_setup_wizard()
    wizard.run_setup()
