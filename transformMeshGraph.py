import json
import MeshGraph
def serialize_instance(obj):
    if isinstance(obj, MeshGraph):
        serialized = {
            '__class__': 'MyClass',
            'name': obj.name,
            'other_instance': obj.other_instance.name if obj.other_instance else None
        }
        return serialized
    # Handle other classes or data types here
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def deserialize_instance(data):
    class_name = data['__class__']
    if class_name == 'MyClass':
        instance = MyClass(data['name'])
        # Restore reference to other_instance
        if data['other_instance']:
            instance.other_instance = MyClass(data['other_instance'])
        return instance
    # Handle other classes or data types here
    raise ValueError(f"Unknown class name: {class_name}")

# Example usage
instance1 = MyClass('Instance 1')
instance2 = MyClass('Instance 2')
instance1.other_instance = instance2

# Serialize instances
serialized_data = {
    'instance1': serialize_instance(instance1),
    'instance2': serialize_instance(instance2)
}

# Save to JSON file
with open('serialized_data.json', 'w') as json_file:
    json.dump(serialized_data, json_file)

# Read from JSON file
with open('serialized_data.json', 'r') as json_file:
    serialized_data = json.load(json_file)

# Deserialize instances
instance1 = deserialize_instance(serialized_data['instance1'])
instance2 = deserialize_instance(serialized_data['instance2'])

# Print the deserialized instances
print(instance1.name)  # Output: Instance 1
print(instance2.name)  # Output: Instance 2
print(instance1.other_instance.name)  # Output: Instance 2
