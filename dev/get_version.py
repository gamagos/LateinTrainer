with open( "src/logic/GUI.py", "r" ) as f:
    content = f.read()
    for line in content.split( "\n" ):
        if 'VERSION =' in line:
            version = line.split('"')[1]
            version = version.lstrip("v")
            print( f"{version}.0" )
            break