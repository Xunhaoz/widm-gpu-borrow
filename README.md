# 😎 中央大學 張嘉惠教授實驗室 GPU登記系統 😎

這是一個登記系統可以看到每個禮拜實驗室中GPU使用登記狀況分析及當前使用量。

## Demo

### 首頁

![index.png](images%2Findex.png)

### 登入

![login.png](images%2Flogin.png)

### 申請借用

![apply_form.png](images%2Fapply_form.png)

### 使用狀況

![weekly_dashboard.png](images%2Fweekly_dashboard.png)

## 安裝指南

### 快速開始

1. 前往 ncu protal 申請開發成員
2. 填寫 config.json 中的內容
3. docker compose up
   ```
   docker-compose up
   ```

### 開發開始

1. 安裝 Python 3.10
2. 使用以下指令安裝所需套件
   ```
   pip install -r requirements.txt
   ```
3. 執行程式
   ```
   python app.py
   ```

## 聯絡方式

若有任何問題或建議，歡迎聯絡：

- 電子郵件：leo20020529@gmail.com