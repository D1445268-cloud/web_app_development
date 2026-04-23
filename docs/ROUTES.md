# 路由設計文件 (API Routes)：食譜收藏夾系統

本文件基於 PRD 與 ARCHITECTURE 設計，規劃 Flask 的路由與頁面，包含每個頁面的 URL 路徑、HTTP 方法、輸入/輸出與對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能模組 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁與查詢 (index)** |
| 首頁 / 公開列表 | GET | `/` | `index.html` | 顯示所有公開食譜，最新發表在前 |
| 關鍵字搜尋 | GET | `/search` | `index.html` | 透過 query parameter `?q=關鍵字` 搜尋食譜 |
| 食材反向搜尋 | GET | `/combo-search` | `index.html` | 透過 query parameter `?ingredients=A,B` 反向搜尋食譜 |
| **會員機制 (auth)** |
| 註冊頁面與處理 | GET, POST | `/auth/register` | `auth/register.html` | 顯示註冊表單與處理帳號建立 |
| 登入頁面與處理 | GET, POST | `/auth/login` | `auth/login.html` | 顯示登入表單與驗證身分 |
| 登出 | GET | `/auth/logout` | — | 清除 Session 後重導向至首頁 |
| **食譜維護 (recipe)** |
| 查看單筆食譜 | GET | `/recipe/<int:id>` | `recipe/detail.html` | 顯示單筆食譜詳細內容 |
| 個人管理面板 | GET | `/recipe/my-recipes` | `recipe/my_recipes.html`| 顯示登入使用者的所有食譜 |
| 新增食譜 | GET, POST | `/recipe/new` | `recipe/form.html` | 顯示新增表單與處理儲存邏輯 |
| 編輯食譜 | GET, POST | `/recipe/<int:id>/edit`| `recipe/form.html` | 顯示編輯表單與處理更新邏輯 |
| 刪除食譜 | POST | `/recipe/<int:id>/delete`| — | 刪除食譜後重導向至個人面板 |

---

## 2. 每個路由的詳細說明

### 首頁與查詢 (Index Blueprint)

#### `GET /`
- **輸入**：無
- **處理邏輯**：呼叫 `recipe.get_all_public_recipes()` 取得最新公開食譜
- **輸出**：渲染 `index.html`，傳入 `recipes` 變數
- **錯誤處理**：無特別錯誤

#### `GET /search`
- **輸入**：URL 參數 `q` (字串)
- **處理邏輯**：呼叫 `recipe.search_recipes_by_keyword(q)`
- **輸出**：渲染 `index.html`，傳入 `recipes` 與 `search_query`
- **錯誤處理**：若未提供 `q`，則重導回 `/`

#### `GET /combo-search`
- **輸入**：URL 參數 `ingredients` (逗號分隔字串，例如 `ingredients=雞肉,洋蔥`)
- **處理邏輯**：將字串拆分為 List，呼叫 `recipe.search_recipes_by_ingredients(list)`
- **輸出**：渲染 `index.html`，傳入 `recipes` 與 `combo_ingredients`
- **錯誤處理**：若未提供 `ingredients`，則重導回 `/`

---

### 會員機制 (Auth Blueprint)

#### `GET, POST /auth/register`
- **輸入**：表單欄位 `username`, `email`, `password`, `confirm_password`
- **處理邏輯**：檢查兩次密碼是否相符、信箱是否重複，將密碼 hash 後呼叫 `user.create_user()`
- **輸出**：註冊成功則重導向至 `/auth/login`；失敗則帶錯誤訊息重新渲染 `auth/register.html`

#### `GET, POST /auth/login`
- **輸入**：表單欄位 `email`, `password`
- **處理邏輯**：呼叫 `user.get_user_by_email()`，並核對 hash 密碼。成功則將 `user_id` 存入 Session
- **輸出**：登入成功重導向至 `/`；失敗則帶錯誤訊息重新渲染 `auth/login.html`

#### `GET /auth/logout`
- **輸入**：無
- **處理邏輯**：清除 Session 內的 `user_id`
- **輸出**：重導向至 `/`

---

### 食譜維護 (Recipe Blueprint)

> **注意**：除查看單筆外，其餘操作皆須登入（檢查 Session）。

#### `GET /recipe/<int:id>`
- **輸入**：URL Path 參數 `id`
- **處理邏輯**：呼叫 `recipe.get_recipe_by_id(id)`。若為私人食譜，需檢查當前 Session 使用者是否為擁有者。
- **輸出**：渲染 `recipe/detail.html`
- **錯誤處理**：若找不到或無權限，回傳 404 或 403 畫面。

#### `GET /recipe/my-recipes`
- **輸入**：Session 內的 `user_id`
- **處理邏輯**：呼叫 `recipe.get_recipes_by_user(user_id)`
- **輸出**：渲染 `recipe/my_recipes.html`

#### `GET, POST /recipe/new`
- **輸入**：表單欄位 `title`, `ingredients`, `steps`, `image_url`, `category`, `is_public`
- **處理邏輯**：接收表單後，驗證必填，呼叫 `recipe.create_recipe()`
- **輸出**：成功後重導向至 `/recipe/my-recipes` 或單筆食譜頁；失敗則回傳 `recipe/form.html`

#### `GET, POST /recipe/<int:id>/edit`
- **輸入**：URL Path 參數 `id`，表單欄位同上
- **處理邏輯**：檢查是否為擁有者，接收表單並呼叫 `recipe.update_recipe()`
- **輸出**：成功後重導向至 `/recipe/<id>`；失敗回傳 `recipe/form.html`

#### `POST /recipe/<int:id>/delete`
- **輸入**：URL Path 參數 `id`
- **處理邏輯**：檢查是否為擁有者或管理員，呼叫 `recipe.delete_recipe()`
- **輸出**：成功後重導向至 `/recipe/my-recipes`

---

## 3. Jinja2 模板清單

所有的 HTML 檔案應放置於 `app/templates/` 目錄下：

- `base.html`: 網站共用的母版，包含 Navbar、Footer 與共用 CSS/JS 引用。
- `index.html`: 首頁與搜尋結果頁（繼承 `base.html`）。
- `auth/`
  - `login.html`: 登入表單頁面（繼承 `base.html`）。
  - `register.html`: 註冊表單頁面（繼承 `base.html`）。
- `recipe/`
  - `my_recipes.html`: 個人食譜管理面板（繼承 `base.html`）。
  - `detail.html`: 單筆食譜詳細內容頁（繼承 `base.html`）。
  - `form.html`: 新增與編輯食譜共用表單（繼承 `base.html`）。
