import json

def update_lottery_results():
    # Load existing data
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)

    # Example new lottery results (this should be replaced with actual results)
    new_results = {
        "lottery_name": "Example Lottery",
        "results": [1, 2, 3, 4, 5, 6],
        "date": "2026-03-29"
    }

    # Update the data
    data['lottery_results'].append(new_results)

    # Save updated data
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    update_lottery_results()