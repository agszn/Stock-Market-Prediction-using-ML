import os

# Get the current working directory (where the script is saved)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the assets folder within the current directory
assets_folder = os.path.join(current_directory, 'images')  # Assuming images is the correct folder name
readme_file = os.path.join(current_directory, 'README.md')

# Create or overwrite the README file
with open(readme_file, 'w') as readme:
    # Write a title for the README
    readme.write("# Asset Descriptions\n\n")
    readme.write("This file contains descriptions of the images in the `assets` folder.\n\n")
    
    # Check if the assets folder exists
    if os.path.exists(assets_folder) and os.path.isdir(assets_folder):
        # Loop through all the files in the assets folder
        for filename in os.listdir(assets_folder):
            # Only consider image files (you can add more extensions if needed)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):
                # Remove the file extension to get the description from the filename
                description = os.path.splitext(filename)[0].replace('_', ' ').title()
                
                # Write the description in the README file
                readme.write(f"### {description}\n")
                readme.write(f"![{description}]({os.path.join('images', filename)})\n\n")  # Fixed the path here
        
        print(f"README.md file generated successfully with descriptions from the {assets_folder} folder!")
    else:
        print(f"Error: The assets folder '{assets_folder}' does not exist.")
