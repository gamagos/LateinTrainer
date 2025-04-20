@echo off
setlocal EnableDelayedExpansion

REM Clean build prompt
set /p clean="Clean old build (y/n)? "
if "%clean%"=="" set clean=n
if /i "!clean!"=="y" (
    if exist "dist" rmdir /s /q "dist"
    if exist "__pycache__" rmdir /s /q "__pycache__"
) else (
    echo Keeping old build files for faster compilation...
)

REM Get version from Python file
for /f "tokens=*" %%i in ('python dev/get_version.py') do set VERSION=%%i

REM Starting nuitka build
call python -m nuitka ^
--standalone ^
--windows-console-mode=disable ^
--windows-icon-from-ico=src/assets/icon.ico ^
--output-dir=dist ^
--output-filename="Latein Formen Trainer" ^
--include-data-dir=src/assets/settings_button/=assets/settings_button ^
--include-data-dir=src/assets/autoSelect_switch/=assets/autoSelect_switch ^
--include-data-dir=src/assets=assets ^
--include-data-dir=src/data=data ^
--include-data-dir=src/logs=logs ^
--enable-plugin=tk-inter ^
--plugin-enable=tk-inter ^
--include-package=tkinter ^
--include-package=_tkinter ^
--include-package=PIL ^
--include-package=email ^
--include-package=requests ^
--include-package=urllib3 ^
--include-module=tkinter.font ^
--include-module=tkinter.ttk ^
--include-module=tkinter.messagebox ^
--include-module=win32api ^
--include-module=win32con ^
--include-module=json ^
--include-module=numpy ^
--include-module=secrets ^
--nofollow-import-to=PyQt5 ^
--nofollow-import-to=PySide2 ^
--nofollow-import-to=django ^
--nofollow-import-to=asyncio ^
--nofollow-import-to=cryptography ^
--nofollow-import-to=sqlite3 ^
--nofollow-import-to=xml ^
--nofollow-import-to=ssl ^
--nofollow-import-to=numpy.testing ^
--nofollow-import-to=numpy.f2py ^
--nofollow-import-to=numpy.distutils ^
--nofollow-import-to=numpy.matlib ^
--nofollow-import-to=numpy.f2py ^
--nofollow-import-to=numpy.distutils ^
--nofollow-import-to=numpy.matlib ^
--nofollow-import-to=numpy.doc ^
--jobs=16 ^
--assume-yes-for-downloads ^
--remove-output ^
--msvc=latest ^
--lto=yes ^
--low-memory ^
--python-flag=no_site ^
--python-flag=no_warnings ^
--python-flag=no_docstrings ^
--static-libpython=no ^
--windows-force-stdout-spec=%TEMP%\nul ^
--windows-force-stderr-spec=%TEMP%\nul ^
--windows-company-name="Sebastian Fiault" ^
--windows-file-description="Sebastian Fiaults Formen Trainer" ^
--windows-product-name="Latein Formen Trainer" ^
--windows-product-version=!VERSION! ^
--windows-file-version=!VERSION! ^
--show-progress ^
src/main.py

REM check if compilation went right
if not exist "dist" (
    echo Compilation failed or dist directory wasn't created.
    pause
    exit /b 1
)

if not exist "dist\main.dist" (
    echo Compilation completed but main.dist directory wasn't created.
    pause
    exit /b 1
)

cd dist
mkdir _internal
robocopy main.dist _internal /E /MOVE

REM Check if the robocopy operation was successful
if %ERRORLEVEL% GTR 7 (
    echo Failed to move files from main.dist to _internal.
    exit /b 1
)
rmdir /s /q main.dist

REM Create shortcut for .exe
if exist "_internal\Latein Formen Trainer.exe" (
    echo Set oWS = CreateObject^("WScript.Shell"^) > CreateShortcut.vbs
    echo sLinkFile = oWS.ExpandEnvironmentStrings^("%~dp0"^) ^& "\Latein Formen Trainer.lnk" >> CreateShortcut.vbs
    echo Set oLink = oWS.CreateShortcut^(sLinkFile^) >> CreateShortcut.vbs
    echo oLink.TargetPath = oWS.ExpandEnvironmentStrings^("%~dp0"^) ^& "\_internal\Latein Formen Trainer.exe" >> CreateShortcut.vbs
    echo oLink.WorkingDirectory = oWS.ExpandEnvironmentStrings^("%~dp0"^) ^& "\_internal" >> CreateShortcut.vbs
    echo oLink.Save >> CreateShortcut.vbs
    cscript CreateShortcut.vbs
    if errorlevel 1 (
        echo Failed to create shortcut
        type CreateShortcut.vbs
        pause
        exit /b 1
    )
    del CreateShortcut.vbs
    echo Build completed successfully.
) else (
    echo Executable file not found in expected location.
    pause
    exit /b 1
)