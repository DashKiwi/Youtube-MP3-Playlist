import json

playlists = {
    "Playlist 1": {
        "Song": "Some song",
        "Song2": "Some other song",
        "Song 4": "Some different song"
    }
}

# Adds the playlist to the json file
save_file = open(r".\Music\test.json", "w")
json.dump(playlists, save_file, indent=6)  
save_file.close()

# Gets read access to the json file 
save_file = open(r".\Music\test.json", "r")
data = json.load(save_file)

# Can list out all the objects inside a sepecific class
for j in data["Playlist 1"]:
    print(data["Playlist 1"][j])

# Chooses the location
data["Playlist 1"]["Song3"] = "Some Other Other Song"

# gains write access to the json file
save_file = open(r".\Music\test.json", "w") 
# adds the new data to the save file
json.dump(data, save_file)
# closes the save file to save
save_file.close()