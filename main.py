import requests

bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
bootstrap_response = requests.get(bootstrap_url)
bootstrap_data = bootstrap_response.json()
players = bootstrap_data['elements']
events = bootstrap_data['events']


user_id = input("Enter user id:")
gameweek_id = next((event['id'] for event in events if event['is_current']), None)
picks_url = f"https://fantasy.premierleague.com/api/entry/{user_id}/event/{gameweek_id}/picks/"
picks_response = requests.get(picks_url)
picks_data = picks_response.json()

player_ids = [pick['element'] for pick in picks_data['picks']]

def all_players():
    player_list = []
    for player in players:
        if player['id'] in player_ids:
            full_name = f"{player['first_name']} {player['second_name']}"
            status = player['status']
            news = player['news']
            if status != 'a':  
                player_list.append({
                    "name": full_name,
                    "status": status,
                    "news": news,
                    "id": player['id'],
                    "cost": player['now_cost'],
                    "position": player['element_type'],
                    "form": float(player['form'])
                })
            else:
                player_list.append({
                    "name": full_name,
                    "status": status,
                    "news": "",
                    "id": player['id'],
                    "cost": player['now_cost'],
                    "position": player['element_type'],
                    "form": float(player['form'])
                })

    print("Manager's Squad:")
    for p in player_list:
        if p["status"] != 'a':
            print(f"{p['name']} - Status: {p['status'].upper()}, Reason: {p['news']}")
        else:
            print(p["name"])
    print("=" * 60)

    return player_list


def suggest_replace():

    squad_players = all_players()

    injured_players = [p for p in squad_players if p['status'] == 'i']
    
    if injured_players:
        target_player = max(injured_players, key=lambda p: p['cost'])
        reason = "Injured"
    else:
        target_player = min(squad_players, key=lambda p: p['form'])
        reason = "Low Form"

    print(f"{reason} Player: {target_player['name']} - Cost: {target_player['cost']/10}M")

    
    replacements = [
        p for p in players
        if p['element_type'] == target_player['position'] and
           p['now_cost'] <= target_player['cost'] and
           p['status'] == 'a' 
    ]
    # Sort replacements by total points or form (optional tweak here)
    replacements = sorted(replacements, key=lambda p: p['form'], reverse=True)

    if replacements:
        best_replacement = replacements[0]
        print(f"Suggested Replacement: {best_replacement['first_name']} {best_replacement['second_name']} - "
              f"Cost: {best_replacement['now_cost']/10}M - Points: {best_replacement['form']}")
    else:
        print("No suitable replacement found.")

suggest_replace()

