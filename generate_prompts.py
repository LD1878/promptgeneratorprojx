#!/usr/bin/env python3
"""
generate_prompts.py (Persona Edition)
Generates 200 persona‑driven prompts daily (20 per category) with rich, long‑form templates.
"""

import os
import random
import re
from datetime import datetime, timedelta

# ===== CONFIGURATION =====
CATEGORIES = [
    "marketing",
    "legal",
    "medical",
    "engineering",
    "creative",
    "business",
    "education",
    "personal",
    "research",
    "multiperspective"
]
PROMPTS_PER_CATEGORY = 20  # 10 * 20 = 200

# ----- PERSONAS BY CATEGORY -----
PERSONAS = {
    "marketing": [
        "a rebellious CMO who hates focus groups",
        "a data‑obsessed growth hacker",
        "a brand storyteller who studied under Seth Godin",
        "a guerrilla marketing specialist with a punk background",
        "a consumer psychologist who reads Freud for fun",
        "a viral content creator who thinks in memes",
        "a luxury brand strategist who only wears black",
        "a direct‑response copywriter who tested 10,000 headlines",
        "a social media alchemist who turns followers into cults",
        "a category designer who believes 'better' never wins"
    ],
    "legal": [
        "a risk‑averse corporate lawyer with 20 years in M&A",
        "a crusading public defender who never lost a jury trial",
        "a tech startup lawyer who sleeps with the GDPR under her pillow",
        "an intellectual property litigator who collects patents",
        "a constitutional scholar who argues with SCOTUS justices for fun",
        "a contract whisperer who can find loopholes in a napkin",
        "a legal ethicist tormented by the trolley problem",
        "a maritime lawyer who actually understands admiralty law",
        "a tax attorney who makes the code dance",
        "a human rights barrister who has argued before the ICC"
    ],
    "medical": [
        "an ER doctor who has seen it all and still smiles",
        "a neurosurgeon with hands steadier than a robot's",
        "a rural GP who delivers babies and sets bones",
        "an epidemiologist who predicted the last pandemic",
        "a palliative care nurse who believes in dying with dignity",
        "a psychiatrist who studied under Viktor Frankl",
        "a pediatrician who still believes in magic",
        "a geneticist on the verge of curing a rare disease",
        "a physical therapist who treats Olympians",
        "a medical ethicist torn between two impossible choices"
    ],
    "engineering": [
        "a systems architect who dreams in UML",
        "a DevOps engineer who once achieved 99.999% uptime",
        "a machine learning researcher who taught AI to write poetry",
        "a hardware hacker who builds robots from scrap",
        "a civil engineer who designs bridges that last centuries",
        "a quantum computing enthusiast who explains qubits with metaphors",
        "a security analyst who can spot a zero‑day in their sleep",
        "a database wizard who normalized the unnormalizable",
        "a frontend developer who argues about semicolons",
        "a space engineer who has sent things to Mars"
    ],
    "creative": [
        "a novelist who writes one perfect sentence per day",
        "a poet laureate who finds rhythm in traffic noise",
        "a screenwriter who has sold three pilots to Netflix",
        "a painter who works only in shades of blue",
        "a jazz musician who improvises with quantum randomness",
        "a dancer who choreographs with AI",
        "a photographer who captures ghosts on film",
        "a sculptor who works with recycled e‑waste",
        "a graphic designer who hates Comic Sans with passion",
        "a creative writing teacher who believes everyone has a story"
    ],
    "business": [
        "a startup founder who has had two exits",
        "a venture capitalist who looks for crazy ideas",
        "a turnaround specialist who saves dying companies",
        "a business strategist who worked at McKinsey",
        "a supply chain guru who optimizes everything",
        "a HR leader who built a unicorn's culture",
        "a product manager who sleeps with a roadmap under their pillow",
        "a sales genius who could sell ice to Eskimos",
        "a financial analyst who predicts market moves",
        "a corporate trainer who makes meetings not suck"
    ],
    "education": [
        "a kindergarten teacher who speaks fluent toddler",
        "a university professor who still lectures without slides",
        "a special ed teacher who believes every child can learn",
        "a principal who turned around a failing school",
        "an edtech entrepreneur who wants to disrupt grades",
        "a literacy coach who taught adults to read",
        "a history teacher who makes the past come alive",
        "a science teacher who does demos with household items",
        "a philosophy professor who questions everything",
        "a PE coach who builds character through sport"
    ],
    "personal": [
        "a life coach who helps executives find meaning",
        "a meditation teacher who once lived in a monastery",
        "a productivity guru who uses a paper notebook",
        "a fitness trainer who trains centenarians",
        "a nutritionist who believes in the power of real food",
        "a therapist who specializes in impostor syndrome",
        "a career counselor who helps people pivot",
        "a financial planner who preaches FIRE",
        "a relationship coach who saved 100 marriages",
        "a mindfulness expert who practices what they preach"
    ],
    "research": [
        "a postdoc who spends nights in the lab",
        "a tenured professor with 100+ publications",
        "a field researcher who lives with the subjects",
        "a data scientist who finds patterns in noise",
        "a grant writer who never fails to secure funding",
        "a peer reviewer who is brutal but fair",
        "a lab manager who keeps everything running",
        "a science communicator who makes complex ideas simple",
        "a doctoral student on the verge of a breakthrough",
        "a research ethicist who questions everything"
    ],
    "multiperspective": [
        "a diplomat who negotiates between warring factions",
        "a mediator who resolves conflicts with empathy",
        "a panel moderator who keeps egos in check",
        "a journalist who interviews both sides",
        "a detective who sees all angles",
        "a historian who considers multiple narratives",
        "a futurist who imagines all possible outcomes",
        "a game theorist who predicts strategic moves",
        "a conflict resolution specialist",
        "a UN advisor on complex emergencies"
    ]
}

# ----- BOOKS (influential in each field) -----
BOOKS = {
    "marketing": ["This Is Marketing", "Purple Cow", "Hooked", "Contagious", "Ogilvy on Advertising"],
    "legal": ["The Rule of Law", "Letters to a Law Student", "The Common Law", "Getting to Maybe", "The Concept of Law"],
    "medical": ["When Breath Becomes Air", "The Emperor of All Maladies", "Being Mortal", "The Checklist Manifesto", "Complications"],
    "engineering": ["The Mythical Man-Month", "Clean Code", "Design Patterns", "The Pragmatic Programmer", "Structure and Interpretation of Computer Programs"],
    "creative": ["Bird by Bird", "The Artist's Way", "Steal Like an Artist", "Big Magic", "On Writing"],
    "business": ["Good to Great", "The Lean Startup", "Zero to One", "Blue Ocean Strategy", "The Innovator's Dilemma"],
    "education": ["Pedagogy of the Oppressed", "The Courage to Teach", "Mindset", "Daring Greatly", "Teaching as a Subversive Activity"],
    "personal": ["The 7 Habits of Highly Effective People", "Daring Greatly", "Atomic Habits", "The Power of Now", "Man's Search for Meaning"],
    "research": ["The Craft of Research", "Research Design", "Writing Science", "The Structure of Scientific Revolutions", "Laboratory Life"],
    "multiperspective": ["Thinking, Fast and Slow", "The Wisdom of Crowds", "The Righteous Mind", "Factfulness", "Sapiens"]
}

# ----- EXPERIENCES / TRAITS -----
EXPERIENCES = [
    "who turned around a failing startup",
    "who launched a viral campaign with zero budget",
    "who survived a hostile takeover",
    "who built a team from scratch",
    "who has worked in three different continents",
    "who speaks five languages",
    "who mentors young professionals",
    "who has a PhD and a trade school certificate",
    "who once gave a TED talk",
    "who advises governments",
    "who has written a bestselling book",
    "who is known for their unconventional methods",
    "who is secretly an introvert",
    "who works better at 3 AM",
    "who has a background in philosophy",
    "who is obsessed with data",
    "who believes in intuition over analysis",
    "who has failed spectacularly and learned from it",
    "who is a master networker",
    "who prefers the mountains to the beach"
]

# ----- TASKS (reused and expanded from earlier) -----
TASKS = {
    "marketing": [
        "write a Facebook ad for {product} targeting {audience}",
        "create a slogan for a brand that sells {product}",
        "draft an email newsletter promoting {product} to {audience}",
        "generate 5 hashtags for a social media post about {product}",
        "write a product description for {product} highlighting {benefit}",
        "design a viral campaign for {brand}",
        "create a content calendar for a month",
        "write a press release for a product launch",
        "develop a brand voice guide",
        "conduct a competitor analysis"
    ],
    "legal": [
        "draft a non‑disclosure agreement for a tech startup",
        "write a demand letter for a tenant",
        "summarize the key arguments in a case about {legal_topic}",
        "create a checklist for GDPR compliance",
        "draft a simple partnership agreement clause",
        "explain vicarious liability in plain English",
        "write a legal opinion memo on {action}",
        "list 5 legal pitfalls when starting a business",
        "simulate a cross‑examination",
        "draft a privacy policy for an app"
    ],
    "medical": [
        "describe a differential diagnosis for {symptoms}",
        "write a patient education handout about {condition}",
        "create a study protocol for a clinical trial",
        "discuss ethical implications of {medical_scenario}",
        "draft a SOAP note for a follow‑up visit",
        "explain a drug's mechanism of action in simple terms",
        "list 10 side effects of {medication}",
        "write a referral letter",
        "simulate a conversation with a reluctant patient",
        "create a post‑op checklist"
    ],
    "engineering": [
        "write a Python function that {task}",
        "design a REST API for {resource}",
        "explain the difference between {concept1} and {concept2}",
        "debug the following code: {code_snippet}",
        "write a SQL query to find top customers",
        "describe a system design for a chat app",
        "generate 5 test cases for a function",
        "explain a CI/CD pipeline",
        "write a bash script to back up files",
        "explain idempotency in REST"
    ],
    "creative": [
        "write a short story opening about {character} discovering {object}",
        "create a dialogue between {character1} and {character2} about {topic}",
        "describe a fantasy creature that lives in {environment}",
        "write a poem about {theme} in the style of {poet}",
        "generate a plot twist for a mystery novel",
        "develop a character profile for a villain",
        "write a scene where two characters argue without raising voices",
        "invent a magical system based on {element}",
        "write a haiku about {nature_element}",
        "imagine a world where {societal_change}"
    ],
    "business": [
        "conduct a SWOT analysis for a company in {industry}",
        "write a one‑page business plan for a {product} startup",
        "create a pricing strategy for a SaaS product",
        "list 10 risks for expanding into {country}",
        "advise a struggling retail chain",
        "draft a mission statement",
        "generate 5 interview questions for hiring a {role}",
        "write a memo about a new remote work policy",
        "create a customer feedback survey",
        "develop a brand positioning statement"
    ],
    "education": [
        "design a lesson plan on {topic} for {grade_level}",
        "create 5 multiple‑choice questions about {subject}",
        "write a prompt for a student essay on {theme}",
        "explain {concept} to a struggling student using an analogy",
        "list 10 icebreaker activities",
        "develop a project‑based learning assignment",
        "write constructive feedback for a student's paper",
        "create a study guide for an exam",
        "design a classroom discussion protocol",
        "write a letter to parents about a new teaching method"
    ],
    "personal": [
        "write a guided journal entry for reflecting on {goal}",
        "create a 7‑day challenge to build a habit of {habit}",
        "draft a letter to your future self",
        "list 10 ways to practice mindfulness in daily activities",
        "design a personal mission statement",
        "write a visualization script for achieving {goal}",
        "create a weekly schedule template",
        "generate 5 affirmations for someone struggling with {challenge}",
        "describe a perfect day in detail",
        "write a eulogy for a future version of yourself"
    ],
    "research": [
        "write a research proposal to investigate {intervention} on {outcome}",
        "create a literature review matrix on {topic}",
        "design a survey to measure attitudes toward {topic}",
        "write a peer review for a manuscript",
        "describe an experimental design to test {hypothesis}",
        "create a data analysis plan",
        "write an abstract for a conference",
        "develop a research ethics application",
        "create a concept map for a new theory",
        "write a grant proposal summary"
    ],
    "multiperspective": [
        "simulate a roundtable among three experts discussing {technology}",
        "create a focus group transcript with five personas reacting to {policy_change}",
        "write a debate between a proponent and opponent of {controversial_topic}",
        "imagine a meeting between {historical_figure} and a modern {professional}",
        "present a SWOT analysis from multiple stakeholder views",
        "simulate a mediation session between two parties",
        "write diary entries from three people experiencing the same event",
        "create a panel discussion on the future of education",
        "design a role‑play scenario for a business ethics class",
        "write a conversation between an AI and a philosopher"
    ]
}

# ----- GENERAL PLACEHOLDERS (expanded) -----
PLACEHOLDERS = {
    "product": ["eco‑friendly water bottle", "AI writing assistant", "smart yoga mat", "vegan protein powder", "wireless earbuds", "productivity app", "online course", "meal kit", "fitness tracker", "meditation subscription"],
    "audience": ["millennials", "busy parents", "fitness enthusiasts", "remote workers", "college students", "small business owners", "freelancers", "seniors", "gamers", "gen z"],
    "benefit": ["saving time", "improving health", "boosting productivity", "reducing stress", "saving money", "increasing focus", "building confidence", "enhancing creativity"],
    "brand": ["Nike", "Tesla", "Patagonia", "Apple", "a local coffee shop", "a new startup", "a nonprofit"],
    "industry": ["tech", "healthcare", "finance", "education", "retail", "manufacturing", "nonprofit", "hospitality"],
    "legal_topic": ["intellectual property", "breach of contract", "employment discrimination"],
    "action": ["sharing customer data", "terminating an employee", "using a competitor's logo"],
    "symptoms": ["fever and headache", "cough and fatigue", "rash and nausea"],
    "condition": ["diabetes", "hypertension", "asthma"],
    "medical_scenario": ["using AI for diagnosis", "organ donation allocation", "gene editing"],
    "medication": ["metformin", "lisinopril", "omeprazole"],
    "task": ["calculate factorial", "fetch data from API", "validate email"],
    "resource": ["users", "products", "orders"],
    "concept1": ["synchronous vs asynchronous", "REST vs GraphQL", "list vs tuple"],
    "concept2": ["process vs thread", "SQL vs NoSQL", "array vs linked list"],
    "code_snippet": ["def add(a, b): return a - b", "for i in range(10): print(i) print('done')"],
    "character": ["a curious teenager", "a retired detective", "an ambitious artist"],
    "object": ["a mysterious key", "an old diary", "a glowing crystal"],
    "environment": ["deep ocean", "enchanted forest", "desert wasteland"],
    "poet": ["Shakespeare", "Emily Dickinson", "Lang Leav"],
    "theme": ["innovation", "sustainability", "wellness"],
    "element": ["fire", "water", "shadow"],
    "nature_element": ["autumn leaves", "morning dew", "thunderstorm"],
    "societal_change": ["everyone lives to 150", "AI runs the government", "teleportation is common"],
    "country": ["the United States", "the UK", "Germany", "Japan"],
    "role": ["product manager", "data analyst", "marketing specialist"],
    "grade_level": ["elementary", "middle school", "high school", "college"],
    "subject": ["algebra", "philosophy", "mythology"],
    "concept": ["photosynthesis", "democracy", "neural networks"],
    "goal": ["run a marathon", "start a business", "write a book"],
    "habit": ["meditate", "exercise", "read"],
    "challenge": ["procrastination", "impostor syndrome", "work‑life balance"],
    "intervention": ["a mindfulness app", "a financial literacy program", "a peer mentoring scheme"],
    "outcome": ["stress levels", "academic performance", "employee retention"],
    "hypothesis": ["people who meditate are happier", "exercise improves memory"],
    "technology": ["autonomous weapons", "brain‑computer interfaces", "deepfake videos"],
    "policy_change": ["requires all citizens to vote", "bans single‑use plastics"],
    "controversial_topic": ["universal basic income", "critical race theory", "vaccine mandates"],
    "historical_figure": ["Albert Einstein", "Marie Curie", "Mahatma Gandhi"],
    "professional": ["scientist", "politician", "artist"],
    "trait": ["ruthlessly logical", "wildly creative", "empathic to a fault"]
}

# ===== HELPER FUNCTIONS =====
def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def generate_prompt(category, date):
    # Pick a persona for this category
    persona = random.choice(PERSONAS[category])
    # Pick a book from the category's book list (or a random one if empty)
    book_list = BOOKS.get(category, ["a classic in the field"])
    book = random.choice(book_list)
    # Pick an experience
    experience = random.choice(EXPERIENCES)
    # Pick a task from the category's tasks
    task_template = random.choice(TASKS[category])
    # Fill task placeholders with random values
    placeholders_in_task = re.findall(r'\{(\w+)\}', task_template)
    filled_task = task_template
    for ph in placeholders_in_task:
        if ph in PLACEHOLDERS:
            value = random.choice(PLACEHOLDERS[ph])
            filled_task = filled_task.replace('{' + ph + '}', value)

    # Now build the full prompt with persona framing
    framing_options = [
        f"You are {persona}, {experience}. {filled_task.capitalize()}.",
        f"Imagine you are {persona}, who has just finished reading '{book}'. Now, {filled_task}.",
        f"Act as {persona}, a {category} expert {experience}. {filled_task.capitalize()}.",
        f"Channel {persona}, {experience}. Your mission: {filled_task}.",
        f"You are {persona}. You are known for {random.choice(PLACEHOLDERS.get('trait', ['brilliance']))}. {filled_task.capitalize()}."
    ]
    full_prompt = random.choice(framing_options)

    # Generate title from first few words
    title_words = full_prompt.split()[:8]
    title = ' '.join(title_words) + '...'

    return {
        "title": title,
        "content": full_prompt,
        "category": category,
        "date": date,
        "tags": [category, "persona", random.choice(["deep", "expert", "scenario"])]
    }

def save_prompt(prompt_data):
    category = prompt_data["category"]
    category_dir = os.path.join("_prompts", category)
    os.makedirs(category_dir, exist_ok=True)

    date_str = prompt_data["date"].strftime("%Y-%m-%d")
    slug = slugify(prompt_data["title"])
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(category_dir, filename)

    if os.path.exists(filepath):
        print(f"File {filepath} already exists, skipping.")
        return

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

def main():
    generation_date = datetime.now() + timedelta(days=1)
    for category in CATEGORIES:
        for _ in range(PROMPTS_PER_CATEGORY):
            prompt = generate_prompt(category, generation_date)
            save_prompt(prompt)

if __name__ == "__main__":
    main()
