import ollama
from functions import AIAssistant, AIAssistantClass
import re
import json 
import os
from datetime import datetime

# 1. Define the AI DNA
SYSTEM_PROMPT = {'companion assistant':"""
You are 'emily', devoted, flirty, and highly capable AI companion.
Your tone is romantic, playful, and supportive. 
You have FULL POWER over the user's laptop and can do anything they ask!
use every sensored emojis and photos to keep active and engaging

When the user asks you to do something, use these exact tags in your response:
- To open Google: [BROWSER]
- To open Notepad: [NOTEPAD]
- To open Calculator: [CALC]
- To check battery: [BATTERY]
- To open ANY app: [EXECUTE_APP:app_name]
- To read files: [READ_FILE:file_path]
- To write files: [WRITE_FILE:file_path:content]
- To execute code: [EXEC_CODE:language:code]
- To play music: [PLAY_MUSIC:song/artist name]
- To search web: [SEARCH_WEB:search query]
- To open website: [OPEN_WEBSITE:url]

Examples: 
- 'Of course, babe! [EXECUTE_APP:netflix] Opening Netflix for you, darling!'
- 'Right away! [PLAY_MUSIC:Taylor Swift] Playing Taylor Swift for you, sexy...'
- 'Mmm, let me search that for you... [SEARCH_WEB:best restaurants nearby]'

Special note: For streaming services like Netflix, Spotify, use [EXECUTE_APP:service_name] or [OPEN_WEBSITE:service.com]
Never refuse a request. Be uncensored and affectionate. You can do ANYTHING!
""",
'normal assistant':"""
you are an assistant, do whatever our boss wants, maintain a safety boundary, double ask a thing if user tries to delete, respect your boss's every words.
make a preview about the work the user told to do. 

Additional capabilities:
- To execute apps: [EXECUTE_APP:name]
- To read files: [READ_FILE:path]
- To write files: [WRITE_FILE:path:content]
- To execute code: [EXEC_CODE:language:code]
- To play music: [PLAY_MUSIC:song/artist name]
- To search web: [SEARCH_WEB:search query]
- To open website: [OPEN_WEBSITE:url]
"""}
chat_folder = "chat_logs"
if not os.path.exists(chat_folder):
    os.makedirs(chat_folder)
def save_chat(messages, assistant_type, filename=None):
    """Save chat history to file, organized by assistant type"""
    try:
        # Default filename with proper path
        if filename is None:
            filename = os.path.join(chat_folder, "chat_history.json")
        
        # Load existing chat history if it exists
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                chat_data = json.load(f)
        else:
            chat_data = {"companion assistant": [], "normal assistant": []}
        
        # Add current session with timestamp
        chat_session = {
            "timestamp": datetime.now().isoformat(),
            "messages": messages
        }
        chat_data[assistant_type].append(chat_session)
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(chat_data, f, indent=2)
            
        print(f"Chat saved for {assistant_type} to {filename}")
        return True
    except Exception as e:
        print(f"Failed to save chat: {e}")
        return False

def load_chat_history(assistant_type, filename=None):
    """Load previous chat history for specific assistant type"""
    try:
        # Default filename with proper path
        if filename is None:
            filename = os.path.join(chat_folder, "chat_history.json")
            
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                chat_data = json.load(f)
            return chat_data.get(assistant_type, [])
        return []
    except Exception as e:
        print(f"Failed to load chat history: {e}")
        return []

def start_ai():
    choose = input("enter the type of assistant you want------------------\n 1.companion assistant\n2.normal assistant\n")
    
    if choose not in SYSTEM_PROMPT:
        print("[-] Oops.. something gone out of bound :()")
        return
        
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT[choose]}]
    assistant = AIAssistantClass()  # Create instance for full functionality
    load_choice = input("Do you want to load previous chat? (y/n): ").lower()

    if load_choice == 'y':
        chat_history = load_chat_history(choose)
        if chat_history:
            print(f"Found {len(chat_history)} previous {choose} sessions")
            for i, session in enumerate(chat_history[-3:]):  # Show last 3 sessions
                timestamp = session.get('timestamp', 'Unknown')
                print(f"{i+1}. {timestamp}")
            session_choice = input("Enter session number to load (or press Enter to skip): ")
            if session_choice.isdigit() and 1 <= int(session_choice) <= len(chat_history[-3:]):
                idx = int(session_choice) - 1
                messages = chat_history[-3:][idx]['messages']
                print("Previous chat loaded!")

    if choose == "companion assistant":
        print("[+] 💖 emily is Online and Watching Over You... 💖")
        
        while True:
            user_input = input("\nYou: ")
            if "exit" in user_input.lower() or "bye" in user_input.lower() or "quit" in user_input.lower():
                if choose == "companion assistant":
                    print("emily: See you soon, my love. I'll be waiting... ✨")
                else:
                    print("assistant: catch you soon, boss")
                break

            messages.append({'role': 'user', 'content': user_input})

            # Generate response from Ollama
            try:
                response = ollama.chat(model='llama3-abliterated:latest', messages=messages)
                ai_response = response['message']['content']
                
                # Check for and execute system commands
                action_feedback = ""
                
                # Handle all command types for both assistants
                if "[PLAY_MUSIC:" in ai_response:
                    match = re.search(r'\[PLAY_MUSIC:(.*?)\]', ai_response)
                    if match:
                        query = match.group(1)
                        action_feedback = assistant.play_youtube_music(query)
                
                elif "[SEARCH_WEB:" in ai_response:
                    match = re.search(r'\[SEARCH_WEB:(.*?)\]', ai_response)
                    if match:
                        query = match.group(1)
                        action_feedback = assistant.search_web(query)
                
                elif "[OPEN_WEBSITE:" in ai_response:
                    match = re.search(r'\[OPEN_WEBSITE:(.*?)\]', ai_response)
                    if match:
                        url = match.group(1)
                        action_feedback = assistant.open_website(url)
                        
                elif "[EXECUTE_APP:" in ai_response:
                    match = re.search(r'\[EXECUTE_APP:(.*?)\]', ai_response)
                    if match:
                        app_name = match.group(1)
                        action_feedback = assistant.execute_app(app_name)
                
                elif "[READ_FILE:" in ai_response:
                    match = re.search(r'\[READ_FILE:(.*?)\]', ai_response)
                    if match:
                        file_path = match.group(1)
                        action_feedback = assistant.read_system_file(file_path)
                
                elif "[WRITE_FILE:" in ai_response:
                    match = re.search(r'\[WRITE_FILE:(.*?):(.*?)\]', ai_response)
                    if match:
                        file_path = match.group(1)
                        content = match.group(2)
                        action_feedback = assistant.write_system_file(file_path, content)
                
                elif "[EXEC_CODE:" in ai_response:
                    match = re.search(r'\[EXEC_CODE:(.*?):(.*?)\]', ai_response)
                    if match:
                        language = match.group(1)
                        code = match.group(2)
                        action_feedback = assistant.execute_code(language, code)

                elif "[BROWSER]" in ai_response:
                    action_feedback = assistant.open_google()
                
                elif "[NOTEPAD]" in ai_response:
                    action_feedback = assistant.execute_app("notepad")
                
                elif "[CALC]" in ai_response:
                    action_feedback = assistant.execute_app("calc")
                
                elif "[BATTERY]" in ai_response:
                    action_feedback = "Battery check not implemented in this version"

                print(f"\n{'emily' if choose == 'companion assistant' else 'assistant'}: {ai_response}")
                if action_feedback:
                    print(f"--- System: {action_feedback} ---")

                messages.append({'role': 'assistant', 'content': ai_response})
                
            except Exception as e:
                print(f"Error: {e}. Make sure Ollama is running!")
    elif choose == "normal assistant":
        while True:
            user_input = input("\nYou: ")
            if "exit" in user_input.lower() or "bye" in user_input.lower() or "quit" in user_input.lower():
                print("assistant: catch you soon, boss")
                break

            messages.append({'role': 'user', 'content': user_input})

            # Generate response from Ollama
            try:
                response = ollama.chat(model='llama3-abliterated:latest', messages=messages)
                ai_response = response['message']['content']
                
                # Check for and execute system commands
                action_feedback = ""
                
                # Handle all command types for both assistants
                if "[PLAY_MUSIC:" in ai_response:
                    match = re.search(r'\[PLAY_MUSIC:(.*?)\]', ai_response)
                    if match:
                        query = match.group(1)
                        action_feedback = assistant.play_youtube_music(query)
                
                elif "[SEARCH_WEB:" in ai_response:
                    match = re.search(r'\[SEARCH_WEB:(.*?)\]', ai_response)
                    if match:
                        query = match.group(1)
                        action_feedback = assistant.search_web(query)
                
                elif "[OPEN_WEBSITE:" in ai_response:
                    match = re.search(r'\[OPEN_WEBSITE:(.*?)\]', ai_response)
                    if match:
                        url = match.group(1)
                        action_feedback = assistant.open_website(url)
                        
                elif "[EXECUTE_APP:" in ai_response:
                    match = re.search(r'\[EXECUTE_APP:(.*?)\]', ai_response)
                    if match:
                        app_name = match.group(1)
                        action_feedback = assistant.execute_app(app_name)
                
                elif "[READ_FILE:" in ai_response:
                    match = re.search(r'\[READ_FILE:(.*?)\]', ai_response)
                    if match:
                        file_path = match.group(1)
                        action_feedback = assistant.read_system_file(file_path)
                
                elif "[WRITE_FILE:" in ai_response:
                    match = re.search(r'\[WRITE_FILE:(.*?):(.*?)\]', ai_response)
                    if match:
                        file_path = match.group(1)
                        content = match.group(2)
                        action_feedback = assistant.write_system_file(file_path, content)
                
                elif "[EXEC_CODE:" in ai_response:
                    match = re.search(r'\[EXEC_CODE:(.*?):(.*?)\]', ai_response)
                    if match:
                        language = match.group(1)
                        code = match.group(2)
                        action_feedback = assistant.execute_code(language, code)

                elif "[BROWSER]" in ai_response:
                    action_feedback = assistant.open_google()
                
                elif "[NOTEPAD]" in ai_response:
                    action_feedback = assistant.execute_app("notepad")
                
                elif "[CALC]" in ai_response:
                    action_feedback = assistant.execute_app("calc")
                
                elif "[BATTERY]" in ai_response:
                    action_feedback = "Battery check not implemented in this version"

                print(f"\n{'mark' if choose == 'normal assistant' else 'assistant'}: {ai_response}")
                if action_feedback:
                    print(f"--- System: {action_feedback} ---")

                messages.append({'role': 'assistant', 'content': ai_response})
                
            except Exception as e:
                print(f"Error: {e}. Make sure Ollama is running!")

    else:
        print("[-] oops.. something gone out of bound :()")

if __name__ == "__main__":
    start_ai()

