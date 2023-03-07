import os
import shutil
import yaml

# Load YAML file
with open('config.yaml') as f:
    config = yaml.safe_load(f)

# Create parent directory
parent_dir = config['project_name']
os.makedirs(parent_dir, exist_ok=True)

# Create sub directories based on number of replicas
for i in range(config['num_replicas']):
    subdir = os.path.join(parent_dir, f'replica_{i}')
    os.makedirs(subdir, exist_ok=True)

    # Copy files based on system type
    if config['system_type'] == 'MARTINI2-Bilayers':
        # Copy files from type1 folder to sub directory
        shutil.copy('MARTINI2_Bilayer/*', subdir)

    # For future expansions to other system type
    elif config['system_type'] == 'type2':
        # Copy files from type2 folder to sub directory
        shutil.copy('type2/abc.abc', subdir)
    else:
        # Handle unsupported system type
        print(f"Unsupported system type: {config['system_type']}")

    # Copy common template files to sub directory
    shutil.copy('common/test1.txt', subdir)
    shutil.copy('common/test2.txt', subdir)

    # # Include template python script based on CV input
    # if config['cv']['name'] == 'distance':
    #     # Include distance.py script in sub directory
    #     shutil.copy('templates/distance.py', subdir)
    #     # Add optional argument to script
    #     with open(os.path.join(subdir, 'distance.py'), 'a') as f:
    #         f.write(f"optional_arg = {config['cv']['optional_arg']}\n")
    # else:
    #     # Handle unsupported CV type
    #     print(f"Unsupported CV type: {config['cv']['name']}")
