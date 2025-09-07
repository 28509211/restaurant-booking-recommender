<?php
$host = getenv('DB_HOST');
$user = getenv('DB_USER');
$pass = getenv('DB_PASSWORD');
$dbnm = getenv('DB_NAME');
$port = (int)getenv('DB_PORT');


$conn = new mysqli($host, $user, $pass, $dbnm, $port);

// 檢查連接
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 設置字符編碼為 UTF-8
$conn->set_charset("utf8");

$sql = "SELECT product_id, store_id, product_name, description, price FROM store_products";
$result = $conn->query($sql);

$menuItems = array();
if ($result->num_rows > 0) {
    // 輸出數據
    while($row = $result->fetch_assoc()) {
        $menuItems[] = $row;
    }
} else {
    echo "0 results";
}
$conn->close();

header('Content-Type: application/json; charset=UTF-8');
echo json_encode($menuItems, JSON_UNESCAPED_UNICODE);
?>
