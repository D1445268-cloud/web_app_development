# 流程圖文件 (Flowchart)：食譜收藏夾系統

本文件根據 `docs/PRD.md` 與 `docs/ARCHITECTURE.md` 的規劃，視覺化使用者的操作路徑與後端系統的資料流，協助團隊確認各項功能的互動邏輯。

## 1. 使用者流程圖（User Flow）

呈現使用者進入網站後的操作動線，並根據是否登入區分不同功能權限。

```mermaid
flowchart LR
    Start([進入網站]) --> Home[首頁 - 瀏覽公開食譜]
    
    Home --> Search{要尋找什麼？}
    Search -->|關鍵字搜尋| KW_Result[食譜搜尋結果頁]
    Search -->|輸入多種食材| Combo_Result[食材組合比對結果頁]
    KW_Result --> Detail[查看單筆食譜詳細資訊]
    Combo_Result --> Detail
    
    Home --> Auth{是否擁有私人空間？}
    Auth -->|未登入| Login[前往登入 / 註冊頁面]
    Login -->|註冊/登入成功| Dashboard[個人食譜管理區]
    
    Auth -->|已登入| Dashboard
    
    Dashboard --> Action{管理個人食譜}
    Action -->|新增| Create[填寫新增食譜表單]
    Action -->|編輯| Edit[修改既有食譜內容]
    Action -->|刪除| Delete[確認刪除彈出視窗]
    
    Create -.儲存.-> Dashboard
    Edit -.儲存.-> Dashboard
    Delete -.確認.-> Dashboard
```

## 2. 系統序列圖（System Sequence Diagram）

以核心功能「**新增食譜**」為例，說明從前端發送請求直到資料庫儲存並回傳結果的完整系統流轉過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (View)
    participant Flask as Flask 路由 (Controller)
    participant Model as 模型 (Model)
    participant DB as SQLite 資料庫

    User->>Browser: 點選「新增食譜」，填具標題、食材與步驟
    User->>Browser: 點擊「送出」按鈕
    Browser->>Flask: POST /recipe/new (攜帶表單資料)
    
    rect rgb(240, 248, 255)
        Note right of Flask: 後端驗證階段
        Flask->>Flask: 檢查 Session (確認已登入)
        Flask->>Flask: 檢查表單格式 (必填欄位是否空白)
    end
    
    alt 驗證成功
        Flask->>Model: 呼叫新增函式 `recipe.create(data, user_id)`
        Model->>DB: 執行 SQL `INSERT INTO recipes ...`
        DB-->>Model: 回傳成功訊息與新的 Recipe ID
        Model-->>Flask: 執行完成，傳回結果
        Flask-->>Browser: HTTP 302 重定向至個人管理頁或單篇食譜頁
        Browser-->>User: 畫面更新，提示「新增成功」並顯示內容
    else 驗證失敗 (如未填標題)
        Flask-->>Browser: HTTP 200 回傳原填寫頁面，帶有錯誤訊息
        Browser-->>User: 畫面上方顯示「食譜名稱不可空白」，維持原表單
    end
```

## 3. 功能清單對照表

下表羅列了系統主要功能的 URL 路徑與對應的 HTTP 方法，供後續開發與路由設計作為基準：

| 功能模組 | 功能描述 | URL 路由路徑 (Route) | 支援 HTTP 方法 |
| :--- | :--- | :--- | :--- |
| **首頁與查詢** | 展示首頁（公開列表） | `/` | GET |
| | 一般關鍵字搜尋食譜 | `/search` | GET |
| | **透過現存食材反向搜尋** | `/combo-search` | GET |
| **會員機制** | 進入註冊與處理註冊送出 | `/auth/register` | GET, POST |
| | 進入登入與處理登入送出 | `/auth/login` | GET, POST |
| | 將使用者登出 | `/auth/logout` | GET |
| **食譜維護** | 查看單筆食譜頁面詳細內容 | `/recipe/<int:id>` | GET |
| | 進入使用者的專屬管理面板 | `/recipe/my-recipes` | GET |
| | 新增食譜頁面與處理送出 | `/recipe/new` | GET, POST |
| | 編輯食譜頁面與處理更新 | `/recipe/<int:id>/edit` | GET, POST |
| | 刪除單篇食譜 (限本人或管理員) | `/recipe/<int:id>/delete`| POST |
