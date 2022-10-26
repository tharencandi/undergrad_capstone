from download_tool.download_script import *
def validate_manifest(lines):
    if len(lines) < 1:
        return False, "Manifest is empty"
    
    i = 0
    if lines[i].strip() != "id	filename	md5	size	state":
        return False, "Invalid file format"
    
    while i < len(lines):
        ln = lines[i].strip()
        sln = lines.split(DELIM)
        if len(sln) != 5:
            return False, f"Line {i} is not valid.\n"
    
