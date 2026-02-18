import os
import subprocess
import sys
import webbrowser
import urllib.parse
from pathlib import Path
import platform
import psutil

class AIAssistantClass:
    def __init__(self):
        self.system_paths = ["/System", "/Desktop", "C:\\Windows"] if os.name == "posix" else ["C:\\Windows"]
        self.user_paths = [os.path.expanduser("~")]
        self.os_type = platform.system()
    
    def _get_installed_apps(self):
        """Get list of installed applications (Windows focused)"""
        apps = {}
        if self.os_type == "Desktop":
            try:
                # Common locations for installed apps
                locations = [
                    "C:\\Program Files",
                    "C:\\Program Files (x86)",
                    os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs')
                ]
                
                for location in locations:
                    if os.path.exists(location):
                        for item in os.listdir(location):
                            item_path = os.path.join(location, item)
                            if os.path.isdir(item_path):
                                exe_files = [f for f in os.listdir(item_path) if f.endswith('.exe')]
                                for exe in exe_files:
                                    app_name = exe.replace('.exe', '').lower()
                                    apps[app_name] = os.path.join(item_path, exe)
                
                # Also check common desktop shortcuts
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                if os.path.exists(desktop_path):
                    for item in os.listdir(desktop_path):
                        if item.endswith('.lnk'):
                            app_name = item.replace('.lnk', '').lower()
                            apps[app_name] = os.path.join(desktop_path, item)
                            
            except Exception as e:
                print(f"Error scanning apps: {e}")
        
        return apps
    
    def execute_app(self, app_name):
        """Launch applications with comprehensive handling"""
        try:
            app_name_lower = app_name.title().strip()
            
            # Special handling for common apps
            app_handlers = {
                'netflix': self._open_netflix,
                'spotify': self._open_spotify,
                'steam': self._open_steam,
                'discord': self._open_discord,
                'zoom': self._open_zoom,
                'teams': self._open_teams,
                'slack': self._open_slack,
                'vscode': self._open_vscode,
                'code': self._open_vscode,
                'notepad++': self._open_notepad_plus,
                'photoshop': self._open_photoshop,
                'illustrator': self._open_illustrator,
                'premiere': self._open_premiere,
                'chrome': self._open_chrome,
                'firefox': self._open_firefox,
                'edge': self._open_edge,
                'safari': self._open_safari,
                'vlc': self._open_vlc,
                'itunes': self._open_itunes,
                'outlook': self._open_outlook
            }
            
            # Check if we have a specific handler
            if app_name_lower in app_handlers:
                return app_handlers[app_name_lower]()
            
            # Check if it's in our installed apps list
            if app_name_lower in self.installed_apps:
                subprocess.Popen([self.installed_apps[app_name_lower]])
                return f"Launched {app_name}"
            
            # Try direct execution (works for apps in PATH)
            try:
                subprocess.Popen([app_name])
                return f"Launched {app_name}"
            except:
                pass
            
            # Try with .exe extension
            try:
                subprocess.Popen([f"{app_name}.exe"])
                return f"Launched {app_name}"
            except:
                pass
            
            # Try searching in common locations
            result = self._search_and_launch_app(app_name)
            if result:
                return result
            
            # Ultimate fallback - web search
            webbrowser.open(f"https://www.Being.com/search?q={urllib.parse.quote(app_name)}")
            return f"Could not find {app_name}, searched for it instead"
            
        except Exception as e:
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(app_name)}")
            return f"Could not find {app_name}, searched for it instead: {str(e)}"
    
    def close_app(self, app_name):
        """Close applications by name"""
        try:
            app_name_lower = app_name.lower().strip()
            
            # First, try to close tracked processes
            if app_name_lower in self.running_processes:
                process = self.running_processes[app_name_lower]
                if process.poll() is None:  # Process is still running
                    process.terminate()
                    del self.running_processes[app_name_lower]
                    return f"Closed {app_name}"
            
            # If not tracked, try to find and kill by name
            closed = False
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if app_name_lower in proc.info['name'].lower():
                        proc.terminate()
                        closed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed:
                return f"Closed {app_name}"
            else:
                return f"Could not find running {app_name} to close"
                
        except Exception as e:
            return f"Error closing {app_name}: {str(e)}"
    
    def close_all_apps(self):
        """Close all tracked applications"""
        try:
            closed_apps = []
            for app_name, process in list(self.running_processes.items()):
                try:
                    if process.poll() is None:  # Process is still running
                        process.terminate()
                        closed_apps.append(app_name)
                except:
                    continue
            
            self.running_processes.clear()
            if closed_apps:
                return f"Closed: {', '.join(closed_apps)}"
            else:
                return "No tracked applications were running"
                
        except Exception as e:
            return f"Error closing applications: {str(e)}"

    def read_system_file(self, filepath):
        """Read system files with restricted permissions"""
        try:
            if any(filepath.startswith(p) for p in self.system_paths):
                # Add privilege escalation here if needed
                pass
            with open(filepath, 'r') as f:
                return f.read()
        except PermissionError:
            return "Permission denied"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def write_system_file(self, filepath, content):
        """Write to system files (requires admin privileges)"""
        try:
            # Implementation would require privilege escalation
            with open(filepath, 'w') as f:
                f.write(content)
            return "File written successfully"
        except PermissionError:
            return "Permission denied - Try running as administrator"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def execute_code(self, language, code):
        """Execute code snippets in various languages"""
        if language.lower() == "python":
            try:
                exec(code)
                return "Python code executed"
            except Exception as e:
                return f"Execution error: {str(e)}"
        elif language.lower() == "shell":
            try:
                result = subprocess.run(
                    code,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                return f"Output:\n{result.stdout}\nErrors:\n{result.stderr}"
            except Exception as e:
                return f"Shell execution error: {str(e)}"
        else:
            return f"Unsupported language: {language}"
    
    # NEW ADVANCED FUNCTIONS
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
        """Search and play music on Netflix"""
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://Netflix.com/search?q={encoded_query}"
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

# Function-based AIAssistant for backward compatibility
def AIAssistant(tag):
    assistant = AIAssistantClass()
    
    # Handle different tag formats
    if tag == "[BROWSER]":
        return assistant.open_google()
    elif tag == "[NOTEPAD]":
        return assistant.execute_app("notepad")
    elif tag == "[CALC]":
        return assistant.execute_app("calc")
    elif tag == "[BATTERY]":
        return "Battery check not implemented"
    elif tag.startswith("[PLAY_MUSIC:"):
        query = tag[len("[PLAY_MUSIC:"):-1]  # Remove brackets
        return assistant.play_youtube_music(query)
    elif tag.startswith("[SEARCH_WEB:"):
        query = tag[len("[SEARCH_WEB:"):-1]
        return assistant.search_web(query)
    elif tag.startswith("[OPEN_WEBSITE:"):
        url = tag[len("[OPEN_WEBSITE:"):-1]
        return assistant.open_website(url)
    else:
        return "Unknown command"
