import os
import random
import discord
from discord.ext import commands

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
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="8ball")
async def eight_ball(ctx, *, question: str = None):
    if not question:
        await ctx.send("🎱 You need to ask a question, e.g. `!8ball Will I be lucky today?`")
        return
    
    # Check if the question ends with "yes or no"
    if question.strip().lower().endswith("yes or no"):
        answer = random.choice(["Yes.", "No."])
    else:
        answer = random.choice(EIGHT_BALL_ANSWERS)
    
    await ctx.send(f"🎱 {answer}")

bot.run(os.getenv("DISCORD_TOKEN"))
