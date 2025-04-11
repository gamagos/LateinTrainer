from __future__ import annotations

import requests
import os
import sys
import zipfile
import tkinter as tk
from packaging import version

GITHUB_REPO = "gamagos/LateinTrainer"

class AutoUpdate:
    def __init__( self, gui: "GUI", version: str ) -> None: # type: ignore
        self.gui = gui
        self.CURRENT_VERSION = version
        
    
    def check_for_updates( self ) -> tuple[bool, str, str]:
        try:
            # Get latest release info from GitHub
            response = requests.get(
                f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            )
            response.raise_for_status()
            release_data = response.json()
        
            latest_version = release_data["tag_name"].replace("v", "")
        
            # Compare versions
            if version.parse( latest_version ) > version.parse( self.CURRENT_VERSION ):
                return True, latest_version, release_data["assets"][0]["browser_download_url"]
        
            return False, self.CURRENT_VERSION, None
    
        except Exception as e:
            self.gui.debug_print( f"Error checking for updates: {e}" )
            return False, self.CURRENT_VERSION, None


    def download_and_install_update( self, download_url: str ) -> bool:
        try:
            temp_dir = os.path.join( os.getenv( "TEMP" ), "LateinTrainer_update" )
            extract_dir = os.path.join( temp_dir, "extracted" )
            os.makedirs( temp_dir, exist_ok = True )
            os.makedirs( extract_dir, exist_ok = True )
        
            # Create update batch script that will run after app closes
            batch_script = f"""
            @echo off
            timeout /t 1 /nobreak >nul
            xcopy /s /y "{extract_dir}\\*.*" "{os.path.dirname( __file__ )}\\..\\..\\*.*"
            start "" "{sys.executable}" "{os.path.abspath( sys.argv[0] )}"
            rmdir /s /q "{temp_dir}"
            del "%~f0"
            """
        
            with open( os.path.join( temp_dir, "update.bat" ), "w" ) as f:
                f.write( batch_script )
        
            # Download and extract update
            update_zip = os.path.join( temp_dir, "update.zip" )
            self.gui.debug_print( "Starting download..." )
        
            response = requests.get( download_url, stream = True )
            total_size = int( response.headers.get( "content-length", 0 ) )
            downloaded_size = 0
        
            self.gui.debug_print( "Starting download..." )
            with open( update_zip, "wb" ) as f:
                for chunk in response.iter_content( chunk_size = 8192 ):
                    if chunk:
                        f.write( chunk )
                        downloaded_size += len( chunk )
                        progress = ( downloaded_size / total_size ) * 100
                        self.gui.debug_print( f"Download progress: {progress:.1f}%" )
                        self.gui.download_progress = round( progress, 1 )
        
            # Extract to temporary directory
            self.gui.debug_print( "Downloading complete. Extracting..." )
            with zipfile.ZipFile( update_zip, "r" ) as zip_ref:
                zip_files = zip_ref.namelist()
                total_files = len( zip_files )
                for index, file in enumerate( zip_files, 1 ):
                    zip_ref.extract( file, extract_dir )
                    progress = ( index / total_files ) * 100
                    self.gui.debug_print( f"Extraction progress: {progress:.1f}%" )
                    self.gui.extraction_progress = round( progress, 1 )
        
            os.remove( update_zip )  # Remove the zip file
        
            # Start the update batch script and exit
            os.startfile( os.path.join( temp_dir, "update.bat" ) )
            self.gui.root.quit()
            sys.exit(0)
        
        except Exception as e:
            self.gui.debug_print( f"Error installing update: {e}" )
            return False


    def run_update_check( self ) -> None:
        update_available, latest_version, download_url = self.check_for_updates( self.gui )
    
        if update_available:
            self.gui.debug_print( f"Update available! Version {latest_version}" )
            if self.download_and_install_update( download_url, self.gui ):
                self.gui.debug_print( "Update installed successfully!" )
            else:
                self.gui.debug_print( "Update installation failed." )
        else:
            self.gui.debug_print( f"You're running the latest version ({self.CURRENT_VERSION})" )