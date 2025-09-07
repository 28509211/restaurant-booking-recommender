<?php
header('Content-Type: application/json; charset=utf-8');
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT); // 讓 SQL 錯誤直接丟出

$host = getenv('DB_HOST');
$user = getenv('DB_USER');
$pass = getenv('DB_PASSWORD');
$dbnm = getenv('DB_NAME');
$port = (int)getenv('DB_PORT');


$conn = new mysqli($host, $user, $pass, $dbnm, $port);

$conn->set_charset("utf8mb4");

if ($conn->connect_error) {
    die(json_encode(['error' => 'Connection failed: ' . $conn->connect_error]));
}

$limit = isset($_GET['limit']) ? intval($_GET['limit']) : 50;
$offset = isset($_GET['offset']) ? intval($_GET['offset']) : 0;
$category = isset($_GET['category']) ? $_GET['category'] : null;

if ($category) {
    // If category parameter is present, return all stores in that category
    $stmt = $conn->prepare("SELECT * FROM storeinfo_table WHERE category = ? LIMIT ? OFFSET ?");
    $stmt->bind_param("sii", $category, $limit, $offset);
} else {
    // If no category parameter, return all distinct categories
    $stmt = $conn->prepare("SELECT DISTINCT category FROM storeinfo_table LIMIT ? OFFSET ?");
    $stmt->bind_param("ii", $limit, $offset);
}

$stmt->execute();
$result = $stmt->get_result();

$data = array();

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
}

echo json_encode($data, JSON_UNESCAPED_UNICODE);

$stmt->close();
$conn->close();
?>
