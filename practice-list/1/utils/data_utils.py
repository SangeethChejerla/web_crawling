import csv
from typing import Any, Dict, List, Set

from models.venue import Venue


def is_duplicate_venue(venue_name: str, seen_names: Set[str]) -> bool:
    """
    Check if a venue name has already been seen.

    Args:
        venue_name: The name of the venue to check
        seen_names: Set of previously processed venue names

    Returns:
        True if the venue name is a duplicate, False otherwise
    """
    return venue_name in seen_names


def is_complete_venue(venue: Dict[str, Any], required_keys: List[str]) -> bool:
    """
    Check if a venue dictionary contains all required keys.

    Args:
        venue: The venue dictionary to check
        required_keys: List of required keys that must be present

    Returns:
        True if the venue contains all required keys, False otherwise
    """
    if not isinstance(venue, dict):
        return False

    return all(key in venue and venue[key] is not None for key in required_keys)


def save_venues_to_csv(venues: List[Dict[str, Any]], filename: str) -> None:
    """
    Save a list of venue dictionaries to a CSV file.

    Args:
        venues: List of venue dictionaries
        filename: Path to the output CSV file
    """
    if not venues:
        print("No venues to save.")
        return

    try:
        # Get field names from Venue model, handling both Pydantic v1 and v2
        try:
            # Pydantic v2 approach
            fieldnames = list(Venue.model_fields.keys())
        except AttributeError:
            # Fallback for Pydantic v1
            fieldnames = list(Venue.__annotations__.keys())

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()

            # Write each venue, handling missing fields
            for venue in venues:
                # Create a sanitized version of the venue with None for missing fields
                sanitized_venue = {field: venue.get(field) for field in fieldnames}
                writer.writerow(sanitized_venue)

        print(f"Successfully saved {len(venues)} venues to '{filename}'.")
    except Exception as e:
        print(f"Error saving venues to '{filename}': {e}")
