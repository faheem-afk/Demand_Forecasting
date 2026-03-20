import matplotlib.pyplot as plt
from pathlib import Path

def show_visuals(df):
    for meal_name in df['meal_name'].unique()[:10]:
        plot_demand_for_meal(df, meal_name)

def plot_demand_for_meal(df, meal_name):
    ax = (
        df[df['meal_name'] == meal_name]
        .groupby(['week_number', 'period'])['num_orders']
        .sum()
        .unstack()
        .plot(title=meal_name, figsize=(10, 5))
    )
    fig = ax.get_figure()
    fig.tight_layout()
    Path("../artifacts/visuals").mkdir(exist_ok=True, parents=True)
    fig.savefig(f"../artifacts/visuals/{meal_name}.png")
    plt.close(fig)