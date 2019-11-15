import os
import yaml

def repos():
    repos_yaml_path = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'repos.yaml')
    with open(repos_yaml_path, 'r') as stream:
        try: return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
