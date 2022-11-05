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
    plt.ylabel('Température')
    plt.savefig('static/images/visualisation/temperatures.png')