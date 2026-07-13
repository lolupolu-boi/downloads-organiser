import os
import shutil
from pathlib import Path

def organize_downloads():
    # Automatically detects the user's default Downloads folder across Windows, Mac, and Linux
    downloads_dir = Path.home() / "Downloads"
    
    if not downloads_dir.exists():
        print(f"Error: Could not find the Downloads folder at {downloads_dir}")
        return

    # Vast extension dictionary mapping file types to logical categories
    EXTENSION_MAPPING = {
        # Documents
        '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents', 
        '.txt': 'Documents', '.rtf': 'Documents', '.odt': 'Documents',
        '.xls': 'Documents', '.xlsx': 'Documents', '.csv': 'Documents',
        '.ppt': 'Documents', '.pptx': 'Documents', '.epub': 'Documents',
        '.pages': 'Documents', '.numbers': 'Documents', '.key': 'Documents',
        '.mobi': 'Documents',
        
        # Images
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', 
        '.gif': 'Images', '.bmp': 'Images', '.svg': 'Images', 
        '.webp': 'Images', '.tiff': 'Images', '.ico': 'Images',
        '.heic': 'Images', '.raw': 'Images', '.cr2': 'Images', '.nef': 'Images',
        
        # Video
        '.mp4': 'Videos', '.mkv': 'Videos', '.avi': 'Videos', 
        '.mov': 'Videos', '.flv': 'Videos', '.wmv': 'Videos', 
        '.webm': 'Videos', '.mpeg': 'Videos', '.3gp': 'Videos', '.m4v': 'Videos',
        
        # Audio
        '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio', 
        '.m4a': 'Audio', '.aac': 'Audio', '.ogg': 'Audio', 
        '.wma': 'Audio', '.mid': 'Audio', '.midi': 'Audio',
        
        # Archives / Compressed
        '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives', 
        '.tar': 'Archives', '.gz': 'Archives', '.bz2': 'Archives', 
        '.xz': 'Archives', '.iso': 'Archives', '.dmg': 'Archives',
        
        # Executables & Installers
        '.exe': 'Applications', '.msi': 'Applications', '.pkg': 'Applications', 
        '.deb': 'Applications', '.rpm': 'Applications', '.apk': 'Applications', 
        '.app': 'Applications',
        
        # Code & Developer Files
        '.py': 'Developer', '.js': 'Developer', '.html': 'Developer', 
        '.css': 'Developer', '.json': 'Developer', '.xml': 'Developer', 
        '.cpp': 'Developer', '.c': 'Developer', '.h': 'Developer', 
        '.java': 'Developer', '.sh': 'Developer', '.bat': 'Developer', 
        '.ts': 'Developer', '.go': 'Developer', '.rs': 'Developer', 
        '.yaml': 'Developer', '.yml': 'Developer', '.sql': 'Developer',
        
        # Design & 3D
        '.psd': 'Design', '.ai': 'Design', '.xd': 'Design', 
        '.fig': 'Design', '.blend': 'Design', '.obj': 'Design', 
        '.stl': 'Design', '.dwg': 'Design'
    }

    print(f"Scanning and organizing: {downloads_dir}\n")
    moved_count = 0

    # Iterate through all items directly inside the Downloads directory
    for item in downloads_dir.iterdir():
        # CRITICAL: Skip directories so we don't accidentally nest previously created folders
        if item.is_dir():
            continue
            
        # Skip hidden system files (like .DS_Store on Mac or temporary files)
        if item.name.startswith('.'):
            continue

        # Extract extension in lowercase to match the dictionary keys
        file_ext = item.suffix.lower()
        
        # Handle files without extensions or fallback formatting
        if not file_ext:
            dest_folder_name = "Other_Files"
        else:
            # Look up the category. If it's a rare/unknown type, make a dedicated folder for it
            dest_folder_name = EXTENSION_MAPPING.get(file_ext, f"{file_ext[1:].upper()}_Files")

        # Set up destination path
        target_dir = downloads_dir / dest_folder_name
        
        # Create folder safely. If it already exists, Python smoothly moves on.
        target_dir.mkdir(exist_ok=True)

        destination = target_dir / item.name

        # Duplicate Protection: If a file with the same name exists, append a unique counter
        if destination.exists():
            base_name = item.stem
            counter = 1
            while destination.exists():
                new_name = f"{base_name} ({counter}){file_ext}"
                destination = target_dir / new_name
                counter += 1

        # Move the file
        try:
            shutil.move(str(item), str(destination))
            print(f"Moved: {item.name} ➔ {dest_folder_name}/")
            moved_count += 1
        except Exception as e:
            print(f"Could not move {item.name}. Reason: {e}")

    print(f"\nDone! Successfully organized {moved_count} new files.")

if __name__ == "__main__":
    organize_downloads()