<?php
$servername = "x";
$username = "x";
$password = "x";
$dbname = "x";
$port = x;

// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname, $port);

// 检查连接
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 获取用户位置，提供默认值
$default_lat = 24.95804413404514;
$default_lng = 121.24075494232851;

$user_lat = isset($_GET['lat']) ? $_GET['lat'] : $default_lat;
$user_lng = isset($_GET['lng']) ? $_GET['lng'] : $default_lng;

// 查询所有店家
$sql = "SELECT si.store_id, si.store_name, si.address, si.phone, si.latitude, si.longitude, su.url,
        ( 6371 * acos( cos( radians(?) ) * cos( radians( si.latitude ) ) 
        * cos( radians( si.longitude ) - radians(?) ) + sin( radians(?) ) 
        * sin( radians( si.latitude ) ) ) ) AS distance 
        FROM storeinfo_table si
        LEFT JOIN store_urls su ON si.store_id = su.store_id
        HAVING distance < 1000 
        ORDER BY distance 
        LIMIT 0 , 1000";

$stmt = $conn->prepare($sql);
$stmt->bind_param("ddd", $user_lat, $user_lng, $user_lat);
$stmt->execute();
$result = $stmt->get_result();

$stores = array();

if ($result->num_rows > 0) {
    // 输出数据
    while($row = $result->fetch_assoc()) {
        $stores[] = $row;
    }
} else {
    echo json_encode([]);
    exit;
}
$stmt->close();
$conn->close();

// 返回JSON格式的数据
header('Content-Type: application/json; charset=utf-8');
echo json_encode($stores, JSON_UNESCAPED_UNICODE);
?>
