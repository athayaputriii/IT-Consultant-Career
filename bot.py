import os
from dotenv import load_dotenv
import discord
import re
import random
import logging
import knowledge_base

logging.basicConfig(
    filename="logs/it_career_bot.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def detect_intents(message: str, confidence_threshold: int = 3) -> list[str]:
    """
    Detects ALL intents that meet the threshold and returns them as a sorted list (intent queue).
    """
    message_lower = message.lower()
    scores = {}
    for intent, keywords in knowledge_base.intent_keywords.items():
        score = sum(weight for keyword, weight in keywords.items() if keyword in message_lower)
        scores[intent] = score

    # Filter intents that meet the threshold
    detected_intents = [intent for intent, score in scores.items() if score >= confidence_threshold]
    
    # Sort by score in descending order so the most relevant intent is first
    detected_intents.sort(key=lambda intent: scores[intent], reverse=True)
    
    return detected_intents

def detect_entities(message: str) -> dict:
    """
    Detects ALL entities and returns them in lists.
    e.g., {'technology': ['python', 'javascript']}
    """
    detected_entities = {}
    message_lower = message.lower()
    
    for entity_type, patterns in knowledge_base.entity_patterns.items():
        for pattern in patterns:
            # Use finditer to find all non-overlapping matches
            matches = re.finditer(pattern, message_lower, re.IGNORECASE)
            for match in matches:
                # Use setdefault to initialize a list if it doesn't exist
                detected_entities.setdefault(entity_type, []).append(match.group(0).lower())
    return detected_entities

def get_single_response_part(intent: str, entities: dict) -> str | None:
    """
    Gets the best response for a SINGLE intent, using all available entities.
    This is the core logic from our previous bot, now made into a helper function.
    """
    responses = knowledge_base.responses
    
    if intent in responses:
        # Check all detected entities against available specific responses
        for entity_type, entity_values in entities.items():
            for entity_value in entity_values:
                if entity_value in responses[intent]:
                    return random.choice(responses[intent][entity_value])
        
        # Fallback to the default response for the intent
        if "default" in responses[intent]:
            return random.choice(responses[intent]["default"])
            
    return None # Return None if no response is found

def generate_composite_response(message: str) -> str:
    """
    The new "brain" of the bot. Detects multiple intents and entities,
    and composes a final response from multiple parts.
    """
    intents = detect_intents(message)
    entities = detect_entities(message)
    
    logging.info(f"Message: '{message}', Intents: {intents}, Entities: {entities}")
    
    if not intents:
        # If no intents are detected, return the generic help message
        return (
            "I'm here to help with IT career advice! You can ask me about:\n"
            "• **Career paths** (e.g., 'how to become a backend developer?')\n"
            "• **Technologies** (e.g., 'what is kubernetes?')\n"
            "• **Salaries** (e.g., 'how much do data scientists earn?')\n"
        )

    response_parts = []
    # Loop through the detected intent queue
    for intent in intents:
        part = get_single_response_part(intent, entities)
        if part:
            response_parts.append(part)

    if not response_parts:
        return "I see you're asking about IT, but I'm not sure how to help. Could you be more specific?"
        
    # Combine the response parts into a single message
    final_response = response_parts[0] # Start with the response for the highest-scored intent
    
    if len(response_parts) > 1:
        # Add the subsequent parts using our connectors
        for i, part in enumerate(response_parts[1:], start=1):
            connector = random.choice(knowledge_base.response_connectors)
            intent_name = intents[i].replace("_", " ") # Format intent name for display
            final_response += connector.format(intent_name=intent_name)
            final_response += part
            
    return final_response

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    response = generate_composite_response(message.content)
    await message.channel.send(response)

client.run(TOKEN)