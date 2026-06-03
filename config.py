from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FOLDER = BASE_DIR / "input"
INPUT_FILE = "data.csv"
OUTPUT_FOLDER = BASE_DIR / "output"

SIMULATION_RUNS = 10000
RISK_RATIOS = [1, 2, 3, 4, 5]
SYMBOL_FILTER = None

COMPARE_FIXED_AND_COMPOUND = True
RANDOM_SEED = 42
USE_EXCEL_OUTPUT = True
USE_PNG_OUTPUT = True
USE_TXT_REPORT = True
CSV_COLUMNS = {"symbol": "Symbol", "return": "Risk"}

# 初始資金
INITIAL_CAPITAL = 10000
# 破產線
RUIN_THRESHOLD = 2000
# 顯示範圍（去頭去尾）
DISPLAY_RANGE = 0.8