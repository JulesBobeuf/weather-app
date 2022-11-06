import matplotlib.pyplot as plt


def temperatureVisu(tabDate, tabTemp):
    """
    Fonction permettant la visualisation des températures.
    :param tabDate: Tableau avec l'ensemble des dates
    :param tabTemp: Tableau avec l'ensemble des températures
    :return: Image de visualisation des températures. Axe X : date | Axe Y : température
    """
    plt.plot(tabDate, tabTemp, 'bo')
    plt.xlabel('Date de relevé')
    plt.ylabel('Température (°C)')
    plt.savefig('static/images/visualisation/temperatures.png')
    plt.clf()

def humiditeVisu(tabDate, tabHumid):
    """
    Fonction permettant la visualisation des températures.
    :param tabDate: Tableau avec l'ensemble des dates
    :param tabTemp: Tableau avec l'ensemble des températures
    :return: Image de visualisation des températures. Axe X : date | Axe Y : température
    """
    plt.plot(tabDate, tabHumid, 'bo')
    plt.xlabel('Date de relevé')
    plt.ylabel('Taux d\'humidité (%)')
    plt.savefig('static/images/visualisation/humidite.png')
    plt.clf()

def pressionVisu(tabDate, tabPress):
    """
    Fonction permettant la visualisation des températures.
    :param tabDate: Tableau avec l'ensemble des dates
    :param tabTemp: Tableau avec l'ensemble des températures
    :return: Image de visualisation des températures. Axe X : date | Axe Y : température
    """
    plt.plot(tabDate, tabPress, 'bo')
    plt.xlabel('Date de relevé')
    plt.ylabel('Pression (hPa)')
    plt.savefig('static/images/visualisation/pression.png')
    plt.clf()