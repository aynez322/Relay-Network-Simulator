from config.settings import ExperimentConfig
from experiments.scenarios import run_experiment4
if __name__ == "__main__":
    df = run_experiment4(ExperimentConfig(seed=42))
    print(df.head())
