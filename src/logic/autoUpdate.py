import requests
import os
import sys
import zipfile
import tkinter as tk
from packaging import version

from logic.GUI import VERSION, GUI

GITHUB_REPO = "gamagos/LateinTrainer"
CURRENT_VERSION = VERSION

def check_for_updates( gui ):
    try:
        # Get latest release info from GitHub
        response = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        )
        response.raise_for_status()
        release_data = response.json()
        
        latest_version = release_data["tag_name"].replace("v", "")
        
        # Compare versions
        if version.parse( latest_version ) > version.parse( CURRENT_VERSION ):
            return True, latest_version, release_data["assets"][0]["browser_download_url"]
        
        return False, CURRENT_VERSION, None
    
    except Exception as e:
        gui.debug_print( f"Error checking for updates: {e}" )
        return False, CURRENT_VERSION, None

def download_and_install_update( download_url, gui ):
    try:
        # Create temp directory for download
        temp_dir = os.path.join( os.getenv("TEMP"), "LateinTrainer_update" )
        os.makedirs( temp_dir, exist_ok = True )
        
        # Download the update
        response = requests.get( download_url, stream = True )
        update_zip = os.path.join( temp_dir, "update.zip" )
        
        with open( update_zip, "wb" ) as f:
            for chunk in response.iter_content( chunk_size = 8192 ):
                f.write( chunk )
        
        # Extract the update
        app_dir = os.path.dirname( os.path.dirname( os.path.dirname( __file__ ) ) )
        with zipfile.ZipFile( update_zip, "r" ) as zip_ref:
            zip_ref.extractall( app_dir )
        
        # Clean up
        os.remove( update_zip )
        return True
    
    except Exception as e:
        gui.debug_print( f"Error installing update: {e}" )
        return False

def run_update_check( gui ):
    update_available, latest_version, download_url = check_for_updates( gui )
    
    if update_available:
        gui.debug_print( f"Update available! Version {latest_version}" )
        if download_and_install_update( download_url, gui ):
            gui.debug_print( "Update installed successfully!" )
            # Restart the application
            os.execv( sys.executable, ["python"] + sys.argv )
        else:
            gui.debug_print( "Update installation failed." )
    else:
        gui.debug_print( f"You're running the latest version ({CURRENT_VERSION})" )

if __name__ == "__main__":
    # For testing purposes only
    from GUI import GUI
    root = tk.Tk()
    gui = GUI( root )
    run_update_check( gui )