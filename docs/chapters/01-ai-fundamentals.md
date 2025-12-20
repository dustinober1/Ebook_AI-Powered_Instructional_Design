---
title: "Chapter 1: AI Fundamentals"
description: "Understanding the engine behind the AI-Powered ID: LLMs, tokens, and the mechanics of generative intelligence."
tags: ["foundations", "LLMs", "technical"]
difficulty: "Intermediate"
last_reviewed: 2025-12-20
reading_time: 10 min
authors: ["Dustin Ober"]
---

# AI Fundamentals for Instructional Designers

To design effective learning experiences with AI, we must first understand the "engine" that powers our tools. This chapter demystifies Large Language Models (LLMs) and explains the core concepts that every instructional designer should know.

## 1. What is an LLM?

A Large Language Model is a type of artificial intelligence trained on massive amounts of text data. It uses statistical patterns to predict the next word (or "token") in a sequence. 

> [!NOTE]
> Think of an LLM as a highly sophisticated "auto-complete" built on the sum of human digital knowledge.

For an ID, an LLM is more than a chatbot; it is a **reasoning engine**. It can synthesize information, take on personas (e.g., "Act as a subject matter expert in physics"), and format content into specific structures (e.g., "Generate a SCORM-compliant outline").

## 2. Tokens and Context Windows

Understanding how AI "reads" and "remembers" is crucial for prompt engineering.

### Tokens
AI doesn't read words like humans do. It breaks text into **tokens**—small chunks of characters. 1,000 tokens is roughly equal to 750 words. 
*Why does this matter?* API costs and model limits are often based on token counts.

### Context Window
The **context window** is the amount of information the model can "hold in its head" at once during a conversation. In 2025, context windows have expanded significantly (with some models handling millions of tokens), but the core principle remains: the more relevant context you provide in your prompt, the better the output.

## 3. Generative vs. Discriminative AI

- **Generative AI**: Creates new content (text, images, video) based on patterns. This is where most ID work happens (e.g., creating case studies).
- **Discriminative AI**: Classifies or analyzes existing data. In ID, this is used for grading, identifying gaps in a curriculum, or sentiment analysis of learner feedback.

## 4. The "Hallucination" Problem

One of the biggest challenges in AI-Powered ID is **hallucination**—when the model generates factually incorrect information that sounds highly convincing.

> [!IMPORTANT]
> Never use AI-generated content in a learning module without a Subject Matter Expert (SME) or your own rigorous verification. AI is a creative assistant, not an encyclopedia.

## 5. Ethical Considerations

As instructional designers, we have a responsibility to our learners:
- **Bias**: AI models can inherit biases from their training data. We must audit outputs for gender, racial, and cultural bias.
- **Privacy**: Never input sensitive student data or proprietary company information into public AI models.
- **Academic Integrity**: We must design assessments that focus on higher-order thinking (Bloom’s Taxonomy) which AI cannot easily replicate without human synthesis.

---

### Reflection Exercise
1.  Choose a topic you are currently teaching.
2.  Write a prompt for an LLM to generate three different ways to introduce that topic.
3.  Evaluate the output: Which one is the most engaging? Did the model hallucinate any facts?

---
*References:*
- Mollick, E. (2024). *Co-Intelligence: Living and Working with AI*. Portfolio.
- EDUCAUSE (2024). *2025 Horizon Report: Teaching and Learning Edition*.
