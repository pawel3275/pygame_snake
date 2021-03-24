import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def plot(scores, mean_scores):
    """
    Helper plotting function that will draw the plot showing the learning curve depending on the score and number of
    games that had been played.
    :param scores: Scores that were achieved by the snake.
    :param mean_scores: Number of mean scores.
    """
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    plt.show()
