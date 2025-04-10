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
        temp_dir = os.path.join( os.getenv( "TEMP" ), "LateinTrainer_update" )
        os.makedirs( temp_dir, exist_ok = True )
        
        # Create update batch script
        batch_script = f"""
@echo off
timeout /t 1 /nobreak >nul
xcopy /s /y "{temp_dir}\\*.*" "{os.path.dirname(__file__)}\\..\\..\\*.*"
start "" "{sys.executable}" "{os.path.abspath(sys.argv[0])}"
del "%~f0"
        """
        
        with open( os.path.join( temp_dir, "update.bat" ), "w" ) as f:
            f.write( batch_script )
        
        # Get file size
        response = requests.get( download_url, stream = True )
        total_size = int( response.headers.get( "content-length", 0 ) )
        downloaded_size = 0
        
        # Download the update
        update_zip = os.path.join( temp_dir, "update.zip" )
        
        gui.debug_print( "Starting download..." )
        with open( update_zip, "wb" ) as f:
            for chunk in response.iter_content( chunk_size = 8192 ):
                if chunk:
                    f.write( chunk )
                    downloaded_size += len( chunk )
                    progress = ( downloaded_size / total_size ) * 100
                    gui.debug_print( f"Download progress: {progress:.1f}%" )
                    gui.download_progress  = round( progress, 1)
        
        # Extract the update
        gui.debug_print( "Downloading complete. Starting installation..." )
        app_dir = os.path.dirname( os.path.dirname( os.path.dirname( __file__ ) ) )
        with zipfile.ZipFile( update_zip, "r" ) as zip_ref:
            zip_files = zip_ref.namelist()
            total_files = len( zip_files )
            for index, file in enumerate( zip_files, 1 ):
                zip_ref.extract( file, app_dir )
                progress = ( index / total_files ) * 100
                gui.debug_print( f"Installation progress: {progress:.1f}%" )
                gui.extraction_progress  = round( progress, 1)
        
        # Clean up
        os.remove( update_zip )
        
        # Instead of restarting directly, run the batch script and exit
        os.startfile( os.path.join( temp_dir, "update.bat" ) )
        gui.root.quit()  # Close the application
        sys.exit(0)  # Exit the Python process
        
    except Exception as e:
        gui.debug_print( f"Error installing update: {e}" )
        return False


def run_update_check( gui ):
    update_available, latest_version, download_url = check_for_updates( gui )
    
    if update_available:
        gui.debug_print( f"Update available! Version {latest_version}" )
        if download_and_install_update( download_url, gui ):
            gui.debug_print( "Update installed successfully!" )
        else:
            gui.debug_print( "Update installation failed." )
    else:
        gui.debug_print( f"You're running the latest version ({CURRENT_VERSION})" )