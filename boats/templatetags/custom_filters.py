from django import template

register = template.Library()

@register.filter
def combine_keys(model_id, port_id):
    """Combine model ID and port ID into a single key."""
    return f"{model_id}_{port_id}"

@register.filter
def get_dict_value(dictionary, key):
    """Safely get a value from a dictionary."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)
    return 0