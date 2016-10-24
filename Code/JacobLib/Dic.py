def Dic_Search(search, diction, Key=True):
    "Look at every values or keys and return true if its there"
    if(Key == True):
        # Try to find the value if it errors return False else True
        try:
            diction[str(search)]
            return True
        except KeyError:
            return False
    else:
        # set a count to determin if all diconery kes have been surched
        count = len(diction.values())
        for values in diction.values():
            count -= 1  # incroment key count
            if values == search:  # check if key is current arg
                return True
            # if the count is equel to the max dictonety keys arg does not
            # exist
            elif count == 0:
                return False
        return False
