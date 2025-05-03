# -*- coding: utf-8 -*-
"""
Module Name: nudge.py

Description:
This module generates unique, practical nudges to help users break their 
routine in meaningful ways. It uses the OpenAI GPT-4 model to provide 
insightful suggestions based on a variety of prompts.

Author: elreysausage

Date: 2025-01-25
"""

import random

import openai


def get_random_prompt(location: str, preferences: list | None) -> str:
    """
    Returns a randomly selected prompt based on user preferences.

    Args:
        location: The city or location to include in the prompt.
        preferences: A list of preferred categories for prompts.

    Returns:
        str: A random prompt for generating a nudge.
    """
    prompts = {
        "intellectual": [
            "Recommend a book that will challenge my way of thinking.",
            "Point me to a speech that presents a unique or controversial perspective.",
            "Introduce me to an aspect of history that people rarely talk about.",
            "Pose a paradox that will force me to rethink my assumptions.",
            "Introduce a philosophical debate that doesn’t have a clear answer.",
            "Explain a scientific concept that is counterintuitive but true.",
            "Describe a psychological study with surprising implications.",
            "Encourage me to rethink an assumption I hold strongly.",
            "Challenge me to engage with a topic I usually avoid.",
            "Suggest an experiment that helps me notice patterns around me.",
            "Give me a documentary that challenges a mainstream belief.",
            "Tell me about a cultural practice that might feel unusual to me.",
            "Suggest a way to look at a common problem from an absurd angle.",
        ],
        "creative": [
            "Suggest an unusual activity that involves using my hands creatively.",
            "Find an artistic practice I can attempt with no prior skill.",
            "Give me a challenge that involves using only my sense of touch.",
            "Suggest a task that forces me to listen more intently.",
            "Suggest a way to bring an element of play into my day.",
            "Propose a creative challenge I can complete in under five minutes.",
            "Suggest a way to reframe a mistake into a discovery.",
            "Encourage me to create something using only found objects.",
            "Give me a creative limitation and challenge me to work within it.",
            "Find an unconventional way to capture a memory.",
            "Give me an interaction challenge that forces creativity.",
        ],
        "social": [
            "Suggest a way to interact with strangers that breaks the norm.",
            "Give me an excuse to talk to a complete stranger today.",
            "Encourage me to interact with someone in a way I wouldn’t normally do.",
            "Suggest an act of generosity that doesn’t involve money.",
            "Propose a social experiment that is harmless but thought-provoking.",
            "Propose an unexpected conversation starter.",
            "Find a simple way to make today’s conversations more engaging.",
            "Suggest a way to make a regular interaction more meaningful.",
            "Encourage me to leave an anonymous note for someone.",
            "Propose an interaction challenge that requires no words.",
            "Give me an exercise that helps me see familiar people in a new light.",
        ],
        "exploration": [
            "Find a micro-adventure I can take within the next hour.",
            "Give me a new way to engage with nature, even in an urban setting.",
            f"Find me a historical site in {location} that most locals don’t know about.",
            f"Point me to a hidden bar or underground venue in {location} that’s not widely advertised.",
            f"What’s an abandoned place in {location} with an interesting backstory?",
            f"Is there a local museum or gallery in {location} with a strange or niche focus that I should visit?",
            f"Find me a restaurant in {location} that serves a dish I’ve likely never tried before.",
            f"Show me an urban legend or mysterious location in {location}.",
            f"Where can I attend an offbeat or underground event happening this week in {location}?",
            f"What’s a quiet, little-known green space in {location} where I can be alone with my thoughts?",
            f"Find a piece of public art in {location} that tells a fascinating or overlooked story.",
            "Suggest a way to interact with my surroundings like an explorer.",
        ],
        "mindfulness": [
            "Recommend an action that will temporarily change my sensory experience.",
            "Challenge me to perceive my environment as if for the first time.",
            "Suggest a challenge that gets me to engage with the present moment.",
            "Find a task that requires full concentration and attention.",
            "Suggest an experiment that forces me to think non-linearly.",
            "Provide a challenge that makes me more aware of my environment.",
            "Challenge me to experience my home differently today.",
            "Encourage me to practice patience in an unexpected way.",
            "Give me a creative way to reflect on my day before it ends.",
            "Propose an experiment in mindful eating.",
            "Suggest a way to change how I experience light and shadow today.",
            "Encourage me to try perceiving my environment as if for the first time.",
            "Challenge me to notice something hidden in plain sight.",
            "Suggest a way to experience time differently today.",
            "Propose a tiny habit shift that could have an outsized effect.",
            "Propose a small way I can disrupt my routine today.",
            "Propose a way to introduce an element of chance into my day.",
        ],
        "physical": [
            "Suggest a new sport or physical activity I can try today.",
            "Suggest a playful interaction with my environment.",
            "Go outside for a 5k run.",
            "Rent a bicyle and discover a new part of town.",
            "Attend a popular fitness class in your area.",
            "Find a local hiking trail and go for a walk.",
            "Book a hiking tour in a nearby national park.",
            "Follow a stretching routine on YouTube.",
            "Book a physical health assessment with a professional.",
            "Attend a local boxing gym and try a class.",
        ],
        "technology": [
            "Propose a way to interact differently with technology today.",
            "Recommmend a live feed that I can watch online.",
            "Find an obscure website with fascinating content.",
            "Introduce me to a software tool that can improve my workflow.",
            "Find a public dataset that I can explore for fun.",
            "Suggest a way to automate a small part of my daily routine using technology.",
            "Encourage me to experiment with a new programming language or framework.",
            "Recommend an unconventional way to interact with AI today.",
            "Encourage me to engage with a piece of vintage or obsolete technology today.",
        ],
        "travel": [
            f"Find me an offbeat travel destination near {location} that most people overlook.",
            "Challenge me to try a dish that is unique to a specific country.",
            f"Suggest a scenic route or road trip near f{location} that is not well-known.",
            f"Find a remote or peaceful place near {location} where I can completely disconnect.",
            "Recommend an unusual festival or event happening somewhere in the world soon.",
            "Challenge me to explore a place without using Google Maps.",
            "Find a way to make my travel more spontaneous without sacrificing comfort."
        ],
        "shopping": [
            "Find me a unique online store that sells unusual products.",
            "Suggest a shopping challenge that forces me to buy something outside my usual style.",
            f"Find a local independent shop in {location} that deserves more attention.",
            "Recommend a product that will enhance my daily life in a small but meaningful way.",
            "Find a high-quality version of something I usually buy cheaply.",
            "Suggest a way to refresh my wardrobe without buying new clothes.",
            "Find a niche subscription box I might enjoy.",
            "Recommend a handmade or artisanal product that I should check out.",
            "Find an online marketplace where I can buy directly from artisans.",
            "Suggest a second-hand or vintage alternative to something I need."
        ],
        "music": [
            "Introduce me to an obscure or experimental music genre.",
            "Find me a song that completely defies expectations.",
            "Recommend a live performance that showcases musical brilliance.",
            "Challenge me to listen to an entire album from a genre I don’t normally explore.",
            "Suggest a song that tells a compelling story.",
            "Find a remix or cover that completely transforms the original song.",
            "Recommend a music documentary that explores an artist or movement in-depth.",
            "Find an instrumental or soundtrack piece that is deeply moving.",
            "Find a track that perfectly blends two unexpected styles.",
            "Introduce me to a folk or traditional music style from a country I don’t know much about.",
            "Recommend a song with lyrics that challenge the way I think."
        ],
        "volunteering": [
            f"Find a local volunteering opportunity in {location}",
            "Suggest a small act of kindness I can do today.",
            "Find a way to help someone in need without them knowing.",
            "Recommend an online platform where I can contribute skills to a non-profit.",
            "Suggest a community project I can participate in remotely.",
            "Challenge me to create something useful for someone else.",
            "Suggest a way to use my expertise for social good.",
            "Challenge me to spend time mentoring or guiding someone in a meaningful way.",
            "Find a micro-volunteering task I can do in under 30 minutes.",
        ]
    }
    if not preferences:
        selected_prompts = sum(prompts.values(), [])
    else:
        selected_prompts = sum([prompts[category] for category in preferences], [])

    return random.choice(selected_prompts)


def generate_nudge(openai_api_key: str, location: str, preferences: list | None) -> str:
    """
    Uses GPT to generate a unique, practical nudge based on a randomized prompt.

    Args:
        openai_api_key: The OpenAI API key for authentication.
        location: The city or location to include in the prompt.
        preferences: A list of preferred categories for prompts.
    
    Returns:
        str: A unique nudge to help users break their routine in meaningful ways.
    """
    openai.api_key = openai_api_key
    random_prompt = get_random_prompt(location, preferences)
    prompt = f"""
        Provide one specific, ingenious activity, action, or recommendation based on the following request:
    
        {random_prompt}
        
        Make it unexpected, thought-provoking, and non-generic. Avoid vague or common suggestions.
        """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You provide unique and insightful nudges "
                        "to help users break their routine in meaningful ways."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=150,
            temperature=0.7
        )
        activity = response['choices'][0]['message']['content'].strip()
        print(f"Today's Nudge: {activity}")
        return activity

    except Exception as e:
        print(f"Error generating activity: {e}")
        return None
