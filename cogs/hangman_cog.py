import disnake
import random
from disnake.ext import commands
from core.config import DISCORD_SERVER_ID
from pathlib import Path
import json

HANGMAN_PICS = [
    "```\n  +---+\n      |\n      |\n      |\n     ===\n```",
    "```\n  +---+\n  O   |\n      |\n      |\n     ===\n```",
    "```\n  +---+\n  O   |\n  |   |\n      |\n     ===\n```",
    "```\n  +---+\n  O   |\n /|   |\n      |\n     ===\n```",
    "```\n  +---+\n  O   |\n /|\\  |\n      |\n     ===\n```",
    "```\n  +---+\n  O   |\n /|\\  |\n /    |\n     ===\n```",
    "```\n  +---+\n  O   |\n /|\\  |\n / \\  |\n     ===\n```"
]

WORD_LIST = ["python", "discord", "hangman", "developer", "openai"]

BASE_DIR = Path(__file__).parent.parent
word_file_path = BASE_DIR / "data" / "German-words-5000-words.json"

with open(word_file_path, "r", encoding="utf-8") as f:
    WORD_LIST = json.load(f)


class GameSession:
    def __init__(self, word: str):
        self.word = word.lower()
        self.guessed = set()
        self.tries = 7

    def masked_word(self) -> str:
        """
        Returns the masked word with underscores between letters.
        Example: haus → _ _ _ _
        """
        return " ".join(c if c in self.guessed else "_" for c in self.word)

    def mask_word(self, word: str, guessed_letters: set):
        """
        Alternative masked-word helper if needed.
        """
        return " ".join(
            letter if letter.lower() in guessed_letters else "_"
            for letter in word.lower()
        )

    def guess(self, letter: str) -> bool:
        letter = letter.lower()
        self.guessed.add(letter)
        if letter not in self.word:
            self.tries -= 1
            return False
        return True

    def is_won(self):
        return all(c in self.guessed for c in self.word)

    def is_lost(self):
        return self.tries <= 0


class Hangman(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sessions = {}

    @commands.slash_command(description="Starte ein Hangman Spiel.", guild_ids=[int(DISCORD_SERVER_ID)])
    async def hangman(self, inter):
        pass

    @hangman.sub_command(description="Starte eine neue Runde Hangman.")
    async def start(self, inter: disnake.ApplicationCommandInteraction, word: str = None):
        if inter.channel.id in self.sessions:
            await inter.response.send_message("In diesem Channel läuft bereits ein Hangmanspiel!", ephemeral=True)
            return

        word = word.lower() if word else random.choice(WORD_LIST).lower()
        self.sessions[inter.channel.id] = GameSession(word)

        session = self.sessions[inter.channel.id]

        embed = disnake.Embed(
            title="Hangman gestartet!",
            description="Rate einen Buchstaben!",
            color=disnake.Color.blue()
        )
        embed.add_field(name="Word", value=session.masked_word(), inline=False)
        embed.add_field(name="Tries left", value=str(session.tries), inline=False)
        embed.add_field(name="Hangman", value=HANGMAN_PICS[0], inline=False)

        await inter.response.send_message(embed=embed)

    @hangman.sub_command(description="Errate einen Buchstaben!")
    async def guess(self, inter: disnake.ApplicationCommandInteraction, letter: str):
        if inter.channel.id not in self.sessions:
            await inter.response.send_message("Kein laufendes Spiel!", ephemeral=True)
            return

        session: GameSession = self.sessions[inter.channel.id]
        letter = letter.lower()

        if len(letter) != 1 or not letter.isalpha():
            await inter.response.send_message("Nur einzelne Buchstaben, Bro!", ephemeral=True)
            return

        if letter in session.guessed:
            await inter.response.send_message("Den Buchstaben hattest du schon!", ephemeral=True)
            return

        session.guess(letter)

        wrong_guesses = 7 - session.tries
        index = min(wrong_guesses, len(HANGMAN_PICS) - 1)

        embed = disnake.Embed(color=disnake.Color.orange())
        embed.add_field(name="Word", value=session.masked_word(), inline=False)
        embed.add_field(name="Tries left", value=str(session.tries), inline=False)
        embed.add_field(name="Hangman", value=HANGMAN_PICS[index], inline=False)

        if session.is_won():
            embed.title = "🎉 YOU WON!"
            embed.color = disnake.Color.green()
            await inter.response.send_message(embed=embed)
            del self.sessions[inter.channel.id]
            return

        if session.is_lost():
            embed.title = "💀 YOU LOST!"
            embed.color = disnake.Color.red()
            embed.add_field(name="Word was", value=session.word, inline=False)
            await inter.response.send_message(embed=embed)
            del self.sessions[inter.channel.id]
            return

        await inter.response.send_message(embed=embed)

    @hangman.sub_command(description="Stop the current game.")
    async def stop(self, inter: disnake.ApplicationCommandInteraction):
        if inter.channel.id not in self.sessions:
            await inter.response.send_message("Kein Spiel am Laufen!", ephemeral=True)
            return

        del self.sessions[inter.channel.id]
        await inter.response.send_message("Spiel gestoppt.")


def setup(bot):
    bot.add_cog(Hangman(bot))
