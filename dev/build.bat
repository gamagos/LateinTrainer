REM Clean previous build
if exist "dist" rmdir /s /q "dist"

REM Compile python source code to C and C++
python -m nuitka ^
--standalone ^
--windows-console-mode=disable ^
--windows-icon-from-ico=src/assets/icon.ico ^
--output-dir=dist ^
--output-filename="Latein Formen Trainer" ^
--include-data-dir=src/logic=src/logic ^
--include-data-dir=src/data=src/data ^
--include-data-dir=src/assets=src/assets ^
--enable-plugin=tk-inter ^
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
--nofollow-import-to=email ^
--nofollow-import-to=pytest ^
--nofollow-import-to=asyncio ^
--nofollow-import-to=cryptography ^
--nofollow-import-to=sqlite3 ^
--nofollow-import-to=xml ^
--nofollow-import-to=ssl ^
--nofollow-import-to=numpy.testing ^
--nofollow-import-to=numpy.f2py ^
--nofollow-import-to=numpy.distutils ^
--nofollow-import-to=numpy.matlib ^
--remove-output ^
--assume-yes-for-downloads ^
--msvc=latest ^
--jobs=4 ^
src/main.py

REM Move everything to _internal except .exe for easier accessablility by users
cd dist/main.dist
mkdir _internal
move *.* _internal/
move "Latein Formen Trainer.exe"
cd ..
rmdir /s /q main.dist