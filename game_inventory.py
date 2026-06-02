"""
You're not wrong that the keys need defining — but the domain model classes ARE where you define them.
The class attributes become the JSON keys.
The JSON keys flow directly from the attribute names — you define them once in the model, 
and storage.py just calls to_dict() / from_dict(). Nothing is hardcoded in two places.

So your instinct was right that the keys need to be decided early, 
but the domain model is still the right place to do it — not a separate schema file or the JSON itself. 
The JSON files are just the output of whatever shape the model produces.
"""