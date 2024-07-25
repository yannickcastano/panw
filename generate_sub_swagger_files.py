import yaml
import os

def extract_base_paths(file_path):
    with open(file_path, 'r') as file:
        swagger = yaml.safe_load(file)
    
    base_paths = set()
    
    paths = swagger.get('paths', {})
    for path in paths.keys():
        # Split the path and take the first two segments
        segments = path.split('/')
        if len(segments) > 2:  # Ensure there are at least two segments
            base_path = f"/{segments[1]}/{segments[2]}"
        else:
            base_path = f"/{segments[1]}"
        base_paths.add(base_path)
    
    return sorted(base_paths), swagger

def adjust_paths(base_path, sub_paths):
    adjusted_paths = {}
    for path, operations in sub_paths.items():
        new_path = path.replace(base_path, '', 1)
        if new_path == '':
            new_path = '/'
        adjusted_paths[new_path] = operations
    return adjusted_paths

def create_sub_swagger(base_path, swagger):
    sub_paths = {}
    for path, operations in swagger['paths'].items():
        if path.startswith(base_path):
            sub_paths[path] = operations

    adjusted_paths = adjust_paths(base_path, sub_paths)
    
    sub_swagger = {
        'swagger': swagger['swagger'],
        'info': swagger['info'],
        'paths': adjusted_paths,
        'definitions': swagger.get('definitions', {})
    }
    
    return sub_swagger

def save_to_file(base_path, sub_swagger):
    # Generate a safe filename from the base path
    filename = base_path.replace('/', '_').strip('_') + '.yaml'
    with open(filename, 'w') as file:
        yaml.dump(sub_swagger, file, default_flow_style=False)

if __name__ == "__main__":
    file_path = 'swagger.yaml'  # Path to your Swagger YAML file
    base_paths, swagger = extract_base_paths(file_path)
    
    for base_path in base_paths:
        sub_swagger = create_sub_swagger(base_path, swagger)
        save_to_file(base_path, sub_swagger)
        print(f"Generated file for base path {base_path} -> {base_path.replace('/', '_').strip('_')}.yaml")