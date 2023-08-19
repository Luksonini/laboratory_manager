import matplotlib
matplotlib.use('agg') 
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def generate_pie_chart(remained, quantity):
    labels = ['Pozostało', 'Zużyte']
    sizes = [remained, quantity - remained]
    colors = ['#12af83', '#ff6666']

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png", transparent=True)
    plt.close()
    
    pie_chart_data = base64.b64encode(buffer.getvalue()).decode()
    return pie_chart_data


