#luggi Tutorial exercise
""" Tutorial exercise for python functions and dicionaries. """

sample = [
    {'name': 'Peach', 'items': ['green shell', 'banana', 'green shell',], 'finish': 3},
    {'name': 'Bowser', 'items': ['green shell',], 'finish': 1},
    # Sometimes the racer's name wasn't recorded
    {'name': None, 'items': ['mushroom',], 'finish': 2},
    {'name': 'Toad', 'items': ['green shell', 'mushroom'], 'finish': 1},
]

full_dataset = [{'name': 'Peach', 'items': ['green shell', 'banana', 'green shell'], 'finish': 3},
    {'name': 'Peach', 'items': ['green shell', 'banana', 'green shell'], 'finish': 1},
    {'name': 'Bowser', 'items': ['green shell'], 'finish': 1},
    {'name': None, 'items': ['green shell'], 'finish': 2}, 
    {'name': 'Bowser', 'items': ['green shell'], 'finish': 1}, 
    {'name': None, 'items': ['red shell'], 'finish': 1}, 
    {'name': 'Yoshi', 'items': ['banana', 'blue shell', 'banana'], 'finish': 7}, 
    {'name': 'DK', 'items': ['blue shell', 'star'], 'finish': 1}
]

def best_items(racers):
    """Given a list of racer dictionaries, return a dictionary mapping items to the number
    of times those items were picked up by racers who finished in first place.
    """
    winner_item_counts = {}
    for i in range(len(racers)):
        # The i'th racer dictionary
        racer = racers[i]
        # We're only interested in racers who finished in first
        if racer['finish'] == 1:
            for item in racer['items']:
                # Add one to the count for this item (adding it to the dict if necessary)
                if item not in winner_item_counts:
                    winner_item_counts[item] = 0
                winner_item_counts[item] += 1

        # Data quality issues :/ Print a warning about racers with no name set. We'll take care of it later.
        if racer['name'] is None:
            print("WARNING: Encountered racer with unknown name on iteration {}/{} (racer = {})".format(
                i+1, len(racers), racer['name'])
                 )
    return winner_item_counts


print("Scanning Sample Dataset:")
print("The items and count: \n" + 
', '.join(["'{}' Cnt: {} ".format(v.capitalize(),a) for v,a in best_items(sample).items()]))
print("\nScanning Full Dataset")
print("The items and count: \n" + 
', '.join(["'{}' Cnt: {} ".format(v.capitalize(),a) for v,a in best_items(full_dataset).items()]))
