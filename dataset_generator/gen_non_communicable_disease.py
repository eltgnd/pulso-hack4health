import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random as rand

def barangay_report(num_seed, trend, barangay):
    weeks = np.arange(1, 31)
    np.random.seed(num_seed)
    def generate_trend(trend_type, base, variance, size):
        if trend_type == 0: #increasing
            trend = base + np.arange(size) * variance / size
        elif trend_type == 1: #decreasing
            trend = base + (size - np.arange(size)) * variance / size
        elif trend_type == 2: #increase_then_decrease
            half = size // 2
            trend = np.concatenate([
                base + np.arange(half) * variance / half,
                base + (half - np.arange(size - half)) * variance / half
            ])
        elif trend_type == 3: #decrease_then_increase
            half = size // 2
            trend = np.concatenate([
                base + (half - np.arange(half)) * variance / half,
                base + np.arange(size - half) * variance / half
            ])
        else:
            raise ValueError("Unknown trend type")
        return trend + np.random.randint(-variance // 2, variance // 2, size)

    trend_type = trend
    base = 10
    variance = 10
    size = 30

    epidemic_thresholds = generate_trend(trend_type, base, variance, size)
    alert_thresholds = epidemic_thresholds - np.random.randint(1, 4, size)
    shift = np.random.randint(-2, 3) 

    cases_2024 = np.roll(alert_thresholds - np.random.randint(5, 15, size), shift)
    cases_2024 = np.maximum(cases_2024, 0)

    cases_2023 = cases_2024 - np.random.randint(0, 3, size)
    cases_2023 = np.maximum(cases_2023, 0)

    cases_2024[18:] = 0

    for i in range(len(weeks)):
        if np.random.rand() > 0.8:
            if i < 18:
                cases_2024[i] = np.random.randint(0, alert_thresholds[i] + 1)
            cases_2023[i] = np.random.randint(0, cases_2024[i] + 1)


    data = {
        'Week': weeks,
        '2024 Cases': cases_2024,
        '2023 Cases': cases_2023,
        'Alert Threshold': alert_thresholds,
        'Epidemic Threshold': epidemic_thresholds
    }
    df = pd.DataFrame(data)
    df.to_csv(f'../datasets/barangay_MRS_dataset/{barangay}_MRS_data.csv', index=False)

    plt.figure(figsize=(12, 6))

    plt.bar(df['Week'], df['2024 Cases'], color='navy', label='MW 1, 2024 - MW 18, 2024')
    plt.plot(df['Week'], df['2023 Cases'], color='grey', marker='o', label='2023')
    plt.plot(df['Week'], df['Alert Threshold'], color='orange', linestyle='--', label='Alert Thresholds')
    plt.plot(df['Week'], df['Epidemic Threshold'], color='red', linestyle='-', label='Epidemic Thresholds')
    plt.axvspan(15, 18, color='red', alpha=0.3, label='Current Analysis Period')

    plt.xlabel('Morbidity Week')
    plt.ylabel('Number of Cases')
    plt.title('Alert and Epidemic Curve of Reported Cases by Morbidity Week', pad = 28, fontweight='bold')

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.07), ncol=5, fontsize='small')

    plt.grid(True)
    plt.savefig(f'../images/barangay_MRS_plot/{barangay}_MRS.png')

barangay_list = [
    "Aliwekwek",
    "Baay",
    "Balangobong",
    "Balococ",
    "Bantayan",
    "Basing",
    "Capandanan",
    "Domalandan Center",
    "Domalandan East",
    "Domalandan West",
    "Dorongan",
    "Dulag",
    "Estanza",
    "Lasip",
    "Libsong East",
    "Libsong West",
    "Malawa",
    "Malimpuec",
    "Maniboc",
    "Matalava",
    "Naguelguel",
    "Namolan",
    "Pangapisan North",
    "Pangapisan Sur",
    "Poblacion",
    "Quibaol",
    "Rosario",
    "Sabangan",
    "Talogtog",
    "Tonton",
    "Tumbar",
    "Wawa"
]

cnt = 1
for barangay in barangay_list:
    trend = rand.randint(0,3)
    barangay_report(cnt, trend, barangay)
    print (f'{barangay}\'s data is successfully created.')