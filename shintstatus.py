def listify(intstatus):
    """ Takes string, returns list """

    # Creates overall list
    mainlist = []
    for line in intstatus.split("\n"):
        if len(line) < 2:
            continue
        # Breaks on two spaces and assigns to sublist "li"
        li = line.split("  ")
        # Removes list elements smaller than len(1),
        # which is the single space ("") elements
        li = [elem for elem in li if len(elem) > 0]
        # Cleans up left-side white space
        li = [elem.lstrip() for elem in li]
        # Removes and returns last element.
        # This includes Speed and the interface type.
        try:
            speedType = li.pop(-1)
        except IndexError:
            break
        # Splits the string on the space and creates two strings.
        speed = speedType.split()[0]
        intType = speedType.split()[1]
        # Appends the strings to the list
        li.append(speed)
        li.append(intType)
        # Appends sublist "li" to overall list "mainlist"
        mainlist.append(li)

    return mainlist
