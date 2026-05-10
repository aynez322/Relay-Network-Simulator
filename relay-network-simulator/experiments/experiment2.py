from config.settings import ExperimentConfig
from experiments.scenarios import run_experiment2
if __name__ == "__main__":
    df = run_experiment2(ExperimentConfig(seed=42))
    print(df.head())
