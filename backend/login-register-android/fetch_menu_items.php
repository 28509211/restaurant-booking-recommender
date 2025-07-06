<?php
$servername = "x";
$username = "x";
$password = "x";
$dbname = "x";
$port = x;

// 創建連接
$conn = new mysqli($servername, $username, $password, $dbname, $port);

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
