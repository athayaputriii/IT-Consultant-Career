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


def detect_intent(message: str, confidence_threshold: int = 3):
    """
    Detects the main intent of the message using a keyword scoring system.
    This is more flexible than rigid regex.
    """
    message_lower = message.lower()
    scores = {}

    for intent, keywords in knowledge_base.intent_keywords.items():
        score = sum(weight for keyword, weight in keywords.items() if keyword in message_lower)
        scores[intent] = score
    
    # Find the intent with the highest score
    best_intent = max(scores, key=scores.get)
    
    # Return the intent only if it meets our confidence threshold
    if scores[best_intent] >= confidence_threshold:
        logging.info(f"Intent detected: '{best_intent}' with score {scores[best_intent]}. Scores: {scores}")
        return best_intent
    
    logging.info(f"No intent met threshold. Best score was '{best_intent}' with {scores[best_intent]}. Scores: {scores}")
    return None

def detect_entities(message: str):
    """Detects entities in the message using regex (which is great for this)."""
    detected_entities = {}
    message_lower = message.lower()
    
    for entity_type, patterns in knowledge_base.entity_patterns.items():
        for pattern in patterns:
            match = re.search(pattern, message_lower, re.IGNORECASE)
            if match:
                # Store the found entity value, normalized
                detected_entities[entity_type] = match.group(0).lower()
                break  # Stop after first match for this entity type
    return detected_entities

def get_career_response(intent: str, entities: dict):
    """
    Gets an appropriate response using a scalable and generic logic.
    """
    responses = knowledge_base.responses
    
    # Look for a specific response based on a detected entity
    if intent in responses:
        # Check if any detected entity has a specific response defined
        for entity_value in entities.values():
            if entity_value in responses[intent]:
                return random.choice(responses[intent][entity_value])
        
        # If no specific entity response was found, use the default for the intent
        if "default" in responses[intent]:
            return random.choice(responses[intent]["default"])
            
    # Ultimate fallback if intent has no responses defined at all
    logging.warning(f"No response found for intent '{intent}' and entities {entities}")
    return "I can help with IT careers, but I'm not sure how to answer that. Could you rephrase?"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    user_message = message.content
    
    # Detect intent and entities
    intent = detect_intent(user_message)
    
    if intent:
        entities = detect_entities(user_message)
        logging.info(f"Message: '{user_message}', Intent: '{intent}', Entities: {entities}")
        response = get_career_response(intent, entities)
        await message.channel.send(response)
    else:
        # If no intent is detected with enough confidence, provide generic help
        logging.info(f"Message: '{user_message}', Intent: None")
        await message.channel.send(
            "I'm here to help with IT career advice! You can ask me about:\n"
            "• **Career paths** (e.g., 'how to become a backend developer?')\n"
            "• **Technologies** (e.g., 'what is kubernetes?')\n"
            "• **Salaries** (e.g., 'how much do data scientists earn?')\n"
            "• **Certifications** and **Interview** prep."
        )

client.run(TOKEN)