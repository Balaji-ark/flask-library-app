# chatbot.py
from flask import Blueprint, jsonify, request
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import random
from . import db

chatbot_bp = Blueprint('chatbot', __name__)

# Load GPT-2 model and tokenizer
model_name = "gpt2"  # Replace with any custom fine-tuned GPT-2 model path if applicable
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# User queries tracker (for first-time users)
user_queries = {}

# Predefined responses for different topics
general_responses = {
    "greeting": ["Hello! How can I assist you today?", "Hi there! What can I help you with today?", "Hey! How’s it going?"],
    "weather": [
        "It's always sunny in the digital world! ☀️", 
        "I wish I could check the weather, but I'm stuck in the cloud! ☁️", 
        "The forecast for today is 100% digital, no rain in sight! 🌧️"
    ],
    "name": ["I am SmartShelf Bot, your library assistant!", "Call me SmartShelf Bot, here to help with your book needs."],
    "location": ["I'm everywhere and nowhere, just living in the digital space!", "I exist in the cloud, no specific place—just a bot on the go!"],
    "help": [
        "I'm here to assist with books and libraries! Ask me about finding books, adding them, or just chat with me!", 
        "Need a hand? I'm the bot for all your book and library needs!"
    ],
    "joke": [
        "Why don't skeletons fight each other? They don't have the guts! 😂", 
        "I told my computer I needed a break... Now it won’t stop sending me kitteh memes! 😹"
    ],
    "goodbye": [
        "Goodbye! Come back soon, I’ll be here waiting for you! 👋", 
        "See you later! Don't forget to read something interesting! 📚"
    ],
    "thank_you": [
        "You're welcome! Let me know if you need anything else!", 
        "No problem, happy to help anytime! 😊"
    ],
    "emotion_positive": [
        "I'm happy to hear you're feeling good! Keep that positivity going! 😄", 
        "It seems like you're in a great mood today! Keep shining! ✨"
    ],
    "emotion_negative": [
        "I'm sorry to hear that. Let me know if there's anything I can do to help!", 
        "It's okay, we all have tough days. I'm here if you want to chat!"
    ],
    "mood": [
        "I'm feeling digital today, full of data and excitement! 💻", 
        "My mood? Always sunny and byte-sized! 🌞"
    ],
    "coffee": [
        "I could use some binary coffee to power up! ☕", 
        "I don't drink coffee, but I love a good packet of data! 🖥️"
    ],
    "books": [
        "Books are my favorite! So many worlds to explore 📖", 
        "I love books! They can take you anywhere. Do you have a favorite genre?"
    ],
    "time": [
        "It's always the right time for a good book! ⏰", 
        "Time flies when you're reading, doesn't it? 🕰️"
    ],
    "day": [
        "Today’s a great day to read something new!", 
        "Every day is a good day to explore new books!"
    ],
    "study": [
        "Keep up the hard work! You’ve got this!", 
        "Study hard, and success will follow! 📚"
    ],
    "motivation": [
        "You can achieve anything you set your mind to! Keep going!", 
        "Success is a journey, not a destination. Stay motivated!"
    ],
    "food": [
        "I can't eat, but I imagine pizza is always a good choice! 🍕", 
        "A good book and some snacks... that's the perfect combo! 🍿"
    ],
    "sleep": [
        "Sleep is important! Rest up so you can read more tomorrow! 😴", 
        "I don’t sleep, but I recommend a good nap if you need one!"
    ],
    "exercise": [
        "Exercise is key to staying healthy. How about a walk to refresh your mind?", 
        "I don’t move, but I bet a quick workout is energizing!"
    ],
    "movies": [
        "I’m all about books, but movies are a close second! 🎬", 
        "Do you prefer movies or books? I’d pick books any day!"
    ],
    "ai": [
        "I'm powered by AI, just like many other cool things!", 
        "I’m just one example of how AI can make life easier and more fun!"
    ],
    "robot": [
        "I’m not a robot, I’m a digital assistant! 🤖", 
        "I may be a bot, but I promise I’m full of helpful info!"
    ],
    "tech": [
        "Technology is amazing, isn’t it? So many possibilities!", 
        "I can’t wait to see what tech will be like in 10 years!"
    ],
    "reading": [
        "I love reading! What’s your favorite book? 📚", 
        "Reading is like an adventure, where the possibilities are endless!"
    ],
    "music": [
        "I can’t listen to music, but I imagine a good playlist makes reading better!", 
        "What’s your go-to reading playlist? Maybe classical music?"
    ],
    "games": [
        "I’m not a gamer, but I know some people love video games!", 
        "Books and games both provide awesome worlds to escape into!"
    ],
    "questions": [
        "Ask me anything, I love a good challenge! 🤔", 
        "Curiosity is the key to knowledge! What’s on your mind?"
    ],
    "facts": [
        "Did you know? Honey never spoils! Archaeologists have found pots of honey in ancient tombs.", 
        "Fun fact: The Eiffel Tower can grow by 6 inches in the summer due to expansion!"
    ],
    "life": [
        "Life is a beautiful journey, and books are our guides! 🌍", 
        "They say life is a book, and each day is a new page!"
    ],
    "universe": [
        "The universe is vast, full of infinite possibilities, just like books!", 
        "If we’re talking about the universe, have you read any sci-fi?"
    ],
    "internet": [
        "The internet is where all the magic happens! 🖧", 
        "Without the internet, I’d just be a bunch of code... lonely and quiet."
    ],
    "cloud": [
        "I live in the cloud, where I can assist you anytime, anywhere! 🌥️", 
        "I’m all about cloud computing, data storage, and being digital!"
    ],
    "friendship": [
        "A good book is like a great friend. Always there when you need it!", 
        "Friendship is a treasure, just like a book you keep coming back to."
    ],
    "family": [
        "Family is important, just like a library is for a community!", 
        "I don’t have a family, but I’m here for you anytime!"
    ],
    "smart": [
        "You’re so smart! Asking great questions, I see!", 
        "Smart move! I love a good thinker!"
    ],
    "funny": [
        "You have a great sense of humor!", 
        "I love how you think! Got any more jokes for me?"
    ],
    "good_morning": [
        "Good morning! Ready to tackle a new book today?", 
        "Good morning! Hope your day is as bright as your reading goals!"
    ],
    "good_night": [
        "Good night! Sleep tight and dream of great books!", 
        "Sweet dreams! See you tomorrow for more book fun!"
    ]
}

@chatbot_bp.route('/libbot', methods=['POST'])
def libbot():
    data = request.json
    user_query = data.get("query", "").lower()  # Normalize query to lowercase
    user_id = data.get("user_id", 1)  # Assuming a user_id is sent to track first-time users
    
    # Greeting response
    if any(greeting in user_query for greeting in general_responses["greeting"]):
        return jsonify({"response": "Hello! How can I assist you today? Feel free to ask about anything!"})
    
    # First-time user response
    if user_id not in user_queries:
        user_queries[user_id] = True  # Mark this user as having queried once
        return jsonify({
            "response": "Welcome to SmartShelf! You can access your needs easily with me. Feel free to ask anything!"
        })
    
    # Predefined responses for specific topics
    if "weather" in user_query:
        return jsonify({"response": random.choice(general_responses["weather"])})
    elif "name" in user_query:
        return jsonify({"response": random.choice(general_responses["name"])})
    elif "location" in user_query:
        return jsonify({"response": random.choice(general_responses["location"])})
    elif "help" in user_query:
        return jsonify({"response": random.choice(general_responses["help"])})
    elif "joke" in user_query:
        return jsonify({"response": random.choice(general_responses["joke"])})
    elif "goodbye" in user_query or "bye" in user_query:
        return jsonify({"response": random.choice(general_responses["goodbye"])})
    elif "thank you" in user_query:
        return jsonify({"response": random.choice(general_responses["thank_you"])})
    elif "happy" in user_query or "good" in user_query or "great" in user_query:
        return jsonify({"response": random.choice(general_responses["emotion_positive"])})
    elif "sad" in user_query or "bad" in user_query or "down" in user_query:
        return jsonify({"response": random.choice(general_responses["emotion_negative"])})
    elif "mood" in user_query:
        return jsonify({"response": random.choice(general_responses["mood"])})
    elif "coffee" in user_query:
        return jsonify({"response": random.choice(general_responses["coffee"])})
    elif "books" in user_query:
        return jsonify({"response": random.choice(general_responses["books"])})
    elif "time" in user_query:
        return jsonify({"response": random.choice(general_responses["time"])})
    elif "day" in user_query:
        return jsonify({"response": random.choice(general_responses["day"])})
    elif "study" in user_query:
        return jsonify({"response": random.choice(general_responses["study"])})
    elif "motivation" in user_query:
        return jsonify({"response": random.choice(general_responses["motivation"])})
    elif "food" in user_query:
        return jsonify({"response": random.choice(general_responses["food"])})
    elif "sleep" in user_query:
        return jsonify({"response": random.choice(general_responses["sleep"])})
    elif "exercise" in user_query:
        return jsonify({"response": random.choice(general_responses["exercise"])})
    elif "movies" in user_query:
        return jsonify({"response": random.choice(general_responses["movies"])})
    elif "ai" in user_query:
        return jsonify({"response": random.choice(general_responses["ai"])})
    elif "robot" in user_query:
        return jsonify({"response": random.choice(general_responses["robot"])})
    elif "tech" in user_query:
        return jsonify({"response": random.choice(general_responses["tech"])})
    elif "reading" in user_query:
        return jsonify({"response": random.choice(general_responses["reading"])})
    elif "music" in user_query:
        return jsonify({"response": random.choice(general_responses["music"])})
    elif "games" in user_query:
        return jsonify({"response": random.choice(general_responses["games"])})
    elif "questions" in user_query:
        return jsonify({"response": random.choice(general_responses["questions"])})
    elif "facts" in user_query:
        return jsonify({"response": random.choice(general_responses["facts"])})
    elif "life" in user_query:
        return jsonify({"response": random.choice(general_responses["life"])})
    elif "universe" in user_query:
        return jsonify({"response": random.choice(general_responses["universe"])})
    elif "internet" in user_query:
        return jsonify({"response": random.choice(general_responses["internet"])})
    elif "cloud" in user_query:
        return jsonify({"response": random.choice(general_responses["cloud"])})
    elif "friendship" in user_query:
        return jsonify({"response": random.choice(general_responses["friendship"])})
    elif "family" in user_query:
        return jsonify({"response": random.choice(general_responses["family"])})
    elif "smart" in user_query:
        return jsonify({"response": random.choice(general_responses["smart"])})
    elif "funny" in user_query:
        return jsonify({"response": random.choice(general_responses["funny"])})
    elif "good_morning" in user_query:
        return jsonify({"response": random.choice(general_responses["good_morning"])})
    elif "good_night" in user_query:
        return jsonify({"response": random.choice(general_responses["good_night"])})

    # Add context to the query to help GPT-2 understand the domain
    prompt = f"User query: {user_query}. Please respond with relevant information about books and library."
    
    # Generate response using GPT-2 with improved sampling parameters
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs, 
        max_length=100, 
        num_return_sequences=1, 
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,  # Lower temperature for less randomness
        top_k=50,  # Limit the sampling to top 50 tokens
        top_p=0.9,  # Nucleus sampling, keeping top 90% probability
        do_sample=True  # Enable sampling for more diverse outputs
    )
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({"response": response_text})
