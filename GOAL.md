設計一個簡約又專業的半導體設備公司網站：
中文公司：倍特爾科技集團有限公司
英文公司：BETTER SCIENCE TECHNOLOGY GROUP co., LIMITED
公司地址：香港九龙佐敦道5号智秀商业大厦10楼
公司負責人： 蘇益宏 （Kerwin)
公司郵箱： kerwin@bettertechgroup.com
公司主要業務經營方向： 
先進半導體9大主製程設備採購，拆裝機及運送服務，先進製程技術導入，先進半導體人材培訓，AI搭配先進製造設備技術的結合及應用
1 . 黃光段設備的銷售及維護：主要是先進製造技術能力日系主力日系品牌NIKON全系列曝光機產品及CANON全系列曝光機包含奈米壓印產品及TEL品牌及DNS品牌旋塗及顯影設備為主⋯⋯
2 . 蝕刻段設備的銷售及維護：主要是先進製造技術能力日系品牌TEL及SAMCO半導體設備商主⋯⋯
3 . 化學氣相設備的銷售及維護：主要是先進製造技術能力日系品牌KE及MATSUSHITA半導體設備商為主
4 . 烘烤製程設備的銷售及維護：主要是先進製造技術能力日系品牌KE及TAZMO兩大設備商為主
5 . 離子植入設備的銷售及維護 ： 主要是先進製造技術能力日系品牌ULVAC及NISSIN兩大設備商為主
6 . CMP研磨製程設備的銷售及維護 ： 主要是先進製造技術能力日系品牌EBARA及ACCRETECH兩大設備商為主
7 . 晶圓水洗製程設備的銷售及維護 ： 主要是先進製造技術能力日系品牌DNS及TEL兩大設備商為主
8 . 晶圓檢測製程設備的銷售及維護 ： 主要是先進製造技術能力日系品牌ADVANTEST及LASERTECHNIK 兩大設備商為主
9 . 掩模版製程設備的銷售及維護 ： 主要是先進製造技術能力日系品牌NUFLARE及JEOL兩大設備商為主
10. 各頁面需要的照片，圖片，影片，分別提供圖片與影片的生成提示詞，另外存成 markdown 格式。
11 . 強調以上各大工藝設備皆整合最前沿的人工智能應用，領先業界。從以下核心架構挑選對標工藝設備代入，包含數字孿生，物理仿真，LithoDreamer, ILT等:
| 領域         | 代表模型（年份）            | 核心架構                          | 輸入數據特徵                           | 輸出／評估指標                              | 關鍵量化結果                          |
| ---------- | ------------------- | ----------------------------- | -------------------------------- | ------------------------------------ | ------------------------------- |
| 晶圓圖缺陷分類    | G2LGAN＋CNN（2025）    | 兩階段 GAN 增強＋MobileNetV2        | 晶圓圖影像（類別不平衡資料）                   | Accuracy／F1／1-NN（生成品質）               | Acc 98.39%、F1 93.01%            |
| 晶圓圖缺陷分類    | CNN-ESN（2026）       | ResNet34＋回聲狀態網路               | 含雜訊晶圓圖                           | Acc（含 σ=0.1 雜訊穩健性）                   | 乾淨 94.74%、雜訊 87.30%             |
| SEM 缺陷分類   | IBM ASMC（2025）      | ViT（DINOv2）＋半監督               | SEM 影像（每類<15 張）                  | 分類準確率                                | >90%（少樣本）                       |
| 良率預測       | PDF Exensio（2025）   | XGBoost＋PCA                   | 線上缺陷、計量、電測、FDC                   | die/wafer pass-fail、precision/recall | 可調閾值平衡 overkill/underkill       |
| 良率根因       | TSMC 智慧製造           | RNN（時序 FDC）＋聯邦學習              | 設備感測器時序、檢測資料                     | 良率影響缺陷預測準確率                          | ~92%（28–3nm）、逃逸率-15%            |
| 熱模擬代理      | DeepOHeat-v1（2025）  | DeepONet＋KAN＋GMRES 細化         | 功耗圖／floorplan（物理資訊訓練，無需模擬資料）     | MAPE、訓練時間、記憶體                        | MAPE 0.035%、訓練-62×、記憶體-31×      |
| 熱-IR 聯合    | ThermEDGe/IREDGe    | Encoder-Decoder CNN           | 時變功耗圖、PDN 密度                     | IR 誤差（mV）、溫度輪廓                       | 平均 IR 誤差 0.053mV                |
| 2.5D 電熱協同  | TTSV-HMO（2025）      | 等效模型＋混合元啟發式（PSO+SA）           | TTSV 間距、chiplet 位置、功耗密度          | 溫度/阻抗 MAE、fitness                    | 溫度 MAE 0.35%、阻抗 3.97%           |
| 靜態 IR Drop | MaxViT/U-Net（2026）  | MaxViT 編碼＋U-Net/FPN 解碼        | 電阻圖、電流圖、電源焊墊圖（SPICE 轉影像）         | MAE、F1（>90% 峰值熱點）、推論時間               | MAE<15×10⁻⁵V、較 NGSPICE 快 10–30× |
| 靜態 IR Drop | ICCAD'23 冠軍流        | ConvNeXtV2-Nano＋UPerNet       | 各金屬層電阻圖＋有效距離圖                    | MAE（mV）、F1                           | MAE 0.075mV、F1 0.56             |
| 動態 IR Drop | PDNNet（2024）        | GNN（PDNGraph）＋CNN 異構          | PDN 結構圖＋動態電流圖                    | NMAE、加速比                             | NMAE 改善 39.3%、545× 加速           |
| 動態 IR Drop | 雙路徑時空模型（DATE'25）    | 3D SW-MSA Transformer         | 時序窗分解功耗圖（內部/開關/漏電/翻轉率）           | 熱點預測精度                               | 超越 2D/3D-CNN 與遞迴 U-Net          |
| 電遷移        | Dey et al.（2020）    | 10 層 NN 迴歸＋邏輯迴歸分類             | J、L、T、IR Drop、MTTF 標註（KLU＋Black） | R²、AMSE、失效段偵測                        | 顯著加速、MTTF 可比精確模型                |
| 電遷移        | BPINN-EM-Post（2025） | 貝氏 PINN                       | Korhonen PDE 物理殘差＋觀測             | 不確定性量化、壽命分佈                          | 克服 PINN 過擬合、支援多線段               |
| ATPG       | InF-ATPG（2025）      | FFR 劃分＋QGNN＋DQN               | 邏輯狀態、SCOAP 可控/可觀測性               | 回溯數、故障覆蓋率、UFP                        | 回溯-55.06%、UFP 0.50%             |
| ATPG（商用）   | Synopsys TSO.ai     | AI 設定調優（黑盒優化）                 | 設計特性、ATPG 引擎行為、約束                | 圖樣數、覆蓋率、收斂迭代                         | 圖樣-20~25%（部分>50%）               |
| BIST 強化    | LITE（2025）          | 標準單元掃描增強＋SCOAP 分析             | 網表超圖、CC0/CC1/CObs                | 圖樣數、隨機圖樣覆蓋率                          | ATPG 圖樣-31%、改善 RPR 覆蓋           |
| KGD/離群偵測   | GPR/RevTransC/共形預測  | GPR 空間建模、無監督轉換、共形 QR＋CatBoost | 晶圓級參數測試資料、WAT                    | AUROC、DPPM、Vmin 區間覆蓋率                | 優於 DPAT；Vmin ~90% 覆蓋保證          |
| 測試時間       | GPU 即時適應性測試         | GPU 加速 ML（產線部署）               | 即時測試資料流                          | 測試時間、缺陷覆蓋維持                          | Blackwell 量產：-25% 測試時間          |
| 佈局熱點       | 可解釋 GAT（ASP-DAC'26） | 圖注意力網路（8 頭）                   | 佈局圖（節點特徵 5 維、鄰接矩陣）               | Recall、誤報率、可解釋性                      | 記憶體較影像法省 5–12×                  |
| e-Beam 複審  | SEMVision H20（2025） | 深度學習影像分類（產線持續訓練）              | CFE e-beam 影像                    | 複審速度、真/假缺陷區分                         | 3× 速度、已導入 2nm/GAA 客戶            |
