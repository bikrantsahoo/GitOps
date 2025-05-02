import sys
import yaml

def update_helm_values(file_path, repository, tag):
    # Read the Helm values file
    with open(file_path, 'r') as file:
        values = yaml.safe_load(file)
    
    # Update the image repository and tag
    values['image']['repository'] = repository
    values['image']['tag'] = tag
    
    # Write back to the file
    with open(file_path, 'w') as file:
        yaml.safe_dump(values, file, default_flow_style=False)
    
    print(f"Updated {file_path} with repository: {repository}, tag: {tag}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python update_helm_values.py <values_file> <repository> <tag>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    repository = sys.argv[2]
    tag = sys.argv[3]
    update_helm_values(file_path, repository, tag)