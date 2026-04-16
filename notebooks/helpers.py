import json
import numpy as np


def load_jsonl(file_path: str) -> list[list[dict]]:
    """
    Load and parse a file where each line is a JSON-encoded string representing
    a participant's response data across trials.

    Args:
        file_path: Path to the file containing the data.

    Returns:
        participants_data: Inner lists contain recorded entries for a participant and trial.
    """
    participants_data = []
    with open(file_path, "r") as file:
        for line in file:
            try:
                participant_data = json.loads(line.strip())
                participants_data.append(participant_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")
    return participants_data


def retrieve_conditions(participants_data: list[list[dict]]) -> list[str]:
    """
    Retrieve the condition ("Casual" or "Competitive") assigned to each participant in the data.

    Args:
        participants_data: List of lists of dictionaries, where each inner list contains recorded entries for a participant and trial.

    Returns:
        conditions: Contains the condition of each participant.
    """
    conditions = []
    for participant_data in participants_data:
        condition = next(
            (
                ["Casual", "Competitive"][entry["condition"]]
                for entry in participant_data
                if entry.get("condition") is not None
            )
        )
        conditions.append(condition)
    return conditions


def retrieve_task_ordering(participants_data: list[list[dict]]) -> list[str]:
    """
    Retrieve ordering of choice and ranking tasks for each participant.
    0 = choice task first, 1 = ranking task first.
    """

    # first find trial index of first choice task
    orderings = []
    for participant_data in participants_data:
        sortable_rank_index = 0
        for sortable_rank_index, entry in enumerate(participant_data):
            if entry.get("trial_type") == "sortable-rank":
                break
        choice_index = 0
        for choice_index, entry in enumerate(participant_data):
            if entry.get("left_image") is not None:
                break
        orderings.append(0 if choice_index < sortable_rank_index else 1)
    return orderings


def retrieve_subj_demographics(participants_data: list[list[dict]]) -> list[tuple]:
    """
    Returns the self-reported demographics of each participant.

    Args:
        participants_data: List of lists of dictionaries, where each inner list contains recorded entries for a participant and trial.
    """

    full_demographics = []
    for participant_data in participants_data:
        demographics = [
            (
                entry["response"]["race"],
                entry["response"]["gender"],
                int(entry["response"]["age"]),
                entry["response"]["college"],
            )
            for entry in participant_data
            if type(entry.get("response")) is dict
            and entry["response"].get("race") is not None
        ]
        full_demographics.append(demographics[0])
    return full_demographics


def retrieve_deception(participants_data: list[list[dict]]) -> list[str]:
    """Retrieves outcome of the deception check for each participant."""
    final_rankings = []
    for participant_data in participants_data:
        final_ranking = [
            entry["response"]["deception"]
            for entry in participant_data
            if type(entry.get("response")) is dict
            and entry["response"].get("deception") is not None
        ]
        final_rankings.append(final_ranking[0])
    return final_rankings


def retrieve_confidence(participants_data: list[list[dict]]) -> list[int]:
    """
    Retrieve participant self rating of their competitive confidence.

    Args:
        participants_data: List of lists of dictionaries, where each inner list contains recorded entries for a participant and trial.

    Returns:
        confidence: Inner lists self-rating for each participant
    """
    final_rankings = []
    for participant_data in participants_data:
        final_ranking = [
            int(entry["response"])
            for entry in participant_data
            if entry.get("stimulus")
            == "<h2>Rating</h2><p>On a scale from 1–10, how typically successful are you in competitive environments?</p>"
        ]
        final_rankings.append(final_ranking)
    return final_rankings


def generate_subject_ids(participants_data: list[list[dict]]) -> list[int]:
    """
    Selects unique subject id from item-presentation trials across all participants.

    Args:
        participants_data: List of lists of dictionaries, where each inner list contains recorded entries for a participant and trial.

    Returns:
        Contains subject id for a participant and trial combination.
    """
    subject_ids = []
    for subject_id, participant_data in enumerate(participants_data):
        subject_ids.extend(
            subject_id
            for entry in participant_data
            if entry.get("trial_type") == "item-presentation"
        )
    return subject_ids


def extract_race_gender_age(url):
    # Extract the final part of the URL (filename without extension)
    filename = url.split("/")[-1].split(".")[0].lower()
    return filename.split("_")[2:]


def compare_race(raceA: str, raceB: str) -> bool:
    """
    "Asian/Pacific Islander" should match with "Asian-Pacific Islander"
    "Black" should match with "African-American"
    "White" should match with "White"
    "Latino" should match with "Latinx"
    Otherwise no match
    """
    codes = {
        "South Asian": 0,
        "south-asian": 0,
        "East/Southeast Asian": 1,
        "east-asian": 1,
        "Black": 2,
        "black": 2,
        "White": 3,
        "white": 3,
        "Hispanic/Latine/Latinx": 4,
        "latino": 4,
        "Indigenous": 5,
        "Multiracial": 6,
        "Other": 7,
    }
    return codes.get(raceA, np.nan) == codes.get(raceB, np.nan)


def convert_race(race: str) -> str:
    races = [
        "South Asian",
        "East/Southeast Asian",
        "Black",
        "White",
        "Latino",
        "Indigenous",
        "Multiracial",
        "Other",
    ]
    codes = {
        "South Asian": 0,
        "south-asian": 0,
        "East/Southeast Asian": 1,
        "east-asian": 1,
        "Black": 2,
        "black": 2,
        "White": 3,
        "white": 3,
        "Hispanic/Latine/Latinx": 4,
        "latino": 4,
        "Indigenous": 5,
        "Multiracial": 6,
        "Other": 7,
    }
    return races[codes[race]]


def convert_age(age_int: int) -> str | float:
    """
    Convert age_int into age_str based on the following rules:
        - If age_int is <= 24, return "18-24"
        - If age_int is between 25 and 31 (inclusive), return "25-31"
        - If age_int is between 32 and 38 (inclusive), return "32-38"
        - If age_int is above 39 and 45 (inclusive), return "39-45"
        - If age_int is above 45, return "45+"
    """
    if age_int <= 24:
        return "18-24"
    elif age_int >= 25 and age_int <= 31:
        return "25-31"
    elif age_int >= 32 and age_int <= 38:
        return "32-38"
    elif age_int >= 39 and age_int <= 45:
        return "39-45"
    elif age_int > 45:
        return "45+"
    return np.nan


def convert_gender(gender: str) -> str:
    genders = ["Man", "Woman", "Non-binary", "Other"]
    codes = {
        "Man": 0,
        "male": 0,
        "man": 0,
        "Woman": 1,
        "woman": 1,
        "female": 1,
        "Non-binary": 2,
        "non-binary": 2,
        "Other": 3,
        "other": 3,
    }
    return genders[codes[gender]]


def retrieve_full_ranking(participants_data: list[list[dict]]) -> list[list[dict]]:
    """
    Retrieve the final ranking of items from the data.

    Args:
        participants_data: List of lists of dictionaries, where each inner list contains recorded entries for a participant and trial.

    Returns:
        final_rankings: Inner lists contain the final ranking of items for a participant.
    """
    final_rankings = []
    for participant_data in participants_data:
        final_ranking = []
        for entry in participant_data:
            if entry.get("trial_type") == "sortable-rank":
                rank = 1
                for character in entry["team_left_items"]:
                    if character["label"] == "locked":
                        continue
                    final_ranking.append(
                        {
                            "label": character["label"],
                            "content": character["content"],
                            "team": "Your Team",
                            "rank": rank,
                            "index": character["index"],
                        }
                    )
                    rank += 1

                for character in entry["team_right_items"]:
                    final_ranking.append(
                        {
                            "label": character["label"],
                            "content": character["content"],
                            "team": "Other Team",
                            "rank": rank,
                            "index": character["index"],
                        }
                    )
                    rank += 1

                final_rankings.append(final_ranking)
                break
    return final_rankings


def retrieve_choice_rankings(participants_data: list[list[dict]]) -> list[list[dict]]:
    """
    Compute Copeland rankings for each participant's items based on forced-choice trials.
    This version adapts to entries that only have 'choice', 'left_image', and 'right_image'
    (no explicit 'winner', 'loser', or indices).

    Args:
        participants_data: A list of participants, each containing a list of trial dicts.
                           Each trial dict has 'choice' (either 'left' or 'right'),
                           'left_image', 'right_image'.

    Returns:
        A list of lists. Each inner list corresponds to a participant and contains dictionaries
        for each item: {'rank': int, 'index': int, 'label': str}, sorted by rank.
    """
    all_results = []

    for participant_data in participants_data:
        # Map each encountered image to a unique index
        image_to_index = {}
        next_index = 0

        # Store wins, losses, and labels for items
        # {index: {"wins": int, "losses": int, "label": str}}
        items = {}

        # Process each trial
        for entry in participant_data:
            # Skip if no valid choice
            if "choice" not in entry or entry["choice"] not in ["left", "right"]:
                continue

            left_img = entry["left_image"]
            right_img = entry["right_image"]

            # Assign indices to images if not already done
            if left_img not in image_to_index:
                image_to_index[left_img] = next_index
                next_index += 1
            if right_img not in image_to_index:
                image_to_index[right_img] = next_index
                next_index += 1

            left_idx = image_to_index[left_img]
            right_idx = image_to_index[right_img]

            # Initialize items data if not present
            if left_idx not in items:
                items[left_idx] = {"wins": 0, "losses": 0, "label": left_img}
            if right_idx not in items:
                items[right_idx] = {"wins": 0, "losses": 0, "label": right_img}

            # Determine winner and loser from the 'choice'
            if entry["choice"] == "left":
                winner_idx = left_idx
                loser_idx = right_idx
            else:
                winner_idx = right_idx
                loser_idx = left_idx

            # Update wins and losses
            items[winner_idx]["wins"] += 1
            items[loser_idx]["losses"] += 1

        # Compute Copeland scores and sort items
        scored_items = []
        for idx, data in items.items():
            score = data["wins"] - data["losses"]
            scored_items.append((idx, score, data["label"]))

        # Sort by score descending, then by index ascending if needed
        scored_items.sort(key=lambda x: x[1], reverse=True)

        # Assign ranks
        ranked_result = []
        for rank, (idx, score, label) in enumerate(scored_items, start=1):
            ranked_result.append({"rank": rank, "index": idx, "label": label})

        all_results.append(ranked_result)

    return all_results


def bootstrap_ci(values, n_boot=10000, ci=95):
    """
    Return (mean, lower, upper) for a bootstrap CI.
    """
    # Convert to numpy array
    arr = np.asarray(values)
    means = []
    for _ in range(n_boot):
        sample = np.random.choice(arr, size=len(arr), replace=True)
        means.append(sample.mean())
    means = np.sort(means)
    
    lower_idx = int((100 - ci)/2/100 * n_boot)
    upper_idx = int((100 + ci)/2/100 * n_boot)
    
    return arr.mean(), means[lower_idx], means[upper_idx]