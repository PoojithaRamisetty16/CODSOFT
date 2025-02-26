

import re
import random
import json
import math
import numpy as np
from datetime import datetime
from textblob import TextBlob
import wikipediaapi
from dateutil import parser
import nltk
from pathlib import Path

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


class EnhancedChatbot:
    def __init__(self): 
        self.todo_list = []
        self.notes = {}
        self.wiki = wikipediaapi.Wikipedia(user_agent="MyChatbot/1.0 (Contact: your-email@example.com)", language="en")

        self.knowledge_base = {
            "python": "Python is a high-level programming language known for its simplicity and readability.",
            "artificial intelligence": "AI is the simulation of human intelligence by machines.",
            "machine learning": "Machine learning is a subset of AI that enables systems to learn from data.",
            "chatbot": "A chatbot is a computer program designed to simulate conversation with human users."
        }
        self.responses_file = Path('chatbot_responses.json')
        if self.responses_file.exists():
            with open(self.responses_file, 'r') as f:
                self.patterns = json.load(f)
        else:
            self.patterns = {
                r'\b(hi|hello|hey)\b': [
                    "Hello! How can I help you today?",
                    "Hi there! What's on your mind?",
                    "Hey! How are you doing?"
                ],
                r'how are you': [
                    "I'm doing well, thank you for asking! How about you?",
                    "I'm great! How can I assist you today?",
                    "All good here! What can I help you with?"
                ],
                r'\b(bye|goodbye|exit)\b': [
                    "Goodbye! Have a great day!",
                    "See you later! Take care!",
                    "Bye! Come back soon!"
                ]
            }

    def analyze_sentiment(self, text):
        """Analyze the sentiment of input text"""
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity < 0:
            return "negative"
        return "neutral"

    def calculate_expression(self, expression):
        """Safely evaluate mathematical expressions"""
        try:
            expression = expression.lower()
            expression = expression.replace('plus', '+')
            expression = expression.replace('minus', '-')
            expression = expression.replace('times', '*')
            expression = expression.replace('divided by', '/')

        
            expression = ''.join(c for c in expression if c in '0123456789+-*/().^ ')

            return str(eval(f"np.{expression}"))
        except:
            return "Sorry, I couldn't calculate that. Please check the expression."

    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        try:
            page = self.wiki.page(query)
            if page.exists():
                
                return ' '.join(page.summary.split('. ')[:2]) + '.'
            return "Sorry, I couldn't find information about that topic."
        except:
            return "Sorry, there was an error searching Wikipedia."

    def manage_todo(self, command, task=""):
        """Manage todo list"""
        if command == "add" and task:
            self.todo_list.append({"task": task, "done": False, "date": datetime.now()})
            return f"Added task: {task}"
        elif command == "list":
            if not self.todo_list:
                return "Your todo list is empty."
            return "\n".join([f"{'[x]' if t['done'] else '[ ]'} {t['task']}" for t in self.todo_list])
        elif command == "clear":
            self.todo_list = []
            return "Todo list cleared."
        return "Invalid todo command."

    def save_note(self, title, content):
        """Save a note"""
        self.notes[title] = {"content": content, "date": datetime.now()}
        return f"Note '{title}' saved successfully."

    def get_note(self, title):
        """Retrieve a note"""
        return self.notes.get(title, {}).get("content", f"Note '{title}' not found.")

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        if not user_input:
            return "Please say something!"

        if "calculate" in user_input:
            expression = user_input.replace("calculate", "").strip()
            return f"Result: {self.calculate_expression(expression)}"

        if user_input.startswith("todo"):
            parts = user_input.split(maxsplit=2)
            command = parts[1] if len(parts) > 1 else ""
            task = parts[2] if len(parts) > 2 else ""
            return self.manage_todo(command, task)

        if user_input.startswith("note save"):
            _, _, title, *content = user_input.split(maxsplit=3)
            return self.save_note(title, content[0] if content else "")
        if user_input.startswith("note get"):
            _, _, title = user_input.split(maxsplit=2)
            return self.get_note(title)

        if "search" in user_input:
            query = user_input.replace("search", "").strip()
            return self.search_wikipedia(query)

        for key in self.knowledge_base:
            if key in user_input:
                return self.knowledge_base[key]

        for pattern, responses in self.patterns.items():
            if re.search(pattern, user_input):
                response = random.choice(responses)
                sentiment = self.analyze_sentiment(user_input)
                if sentiment == "negative":
                    return f"{response} (I notice you seem unhappy. Is everything okay?)"
                return response

        return "I'm not sure how to respond to that. Try asking about topics in my knowledge base, using the calculator, managing todos, or searching Wikipedia!"

    def start_chat(self):
        print("Enhanced ChatBot: Hello! Here are some things I can do:")
        print("- Basic conversation")
        print("- Calculate expressions (e.g., 'calculate 2 plus 2')")
        print("- Manage todos (e.g., 'todo add buy milk', 'todo list')")
        print("- Save and retrieve notes (e.g., 'note save title content', 'note get title')")
        print("- Search Wikipedia (e.g., 'search Python programming')")
        print("Type 'bye' to exit.")

        while True:
            user_input = input("You: ")

            if user_input.lower().strip() in ['bye', 'goodbye', 'exit']:
                print("ChatBot:", self.get_response(user_input))
                break

            response = self.get_response(user_input)
            print("ChatBot:", response)


def main():
    chatbot = EnhancedChatbot()
    chatbot.start_chat()


if __name__ == "__main__":  
    main()


