import os
import random
import discord
from discord.ext import commands
from googletrans import Translator
# 20 official Magic 8-Ball answers
EIGHT_BALL_ANSWERS = [
    # Positive
    "It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes – definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    # Negative
    "Don’t count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful.",
    # Non-committal
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again."
]

# Intents

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} commands globally")
    except Exception as e:
        print(f"❌ Sync error: {e}")
    print(f"Logged in as {bot.user}")

# 8ball command
@bot.command(name="8ball")
async def eight_ball(ctx, *, question: str = None):
    if not question:
        await ctx.send("🎱 Асуултаа асуу, жишээ: `!8ball Am I Really GAY?`")
        return
    
    # Check if the question ends with "yes or no"
    if question.strip().lower().endswith("yes or no"):
        answer = random.choice(["Yes.", "No."])
    else:
        answer = random.choice(EIGHT_BALL_ANSWERS)
    
    await ctx.send(f"🎱 {answer}")

# Calculator command
@bot.command(name="calc")
async def calc(ctx, *, expression: str):
    """
    Simple math calculator: + - * / ^
    Usage: !calc 2+3*4
    """
    try:
        # Replace ^ with ** for power operation
        expression = expression.replace("^", "**")

        # Allow only safe characters
        allowed = "0123456789+-*/().** "
        if not all(ch in allowed for ch in expression):
            await ctx.send("❌ Юу шаагаад бган зөв бич!!")
            return

        result = eval(expression)
        # Format result: remove unnecessary decimals
        if isinstance(result, float):
            # Round to 10 decimal places, then strip trailing zeros
            result = f"{result:.10f}".rstrip("0").rstrip(".")
        await ctx.send(f"📊 Хариу: `{result}`")

    except Exception as e:
        await ctx.send(f"⚠️ Юу аашаад бган!: {str(e)}")

translator = Translator()
# Slash command: /translate
@bot.tree.command(name="translate", description="Translate text into another language")
async def translate(interaction: discord.Interaction, target_lang: str, *, text: str):
    try:
        result = translator.translate(text, dest=target_lang)
        await interaction.response.send_message(
            f"🌍 **Translated to {target_lang}**:\n{result.text}"
        )
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Error: {e}")

# Run bot
bot.run(os.getenv("DISCORD_TOKEN"))
