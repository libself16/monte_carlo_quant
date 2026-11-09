# Monte Carlo Quant

Monte Carlo Quant 是一個 Python 模擬工具，專門用於交易策略風險測試。它會載入交易報酬數據（以 R 倍數表示），從歷史交易中有放回地隨機抽樣（bootstrap），依據設定的風險比例進行大量 Monte Carlo 模擬，並同時比較固定風險與複利結果。

## 主要功能

- 支援 CSV 或 Excel 輸入資料
- 讀取「標的」與「報酬（R 倍數）」兩欄資料，欄位名稱可在 `config.py` 的 `CSV_COLUMNS` 設定（預設為 `Symbol` 與 `Profit`）
- 同時比較：
  - 固定風險（fixed）
  - 複利風險（compound）
- 可自訂多組風險比例（`RISK_RATIOS`，目前預設為 `[3]`，即 3%；可改成例如 `[0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]` 一次比較多組）
- 可自訂模擬次數（預設 10000 次）
- 產生 Excel 統計報表
- 產生文字報告（TXT）
- 可選 PNG 圖表輸出
- 計算風險指標：
  - 最大回撤（Max Drawdown）
  - 連續虧損次數
  - 破產率（Risk of Ruin）：最終權益 ≤ `RUIN_THRESHOLD` 的模擬比例（全樣本）
  - 盈利機率（Probability of Profit）：在 `DISPLAY_RANGE` 區間內，最終權益高於初始資金的比例
  - 勝率 / 期望值 / Profit Factor

## 安裝

請先建立虛擬環境，然後安裝相依套件：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 使用方式

將交易資料放在 `input/` 資料夾，預設檔名為 `data.csv`。若將 `INPUT_FILE` 設為 `None`，會讀取 `input/` 內所有 `.csv` 與 `.xls*` 檔案並合併。

執行：

```powershell
python main.py
```

執行後會在 `output/` 下建立新的時間戳記子資料夾，裡面包含輸出結果，並會複製一份輸入檔作為紀錄。

## 輸入資料格式

輸入檔案必須包含以下兩個欄位（欄位名稱由 `config.py` 的 `CSV_COLUMNS` 對應）：

| 用途 | `CSV_COLUMNS` 鍵 | 預設欄位名稱 | 說明 |
| --- | --- | --- | --- |
| 標的 | `symbol` | `Symbol` | 商品或資產代號 |
| 報酬 | `return` | `Profit` | 單筆交易的 R 倍數（例如 `2` 代表賺 2R、`-1` 代表虧 1R） |

其他欄位會被忽略；報酬欄位無法轉成數字的列會被略過。

模擬時，每筆交易的損益為 `R × 風險比例`。例如風險比例 1%、R = 2 時，該筆獲利為資金的 2%：

- 固定風險（fixed）：每筆以「初始資金」計算損益
- 複利風險（compound）：每筆以「當下資金」計算損益

## 輸出結果

`main.py` 會輸出以下內容：

- `output/<timestamp>/monte_carlo_summary.xlsx`
  - Excel 報表包含各風險比例下的統計數據
  - 核心欄位包含：
    - `Average Final Equity (平均權益)`
    - `Median Final Equity (中位數權益)`
    - `Best Case / High Bound` / `Worst Case / Low Bound`：`DISPLAY_RANGE` 區間的上下限（例如 0.8 為第 90 / 第 10 百分位）
    - `Probability of Profit (區間內勝率)`
    - `Risk of Ruin (全樣本破產率)`
    - `Avg Max Drawdown` / `Worst Max Drawdown` / `Best Max Drawdown`
    - `Avg Losing Streak` / `Worst Losing Streak` / `Best Losing Streak`
    - `Win Rate (勝率)` / `Expectancy (每筆期望值)` / `Profit Factor (獲利因子)`
- `output/<timestamp>/monte_carlo_report.txt`
  - 文字報告包含同樣結果與各項統計說明
- `output/<timestamp>/plots/`（若啟用 PNG 輸出）
  - 各風險比例的蒙地卡羅資產曲線圖（標示全樣本中最佳與最差的路徑）

## 設定項目

可編輯 `config.py` 以調整：

- `INPUT_FOLDER`：輸入資料夾
- `INPUT_FILE`：輸入檔名（設為 `None` 時讀取資料夾內所有 CSV / Excel 檔）
- `CSV_COLUMNS`：標的與報酬欄位名稱對應（預設 `{"symbol": "Symbol", "return": "Profit"}`）
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
- `RUIN_THRESHOLD`：破產門檻（最終權益低於或等於此值視為破產）
- `DISPLAY_RANGE`：統計時顯示範圍（如 0.8 代表去頭去尾各 10%），用於上下限與盈利機率

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