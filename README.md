# 音訊轉文字工具

## 簡介
音訊轉文字工具是一個基於Flask和OpenAI的應用，用於將使用者上傳的音訊或影片中的音訊轉換成文字，並通過OpenAI的API自動生成文本摘要。該應用支援多種音訊格式，並提供GPU加速選項以提高轉換效率。

## 功能
- 上傳音訊或影片文件並將音訊轉換成文字
- 支持多種音訊格式（如MP3、WAV等）
- 使用OpenAI的API自動生成文本摘要
- 支援選擇顯示卡進行加速轉換
- 支援錄音功能並將錄音轉換成文字
- 支持自動下載轉換結果
- 支持將結果通過電子郵件發送給使用者

## 安裝
請按照以下步驟安裝並運行此應用：

1. **克隆此存儲庫**

2. **創建虛擬環境並安裝依賴**
   ```sh
   python -m venv venv
   source venv/bin/activate  # 在Windows上使用 `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **設置環境變量**
   將你的OpenAI API密鑰設置為環境變量：
   ```sh
   export OPENAI_API_KEY='your_openai_api_key'  # 在Windows上使用 `set OPENAI_API_KEY='your_openai_api_key'`
   ```

4. **運行Flask應用**
   ```sh
   python app.py
   ```

5. **打開瀏覽器並訪問**
   ```
   http://127.0.0.1:5000
   ```

## 使用說明
1. **上傳文件**
   - 打開瀏覽器並訪問應用。
   - 點擊“選擇檔案”按鈕上傳音訊或影片文件。
   - 選擇輸出格式（文字檔案、帶時間戳的文字檔案或SubRip字幕文件）。
   - 選擇顯示卡進行加速轉換（如果有多個顯示卡）。
   - 點擊“上傳並轉換”按鈕開始轉換。

2. **錄音轉換**
   - 點擊“開始錄音”按鈕開始錄音。
   - 點擊“停止錄音”按鈕結束錄音並自動上傳錄音文件進行轉換。

3. **自動下載和電子郵件發送**
   - 勾選“是否完成後自動下載”選項以在轉換完成後自動下載結果文件。
   - 勾選“是否將結果重送至信箱”選項並輸入電子郵件地址，以在轉換完成後通過電子郵件發送結果。

## 文件結構
```
音訊轉文字工具/
├── app.py                # Flask主應用
├── transcribe.py         # 音訊轉文字和摘要生成邏輯
├── send_email.py         # 發送電子郵件模塊
├── summarize.py          # 生成文本摘要模塊
├── templates/
│   ├── index.html        # 主頁面模板
│   ├── login.html        # 登錄頁面模板
├── static/
│   ├── styles.css        # CSS樣式表
│   ├── script.js         # JavaScript腳本
│   ├── loading.gif       # 加載動畫
│   ├── recording.gif     # 錄音指示動畫
├── requirements.txt      # 依賴包列表
├── config.py             # 配置文件
└── README.md             # 此README文件
```

## 技術細節
- **前端：** 使用HTML、CSS和JavaScript實現的簡單網頁界面。
- **後端：** 使用Flask框架構建的Web服務器。
- **音訊轉文字：** 使用OpenAI的Whisper模型進行音訊轉文字轉換。
- **文本摘要：** 使用OpenAI的GPT-3.5-turbo模型生成文本摘要。
- **錄音功能：** 使用瀏覽器的MediaRecorder API進行錄音。
- **GPU加速：** 使用PyTorch進行GPU加速。

## 貢獻
歡迎任何形式的貢獻！如果你有任何改進建議或發現了任何問題，請提交Issue或Pull Request。

## 授權
此項目基於MIT許可證進行授權，詳細信息請參閱LICENSE文件。