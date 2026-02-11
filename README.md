This project is an LLM Agent designed to represent me professionally. It serves as a conversational interface for my CV and portfolio, allowing recruiters and visitors to ask questions about my background, skills, and experience.

The agent is grounded in my actual data (LinkedIn profile and professional summary) and has tool-use capabilities to notify me instantly via Slack when a user expresses interest.

Features:

Persona Simulation: acts as a digital twin, answering questions in the first person.

Context Awareness: ingests text from a summary.txt file and parses a linkedin_profile.pdf to ground answers in factual data.

Agentic Capabilities (Function/Tool Calling): detects when a user wants to connect and triggers a Python function to capture their email and name.

Slack Integration: sends a real-time notification to my personal Slack workspace via Webhook when a lead is captured.

Interactive UI: built with Gradio for a clean, chat-based web interface


