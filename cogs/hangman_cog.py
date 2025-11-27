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

STATS_FILE = BASE_DIR / "data" / "hangman_stats.json"

def load_stats():
    if not STATS_FILE.exists():
        return {}
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

def ensure_user(stats, user_id: int):
    user_id = str(user_id)
    if user_id not in stats:
        stats[user_id] = {
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0,
            "letters_guessed": 0,
            "correct_letters": 0,
            "wrong_letters": 0,
            "points_total": 0,
        }
    return stats[user_id]

def get_leaderboard(sort_by="points_total", limit=10):
    stats = load_stats()

    if not stats:
        return []

    # sortiere Spieler
    sorted_players = sorted(
        stats.items(),
        key=lambda x: x[1].get(sort_by, 0),
        reverse=True
    )

    return sorted_players[:limit]


class GameSession:
    def __init__(self, word: str):
        self.word = word.lower()
        self.guessed = set()
        self.tries = 7
        self.players = {}

    def masked_word(self) -> str:
        masked = " ".join(c if c in self.guessed else r"\_" for c in self.word)
        return masked

    def add_point(self, user_id: int):
        """Adds a point to a player"""
        if user_id not in self.players:
            self.players[user_id] = 0
        self.players[user_id] +=1
            
    def guess(self, letter: str, user_id: int) -> bool:
        """Returns True if guess was correct."""
        letter = letter.lower()
        self.guessed.add(letter)

        if letter in self.word:
            self.add_point(user_id)
            return True

        self.tries -= 1
        return False

    def is_won(self):
        return all(c in self.guessed for c in self.word)

    def is_lost(self):
        return self.tries <= 0
    
    def leaderboard(self):
        """Returns a sorted scoreboard."""
        if not self.players:
            return "Keine Punkte vergeben."
        sorted_players = sorted(self.players.items(), key=lambda x: x[1], reverse=True)
        text = ""
        for uid, score in sorted_players:
            text += f"<@{uid}> — **{score} Punkte**\n"
        return text


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

        correct = session.guess(letter, inter.author.id)
        stats = load_stats()
        user_stats = ensure_user(stats, inter.author.id)

        user_stats["letters_guessed"] += 1
        if correct:
            user_stats["correct_letters"] += 1
        else:
            user_stats["wrong_letters"] += 1

        save_stats(stats)
        wrong_guesses = 7 - session.tries
        index = min(wrong_guesses, len(HANGMAN_PICS) - 1)

        embed = disnake.Embed(color=disnake.Color.orange())
        embed.add_field(name="Word", value=session.masked_word(), inline=False)
        embed.add_field(name="Tries left", value=str(session.tries), inline=False)
        embed.add_field(name="Hangman", value=HANGMAN_PICS[index], inline=False)

        if session.is_won():
            stats = load_stats()
            for uid in session.players:
                user_stats = ensure_user(stats, uid)
                user_stats["games_played"] += 1
                user_stats["games_won"] += 1
                user_stats["points_total"] += session.players[uid]
            save_stats(stats)

            embed.title = "🎉 Alle haben das Wort erraten!"
            embed.color = disnake.Color.green()
            embed.add_field(name="🏆 Punkte", value=session.leaderboard(), inline=False)
            await inter.response.send_message(embed=embed)
            del self.sessions[inter.channel.id]
            return

        if session.is_lost():
            stats = load_stats()
            for uid in session.players:
                user_stats = ensure_user(stats, uid)
                user_stats["games_played"] += 1
                user_stats["games_lost"] += 1
                user_stats["points_total"] += session.players[uid]
            save_stats(stats)

            embed.title = "💀 Ihr habt verloren!"
            embed.color = disnake.Color.red()
            embed.add_field(name="Wort war", value=session.word, inline=False)
            embed.add_field(name="🏆 Punkte", value=session.leaderboard(), inline=False)
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
        
    @hangman.sub_command(description="Zeige deine Hangman-Statistiken.")
    async def stats(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member = None):
        user = user or inter.author

        stats = load_stats()
        user_data = stats.get(str(user.id))

        if not user_data:
            await inter.response.send_message(f"{user.mention} hat noch keine Statistik!")
            return

        embed = disnake.Embed(
            title=f"📊 Hangman Statistik für {user.name}",
            color=disnake.Color.blurple()
        )

        embed.add_field(name="Gespielte Spiele", value=user_data["games_played"])
        embed.add_field(name="Gewonnen", value=user_data["games_won"])
        embed.add_field(name="Verloren", value=user_data["games_lost"])
        embed.add_field(name="Geratene Buchstaben", value=user_data["letters_guessed"])
        embed.add_field(name="Richtig", value=user_data["correct_letters"])
        embed.add_field(name="Falsch", value=user_data["wrong_letters"])
        embed.add_field(name="Punkte insgesamt", value=user_data["points_total"])

        await inter.response.send_message(embed=embed)
        
    @hangman.sub_command(description="Zeige das globale Hangman-Leaderboard.")
    async def leaderboard(self,inter: disnake.ApplicationCommandInteraction,
        sort_by: str = commands.Param(
            choices=["points_total", "games_won", "games_played"],
            default="points_total",
            description="Sortierung des Leaderboards"
            )):
        board = get_leaderboard(sort_by)

        if not board:
            await inter.response.send_message("Noch keine Statistiken vorhanden!")
            return

        embed = disnake.Embed(
            title="🏆 Globales Hangman Leaderboard",
            description=f"Sortiert nach: **{sort_by.replace('_', ' ').title()}**",
            color=disnake.Color.gold()
        )

        placement = 1
        for user_id, data in board:
            uid = int(user_id)
            username = None

            # 1) Try guild member → best case
            member = inter.guild.get_member(uid)
            if member:
                username = member.display_name

            # 2) Try bot user cache
            if username is None:
                user = inter.bot.get_user(uid)
                if user:
                    username = user.display_name if hasattr(user, "display_name") else user.name

            # 3) Try API fetch
            if username is None:
                try:
                    fetched = await inter.bot.fetch_user(uid)
                    username = fetched.display_name if hasattr(fetched, "display_name") else fetched.name
                except:
                    username = f"User {uid}"

            value = data.get(sort_by, 0)
            embed.add_field(
                name=f"#{placement} — @{username}",
                value=(
                    f"Punkte: **{data['points_total']}**\n"
                    f"Wins: **{data['games_won']}**\n"
                    f"Games: **{data['games_played']}**"
                ),
                inline=False
            )

            placement += 1

        await inter.response.send_message(embed=embed)




def setup(bot):
    bot.add_cog(Hangman(bot))
