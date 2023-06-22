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
    subdir = os.path.join(parent_dir, f'{i+1:02d}')
    os.makedirs(subdir, exist_ok=True)

    #  1. Copy files based on system type

    #  1.1 MARTINI2-Bilayers
    if config['system_type'] == 'MARTINI2-Bilayers':
        # Copy files from type1 folder to sub directory
        shutil.copytree('systemTypes/MARTINI2_Bilayers', subdir, dirs_exist_ok=True)
    # For future expansions to other system types
    elif config['system_type'] == 'type2':
        # Copy files from type2 folder to sub directory
        shutil.copytree('systemTypes/type2', subdir, dirs_exist_ok=True)
    else:
        # Handle unsupported system type
        print(f"Unsupported system type: {config['system_type']}")

    #  2. Copy files based on enhanced sampling method

    #  2.1 Weighted Ensemble
    if config['enhanced_sampling']['method'] == 'WE':
        # Copy WESTPA1 specific files sub directory
        if config['enhanced_sampling']['implementation'] == 'WESTPA1':
            shutil.copytree('enhancedSampling/WE/WESTPA1', subdir, dirs_exist_ok=True)
        # Copy WESTPA2 specific files sub directory
        elif config['enhanced_sampling']['implementation'] == 'WESTPA2':
            shutil.copytree('enhancedSampling/WE/WESTPA2', subdir, dirs_exist_ok=True)

        # Copy type2 specific files sub directory : Future expansion
        elif config['enhanced_sampling']['implementation'] == 'type2':
            shutil.copytree('enhancedSampling/WE/type2', subdir, dirs_exist_ok=True)

        else:
            # Handle unsupported enahnced sampling implementation
            print(f"Unsupported system type: {config['enhanced_sampling']['implementation']}")

    # For future expansions to other enhanced sampling methods
    elif config['enhanced_sampling']['method'] == 'type2':
        # Copy type2 specific files sub directory : Future expansion
        if config['enhanced_sampling']['implementation'] == 'ABC':
            shutil.copytree('enhancedSampling/type2/ABC', subdir, dirs_exist_ok=True)
    else:
        # Handle unsupported enhanced sampling method
        print(f"Unsupported enhanced sampling method: {config['enhanced_sampling']['method']}")

    #  3. Copy common template files to sub directory
    shutil.copytree('common/stdMD', subdir, dirs_exist_ok=True)
    #  shutil.copytree('common/', subdir, dirs_exist_ok=True)

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
