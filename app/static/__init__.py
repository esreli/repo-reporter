import os
import yaml

def collection():
    collection_yaml_path = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'collection.yaml')
    with open(collection_yaml_path, 'r') as stream:
        try: return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
