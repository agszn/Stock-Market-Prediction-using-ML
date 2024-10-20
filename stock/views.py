from django.shortcuts import render
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend, which supports saving figures

graph_path = 'static/graph'
directory_path = 'data'

# Function to load and preprocess the stock data
def load_stock_data(file_paths):
    dfs = [pd.read_csv(file_path) for file_path in file_paths]
    df = pd.concat(dfs, ignore_index=True)
    return df

# Function to preprocess the stock data (fillna and dropna)
def preprocess_stock_data(df):
    df_filled = df.apply(lambda x: x.fillna(x.mean()) if x.dtype.kind in 'biufc' else x)
    df_cleaned = df.dropna()
    return df_filled, df_cleaned

# Function to calculate average closing price by symbol
def calculate_average_closing_price(df):
    average_closing_price = df.groupby('Symbol')['Close'].mean()
    return average_closing_price

# # Function to plot average closing price history
# def plot_average_closing_price(df, output_file):
#     average_closing_price = df.groupby('Symbol')['Close'].mean()
#     # Your plotting code here
#     plt.figure(figsize=(16, 6))
#     plt.title('Average Closing Price History')
#     df['Date'] = pd.to_datetime(df['Date'])  
#     df_subset = df.iloc[:len(average_closing_price)]
#     plt.plot(df_subset['Date'], average_closing_price, label='Average Closing Price', color='blue')
#     plt.xlabel('Date', fontsize=18)
#     plt.ylabel('Average Closing Price', fontsize=18)
#     plt.legend()
#     plt.savefig(output_file)
#     plt.close()  # Close the plot to free up memory

# Function to generate box plot
def generate_box_plot(df, output_file):
    # Your box plot code here
    plt.figure(figsize=(16, 6))
    sns.boxplot(x='Symbol', y='Close', data=df, whis=1.5)
    plt.title('Box Plot of Closing Prices for Different Stocks')
    plt.xlabel('Stock')
    plt.ylabel('Close Price')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.savefig(output_file)
    plt.close()  # Close the plot to free up memory

# Function to generate correlation heatmap
def generate_correlation_heatmap(df, output_file):
    plt.figure(figsize=(10, 8))
    correlation_matrix = df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5)
    plt.title('Correlation Heatmap')
    plt.savefig(output_file)
    plt.close()  # Close the plot to free up memory

# Function to generate pair plot
def generate_pair_plot(df, output_file):
    plt.figure(figsize=(16, 10))
    sns.pairplot(df, diag_kind='kde', height=5)
    plt.title('Pair Plot')
    plt.savefig(output_file)
    plt.close()  # Close the plot to free up memory

# Django views
def analyze_stocks(request):
    default_file_paths = [
        "data/ADANIPORTS.csv",
    ]

    file_paths = default_file_paths.copy()  # Initialize with default file paths

    if request.method == 'POST':
        selected_files = request.FILES.getlist('selected_files')  # Get selected files from the form
        for uploaded_file in selected_files:
            file_path = os.path.join(directory_path, uploaded_file.name)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            file_paths.append(file_path)  # Append the uploaded file path to the list of file paths

    # Load and preprocess stock data
    df = load_stock_data(file_paths)
    df_filled, _ = preprocess_stock_data(df)

    # Perform analysis and generate plots
    average_closing_price = calculate_average_closing_price(df_filled)
    plot_file_avg_closing = os.path.join(graph_path, 'plot_avg_closing.png')
    # plot_average_closing_price(df, plot_file_avg_closing)
    generate_box_plot(df_filled, os.path.join(graph_path, 'box_plot.png'))
    # generate_correlation_heatmap(df_filled, os.path.join(graph_path, 'correlation_heatmap.png'))
    generate_pair_plot(df_filled, os.path.join(graph_path, 'pair_plot.png'))

    return render(request, 'analyze_stocks.html', {
        'average_closing_price': average_closing_price,
        'plot_file_avg_closing': plot_file_avg_closing,
        'file_paths': file_paths,
    })
