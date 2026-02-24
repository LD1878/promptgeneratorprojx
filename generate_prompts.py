#!/usr/bin/env python3
"""
generate_prompts.py
Generates 100 LLM prompts (20 per category) using templates and random placeholders.
Saves them as Markdown files in _prompts/<category>/ with front matter.
"""

import os
import random
import re
from datetime import datetime, timedelta

# ===== CONFIGURATION =====
CATEGORIES = ["marketing", "personal", "sales", "research", "ideas"]
PROMPTS_PER_CATEGORY = 20

# Templates for each category (you can edit these)
TEMPLATES = {
    "marketing": [
        "Write a Facebook ad for {product} targeting {audience}.",
        "Create a catchy slogan for a brand that sells {product}.",
        "Draft an email newsletter promoting {product} to {audience}.",
        "Generate 5 hashtags for a social media post about {product}.",
        "Write a persuasive product description for {product} highlighting {benefit}."
    ],
    "personal": [
        "Write a journal entry about {topic}.",
        "Create a to-do list for {day} focusing on {goal}.",
        "Draft a personal statement for a job application in {field}.",
        "Write a letter to your future self about {aspiration}.",
        "List 10 ideas for self-improvement in {area}."
    ],
    "sales": [
        "Write a cold email to a potential client in {industry}.",
        "Create a sales pitch for {product} emphasizing {benefit}.",
        "Draft a follow-up message after a sales meeting about {topic}.",
        "Write a script for a sales call to {audience}.",
        "List 5 objections a customer might have about {product} and how to overcome them."
    ],
    "research": [
        "Summarize the latest findings in {field} regarding {topic}.",
        "Propose a research question about {subject}.",
        "List 10 sources for a literature review on {theme}.",
        "Write an abstract for a paper on {topic}.",
        "Generate hypotheses for a study about {phenomenon}."
    ],
    "ideas": [
        "Brainstorm 10 business ideas related to {industry}.",
        "Generate 5 app concepts that solve {problem}.",
        "List creative ways to use {product}.",
        "Come up with 10 blog post topics about {theme}.",
        "Think of 5 innovative marketing campaigns for {brand}."
    ]
}

# Placeholder lists (add more as you like)
PLACEHOLDERS = {
    "product": ["eco-friendly water bottle", "AI writing assistant", "smart yoga mat", "vegan protein powder", "wireless earbuds"],
    "audience": ["millennials", "busy parents", "fitness enthusiasts", "remote workers", "college students"],
    "benefit": ["saving time", "improving health", "boosting productivity", "reducing stress", "saving money"],
    "topic": ["productivity hacks", "mindfulness", "remote work challenges", "sustainable living", "digital minimalism"],
    "day": ["Monday", "the weekend", "your day off", "a busy Tuesday", "Sunday morning"],
    "goal": ["learning a new skill", "exercising more", "reading 20 pages", "completing a project", "connecting with friends"],
    "field": ["data science", "graphic design", "education", "healthcare", "finance"],
    "aspiration": ["starting a business", "writing a book", "traveling the world", "learning an instrument", "running a marathon"],
    "area": ["fitness", "career", "relationships", "finances", "mental health"],
    "industry": ["tech startups", "real estate", "e-commerce", "consulting", "nonprofit"],
    "subject": ["climate change", "artificial intelligence", "mental health", "urban planning", "genetics"],
    "theme": ["innovation", "sustainability", "wellness", "education", "community"],
    "phenomenon": ["the placebo effect", "social media addiction", "remote work productivity", "consumer behavior", "learning styles"],
    "problem": ["time management", "food waste", "loneliness", "fitness motivation", "financial literacy"],
    "brand": ["Nike", "Tesla", "Patagonia", "Apple", "a local coffee shop"]
}

# ===== HELPER FUNCTIONS =====
def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)  # Remove punctuation
    text = re.sub(r'[\s_-]+', '-', text)  # Replace spaces with hyphens
    text = re.sub(r'^-+|-+$', '', text)   # Trim hyphens
    return text

def generate_prompt(category, date):
    """Generate a single prompt for a given category with random placeholders."""
    template = random.choice(TEMPLATES[category])
    # Find all placeholders in the template
    placeholders_in_template = re.findall(r'\{(\w+)\}', template)
    filled = template
    for ph in placeholders_in_template:
        if ph in PLACEHOLDERS:
            value = random.choice(PLACEHOLDERS[ph])
            filled = filled.replace('{' + ph + '}', value)
    # Generate a title from the first few words
    title_words = filled.split()[:6]
    title = ' '.join(title_words) + '...'
    return {
        "title": title,
        "content": filled,
        "category": category,
        "date": date,
        "tags": [category, "daily"]
    }

def save_prompt(prompt_data):
    """Save a prompt as a Markdown file in _prompts/<category>/ with front matter."""
    category = prompt_data["category"]
    # Create category folder if it doesn't exist
    category_dir = os.path.join("_prompts", category)
    os.makedirs(category_dir, exist_ok=True)

    # Create filename: YYYY-MM-DD-title.md
    date_str = prompt_data["date"].strftime("%Y-%m-%d")
    slug = slugify(prompt_data["title"])
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(category_dir, filename)

    # Avoid overwriting if file already exists (shouldn't happen with new dates)
    if os.path.exists(filepath):
        print(f"File {filepath} already exists, skipping.")
        return

    # Build front matter
    front_matter = f"""---
title: "{prompt_data['title']}"
date: {prompt_data['date'].strftime('%Y-%m-%d %H:%M:%S %z')}
categories: [{prompt_data['category']}]
tags: {prompt_data['tags']}
---

{prompt_data['content']}
"""
    with open(filepath, 'w') as f:
        f.write(front_matter)
    print(f"Saved: {filepath}")

# ===== MAIN GENERATION =====
def main():
    # Use tomorrow's date so prompts appear fresh each day
    generation_date = datetime.now() + timedelta(days=1)

    for category in CATEGORIES:
        for _ in range(PROMPTS_PER_CATEGORY):
            prompt = generate_prompt(category, generation_date)
            save_prompt(prompt)

if __name__ == "__main__":
    main()
