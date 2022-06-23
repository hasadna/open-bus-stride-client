import urbanaccess.network


def load_network(network_path):
    *dir, filename = network_path.split('/')
    dir = '/'.join(dir)
    return urbanaccess.network.load_network(dir=dir, filename=filename)
