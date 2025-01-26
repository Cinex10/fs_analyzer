import discord
from discord.ext import commands
from neo4j import Neo4jDriver
from neo4j import GraphDatabase
import discord
from discord.ext import commands
import networkx as nx
import matplotlib.pyplot as plt
import io
import os
from dotenv import load_dotenv

class Neo4jGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_graph(self):
        with self.driver.session() as session:
            # Query to get nodes and relationships
            result = session.run("""
                MATCH (n) RETURN n;
            """)
            
            G = nx.DiGraph()
            
            for record in result:
                source = record["n"]["name"]  # Adjust property as needed
                target = record["m"]["name"]
                G.add_edge(source, target)
            
            return G

# Initialize bot with command prefix '!'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='hello')
async def hello(ctx):
    """Responds with a greeting when user types !hello"""
    await ctx.send(f'Hello {ctx.author.name}!')

@bot.command(name='ping')
async def ping(ctx):
    """Check bot's latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')

@bot.event
async def on_message(message):
    # Don't respond to bot's own messages
    if message.author == bot.user:
        return

    # Process commands
    await bot.process_commands(message)

    # Respond to specific keywords
    if 'help' in message.content.lower():
        graph = Neo4jGraph("bolt://localhost:7687", "neo4j", "password")
        print('sdhj')
        # Get NetworkX graph
        G = graph.get_graph()
        
        # Create visualization
        plt.figure(figsize=(10, 8))
        nx.draw(G, with_labels=True, node_color='lightblue', 
                node_size=1500, arrowsize=20)
        
        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # Send image to Discord
        await message.channel.send(file=discord.File(buffer, 'graph.png'))
        
        plt.close()
        graph.close()

# Run the bot (replace with your bot token)
bot.run()
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot.run(BOT_TOKEN)