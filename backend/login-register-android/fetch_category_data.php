<?php
$servername = "localhost";
$username = "x";
$password = "x";
$dbname = "x";
$port = x;

$conn = new mysqli($servername, $username, $password, $dbname, $port);

$conn->set_charset("utf8");

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
