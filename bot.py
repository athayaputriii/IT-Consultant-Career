import os
from dotenv import load_dotenv
import discord
import re
import random
import logging
import knowledge_base

# Logging
logging.basicConfig(
    filename="logs/it_career_bot.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Load Bot's Token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def detect_intent(message: str):
    """Detect the main intent of the message"""
    # Reference the variable from the knowledge file
    for intent_name, patterns in knowledge_base.intent_patterns.items():
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return intent_name
    return None

def detect_entities(message: str):
    """Detect entities in the message"""
    detected_entities = {}
    # Reference the variable from the knowledge file
    for entity_type, patterns in knowledge_base.entity_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                detected_entities[entity_type] = match.group()
                break  # Stop after first match for this entity type
    return detected_entities

def get_career_response(intent: str, entities: dict):
    """Get appropriate response based on intent and entities"""
    role = entities.get('role')
    technology = entities.get('technology')
    experience = entities.get('experience_level')
    
    # Reference the variable from the knowledge file
    responses = knowledge_base.responses

    # Check for specific role or technology responses
    if intent == "career_path" and role:
        role_responses = responses.get("career_path", {}).get(role.lower())
        if role_responses:
            return random.choice(role_responses)
    
    if intent == "technology" and technology:
        tech_responses = responses.get("technology", {}).get(technology.lower())
        if tech_responses:
            return random.choice(tech_responses)
    
    # Fallback to default responses for the intent
    default_responses = responses.get(intent, {}).get("default")
    if default_responses:
        return random.choice(default_responses)
    
    # Ultimate fallback
    return "That's an interesting question about IT careers! Could you provide more details so I can give you better advice?"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Process the message
    user_message = message.content.lower()
    
    # Detect intent and entities
    intent = detect_intent(user_message)
    entities = detect_entities(user_message)
    
    if intent:
        response = get_career_response(intent, entities)
        await message.channel.send(response)
    else:
        # If no intent detected, provide generic help
        await message.channel.send(
            "I'm here to help with IT career advice! You can ask me about:\n"
            "• Career paths (how to become a developer, engineer, etc.)\n"
            "• Technologies to learn (Python, JavaScript, AWS, etc.)\n"
            "• Salaries and job market trends\n"
            "• Certifications and interview preparation\n"
            "Try asking something like: 'How to become a cloud engineer?' or 'Should I learn React or Vue?'"
        )

client.run(TOKEN)