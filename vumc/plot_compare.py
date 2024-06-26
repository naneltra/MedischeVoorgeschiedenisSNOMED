import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



"""
Plots the labels for both matlab scipt approach and snomed annotation approach
Hardcoded data for simplicity
"""
def plot_tiles():

    data =[
            ('PulmonaalLijden',79057,111485),
            ('CardiovasculairLijden',205388,210754),
            ('CerebrovasculairLijden',122840,252201),
            ('DiabetesMellitus',82602,140808),
            ('Dementie',96929,98930),
            ('Nierfalen',48859,93306),
            ('Obesitas',7026,12599),
            ('Parkinson',14867,23032),
            ('Korsakov',8578,13449),
            ('Huntington',740,0)
        ]

    # Unpacking the data into separate lists
    categories, sum_methodA, sum_methodB = zip(*data)
    
    # The position of the bars on the x-axis
    x = range(len(categories))
    
    # Width of a bar
    bar_width = 0.35
    
    # Creating the bar plot
    fig, ax = plt.subplots()
    
    # Creating bars for sum_methodA
    bars1 = ax.bar(x, sum_methodA, width=bar_width, label='Matlab Script', color='b')
    
    # Creating bars for sum_methodB, shifted by bar_width to the right
    bars2 = ax.bar([p + bar_width for p in x], sum_methodB, width=bar_width, label='SNOMED Mapping', color='r')
    
    # Adding labels, title, and legend
    ax.set_xlabel('Category')
    ax.set_ylabel('Sum')
    ax.set_title('Voorgeschiedenis clustering obv zoektermen en SNOMED')
    ax.set_xticks([p + bar_width / 2 for p in x])
    ax.set_xticklabels(categories, rotation=90)
    ax.legend()
    
    # Adding value labels on top of the bars
    for bars in [bars1, bars2]:
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, round(yval, 2), va='bottom')  # va: vertical 
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,}'.format(int(x))))
    plt.show()