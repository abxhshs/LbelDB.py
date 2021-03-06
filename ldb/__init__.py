tab = True
try:
    from tabulate import tabulate
except ModuleNotFoundError:
    tab = False

idv = 10000
temp = []
lbels = []
data = []
cols = 0


def init():
    """
    Creates the required files
    Should be run for initialization
    Can be run anytime
    :return: None
    """
    try:
        l = open("dbs.lbel", "r")
        l.close()
        d = open("dat.lbel", "r")
        d.close()
    except FileNotFoundError:
        l = open("dbs.lbel", "w")
        l.close()
        d = open("dat.lbel", "w")
        d.close()


def create(labels: tuple or list):
    """
    Creates the Headers or labels:
    To be run at the first run with init()
    :param labels: A list of the headers or labels
    """
    global lbels
    global cols
    global idv
    labels = list(labels)
    labels.insert(0, "id")
    lbels = list(labels)
    cols = len(lbels)


def clear_r(inx: int or tuple or list):
    """
    Deletes the specified row or rows
    :param inx: index of the row or rows to be deleted
    """
    global data
    if type(inx) == int:
        try:
            data.pop(inx)
        except IndexError:
            raise Exception("No rows present or specified index is out of range")
    else:
        for x in inx:
            data.pop(x)
    genid()


def clear_c(inx: int or tuple or list):
    """
    Deletes the specified columns or columns
    :param inx: index of the column or columns to be deleted
    """
    global data
    global lbels
    global cols
    if type(inx) == int:
        lbels.pop(inx)
        for i in range(len(data)):
            data[i].pop(inx)
    else:
        for x in inx:
            lbels.pop(x)
    cols = len(lbels)


def clearall():
    """
    Deletes the database
    :note: does not delete the files
    """
    l = open("dbs.lbel", "w")
    l.close()
    d = open("dat.lbel", "w")
    d.close()


def add_l(arg: str or list or tuple):
    """
    Creates a column in the database
    """
    global lbels
    global data
    global cols
    if type(arg) == int:
        lbels.append(arg)
        nol = 1
    else:
        for i in arg:
            lbels.append(i)
        nol = len(arg)
    for _ in range(nol):
        for i in range(len(data)):
            data[i].append("")
    cols = len(lbels)


def add_d(dat: tuple or list):
    """
    Adds a row to the database
    note: Please leave None or an empty string => "" is no data for the respective label if any
    """
    global data
    global cols
    global idv
    if cols >= len(dat):
        idv += 1
        dat = list(dat)
        dat.insert(0, idv)
        data.append(dat)
    else:
        print("Number of columns exceed number of labels")


def store():
    """
    Stores the data in the db
    :Note: This clears everything from local memory and cant be retrieved without retrieve()
    """
    global data
    global lbels
    global cols
    with open("dat.lbel", "a") as d:
        for i in data:
            for x in i:
                d.write(str(x) + "\n")
        data = []

    with open("dbs.lbel", "w") as f:
        for i in lbels:
            f.write(str(i) + "\n")
        lbels = []
        cols = None


def retrieve():
    """
    Retrieves the database from the stored state
    """
    global lbels
    global data
    global cols
    with open("dbs.lbel", "r+") as l:
        lbels = [line.rstrip() for line in l]
    cols = len(lbels)
    file = open("dat.lbel", "r+")
    counter = 0
    content = file.read()
    colist = content.split("\n")
    for i in colist:
        if i:
            counter += 1
    file.close()
    with open("dat.lbel", "r+") as f:
        lines = list(f.read().splitlines())
        try:
            for a in range(int((counter / cols + 1))):
                global temp
                it = 1
                temp = []
                for i in lines:
                    temp.append(i)
                    if it == cols:
                        data.append(temp)
                        temp = []
                        for _ in range(cols):
                            lines.pop(0)
                        break
                    it += 1
        except ZeroDivisionError:
            raise Exception("Retrieved without adding data to DBs")


def view():
    """
    View the data base
    Better results if using Tabulate module but not necessary
    Note: Not to be used with intensive databases as it can be resource intensive
    """
    global lbels
    global data
    if tab:
        print(tabulate(data, headers=lbels, tablefmt="fancy_grid"))
    else:
        print("Module tabulate is a dependency. ModuleNotFound")
        print(lbels)
        for x in data:
            print(x)


def return_r(inx: int):
    """
    Returns a requested row from the db
    :param inx: The row number
    :return: The requested row
    """
    return data[inx]


def return_rs(inx: list or tuple):
    """
    Returns the requested rows from the db
    :param inx: list or tuple: The row numbers
    :return: The requested rows
    """
    global data
    inx = list(inx)
    tempc = []
    for x in inx:
        tempc.append(list(data[x]))
    return tempc


def return_c(inx: int):
    """
    Returns a requested column from the db
    :param inx: The column number
    :return: The requested column
    """
    global data
    tempv = [lbels[inx]]
    for i in range(len(data)):
        tempv.append(data[i][inx])
    return tempv


def genid():
    """
    Use only if ids generated a corrupt
    """
    global data
    global idv
    idv = 10000
    for i in range(len(data)):
        idv += 1
        data[i].pop(0)
        data[i].insert(0, idv)


def update_r(inx: int, val: list or tuple):
    """
    Updates the whole selected row
    :param inx: index of the row
    :param val: a list or tuple of the updated row
    """
    global data
    global cols
    global lbels
    lbels.pop(0)
    val = list(val)
    try:
        if len(val) > cols:
            print("no of columns in provided list too high")
            raise AttributeError
        data[inx] = val
        data[inx].insert(0, "")
    except IndexError:
        raise Exception("Row number invalid")
    lbels.insert(0, "id")
    genid()


def sort_col(index: int, reverse: bool = False):
    """
    Sorts the chosen column in descending order
    :param index: the index of the column
    :param reverse: reverse = True or False
    """
    global lbels
    global data
    global cols
    data.sort(key=lambda x: x[index])
    if reverse:
        data.reverse()
    genid()
