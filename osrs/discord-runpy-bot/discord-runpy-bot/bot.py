import os
import sys
import asyncio
import shlex
from pathlib import Path
import io
import traceback

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Configuration (can be overridden via environment variables)
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # required
GUILD_ID = os.getenv("DISCORD_GUILD_ID")  # optional: restrict command sync to a single guild for faster updates
SCRIPTS_DIR = Path(os.getenv("SCRIPTS_DIR", "scripts")).resolve()
MAX_RUN_SECONDS = int(os.getenv("MAX_RUN_SECONDS", "60"))
PYTHON_EXECUTABLE = os.getenv("PYTHON_EXECUTABLE", sys.executable)

intents = discord.Intents.default()
# message_content is not needed for slash commands; we keep defaults minimal for safety.

class RunPyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
        )
        self.run_lock = asyncio.Lock()  # keep your lock

    async def setup_hook(self):
        # Use the existing tree: self.tree
        # if GUILD_ID:
        #     guild = discord.Object(id=int(GUILD_ID))
        #     # copy global commands into the guild and sync for fast registration
        #     self.tree.copy_global_to(guild=guild)
        #     synced = await self.tree.sync(guild=guild)
        #     print(f"Synced {len(synced)} commands to guild {GUILD_ID}")
        # else:
        synced = await self.tree.sync()
        print(f"Globally synced {len(synced)} commands")

bot = RunPyBot()  # no CommandTree here, use bot.tree below


def list_scripts():
    if not SCRIPTS_DIR.exists():
        return []
    return sorted(
        [
            str(p.relative_to(SCRIPTS_DIR)).replace(os.sep, "/")
            for p in SCRIPTS_DIR.rglob("*.py")
            if p.is_file()
        ]
    )

def resolve_script(script_name: str) -> Path:
    base = SCRIPTS_DIR
    candidate = (base / script_name).with_suffix(".py") if not script_name.endswith(".py") else base / script_name
    resolved = candidate.resolve()
    # Ensure the resolved path stays under SCRIPTS_DIR and is a .py file
    if not str(resolved).startswith(str(base)) or resolved.suffix != ".py":
        raise ValueError("Invalid script path.")
    if not resolved.exists():
        raise FileNotFoundError(f"Script not found: {resolved.relative_to(base)}")
    return resolved

async def run_python_script(resolved_path: Path, args: list[str]):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"  # force UTF-8 text I/O
    env["PYTHONUTF8"] = "1"            # enable UTF-8 mode (Python 3.7+)

    process = await asyncio.create_subprocess_exec(
        PYTHON_EXECUTABLE,
        str(resolved_path),
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(SCRIPTS_DIR),
        env=env,                         # <<< add this
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=MAX_RUN_SECONDS)
        code = process.returncode
    except asyncio.TimeoutError:
        try:
            process.kill()
        except ProcessLookupError:
            pass
        return (124, b"", f"Timed out after {MAX_RUN_SECONDS}s".encode())

    return (code, stdout, stderr)

def format_output(code: int, stdout: bytes, stderr: bytes) -> tuple[str, io.BytesIO | None]:
    MAX_MESSAGE = 1900  # leave headroom within Discord's 2000-char limit
    out = stdout.decode("utf-8", errors="replace")
    err = stderr.decode("utf-8", errors="replace")

    body = []
    body.append(f"**Exit code:** `{code}`")
    if out.strip():
        body.append("**stdout**:")
        body.append(f"```text\n{out}\n```")
    if err.strip():
        body.append("**stderr**:")
        body.append(f"```text\n{err}\n```")
    message = "\n".join(body)

    if len(message) <= MAX_MESSAGE:
        return (message, None)

    # Too long: send a short summary + attach full logs as a file
    summary = f"**Exit code:** `{code}`\nOutput too long — attached as file."
    content = f"=== stdout ===\n{out}\n\n=== stderr ===\n{err}\n"
    buf = io.BytesIO(content.encode("utf-8"))
    buf.name = "runpy_output.txt"
    return (summary, buf)

# -------------- Slash commands --------------

@bot.tree.command(name="listscripts", description="List runnable Python scripts in the configured scripts directory.")
async def listscripts(interaction: discord.Interaction):
    scripts = list_scripts()
    if not scripts:
        await interaction.response.send_message(f"No scripts found in `{SCRIPTS_DIR}`.")
        return
    formatted = "\n".join(f"- `{s}`" for s in scripts[:50])
    extra = "" if len(scripts) <= 50 else f"\n…and {len(scripts) - 50} more"
    await interaction.response.send_message(f"**Scripts in** `{SCRIPTS_DIR}`:\n{formatted}{extra}")

@bot.tree.command(name="runpy", description="Run a Python script from your server-side scripts directory.")
@app_commands.describe(
    script="Relative path/name under the scripts directory (with or without .py)",
    args="Optional arguments separated by spaces (quoted if they contain spaces)",
)
async def runpy(interaction: discord.Interaction, script: str, args: str | None = None):
    await interaction.response.defer(thinking=True)

    # Parse args safely using shlex
    argv = shlex.split(args) if args else []

    try:
        resolved = resolve_script(script)
    except Exception as e:
        await interaction.followup.send(f"❌ {e}")
        return

    # Prevent overlapping runs if desired
    async with bot.run_lock:
        code, stdout, stderr = await run_python_script(resolved, argv)

    message, attachment = format_output(code, stdout, stderr)
    if attachment:
        await interaction.followup.send(message, file=discord.File(attachment))
    else:
        await interaction.followup.send(message)

@runpy.autocomplete("script")
async def script_autocomplete(interaction: discord.Interaction, current: str):
    choices = [app_commands.Choice(name=s, value=s) for s in list_scripts() if current.lower() in s.lower()][:25]
    return choices

# -------------- Entrypoint --------------

def main():
    if not TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN is not set. Put it in your environment or .env file.", file=sys.stderr)
        raise SystemExit(2)
    # Ensure scripts dir exists
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
