import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from tmdbv3api import TMDb, Movie
from collections import defaultdict
import asyncio

# Initialize TMDb API
tmdb = TMDb()
tmdb.api_key = 'b76f443625dcf981f3660aae01ffa3dc'
movie = Movie()

# Genre Mapping
GENRE_MAPPING = {
    'Action': 28,
    'Adventure': 12,
    'Animation': 16,
    'Comedy': 35,
    'Crime': 80,
    'Documentary': 99,
    'Drama': 18,
    'Family': 10751,
    'Fantasy': 14,
    'History': 36,
    'Horror': 27,
    'Music': 10402,
    'Mystery': 9648,
    'Romance': 10749,
    'Science Fiction': 878,
    'TV Movie': 10770,
    'Thriller': 53,
    'War': 10752,
    'Western': 37
}

# Function to search movies
def search_movies(genre_id=None, sort_by='popularity.desc'):
    results = movie.popular()
    if genre_id:
        filtered_results = [m for m in results if genre_id in m.genre_ids]
        results = filtered_results
    
    # Sort results based on the specified criteria
    if sort_by == 'popularity.desc':
        results = sorted(results, key=lambda x: x.popularity, reverse=True)
    elif sort_by == 'vote_count.desc':
        results = sorted(results, key=lambda x: x.vote_count, reverse=True)
    elif sort_by == 'vote_average.desc':
        results = sorted(results, key=lambda x: x.vote_average, reverse=True)
    
    return results

# Helper function to get genre ID
def get_genre_id(genre_name):
    return GENRE_MAPPING.get(genre_name)

# Bot Class
class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(self.token).build()
        self.user_stats = defaultdict(int)

    async def start(self, update: Update, context):
        user_id = update.effective_chat.id
        self.user_stats[user_id] += 1
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your bot. How can I help you?")

    async def help(self, update: Update, context):
        help_text = """
        Available Commands:
        /start - Start interacting with the bot
        /help - Display this help message
        /weather <city> - Get weather information for a specific city
        /joke - Get a random joke
        /news - Get the latest news headlines
        /movies <genre> - Search for movies by genre
        """
        await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

    async def movies(self, update: Update, context):
        genre_name = ' '.join(context.args)
        if not genre_name:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Please specify a genre.")
            return

        genre_id = get_genre_id(genre_name)

        if genre_id:
            trending_movies = search_movies(genre_id=genre_id, sort_by='popularity.desc')
            message = "Trending Movies:\n"
            message += "\n".join([f"{m.title} ({m.release_date.split('-')[0]})" for m in trending_movies])
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Genre '{genre_name}' not found.")

    def setup_handlers(self):
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('help', self.help))
        self.application.add_handler(CommandHandler('movies', self.movies))

    async def run(self):
        self.setup_handlers()
        await self.application.run_polling()  # Start polling to listen for updates

async def main():
    bot = TelegramBot(token='7510427301:AAEpmzXzcTaGQ479m4Lx8AlVvuO1t-CAorU')
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
