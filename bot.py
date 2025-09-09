import os
import re
import random
import logging
import discord
from dotenv import load_dotenv

# Import the knowledge base
import knowledge_base

# --- INITIALIZATION ---

# Set up logging to a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler() # Also print logs to console
    ]
)

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    logging.error("FATAL: DISCORD_TOKEN environment variable not set.")
    exit()

# Set up Discord client with necessary intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# --- PRE-COMPUTATION AT STARTUP ---

# Compile all regex patterns for efficiency
COMPILED_INTENT_PATTERNS = {
    intent: [(re.compile(pattern, re.IGNORECASE), weight) for pattern, weight in patterns]
    for intent, patterns in knowledge_base.intent_patterns.items()
}


COMPILED_ENTITY_PATTERNS = {
    entity: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for entity, patterns in knowledge_base.entity_patterns.items()
}

def build_skill_to_role_map():
    """
    Creates an inverted index mapping skills to a list of roles requiring them.
    This is crucial for the 'Skills -> Role' feature and is run only once at startup.
    """
    skill_map = {}
    for role_id, data in knowledge_base.role_skill_map.items():
        all_skills = []
        for skill_list in data['skills'].values():
            all_skills.extend(skill_list)
        
        for skill in set(all_skills): # Use set to avoid duplicates
            if skill not in skill_map:
                skill_map[skill] = []
            skill_map[skill].append(role_id)
    return skill_map

# This inverted map is the key to finding roles from skills quickly.
SKILL_TO_ROLE_MAP = build_skill_to_role_map()
logging.info("Skill-to-Role map built successfully.")

# --- CORE LOGIC FUNCTIONS ---


def detect_intents(message: str) -> list:
    """Detects intents based on regex patterns and scores, returning a sorted list."""
    scores = {}
    message_lower = message.lower()
    
    for intent, pattern_weights in COMPILED_INTENT_PATTERNS.items():
        score = 0
        for pattern, weight in pattern_weights:
            matches = pattern.findall(message_lower)
            if matches:
                score += weight * len(matches)  # Increase score based on number of matches
        if score > 0:
            scores[intent] = score
    
    # Sort intents by score in descending order
    return sorted(scores.keys(), key=lambda k: scores[k], reverse=True)

def detect_entities(message: str) -> dict:
    """
    Detects all entities (roles, technologies) in a message.
    
    BUG FIX: Switched from re.findall() to re.finditer() to capture the
    full match of a pattern, not just the parenthesized group. This ensures
    that "backend developer" is extracted instead of just "backend".
    """
    detected = {}
    message_lower = message.lower()
    for entity_type, patterns in COMPILED_ENTITY_PATTERNS.items():
        found_entities = set()
        for pattern in patterns:
            # Use finditer to get match objects, ensuring we get the full match
            matches = pattern.finditer(message_lower)
            for match in matches:
                # .group(0) returns the entire matched string (e.g., "backend developer")
                found_entities.add(match.group(0).strip())
        if found_entities:
            detected[entity_type] = list(found_entities)
    return detected

def handle_role_to_skill_query(entities: dict) -> str:
    """
    Handles 'career_path' intent.
    Formats a response detailing the skills needed for a detected role.
    """
    if "role" not in entities or not entities["role"]:
        return "I can see you're asking about a career path, but which role are you interested in? For example, try 'what skills are needed for a devops engineer?'"

    # Take the first role detected
    role_entity = entities["role"][0]
    
    # Normalize the entity to match the key in role_skill_map (e.g., "backend developer" -> "backend_developer")
    role_key = role_entity.lower().replace(" ", "_").replace("-", "_")
    
    if role_key in knowledge_base.role_skill_map:
        role_data = knowledge_base.role_skill_map[role_key]
        response = f"Excellent choice! To become a **{role_data['display_name']}**, you'll generally need the following skills:\n\n"
        response += f"_{role_data['description']}_\n\n"
        
        for category, skills in role_data['skills'].items():
            # Format category name nicely (e.g., 'core_concepts' -> 'Core Concepts')
            category_name = category.replace('_', ' ').title()
            skill_list = ", ".join(f"`{s}`" for s in skills)
            response += f"• **{category_name}:** {skill_list}\n"
        
        return response
    else:
        return f"I don't have detailed information on the '{role_entity}' role just yet, but I'm constantly learning! Try asking about another role."

def handle_skill_to_role_query(entities: dict) -> str:
    """
    Handles 'role_suggestion' intent.
    Finds and scores potential roles based on the user's mentioned skills.
    """
    if "technology" not in entities or not entities["technology"]:
        return "Please tell me what skills you have! For example, 'I am proficient in Python and React'."

    user_skills = set(entities["technology"])
    role_scores = {}

    for skill in user_skills:
        # Check our pre-computed map for roles associated with this skill
        if skill in SKILL_TO_ROLE_MAP:
            for role_id in SKILL_TO_ROLE_MAP[skill]:
                role_scores[role_id] = role_scores.get(role_id, 0) + 1

    if not role_scores:
        return f"Based on the skills you mentioned ({', '.join(f'`{s}`' for s in user_skills)}), I couldn't find a direct career match in my database. Perhaps try listing some other technologies you know?"

    # Sort roles by how many of the user's skills matched
    sorted_roles = sorted(role_scores.items(), key=lambda item: item[1], reverse=True)

    response = f"With skills in **{', '.join(user_skills)}**, you have several great career prospects! Here are some top matches based on your skills:\n\n"
    
    # Show top 3 matches
    for role_id, score in sorted_roles[:3]:
        role_data = knowledge_base.role_skill_map[role_id]
        display_name = role_data['display_name']
        match_quality = f"({score} of your skills match)"
        response += f"• **{display_name}** {match_quality}\n"

    response += "\nYou can ask me for more details on any of these roles to see the full skill set required!"
    return response

def generate_response(message: str) -> str:
    """
    The main response dispatcher. It detects intents and entities,
    then routes to the appropriate handler function.
    """
    intents = detect_intents(message)
    entities = detect_entities(message)
    
    logging.info(f"Message: '{message}' | Intents: {intents} | Entities: {entities}")

    if not intents:
        return "I'm not sure how to help with that. Try asking me what skills you need for a job, or what jobs you can get with your skills!"

    primary_intent = intents[0]
    
    # Route to handlers based on intent
    if primary_intent == "greeting":
        return random.choice(knowledge_base.simple_responses["greeting"])
    elif primary_intent == "consultation_start":
        return random.choice(knowledge_base.simple_responses["consultation_start"])
    elif primary_intent == "thanks":
        return random.choice(knowledge_base.simple_responses["thanks"])
    elif primary_intent == "career_path":
        return handle_role_to_skill_query(entities)
    elif primary_intent == "role_suggestion":
        return handle_skill_to_role_query(entities)
    
    # Fallback if an intent was detected but has no handler
    return "I see you're asking about something tech-related, but I'm not sure how to answer. Could you rephrase your question?"

# --- DISCORD CLIENT EVENTS ---

@client.event
async def on_ready():
    """Event handler for when the bot has connected to Discord."""
    logging.info(f'Bot logged in as {client.user}')
    print(f'Logged in as {client.user}. The bot is ready!')

@client.event
async def on_message(message):
    """Event handler for when a message is sent in a channel the bot can see."""
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Generate and send the response
    response_text = generate_response(message.content)
    await message.channel.send(response_text)

# --- RUN THE BOT ---
if __name__ == "__main__":
    if not os.path.exists('logs'):
        os.makedirs('logs')
    client.run(TOKEN)

