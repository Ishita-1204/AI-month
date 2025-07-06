#!/usr/bin/env python3
"""
Test script to add sample tasks for today
"""

import requests
import json
from datetime import datetime

# API base URL
API_BASE = 'http://localhost:5000'

def create_test_task(title, body, token):
    """Create a test task"""
    try:
        response = requests.post(f'{API_BASE}/api/announce', 
                               json={
                                   'title': title,
                                   'body': body,
                                   'token': token
                               })
        
        if response.status_code == 200:
            print(f"✅ Created task: {title}")
            return response.json()
        else:
            print(f"❌ Failed to create task: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating task: {e}")
        return None

def main():
    print("🚀 Adding test tasks for today...")
    
    # First, sign in to get a token
    try:
        # Try to sign in with existing user
        signin_response = requests.post(f'{API_BASE}/api/signin', 
                                      json={
                                          'username': 'alice',
                                          'password': 'password1'
                                      })
        
        if signin_response.status_code == 200:
            token = signin_response.json()['token']
            print("✅ Signed in successfully")
        else:
            # Create a new user if signin fails
            signup_response = requests.post(f'{API_BASE}/api/signup', 
                                          json={
                                              'username': 'alice',
                                              'password': 'password1'
                                          })
            if signup_response.status_code == 200:
                token = signup_response.json()['token']
                print("✅ Created new user and signed in")
            else:
                print("❌ Failed to authenticate")
                return
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    # Sample tasks for today
    test_tasks = [
        {
            'title': '🧠 Complete Machine Learning Tutorial',
            'body': 'Start with the basics of machine learning. Learn about supervised learning, unsupervised learning, and neural networks. Complete the interactive tutorial in the resources section.'
        },
        {
            'title': '🤖 Build Your First AI Chatbot',
            'body': 'Create a simple AI chatbot using Python. Follow the step-by-step guide to build a chatbot that can answer basic questions. Use natural language processing techniques.'
        },
        {
            'title': '📊 Analyze a Dataset with Python',
            'body': 'Practice data analysis with Python. Use pandas, numpy, and matplotlib to analyze a real-world dataset. Create visualizations and draw insights from the data.'
        },
        {
            'title': '🎯 Daily Challenge: Image Classification',
            'body': 'Build an image classification model using TensorFlow or PyTorch. Train it on a small dataset and test its accuracy. Share your results with the community!'
        },
        {
            'title': '📚 Read AI Research Paper',
            'body': 'Read and summarize one AI research paper from the recommended list. Focus on understanding the methodology and key findings. Prepare a brief presentation.'
        }
    ]
    
    # Create tasks
    for i, task in enumerate(test_tasks, 1):
        print(f"\n📋 Creating task {i}/{len(test_tasks)}...")
        create_test_task(task['title'], task['body'], token)
    
    print(f"\n✅ Added {len(test_tasks)} test tasks for today!")
    print("🎉 You can now test the 'Today\'s Tasks' feature in the extension!")

if __name__ == '__main__':
    main() 