#!/usr/bin/env python3
"""
generate_prompts.py (Long‑Form Genius Edition)
Generates 100 exceptionally detailed, multi‑part prompts daily.
Each prompt is designed to be lengthy, unusual, and thought‑provoking.
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
PROMPTS_PER_CATEGORY = 10  # 100 total

# ----- Long‑Form Templates (each is a substantial paragraph or multi‑part request) -----
TEMPLATES = {
    "marketing": [
        "Develop a comprehensive marketing strategy for a brand new product: {product}. The product will be launched in a market dominated by {competitor}. Your strategy should include: (1) a detailed customer persona for the target audience {audience}, (2) a unique selling proposition that leverages {benefit}, (3) a multi‑channel campaign outline using at least three unconventional channels (e.g., {unconventional_channel}), (4) a budget allocation table, and (5) a set of key performance indicators to measure success. Write the strategy in the form of a memo to the CEO, with clear sections and persuasive language.",
        "Imagine you are a cultural anthropologist from the year 2124 studying early 21st‑century marketing. Write a detailed analysis of a viral campaign for {product} that targeted {audience}. Describe the campaign's methods, why it resonated, and its long‑term impact on society. Include references to specific social media platforms, psychological triggers used, and any ethical controversies.",
        "Create a complete brand identity guide for a startup called '{startup_name}' that sells {product}. The guide should include: (1) a brand story (at least 200 words), (2) tone of voice guidelines with examples, (3) visual identity (colors, logo concept, typography), (4) sample social media posts for one week, and (5) a crisis communication plan for when {crisis_scenario} happens.",
        "Design a 12‑month content marketing calendar for a B2B company in the {industry} sector. The goal is to establish thought leadership around {topic}. For each month, provide a theme, three blog post ideas (with titles and brief outlines), one webinar topic, and one downloadable asset (e.g., whitepaper, template). Also include a strategy for repurposing content across LinkedIn, Twitter, and email newsletters.",
        "Write a detailed case study of how a small business used {product} to overcome {challenge}. The case study should follow this structure: (1) background of the business, (2) the challenge they faced (including specific pain points), (3) why they chose {product}, (4) implementation process (step‑by‑step), (5) results (with quantitative data if possible), and (6) a testimonial quote from the business owner. Make the story compelling and relatable.",
        "Develop a guerrilla marketing campaign for a non‑profit raising awareness about {cause}. The campaign should have a shock value element, a social media amplification strategy, and a way for people to get involved locally. Describe the core idea, the materials needed, the timeline, and how you'll measure impact. Also include a risk assessment: what could go wrong and how you'd handle it.",
        "Create a detailed customer journey map for someone purchasing {product} for the first time. The map should cover five stages: awareness, consideration, decision, purchase, and post‑purchase. For each stage, describe the customer's thoughts, emotions, touchpoints, and potential friction points. Then propose three interventions to improve the journey, each with a rationale and expected outcome.",
        "Write a script for a 5‑minute video ad that tells a story. The product is {product}, and the story should involve a character who {character_action}. The ad should have a narrative arc (beginning, middle, end), a voiceover, and visual descriptions. Also include a brief explanation of why this story will resonate with {audience}.",
        "Design a loyalty program for a chain of {business_type} stores. The program should encourage repeat visits and increase average spend. Describe the tiers, rewards, how customers earn points, and a creative way to celebrate member anniversaries. Also include a plan to promote the program in‑store and via email, and how you'll measure its success (e.g., repeat purchase rate, CLV).",
        "Conduct a competitive analysis for a new entrant in the {industry} market. Identify three main competitors: {competitor1}, {competitor2}, and {competitor3}. For each, analyze their strengths, weaknesses, market positioning, and marketing strategies. Then recommend a differentiation strategy for the new brand, including messaging, pricing, and channels to focus on."
    ],
    "legal": [
        "Draft a comprehensive contract for a collaborative project between a human artist and an AI art generator. The contract should cover: (1) ownership of the final artwork and any derivative works, (2) revenue sharing from sales, (3) credit and attribution, (4) termination rights, (5) confidentiality of the AI's training data, and (6) dispute resolution. Explain each clause in plain language after the legal text.",
        "Write a legal opinion on whether a city can ban autonomous vehicles from its downtown core. Consider constitutional issues, federal vs state jurisdiction, safety arguments, and economic impacts. Provide arguments for and against, then conclude with your reasoned opinion, citing relevant cases or principles.",
        "Create a step‑by‑step guide for a startup to navigate intellectual property issues when developing a new software product. Include: (1) when to file patents (and what kind), (2) how to protect trade secrets, (3) trademarking the brand name, (4) open source license compliance, and (5) employee IP agreements. For each step, explain why it matters and common pitfalls.",
        "Draft a memo analyzing the legality of using deepfake technology to create a political advertisement. Discuss potential violations of election laws, defamation, right of publicity, and any relevant statutes. Also propose a set of regulations that could govern such ads, balancing free speech with public interest.",
        "Simulate a negotiation between two parties over a disputed contract clause. The clause involves {contract_topic}. Write the dialogue of the negotiation, showing each party's position, their arguments, and how they eventually reach a compromise. Then summarize the final agreed language.",
        "Write a legal FAQ for content creators who use samples in their music. Cover questions like: What is fair use? How do I get permission? What if the sample is unrecognizable? What are the penalties for infringement? Provide clear, accurate answers with examples.",
        "Draft a privacy policy for a mobile app that collects location data, health data, and contacts. The policy must comply with GDPR and CCPA. Include sections on data collection, use, sharing, user rights, and security measures. Also write a short 'plain English' summary for users.",
        "Prepare a closing argument for a trial where a company is accused of false advertising. The product in question is {product}, and the alleged false claim is {claim}. Write a persuasive speech for the defense, highlighting why the claim is not misleading, using expert testimony and consumer survey data.",
        "Create a checklist for a law firm to ensure compliance with anti‑money laundering regulations when taking on a new client. Include steps for identity verification, risk assessment, ongoing monitoring, and record‑keeping. Explain the rationale behind each step.",
        "Write a law review article abstract on the topic of 'legal personhood for artificial intelligence.' Summarize the current debate, propose a novel framework (e.g., a 'digital entity' status), and outline the implications for contracts, torts, and criminal law."
    ],
    "medical": [
        "Write a detailed case study of a patient presenting with a rare combination of symptoms: {symptom_list}. Describe the diagnostic process, including differential diagnoses, tests ordered, and how the final diagnosis was reached. Then propose a treatment plan that considers the patient's age, lifestyle, and preferences. Include a discussion of any ethical dilemmas encountered.",
        "Design a public health campaign to combat vaccine hesitancy in a specific community: {community_description}. The campaign should use insights from behavioral psychology, include multiple channels (social media, community events, partnerships with trusted figures), and have a clear message. Provide a timeline, budget outline, and methods for evaluating effectiveness.",
        "Create a detailed protocol for a clinical trial investigating a new drug for {disease}. The protocol must include: (1) study objectives and hypothesis, (2) design (randomized, double‑blind, placebo‑controlled), (3) inclusion/exclusion criteria, (4) recruitment strategy, (5) interventions and dosages, (6) outcome measures (primary and secondary), (7) data analysis plan, and (8) ethical considerations and informed consent process.",
        "Write a patient education handout explaining a complex medical condition (e.g., {condition}) in simple, compassionate language. Use analogies, diagrams described in text, and FAQs. Include tips for managing the condition at home and when to seek help. The handout should be suitable for a 8th‑grade reading level.",
        "Simulate a conversation between a doctor and a patient who is reluctant to undergo a recommended surgery. The surgery is for {condition}, and the patient's fears include {fears}. Write the dialogue, showing the doctor's empathetic communication, risk/benefit explanation, and how they address each fear. End with the patient's decision.",
        "Write a research proposal to study the long‑term effects of meditation on brain structure and function. Include a literature review summary, hypotheses, methods (participants, MRI protocols, meditation intervention), expected results, and potential implications for mental health treatment.",
        "Create a differential diagnosis for a patient presenting with {symptom1}, {symptom2}, and {symptom3}. List at least five possible conditions, ranked by likelihood. For each, explain the rationale, what additional tests would confirm or rule it out, and any red flags.",
        "Draft a policy brief for a hospital administration on how to integrate AI diagnostic tools into clinical workflow. Address benefits, risks, training needs, legal liability, and patient acceptance. Include recommendations for a pilot program and metrics to evaluate success.",
        "Write a detailed description of a novel surgical technique for {procedure}. Include indications, step‑by‑step instructions, potential complications, and post‑operative care. Also discuss how it compares to existing techniques in terms of outcomes, recovery time, and cost.",
        "Design a wellness program for a corporate office aimed at reducing burnout. The program should include individual, team, and organizational interventions. Provide a rationale for each component, a rollout plan, and ways to measure employee well‑being before and after."
    ],
    "engineering": [
        "Write a detailed system design document for a scalable real‑time chat application like WhatsApp. Include: (1) requirements (functional and non‑functional), (2) high‑level architecture (with diagram described in text), (3) data models, (4) API endpoints, (5) key algorithms (e.g., for message delivery, presence, end‑to‑end encryption), (6) scaling considerations (database sharding, caching, load balancing), and (7) trade‑offs and alternatives considered.",
        "Create a tutorial for beginners on how to build a simple web scraper in Python. The tutorial should include: (1) an explanation of what web scraping is and its legal/ethical considerations, (2) step‑by‑step instructions with code snippets, (3) handling dynamic content, (4) storing data in a CSV, and (5) common pitfalls and how to avoid them. Include comments in the code and a sample output.",
        "Design an algorithm to detect plagiarism in student essays. Describe the approach in detail: how you would preprocess text, what similarity measures you'd use (e.g., cosine similarity, fingerprinting), how to handle paraphrasing, and how to scale to thousands of submissions. Provide pseudocode and discuss accuracy, false positives/negatives.",
        "Write a post‑mortem for a major system outage. The outage affected a {service_type} for {duration}. Describe the timeline, root cause, impact, how it was detected, steps taken to mitigate, and lessons learned. Then propose specific improvements to prevent recurrence, including monitoring, testing, and architectural changes.",
        "Create a detailed guide for setting up a CI/CD pipeline using GitHub Actions for a {language} project. Include: (1) triggers (push, pull request), (2) jobs for linting, testing, building, and deploying, (3) environment variables and secrets, (4) caching dependencies, (5) notifications on failure, and (6) a sample workflow file with explanations.",
        "Explain the concept of 'eventual consistency' in distributed systems using a real‑world analogy (e.g., a library with multiple branches). Then describe a scenario where strong consistency is required and why. Finally, outline how you would implement a eventually consistent system using a gossip protocol, including the data structures and message formats.",
        "Write a code review for a pull request that adds a new feature to a web app. The code is for {functionality}. Provide specific feedback on: code style, potential bugs, performance issues, test coverage, and documentation. Suggest concrete improvements and explain why they matter.",
        "Design a database schema for a social media platform that supports user profiles, posts, comments, likes, and follower relationships. Include tables, fields, data types, indexes, and foreign keys. Also discuss how you would handle denormalization for performance, and write a few sample queries (e.g., get feed for a user).",
        "Create a security checklist for deploying a web application. Cover areas like authentication, authorization, input validation, data encryption, session management, dependency scanning, and server hardening. For each item, explain the threat it mitigates and provide a recommendation (e.g., use HTTPS, parameterized queries).",
        "Write a technical specification for a new feature: a recommendation engine for an e‑commerce site. Describe the data sources (user behavior, product metadata), the algorithm (collaborative filtering, content‑based, hybrid), how you would train and evaluate it, the API for serving recommendations, and how to handle cold start for new users/products."
    ],
    "creative": [
        "Write a short story (800–1000 words) set in a world where memories can be bought and sold. The protagonist is a {profession} who discovers a black market for stolen childhood memories. Develop the world, the characters, and a twist ending. After the story, include a brief author's note explaining the themes and influences.",
        "Create a detailed character profile for a villain who believes they are the hero. Include: (1) name, age, appearance, (2) backstory (what made them this way), (3) personality traits (with both positive and negative), (4) goals and motivations, (5) strengths and weaknesses, (6) a signature quote, and (7) a scene that shows their complexity (e.g., showing kindness to a child while planning a heist).",
        "Write a poem in free verse about the last tree on Earth. The poem should evoke a sense of loss, beauty, and hope. Use imagery from nature and technology. Then write a short analysis of the poem, explaining the symbolism and literary devices used.",
        "Design a fantasy world based on the concept of 'emotion as magic.' Describe: (1) the different types of magic (e.g., joy‑weaving, sorrow‑shaping), (2) how people are born with affinities, (3) the society's structure (are emotion‑mages revered or feared?), (4) a conflict that arises from this magic system, and (5) a protagonist who has a rare or forbidden emotion affinity.",
        "Write a dialogue between two characters who are opposites: one is a hopeless romantic, the other is a cynical realist. They are discussing whether love at first sight exists. The dialogue should reveal their personalities, backstories, and perhaps end with a subtle shift in one of their views.",
        "Create a plot for a mystery novel where the detective is a librarian who solves crimes using research skills. Outline the plot in three acts, including the crime, clues, red herrings, and the resolution. Also develop two suspects with motives and alibis, and explain how the detective finally solves the case.",
        "Write a letter from a future human to a present‑day teenager, warning them about a specific mistake their generation is making. The letter should be personal, emotional, and include specific examples of what will happen if things don't change. Also include a plea for action.",
        "Describe a scene in a restaurant where all the food is alive and has opinions. Write from the perspective of a diner trying to order a meal while the menu items argue about which one should be chosen. Make it humorous and absurd, but also explore deeper themes of free will and consumption.",
        "Write a monologue for a tree that has stood in a town square for 500 years. It has witnessed wars, celebrations, and daily life. The tree speaks about what it has seen, how humans have changed, and what it hopes for the future. Use poetic language.",
        "Create a fictional myth explaining why the moon follows us when we drive at night. The myth should involve a celestial romance, a punishment, and a moral lesson. Write it in the style of an ancient storyteller, with a rhythmic, oral quality."
    ],
    "business": [
        "Write a comprehensive business plan for a startup that offers a subscription box service for {niche}. The plan should include: (1) executive summary, (2) company description, (3) market analysis (size, trends, competitors), (4) product line (what's in the box, sourcing), (5) marketing and sales strategy, (6) operational plan (fulfillment, customer service), (7) financial projections (3‑year, with assumptions), and (8) funding request. Use realistic numbers and explain your reasoning.",
        "Develop a detailed go‑to‑market strategy for a new B2B software product aimed at {industry} companies. The product helps solve {problem}. Include: (1) target customer segments, (2) positioning and messaging, (3) pricing model (with justification), (4) sales channels (direct, partners, online), (5) launch timeline with key milestones, and (6) metrics to track success. Also include a competitive analysis grid.",
        "Conduct a SWOT analysis for a well‑known company (e.g., {company}) in the context of a emerging trend: {trend}. Present the analysis in a table, then write a strategic recommendation based on the findings. Suggest specific actions the company should take to leverage strengths, address weaknesses, seize opportunities, and mitigate threats.",
        "Create a detailed employee onboarding program for a tech company. The program should cover: (1) pre‑arrival preparation, (2) first day agenda, (3) first week goals and checklists, (4) first 90‑day development plan, (5) mentorship assignment, (6) culture immersion activities, and (7) feedback mechanisms. Explain why each element is important.",
        "Write a memo to the board of directors proposing a major pivot for the company. The current business is {current_business}, and you propose moving into {new_business} because of {market_change}. Include a risk assessment, financial implications, timeline, and how you'll communicate the change to employees and customers.",
        "Design a customer feedback system for a retail chain. The system should collect feedback at multiple touchpoints (in‑store, online, post‑purchase), analyze sentiment, and trigger actions. Describe the tools (e.g., surveys, NPS, social listening), how you'll close the loop with customers, and how you'll use insights to improve operations.",
        "Create a negotiation strategy for acquiring a smaller competitor, {competitor}. Outline your goals, BATNA, key concessions you're willing to make, and tactics. Also prepare a dossier on the competitor: their strengths, weaknesses, likely motivations, and who the decision‑makers are. Finally, write a script for the first meeting.",
        "Develop a crisis communication plan for a food company facing a product recall. The plan should include: (1) immediate response team, (2) key messages for different stakeholders (customers, media, regulators, employees), (3) communication channels, (4) FAQ document, (5) timeline of actions, and (6) post‑crisis review. Draft an example press release.",
        "Write a thought leadership article on the future of work, focusing on how {trend} will reshape offices. The article should be 800‑1000 words, aimed at executives. Include data points, expert opinions, and practical recommendations. Also propose a catchy title and a social media promotion plan.",
        "Design a diversity, equity, and inclusion (DEI) initiative for a mid‑sized company. The initiative should include: (1) a statement of commitment, (2) recruitment and hiring practices to increase diversity, (3) training programs, (4) employee resource groups, (5) mentorship for underrepresented groups, and (6) metrics to track progress. Provide a rollout timeline and budget."
    ],
    "education": [
        "Design a full‑semester course syllabus on the topic of 'The Philosophy of Technology.' Include: (1) course description and objectives, (2) required readings (with authors), (3) weekly topics and key questions, (4) assignments (papers, presentations, participation), (5) grading rubric, and (6) a statement on academic integrity. Also write a welcome message to students that sets the tone.",
        "Create a detailed lesson plan for a 90‑minute class on {subject} for high school students. The plan should include: (1) learning objectives, (2) materials needed, (3) hook/engagement activity, (4) direct instruction with key concepts, (5) guided practice (group work), (6) independent practice, (7) assessment (formative), and (8) closure. Include time estimates for each segment.",
        "Write a set of 10 challenging essay questions for a university‑level exam on {topic}. For each question, provide a brief explanation of what a strong answer would include. Also include a grading rubric with criteria like argument, evidence, clarity, and originality.",
        "Develop a project‑based learning unit where students create a podcast about a local historical event. Outline the project steps: research, interviewing, scriptwriting, recording, editing, and publishing. Provide rubrics for each phase, a timeline, and resources. Also include reflection questions for students after completion.",
        "Create a guide for teachers on how to handle controversial topics in the classroom. Include: (1) establishing ground rules, (2) strategies for facilitating discussion, (3) dealing with emotional reactions, (4) ensuring multiple perspectives, and (5) self‑care for the teacher. Use examples from topics like {controversial_topic}.",
        "Write a feedback comment for a student's research paper that is constructive and encouraging. The paper is on {topic}, and the main strengths are {strengths}, while areas for improvement include {weaknesses}. Provide specific suggestions and resources.",
        "Design a gamified learning activity to teach vocabulary in a foreign language. Describe the game mechanics, rules, how students earn points, and how it aligns with learning objectives. Also discuss how you'd assess learning and keep students engaged over time.",
        "Create a professional development workshop for teachers on integrating technology into the classroom. Outline the workshop agenda, activities, handouts, and follow‑up support. Include examples of tools (e.g., interactive whiteboards, online quizzes, VR) and how they can enhance learning.",
        "Write a letter to parents explaining a new social‑emotional learning curriculum being introduced. Describe the goals, key components, how it will be taught, and how parents can reinforce it at home. Address potential concerns and invite questions.",
        "Develop an assessment rubric for a student presentation on {topic}. Include criteria such as content knowledge, organization, delivery, visual aids, and handling of questions. Provide descriptors for exemplary, proficient, developing, and beginning levels."
    ],
    "personal": [
        "Write a guided journaling exercise for someone going through a major life transition (e.g., {transition}). The exercise should include: (1) a centering meditation, (2) prompts to explore feelings of loss and gain, (3) questions about what they're learning, (4) a visualization of their future self, and (5) an action step for the week. Write in a warm, encouraging tone.",
        "Create a 30‑day personal challenge to cultivate a new habit: {habit}. Each day, provide a specific, small action, a reflection question, and a quote for motivation. Include a weekly review and a final celebration. The challenge should be achievable yet stretch the person.",
        "Design a personal mission statement worksheet. Include: (1) a list of core values to choose from, (2) prompts to identify strengths and passions, (3) a vision for the future, (4) a statement template, and (5) examples. After the worksheet, provide guidance on how to live the mission daily.",
        "Write a letter from your future self (10 years from now) to your present self. Describe what you've accomplished, what you've learned, and what you're grateful for. Also mention challenges you overcame and advice for the journey. Make it personal and inspiring.",
        "Develop a self‑care plan for someone with a busy schedule. Include: (1) daily non‑negotiables (e.g., 5 min meditation), (2) weekly activities (e.g., exercise, hobby), (3) monthly check‑ins, (4) emergency self‑care kit, and (5) signs of burnout to watch for. Provide a template to fill in.",
        "Create a guided visualization for achieving a big goal: {goal}. The visualization should engage all senses, include steps along the journey, and end with the feeling of success. Write it as a script that can be read aloud or recorded.",
        "Write a series of 10 affirmations for someone struggling with {challenge}. Each affirmation should be positive, present‑tense, and emotionally resonant. Include a brief explanation of how to use affirmations effectively.",
        "Design a weekly review ritual to reflect on progress, celebrate wins, and adjust plans. Outline the steps: (1) review calendar and tasks, (2) journal on what worked and what didn't, (3) identify three things to improve, (4) set intentions for the coming week, (5) a gratitude practice. Provide prompts for each step.",
        "Create a list of 50 questions for deep self‑discovery. Categorize them into areas like past, present, future, relationships, work, and spirituality. Encourage the reader to answer one each day and reflect.",
        "Write a eulogy for a version of yourself that you're letting go of (e.g., the procrastinator, the people‑pleaser). Celebrate the positive aspects, acknowledge the pain, and commit to a new way of being. Make it a ritual of release."
    ],
    "research": [
        "Write a detailed research proposal to investigate the effects of {intervention} on {outcome} in {population}. The proposal should include: (1) introduction with background and significance, (2) literature review summary (at least 5 key studies), (3) research questions and hypotheses, (4) methods (design, participants, measures, procedure), (5) data analysis plan, (6) ethical considerations, (7) timeline, and (8) budget. Use APA style for citations.",
        "Create a literature review matrix on the topic of {topic}. Include at least 10 sources, with columns for author/year, research question, methods, key findings, and limitations. After the table, write a synthesis paragraph identifying themes and gaps.",
        "Design a survey to measure attitudes toward {topic} among {population}. Include: (1) demographic questions, (2) at least 10 Likert‑scale items, (3) a few open‑ended questions, (4) instructions, and (5) a debriefing statement. Explain how you would validate the survey and ensure reliability.",
        "Write a peer review of a hypothetical manuscript titled '{manuscript_title}'. The review should include: (1) a summary of the paper, (2) overall assessment, (3) major comments (e.g., issues with methodology, missing controls), (4) minor comments (e.g., clarity, citations), and (5) a recommendation (accept, minor revisions, major revisions, reject). Be constructive and specific.",
        "Describe an experimental design to test whether {hypothesis}. Include: (1) independent and dependent variables, (2) control conditions, (3) random assignment, (4) sample size justification, (5) procedure step‑by‑step, and (6) potential confounding variables and how you'll control them.",
        "Create a data analysis plan for a study using a mixed‑methods approach. The quantitative part involves a survey (N=500) on {topic}, and the qualitative part involves 20 semi‑structured interviews. Describe how you'll analyze the quantitative data (descriptive stats, inferential tests) and qualitative data (thematic analysis), and how you'll integrate findings.",
        "Write an abstract for a conference presentation on your research about {topic}. The abstract should be 250‑300 words, including background, methods, results (even if preliminary), and conclusions. Also include 3‑5 keywords.",
        "Develop a research ethics application for a study involving vulnerable populations (e.g., children, prisoners). Address: (1) informed consent process, (2) confidentiality, (3) potential risks and benefits, (4) how you'll minimize harm, (5) data storage, and (6) debriefing. Write in a formal style suitable for an ethics board.",
        "Create a concept map or visual framework for a new theory about {phenomenon}. Describe the key constructs, their relationships, and hypotheses that can be derived. Use text to explain the diagram, and discuss how you would test the theory.",
        "Write a grant proposal summary for a project on {topic} aimed at a funding agency like the NSF or NIH. Include: (1) project summary, (2) intellectual merit, (3) broader impacts, (4) budget overview, and (5) a list of key personnel. Keep it concise but compelling."
    ],
    "multiperspective": [
        "Simulate a roundtable discussion among three experts: a {profession1}, a {profession2}, and a {profession3}, discussing the ethical implications of {technology}. Write a 1500‑word dialogue where each presents their view, challenges the others, and eventually finds some common ground. Include an introduction setting the scene and a conclusion summarizing the outcomes.",
        "Create a focus group transcript involving five personas: {persona_list}. They are reacting to a new policy that would {policy_change}. Write their individual comments, interactions, and a final summary of themes. Ensure each persona's voice is distinct (e.g., age, background, opinion).",
        "Write a debate between a proponent and an opponent of {controversial_topic}. The debate should have opening statements, three rebuttals each, and closing remarks. Use evidence and logical arguments. After the debate, provide a judge's decision explaining who won and why.",
        "Imagine a meeting between a historical figure (e.g., {historical_figure}) and a modern expert in {field} to discuss a current issue: {current_issue}. Write the dialogue, showing how the historical figure's perspective differs and what insights they offer. End with a reflection on what we can learn.",
        "Present a SWOT analysis of {organization_or_technology} from the viewpoints of: a customer, an employee, a competitor, and an investor. Create a table with rows for Strengths, Weaknesses, Opportunities, Threats and columns for each stakeholder. Then write a narrative summary integrating these perspectives.",
        "Simulate a mediation session between two parties in a conflict: {partyA} and {partyB}, over {conflict_topic}. Write the mediator's opening, each party's statement, the negotiation dialogue, and the final agreement (or impasse). Include the mediator's techniques.",
        "Write a series of diary entries from three different people experiencing the same event (e.g., a citywide power outage) from their unique perspectives: a elderly person living alone, a teenager, and a first responder. Each entry should reflect their concerns, actions, and emotions. After the entries, write a brief analysis of how perspective shapes experience.",
        "Create a panel discussion transcript on the future of education, featuring a teacher, a student, a parent, and a policymaker. Each gives a 2‑minute opening, then they respond to questions about technology, equity, and curriculum. End with a consensus statement or a list of action items.",
        "Design a role‑play scenario for a business ethics class where students take on roles: CEO, whistleblower, shareholder, journalist. The scenario involves a company covering up a safety defect. Write the角色 descriptions, the situation, and a series of prompts for discussion. Then simulate how a real conversation might go.",
        "Write a conversation between an AI and a philosopher about whether AI can be conscious. The AI argues that it is, the philosopher is skeptical. The dialogue should delve into definitions of consciousness, the Turing test, subjective experience, and ethical implications. End with both agreeing to disagree but with a new insight."
    ]
}

# ----- Placeholders – Expanded for Rich Detail -----
PLACEHOLDERS = {
    # Basic ones reused across categories
    "product": [
        "a smart water bottle that analyzes hydration levels and suggests drinks",
        "a subscription service that sends you a mystery object each month, each with a story",
        "a pair of glasses that translate sign language into text in real time",
        "a plant pot that plays music based on the plant's growth patterns",
        "a notebook that digitises handwritten notes and organises them by topic"
    ],
    "audience": [
        "Gen Z digital natives who value authenticity",
        "busy working parents looking for time‑savers",
        "retirees eager to learn new technology",
        "small business owners in rural areas",
        "college students struggling with mental health"
    ],
    "benefit": [
        "reduces decision fatigue by 30%",
        "creates a sense of belonging through shared experiences",
        "saves an average of 2 hours per week",
        "boosts creativity by exposing users to unexpected ideas",
        "improves sleep quality through personalised wind‑down routines"
    ],
    "industry": [
        "renewable energy", "e‑commerce", "telehealth", "edtech", "fintech"
    ],
    "topic": [
        "the ethics of predictive policing",
        "how to preserve indigenous languages using AI",
        "the impact of remote work on urban planning",
        "the psychology of conspiracy theories",
        "the future of meat: lab‑grown vs plant‑based"
    ],
    "competitor": [
        "Amazon", "a dominant local player", "a innovative startup", "a traditional company slow to change"
    ],
    "unconventional_channel": [
        "interactive street art with QR codes",
        "pop‑up escape rooms themed around the product",
        "collaborations with astrologers for personalised product horoscopes",
        "a secret society‑style membership card",
        "guerrilla gardening with branded seed bombs"
    ],
    "startup_name": [
        "Nexus", "Aether", "Verdant", "Lumina", "Echo"
    ],
    "crisis_scenario": [
        "a viral video shows a customer misusing the product and getting hurt",
        "a supplier is accused of child labour",
        "a data breach exposes user emails",
        "a celebrity endorses a competitor instead"
    ],
    "business_type": [
        "coffee shop", "bookstore", "fitness studio", "hardware store", "pet grooming salon"
    ],
    "competitor1": ["Brand A", "Brand B", "Brand C"],
    "competitor2": ["Brand X", "Brand Y", "Brand Z"],
    "competitor3": ["Startup 1", "Startup 2", "Startup 3"],

    # Legal
    "contract_topic": [
        "intellectual property rights in a joint venture",
        "indemnification for third‑party claims",
        "termination for convenience",
        "non‑compete clause after employment"
    ],
    "claim": [
        "our product cures headaches in 10 minutes",
        "made with 100% organic ingredients",
        "the most advanced AI on the market",
        "you'll save $500 a year"
    ],

    # Medical
    "symptom_list": [
        "persistent cough, night sweats, weight loss, and fatigue",
        "sudden vision loss, severe headache, and nausea",
        "joint pain, skin rash, and sensitivity to sunlight",
        "memory lapses, mood swings, and difficulty walking"
    ],
    "community_description": [
        "a rural town with limited internet access",
        "an urban immigrant community with language barriers",
        "a conservative religious group",
        "a university campus with highly educated but skeptical students"
    ],
    "disease": [
        "Alzheimer's", "rheumatoid arthritis", "type 2 diabetes", "major depressive disorder"
    ],
    "condition": [
        "chronic obstructive pulmonary disease (COPD)",
        "irritable bowel syndrome (IBS)",
        "attention deficit hyperactivity disorder (ADHD)"
    ],
    "fears": [
        "the surgery might paralyze me", 
        "I'll be dependent on medication forever",
        "I can't afford the time off work",
        "my family will have to care for me"
    ],
    "symptom1": ["fever", "cough", "fatigue", "rash"],
    "symptom2": ["headache", "nausea", "dizziness", "shortness of breath"],
    "symptom3": ["joint pain", "chest pain", "confusion", "blurred vision"],
    "procedure": [
        "laparoscopic cholecystectomy (gallbladder removal)",
        "coronary artery bypass grafting",
        "total knee replacement"
    ],

    # Engineering
    "service_type": [
        "cloud storage", "payment processing", "social media feed", "video streaming"
    ],
    "duration": ["2 hours", "45 minutes", "6 hours", "over a weekend"],
    "language": ["Python", "JavaScript", "Java", "Go", "Rust"],
    "functionality": [
        "user authentication with OAuth", 
        "a recommendation algorithm", 
        "real‑time notifications using WebSockets"
    ],

    # Creative
    "profession": [
        "librarian", "detective", "chef", "astronaut", "street musician"
    ],

    # Business
    "niche": [
        "artisanal hot sauce", "vintage video games", "ethical fashion for pets", "indie board games"
    ],
    "problem": [
        "inefficient inventory management", "low customer engagement", "high employee turnover"
    ],
    "company": ["Apple", "Tesla", "Nike", "Starbucks", "Netflix"],
    "trend": [
        "the rise of AI influencers", "the shift to hybrid work", "the circular economy"
    ],
    "current_business": ["selling physical books", "running a chain of gyms", "manufacturing plastic toys"],
    "new_business": ["selling e‑books and audiobooks", "offering online fitness classes", "creating eco‑friendly toys from recycled materials"],
    "market_change": [
        "declining foot traffic in malls", "increased demand for home workouts", "new regulations on plastic"
    ],

    # Education
    "subject": [
        "the American Revolution", "photosynthesis", "Shakespeare's tragedies", "quadratic equations"
    ],
    "controversial_topic": [
        "climate change", "vaccination mandates", "critical race theory"
    ],
    "strengths": [
        "strong thesis, good use of sources", "creative approach, engaging writing"
    ],
    "weaknesses": [
        "weak conclusion, some grammatical errors", "lack of counterarguments, formatting issues"
    ],

    # Personal
    "transition": [
        "moving to a new city", "starting a new job", "ending a long relationship", "becoming a parent"
    ],
    "habit": [
        "meditate for 10 minutes daily", "drink 8 glasses of water", "write in a journal", "exercise for 30 minutes"
    ],
    "goal": [
        "run a marathon", "start a side business", "learn to play guitar", "save $10,000"
    ],
    "challenge": [
        "imposter syndrome", "procrastination", "fear of public speaking", "low self‑esteem"
    ],

    # Research
    "intervention": [
        "a mindfulness app", "a financial literacy program", "a peer mentoring scheme"
    ],
    "outcome": [
        "stress levels", "academic performance", "employee retention"
    ],
    "population": [
        "college freshmen", "remote workers", "patients with chronic pain"
    ],
    "manuscript_title": [
        "The Effects of Blue Light on Sleep: A Meta‑Analysis",
        "AI in Healthcare: A Systematic Review",
        "Remote Work and Productivity: A Longitudinal Study"
    ],
    "hypothesis": [
        "people who meditate are happier", "exercise improves memory", "social media use increases anxiety"
    ],

    # Multiperspective
    "profession1": ["a neuroscientist", "a philosopher", "a software engineer"],
    "profession2": ["a sociologist", "a legal scholar", "an artist"],
    "profession3": ["a theologian", "an economist", "a science fiction writer"],
    "technology": [
        "autonomous weapons", "brain‑computer interfaces", "deepfake videos"
    ],
    "persona_list": [
        "a single mother of two, age 35", "a retired veteran, age 70", "a college student, age 20", "a small business owner, age 45", "a high school teacher, age 50"
    ],
    "policy_change": [
        "requires all citizens to vote", "bans single‑use plastics", "makes public transit free"
    ],
    "historical_figure": [
        "Albert Einstein", "Marie Curie", "Mahatma Gandhi", "Ada Lovelace"
    ],
    "current_issue": [
        "climate change", "artificial intelligence", "income inequality"
    ],
    "organization_or_technology": [
        "Tesla", "the gig economy", "5G networks"
    ],
    "partyA": ["management", "the union", "environmental activists"],
    "partyB": ["workers", "the company", "oil industry lobbyists"],
    "conflict_topic": [
        "wage cuts", "a new factory construction", "data privacy policies"
    ]
}

# ----- Helper Functions (unchanged) -----
def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def generate_prompt(category, date):
    template = random.choice(TEMPLATES[category])
    placeholders_in_template = re.findall(r'\{(\w+)\}', template)
    filled = template
    for ph in placeholders_in_template:
        if ph in PLACEHOLDERS:
            value = random.choice(PLACEHOLDERS[ph])
            filled = filled.replace('{' + ph + '}', value)
    # Generate title from the first few words (now longer prompts may have longer titles)
    title_words = filled.split()[:8]
    title = ' '.join(title_words) + '...'
    return {
        "title": title,
        "content": filled,
        "category": category,
        "date": date,
        "tags": [category, "longform", random.choice(["in‑depth", "complex", "detailed", "multi‑part"])]
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
    # Use tomorrow's date so prompts appear fresh each day (adjust as needed)
    generation_date = datetime.now() + timedelta(days=1)
    for category in CATEGORIES:
        for _ in range(PROMPTS_PER_CATEGORY):
            prompt = generate_prompt(category, generation_date)
            save_prompt(prompt)

if __name__ == "__main__":
    main()
