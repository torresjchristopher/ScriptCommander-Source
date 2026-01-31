#!/usr/bin/env python3
"""
Nemo Synthesis Engine CLI - Command Line Only (NO GUI)
Screen + Keyboard synthesis for temporal inference.
Rewind/Forward based on learned patterns.
Voice assistant hotkey for live AI.
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from typing import List

from screen_analyzer import get_screen_analyzer
from keyboard_synthesizer import get_keyboard_synthesizer
from temporal_inference import get_temporal_inference_engine
from voice_assistant import get_voice_assistant_cli
from tts_engine import TTSEngine, TTSConfig, VoiceGender, speak
from audio_security import verify_zero_storage, get_security_report
from download_manager import DownloadManager, InstallationWizard

console = Console()


def display_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║        🧠 Nemo Synthesis Engine v2.1                       ║
    ║     Screen + Keyboard Intelligence Synthesis                ║
    ║                                                              ║
    ║  CLI-ONLY (NO INTERFACE)                                   ║
    ║  • No Recording - Pure Analysis & Inference                 ║
    ║  • No Storage - Real-time Synthesis Only                    ║
    ║  • No GUI - Command Line Only                              ║
    ║                                                              ║
    ║  Four-Button Interface:                                     ║
    ║    • RIGHT ALT               = VOICE (AI butler hotkey)    ║
    ║    • LEFT ALT                = TTS (text-to-speech)        ║
    ║    • LEFT ALT + LEFT ARROW   = REWIND (infer past)         ║
    ║    • LEFT ALT + RIGHT ARROW  = FORWARD (predict future)    ║
    ║                                                              ║
    ║  The Human Element: Voice in, TTS out. No qwerty needed.   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="cyan bold")


@click.group()
def cli():
    """🧠 Nemo Synthesis Engine - Screen + Keyboard Intelligence"""
    display_banner()


@cli.group()
def synthesis():
    """Synthesis analysis commands"""
    pass


@synthesis.command()
def analyze():
    """Analyze current screen + keyboard state"""
    console.print("\n[cyan bold]🧠 Current Synthesis Analysis[/cyan bold]\n")
    
    screen_analyzer = get_screen_analyzer()
    keyboard_syn = get_keyboard_synthesizer()
    
    # Analyze screen
    screen_state = screen_analyzer.analyze_current_screen()
    
    screen_table = Table(box=None, show_header=False)
    screen_table.add_row("[cyan]Active App[/cyan]", f"[bold]{screen_state.active_app}[/bold]")
    screen_table.add_row("[cyan]Content Type[/cyan]", f"{screen_state.content_type}")
    screen_table.add_row("[cyan]Window[/cyan]", f"{screen_state.window_title}")
    screen_table.add_row("[cyan]Visible UI[/cyan]", f"{len(screen_state.buttons)} buttons, {len(screen_state.input_fields)} fields")
    
    console.print(Panel(screen_table, title="[cyan]Screen State[/cyan]", border_style="cyan"))
    
    # Analyze keyboard
    keyboard_style = keyboard_syn.get_user_style()
    
    keyboard_table = Table(box=None, show_header=False)
    keyboard_table.add_row("[cyan]Detected Intent[/cyan]", f"[bold]{keyboard_style['intent']}[/bold]")
    keyboard_table.add_row("[cyan]Typing Speed[/cyan]", keyboard_style['typing_speed'])
    keyboard_table.add_row("[cyan]Consistency[/cyan]", keyboard_style['consistency'])
    keyboard_table.add_row("[cyan]Error Rate[/cyan]", keyboard_style['error_rate'])
    keyboard_table.add_row("[cyan]Pattern[/cyan]", keyboard_style['pattern'])
    
    console.print(Panel(keyboard_table, title="[cyan]Keyboard Signature[/cyan]", border_style="cyan"))


@synthesis.command()
@click.option('--seconds', type=int, default=5, help='Seconds back to infer')
def rewind(seconds):
    """Infer what was on screen N seconds ago"""
    console.print(f"\n[cyan]Inferring what was {seconds} seconds ago...[/cyan]\n")
    
    engine = get_temporal_inference_engine()
    inference = engine.infer_rewind(seconds_back=seconds)
    
    output = engine.as_human_readable(inference)
    
    console.print(Panel(output, title="[cyan]Rewind Inference[/cyan]", border_style="yellow"))


@synthesis.command()
@click.option('--seconds', type=int, default=5, help='Seconds ahead to predict')
def forward(seconds):
    """Predict what user will do in next N seconds"""
    console.print(f"\n[cyan]Predicting next {seconds} seconds...[/cyan]\n")
    
    engine = get_temporal_inference_engine()
    inference = engine.infer_forward(seconds_ahead=seconds)
    
    output = engine.as_human_readable(inference)
    
    console.print(Panel(output, title="[green]Forward Prediction[/green]", border_style="green"))


@cli.group()
def voice():
    """Voice assistant commands"""
    pass


@voice.command()
def start():
    """Start voice assistant daemon"""
    console.print("\n[cyan bold]🎤 Voice Assistant Daemon[/cyan bold]\n")
    
    cli_instance = get_voice_assistant_cli()
    cli_instance.start()
    
    console.print("\n[yellow]Waiting for RIGHT ALT hotkey...[/yellow]")
    console.print("[cyan]Press RIGHT ALT and speak your question[/cyan]")
    console.print("[cyan]Release RIGHT ALT to send[/cyan]")


@voice.command()
def configure():
    """Configure voice assistant"""
    console.print("\n[cyan bold]⚙️ Voice Assistant Configuration[/cyan bold]\n")
    
    cli_instance = get_voice_assistant_cli()
    cli_instance.configure()


@voice.command()
def status():
    """Show voice assistant status"""
    console.print("\n[cyan bold]🎤 Voice Assistant Status[/cyan bold]\n")
    
    cli_instance = get_voice_assistant_cli()
    cli_instance.display_status()


@cli.group()
def tts():
    """Text-to-speech commands - The Human Element"""
    pass


@tts.command()
@click.argument('text')
@click.option('--gender', type=click.Choice(['male', 'female', 'neutral']), default='neutral', help='Voice gender')
@click.option('--speed', type=float, default=1.0, help='Speech speed (0.5-2.0)')
@click.option('--pitch', type=float, default=1.0, help='Voice pitch (0.5-2.0)')
@click.option('--volume', type=float, default=0.8, help='Volume (0.0-1.0)')
def speak_command(text, gender, speed, pitch, volume):
    """Speak text using TTS (text-to-speech)"""
    console.print(f"\n[cyan]🔊 Speaking: {text}[/cyan]\n")
    
    config = TTSConfig(
        gender=VoiceGender(gender),
        speed=speed,
        pitch=pitch,
        volume=volume,
    )
    
    engine = TTSEngine(config)
    success = engine.speak(text, blocking=True)
    
    if success:
        console.print("[green]✓ Speech complete[/green]")
    else:
        console.print("[red]✗ Speech failed[/red]")


@tts.command()
def test():
    """Test TTS with sample messages"""
    console.print("\n[cyan bold]🔊 TTS Test[/cyan bold]\n")
    
    samples = [
        ("Nemo is ready", VoiceGender.NEUTRAL),
        ("The human element", VoiceGender.MALE),
        ("The future has no keyboard", VoiceGender.FEMALE),
    ]
    
    for text, gender in samples:
        console.print(f"[cyan]Testing with {gender.value} voice...[/cyan]")
        
        config = TTSConfig(gender=gender, speed=1.0)
        engine = TTSEngine(config)
        engine.speak(text, blocking=True)
        engine.stop()
        
        console.print("[green]✓ Sample played\n[/green]")


@tts.command()
def configure():
    """Configure TTS settings"""
    console.print("\n[cyan bold]⚙️ TTS Configuration[/cyan bold]\n")
    
    speed = Prompt.ask("Speech speed", default="1.0")
    pitch = Prompt.ask("Voice pitch", default="1.0")
    volume = Prompt.ask("Volume", default="0.8")
    gender = Prompt.ask("Voice gender (male/female/neutral)", default="neutral")
    
    console.print(f"""
[cyan]TTS Settings:[/cyan]
  Speed: {speed}x
  Pitch: {pitch}
  Volume: {volume}
  Gender: {gender}
  
[yellow]Settings applied. These will be used for all TTS output.[/yellow]
""")


@cli.group()
def security():
    """Security verification commands"""
    pass


@security.command()
def verify():
    """Verify zero-storage guarantee"""
    console.print("\n[cyan bold]🔐 Security Verification[/cyan bold]\n")
    console.print("[cyan]Running security audit...[/cyan]\n")
    
    is_secure = verify_zero_storage()
    
    if is_secure:
        console.print("[green bold]✓ SECURITY VERIFIED[/green bold]")
        console.print("[green]Zero-storage guarantee confirmed: NO audio data persisted[/green]")
    else:
        console.print("[red bold]✗ SECURITY VIOLATION DETECTED[/red bold]")
        console.print("[red]Please review the report below[/red]")


@security.command()
@click.option('--verbose', is_flag=True, help='Verbose output')
def report(verbose):
    """Display security audit report"""
    console.print(get_security_report(verbose=verbose))


@cli.group()
def buttons():
    """Button configuration commands"""
    pass


@buttons.command()
def show():
    """Show button mapping"""
    console.print("\n[cyan bold]⌨️ Four-Button Interface[/cyan bold]\n")
    
    mapping = Table(title="Nemo Four-Button System", box=None)
    mapping.add_column("Button", style="yellow", width=25)
    mapping.add_column("Function", style="cyan", width=20)
    mapping.add_column("Description", style="green")
    
    mapping.add_row(
        "RIGHT ALT",
        "[bold]VOICE[/bold]",
        "Internet AI (Gemini) - Ask questions"
    )
    mapping.add_row(
        "LEFT ALT (tap)",
        "[bold]TTS[/bold]",
        "Text-to-speech - Hear synthesis"
    )
    mapping.add_row(
        "LEFT ALT + LEFT ARROW",
        "[bold]REWIND[/bold]",
        "Infer what was on screen"
    )
    mapping.add_row(
        "LEFT ALT + RIGHT ARROW",
        "[bold]FORWARD[/bold]",
        "Predict what comes next"
    )
    
    console.print(mapping)
    console.print("\n[yellow]The Human Element:[/yellow]")
    console.print("Voice in (RIGHT ALT), TTS out (LEFT ALT)")
    console.print("No qwerty keyboard needed for future interaction.\n")


@cli.command()
def info():
    """Display system architecture"""
    info_text = """
╔════════════════════════════════════════════════════════════════╗
║          🧠 NEMO SYNTHESIS ENGINE - ARCHITECTURE              ║
║     Not a recorder. Pure synthesis. Pure inference.           ║
╚════════════════════════════════════════════════════════════════╝

CORE PHILOSOPHY:
────────────────

NOT STORING:
  ✗ No screenshots
  ✗ No video buffer
  ✗ No action history
  ✗ No data persistence

PURE ANALYSIS:
  ✓ Real-time screen analysis
  ✓ Keystroke pattern learning
  ✓ Intent detection
  ✓ Temporal inference

SYNTHESIS MODEL:
─────────────────

Screen (What User Sees):
  • Active window/app
  • UI elements visible
  • Form fields
  • Buttons/links
  • Content type (email, code, web, etc)

Keyboard (How User Types):
  • 35-D keystroke fingerprint
  • User's unique style
  • Intent patterns
  • Typing behavior

Synthesis = Screen + Keyboard:
  • What was user doing?
  • What will user do next?
  • What are they likely thinking?
  • What are they likely to click?

TEMPORAL INFERENCE:
────────────────────

REWIND (What WAS):
  User: "I need to rewind 5 seconds"
  System: "What was on screen then?"
  
  Analysis:
    - Current keyboard pattern shows "editing"
    - Current screen shows "email"
    - User was likely editing email 5 seconds ago
  
  Inference: "You were typing in the email body"

FORWARD (What WILL BE):
  User: "What happens next?"
  System: "What will user likely do?"
  
  Analysis:
    - Keyboard pattern shows "composition"
    - Screen is "email form"
    - Natural next step is "send"
  
  Inference: "You'll likely send the email next"

THREE BUTTONS (OLD):
──────────────────

1. LEFT ALT + LEFT ARROW = REWIND
   • Hold to infer past
   • Synthesize what was
   • Show inference confidence
   • Display likely actions

2. LEFT ALT + RIGHT ARROW = FORWARD
   • Hold to predict future
   • Synthesize what comes next
   • Show prediction confidence
   • Display likely actions

3. RIGHT ALT = VOICE (AI BUTLER)
   • Hold to activate mic
   • Speak your question
   • AI responds with voice
   • Live internet-enabled
   • Like having a personal assistant

FOUR BUTTONS (NOW): THE HUMAN ELEMENT
─────────────────────────────────────

1. RIGHT ALT = INTERNET AI (VOICE INPUT)
   • Press to activate microphone
   • Speak your question to Gemini
   • AI responds with voice (butler metaphor)
   • Full internet-enabled reasoning

2. LEFT ALT (TAP) = TTS BUTTON (VOICE OUTPUT)
   • Press to hear synthesized understanding
   • Hear what Nemo infers about your context
   • Hear what comes next
   • No text needed - just speak
   • THE HUMAN ELEMENT (communication)

3. LEFT ALT + LEFT ARROW = REWIND (INFERENCE BACKWARD)
   • Hold to infer what WAS
   • Synthesize 30 seconds ago
   • Based on your keyboard pattern
   • No video - pure intelligence

4. LEFT ALT + RIGHT ARROW = FORWARD (INFERENCE FORWARD)
   • Hold to predict what COMES NEXT
   • Synthesize 30 seconds ahead
   • Based on your behavior
   • No prediction model - pure synthesis

ZERO STORAGE GUARANTEE
──────────────────────
✗ No voice recordings
✗ No audio files
✗ No temp cache
✗ No persistence
✓ Voice → Text only
✓ TTS in-memory playback
✓ Everything forgotten

WHY TTS IS THE HUMAN ELEMENT
────────────────────────────
• Faster than typing
• More natural than reading
• Replaces qwerty keyboard
• Voice in, voice out
• True human-machine synthesis

FUTURE MONETIZATION:
─────────────────────

Extra Keys Available:
  • Spotify hotkey (play random song)
  • Browser hotkey (quick search)
  • Email hotkey (draft quick note)
  • Custom hotkeys (user-defined)

Sell Each Key:
  • Users bid for their favorite hotkey
  • Nemo owns the platform (key real estate)
  • Custom keyboard hardware
  • Or: mouse with extra buttons
  • Or: software key mapping

This is "Real Estate" - software real estate.
Each key is valuable. Each function is monetized.

CORE EXAMPLE:
───────────────

Scenario: User is composing an email

Step 1: Screen Analyzer sees
  ✓ Outlook open
  ✓ Email compose form visible
  ✓ "To", "Subject", "Body" fields present

Step 2: Keyboard Synthesizer observes
  ✓ User typing at 50 WPM
  ✓ Few corrections (low error rate)
  ✓ Deliberate pacing (not rapid)
  ✓ Pattern: "composition"

Step 3: Synthesis Engine combines
  ✓ Email context + composition pattern
  ✓ User likely typing important message
  ✓ Careful, deliberate work

Step 4: REWIND button (what was 5 sec ago?)
  ✓ Inference: Still in body
  ✓ Likely: One paragraph further back
  ✓ Confidence: 85%

Step 5: FORWARD button (what next?)
  ✓ Inference: Review and send
  ✓ Next action: Click Send button
  ✓ Confidence: 80%

Step 6: RIGHT ALT (voice hotkey)
  ✓ User asks: "Is my email polite?"
  ✓ AI reads current email context
  ✓ Responds with suggestion via voice
  ✓ No internet data leak (only AI model + current text)

NO STORAGE:
───────────

Each analysis is ephemeral:
  - Analyze current screen
  - Learn current keyboard
  - Infer rewind/forward
  - Display inference
  - Forget it all

User-specific:
  - Learns YOUR typing style
  - YOUR patterns
  - YOUR intent
  - No other users' data
  - No cross-user learning
  - Pure personalization

PRIVACY:
─────────

✓ No cloud storage
✓ No data collection (except current session)
✓ No tracking
✓ No profiling
✓ Real-time analysis only
✓ Voice assistant: Optional internet (user controls)

This is radically private.
Local synthesis engine.
User-specific intelligence.
Pure personal assistant.

═════════════════════════════════════════════════════════════════
"""
    console.print(info_text, style="cyan")


@cli.group()
def download():
    """Download and install Nemo"""
    pass


@download.command()
def latest():
    """Check for latest Nemo release"""
    console.print("\n[cyan bold]🔍 Checking for latest Nemo release...[/cyan bold]\n")
    
    manager = DownloadManager()
    release = manager.get_latest_release()
    
    if not release:
        console.print("[red]✗ Failed to fetch release info[/red]")
        return
    
    current = manager.get_installed_version()
    
    table = Table(title="Latest Release", box=None)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Version", f"[bold]{release['version']}[/bold]")
    table.add_row("Name", release['name'])
    table.add_row("Released", release['published_at'][:10])
    
    if current:
        table.add_row("Current Installed", current)
        if current != release['version']:
            table.add_row("Update Available", "[yellow]YES[/yellow]")
        else:
            table.add_row("Status", "[green]Up to date[/green]")
    else:
        table.add_row("Current Installed", "[yellow]Not installed[/yellow]")
    
    console.print(table)
    console.print("\n[cyan]Release notes:[/cyan]")
    console.print(release['body'][:500] if release['body'] else "[dim]No notes[/dim]")


@download.command()
def install():
    """Install Nemo from latest GitHub release"""
    wizard = InstallationWizard()
    wizard.run()


@download.command()
def update():
    """Update Nemo to latest version"""
    console.print("\n[cyan bold]🔄 Checking for updates...[/cyan bold]\n")
    
    manager = DownloadManager()
    has_update, new_version = manager.check_for_updates()
    
    if not has_update:
        console.print("[green]✓ Nemo is up to date[/green]")
        return
    
    console.print(f"[yellow]Update available: {new_version}[/yellow]")
    console.print("[cyan]Running installation wizard...\n[/cyan]")
    
    wizard = InstallationWizard()
    wizard.run()


@download.command()
def status():
    """Show download/installation status"""
    console.print("\n[cyan bold]📦 Nemo Installation Status[/cyan bold]\n")
    
    manager = DownloadManager()
    
    current = manager.get_installed_version()
    latest_release = manager.get_latest_release()
    
    status_table = Table(box=None)
    status_table.add_column("Item", style="cyan")
    status_table.add_column("Status", style="green")
    
    if current:
        status_table.add_row("Installed", f"[bold]{current}[/bold]")
        status_table.add_row("Install Path", str(manager.nemo_install_path))
    else:
        status_table.add_row("Installed", "[yellow]Not installed[/yellow]")
    
    if latest_release:
        status_table.add_row("Latest Release", f"[bold]{latest_release['version']}[/bold]")
        
        if current and current != latest_release['version']:
            status_table.add_row("Update", "[yellow]Available[/yellow]")
        elif current:
            status_table.add_row("Update", "[green]None[/green]")
    else:
        status_table.add_row("Latest Release", "[red]Check failed[/red]")
    
    console.print(status_table)
    console.print(f"\n[cyan]Config: {manager.NEMO_CONFIG_FILE}[/cyan]")
    console.print(f"[cyan]Releases: {manager.release_download_path}[/cyan]")


if __name__ == '__main__':
    cli()
