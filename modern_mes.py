import pandas as pd
import time
import joblib
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

console = Console()

# Eğitilmiş modeli yükle (Dosya yoksa varsayılan kurala düşer)
try:
    model = joblib.load('failure_model.pkl')
    has_model = True
except Exception:
    has_model = False

def create_dashboard(row, current_idx, total_rows, total_failures):
    table = Table(title="🏭 MES Real-Time Production & Telemetry Stream", expand=True)
    table.add_column("Sıra", justify="center")
    table.add_column("Ürün Kodu", justify="center")
    table.add_column("Tip", justify="center")
    table.add_column("Sıcaklık (K)", justify="right")
    table.add_column("Tork (Nm)", justify="right")
    table.add_column("Tahmin / Durum", justify="center")

    temp = row['Air temperature [K]']
    torque = row['Torque [Nm]']
    m_type = row['Type']
    actual_failure = row['Machine failure']

    # AI Model Tahmini Yap (varsa)
    if has_model:
        input_df = pd.DataFrame([{
            'Type': m_type,
            'Air temperature [K]': temp,
            'Process temperature [K]': row['Process temperature [K]'],
            'Rotational speed [rpm]': row['Rotational speed [rpm]'],
            'Torque [Nm]': torque,
            'Tool wear [min]': row['Tool wear [min]']
        }])
        pred = model.predict(input_df)[0]
        status = "[bold red]🚨 ML ALARM: ARIZA[/bold red]" if pred == 1 else "[bold green]🟢 STABİL[/bold green]"
    else:
        status = "[bold red]🚨 ARIZA[/bold red]" if actual_failure == 1 else "[bold green]🟢 STABİL[/bold green]"

    table.add_row(
        f"{current_idx}/{total_rows}", 
        str(row['Product ID']), 
        m_type, 
        f"{temp:.1f}", 
        f"{torque:.1f}", 
        status
    )

    efficiency = ((current_idx - total_failures) / current_idx) * 100
    summary = f"Okunan: {current_idx}/{total_rows} | Toplam Arıza: {total_failures} | Verimlilik: %{efficiency:.1f}"
    
    return Panel(table, subtitle=summary, title="[bold cyan]IIoT Live Engine[/bold cyan]")

def run():
    df = pd.read_csv('ai4i2020.csv').tail(30)
    failures = 0

    with Live(refresh_per_second=4, console=console) as live:
        for i in range(len(df)):
            row = df.iloc[i]
            if row['Machine failure'] == 1:
                failures += 1
                
            live.update(create_dashboard(row, i + 1, len(df), failures))
            time.sleep(0.5)

if __name__ == "__main__":
    run()