from AppOpener import open
import os
from pathlib import Path
import psutil
import urllib.parse
import webbrowser

path = "C:/Users/swaya/Desktop/"
desktop_app = Path.home()/ "Desktop"
all_apps = os.listdir(path)
apps = [app for app in desktop_app.iterdir() if app.is_file()]

class AIAssistantClass:
    def app_opener(self,app_name):
            try:
                full_path = os.path.join(path, app_name)
                if os.path.exists(full_path):
                    print("Success! File found.")
                    os.startfile(full_path)
                    print()
                else:
                    print("not such directory")
                    files = os.listdir*(path)
                    for f in files:
                        if app_name.lower() in f.lower():
                            print(f"did you mean: {f}?")
            except Exception as e:
                print(f"oops..somethings gone wrong: {e}")
    def execute_app(self,app_name):
        try:
            app_name_lower = app_name.lower().strip()

            if app_name_lower in apps:
                return open(app_name_lower)
            else:
                print("[+] no such app")

                return None
        except Exception as e:
            print(f"error occured: {e}")

    def close_apps(self,app_name):
        for app in psutil.process_iter(['name']):
            try:
                if app_name.lower() in app.info['name'].lower():
                    app.terminate()
                    print(f"{app_name} is successfully deleted")
                else:
                    print("no such file is opened")
            except Exception as e:
                print(f"something gone wrong: {e}")
                return None
    def open_google(self):
        """Open Google in default browser"""
        try:
            webbrowser.open("https://www.google.com")
            return "Google opened successfully"
        except Exception as e:
            return f"Error opening Google: {str(e)}"
    
    def play_youtube_music(self, query):
        """Search and play music on YouTube Music"""
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://music.youtube.com/search?q={encoded_query}"
            webbrowser.open(url)
            return f"Playing '{query}' on YouTube Music"
        except Exception as e:
            return f"Error playing music: {str(e)}"
        
    def open_netflix(self, query):
        """Search and play movie on Netflix"""
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"C://Program Files (x86)//Microsoft//Edge//Application{encoded_query}"
            webbrowser.open(url)
            return f"Playing '{query}' on Netflix"
        except Exception as e:
            return f"Error playing music: {str(e)}"
    def open_website(self, url):
        """Open any website"""
        try:
            if not url.startswith("http"):
                url = "https://" + url
            webbrowser.open(url)
            return f"Opened {url}"
        except Exception as e:
            return f"Error opening website: {str(e)}"
    
    def search_web(self, query, engine="Bing"):
        """Search the web using specified search engine"""
        try:
            encoded_query = urllib.parse.quote(query)
            if engine == "google":
                url = f"https://www.google.com/search?q={encoded_query}"
            elif engine == "Bing":
                url = f"https://www.Bing.com/?q={encoded_query}"
            else:
                url = f"https://www.{engine}.com/search?q={encoded_query}"
            
            webbrowser.open(url)
            return f"Searched '{query}' on {engine}"
        except Exception as e:
            return f"Error searching: {str(e)}"