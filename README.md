# Monte Carlo Quant

Monte Carlo Quant 是一個 Python 模擬工具，專門用於交易策略風險測試。它會載入交易報酬數據，依據設定的風險比例進行大量 Monte Carlo 模擬，並同時比較固定風險與複利結果。

## 主要功能

- 支援 CSV 或 Excel 輸入資料
- 使用 `S` 與 `R` 兩欄資料
- 同時比較：
  - 固定風險（fixed）
  - 複利風險（compound）
- 可自訂多組風險比例（預設：0.25%、0.5%、0.75%、1.0%、1.25%、1.5%、2.0%、3.0%）
- 可自訂模擬次數（預設 10000 次）
- 產生 Excel 統計報表
- 產生文字報告（TXT）
- 可選 PNG 圖表輸出
- 計算風險指標：
  - 最大回撤（Max Drawdown）
  - 連續虧損次數
  - 破產率（Risk of Ruin）
  - 盈利機率（Probability of Profit）
  - 期望值 / Profit Factor

## 安裝

請先建立虛擬環境，然後安裝相依套件：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 使用方式

將交易資料放在 `input/` 資料夾，預設檔名為 `data.csv`。

執行：

```powershell
python main.py
```

執行後會在 `output/` 下建立新的時間戳記子資料夾，裡面包含輸出結果。

## 輸入資料格式

輸入檔案必須包含以下欄位：

- `S`：商品或資產代號
- `R`：單筆報酬率或報酬乘數

預設配置會自動讀取 `input/data.csv`。若需要自訂欄位名稱，可修改 `config.py` 中的 `CSV_COLUMNS`。

## 輸出結果

`main.py` 會輸出以下內容：

- `output/<timestamp>/monte_carlo_summary.xlsx`
  - Excel 報表包含各風險比例下的統計數據
  - 核心欄位包含：
    - `Average Final Equity (平均權益)`
    - `Median Final Equity (中位數權益)`
    - `Best Case / High Bound` / `Worst Case / Low Bound`
    - `Probability of Profit (區間內勝率)`
    - `Risk of Ruin (全樣本破產率)`
    - `Avg Max Drawdown` / `Worst Max Drawdown` / `Best Max Drawdown`
    - `Avg Losing Streak` / `Worst Losing Streak` / `Best Losing Streak`
- `output/<timestamp>/monte_carlo_report.txt`
  - 文字報告包含同樣結果與各項統計說明
- `output/<timestamp>/plots/`（若啟用 PNG 輸出）
  - 各風險比例的蒙地卡羅資產曲線圖

## 設定項目

可編輯 `config.py` 以調整：

- `INPUT_FOLDER`：輸入資料夾
- `INPUT_FILE`：輸入檔名
- `OUTPUT_FOLDER`：輸出資料夾
- `SIMULATION_RUNS`：模擬次數
- `RISK_RATIOS`：風險比例清單
- `SYMBOL_FILTER`：若需篩選單一標的，可設為字串或清單
- `COMPARE_FIXED_AND_COMPOUND`：是否同時輸出固定與複利結果
- `RANDOM_SEED`：隨機種子，用以重現模擬結果
- `USE_EXCEL_OUTPUT`：是否輸出 Excel
- `USE_PNG_OUTPUT`：是否輸出 PNG
- `USE_TXT_REPORT`：是否輸出文字報告
- `INITIAL_CAPITAL`：初始資金
- `RUIN_THRESHOLD`：破產門檻
- `DISPLAY_RANGE`：統計時顯示範圍（如 0.8 代表去頭去尾 10%）

## 專案結構

```text
monte_carlo_quant/
├── config.py
├── main.py
├── README.md
├── requirements.txt
├── core/
│   ├── io.py
│   ├── metrics.py
│   ├── monte_carlo.py
│   └── report.py
├── input/
│   └── data.csv
└── output/
```

## 作者與備註

本工具適合用於交易資料回測與風險比例比較分析。若要擴充更多策略，可在 `core/monte_carlo.py` 與 `core/metrics.py` 中新增風險衡量指標。

如需進一步自訂輸入欄位或輸出格式，請修改 `config.py` 和 `core/report.py`。