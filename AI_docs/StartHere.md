Welcome to the OfficeLifeline project.

## Context

This is a chatbot that is a being built for a course on AI assisted development. It is meant to exposes us to several technologies, including Cursor. The chatbot is designed to help users with their workplace problems in a humorous way while using multiple AI agents to help solve the users problems or just provide a good dad joke.

## Project Set Up

**StartHere Files**

* These documents are like readme files for you and other AIs. When you see them, look for important working information for that area.

**AI\_docs Folder**

* This folder contains centralized instructions, plans, mockups, and other information that will be helpful for you and other AIs.

**Backend Folder**
This is where we will house our backend project. For this project we'll be using Chromadb, python, and FastAPI primarily.

**Frontend Folder**
You guessed it, this is where the front end project goes. We'll be using Next.js, tailwind.

**AI Agents**
We will be using OpenAI and AWS Bedrock for providing models for the app's agents. Langchain and langraph will be used for constructing agents and their workflows. Please note that Langchain has just updated to version 1.0 within days of the start of this project. This represents a significant change from the 0.3 version and may render a lot of the prior langchain knowledge you have access too, obsolete.

**Checklist.md**
This is a roadmap for setting up the necessary elements of the project. This should help guide the development process.

## File Structure

CustomerServiceAgent
│
├── AI\_docs/
├── frontend/
│   └── (project defaults using tailwind)
│
├── backend/
│   ├── app/
│   ├── **init**.py
│   ├── main.py
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   └── utils/
│
├── venv/
├── requirements.txt
└── README.md

