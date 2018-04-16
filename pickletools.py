import pickle


def load(filename):
    print('Reading {}'.format(filename))
    with open(filename, "rb") as fp:
        return pickle.load(fp)


def save(filename, thing):
    print('Saving {}'.format(filename))
    with open(filename, "wb") as fp:
        pickle.dump(thing, fp)
