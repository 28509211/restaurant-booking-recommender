<?php
header('Content-Type: application/json; charset=utf-8');

// 連接到 MySQL 資料庫
$host = getenv('DB_HOST');
$user = getenv('DB_USER');
$pass = getenv('DB_PASSWORD');
$dbnm = getenv('DB_NAME');
$port = (int)getenv('DB_PORT');


$conn = new mysqli($host, $user, $pass, $dbnm, $port);


if ($conn->connect_error) {
    die(json_encode(['error' => 'Connection failed: ' . $conn->connect_error]));
}


$conn->set_charset("utf8");


$limit = isset($_GET['limit']) ? intval($_GET['limit']) : 50;
$offset = isset($_GET['offset']) ? intval($_GET['offset']) : 0;

$sql = "SELECT store_id, store_name, category, address, ratings, service FROM storeinfo_table LIMIT $limit OFFSET $offset";
$result = $conn->query($sql);

$stores = array();

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $store_id = $row['store_id'];
        
        $hours_sql = "SELECT day_of_week, open_time_1, close_time_1, open_time_2, close_time_2 FROM openhours WHERE store_id = $store_id";
        $hours_result = $conn->query($hours_sql);
        $store_hours = array();
        
        if ($hours_result->num_rows > 0) {
            while ($hours_row = $hours_result->fetch_assoc()) {
                $store_hours[] = $hours_row;
            }
        }

        // 查询店铺URL
        $url_sql = "SELECT url FROM store_urls WHERE store_id = $store_id";
        $url_result = $conn->query($url_sql);
        $url = '';
        if ($url_result->num_rows > 0) {
            $url_row = $url_result->fetch_assoc();
            $url = $url_row['url'] ?: '';
        }

        $row['store_hours'] = $store_hours;
        $row['store_url'] = $url;
        $stores[] = $row;
    }
}

echo json_encode($stores, JSON_UNESCAPED_UNICODE);

$conn->close();
?>
