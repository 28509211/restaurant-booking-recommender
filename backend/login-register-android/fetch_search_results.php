<?php
$servername = "x";
$username = "x";
$password = "x";
$dbname = "x";
$port = x;

$conn = new mysqli($servername, $username, $password, $dbname, $port ); // 建立到資料庫的連接

$conn->set_charset("utf8"); // 設置資料庫連接的字符集為 UTF-8

if ($conn->connect_error) { // 檢查連接是否成功
    die(json_encode(['error' => 'Connection failed: ' . $conn->connect_error])); // 如果連接失敗，返回錯誤信息
}

$query = isset($_GET['query']) ? $conn->real_escape_string($_GET['query']) : ''; // 從請求中獲取搜索字串，並對其進行轉義處理


// 主查詢：從 storeinfo_table 和 store_urls 表聯合查詢店家信息及圖片 URL
$sql = "SELECT storeinfo_table.*, store_urls.url AS store_url 
        FROM storeinfo_table 
        LEFT JOIN store_urls ON storeinfo_table.store_id = store_urls.store_id 
        WHERE storeinfo_table.store_name LIKE '%$query%'";
$result = $conn->query($sql); // 執行查詢

$stores = array(); // 初始化結果集合

if ($result->num_rows > 0) { // 如果查詢到店家數據
    while ($row = $result->fetch_assoc()) { // 遍歷每個店家
        $storeId = $row['store_id']; // 獲取店家的 store_id

        // 子查詢：從 store_hours_table 查詢對應店家的營業時間
        $hoursSql = "SELECT day_of_week, open_time_1, open_time_2, close_time_1, close_time_2 
                     FROM openhours
                     WHERE store_id = $storeId"; // 查詢對應店家的營業時間
        $hoursResult = $conn->query($hoursSql); // 執行查詢

        $storeHours = array(); // 初始化營業時間集合
        if ($hoursResult->num_rows > 0) { // 如果查詢到營業時間數據
            while ($hoursRow = $hoursResult->fetch_assoc()) { // 遍歷每個營業時間記錄
                $storeHours[] = $hoursRow; // 將營業時間記錄添加到集合中
            }
        }

        // 將 store_hours 加入到店家數據中
        $row['store_hours'] = $storeHours; // 將營業時間數據添加到店家信息中
        $stores[] = $row; // 將完整的店家信息添加到結果集合中
    }
}

echo json_encode($stores, JSON_UNESCAPED_UNICODE); // 將結果集合編碼為 JSON 並返回

$conn->close(); // 關閉資料庫連接
?>





