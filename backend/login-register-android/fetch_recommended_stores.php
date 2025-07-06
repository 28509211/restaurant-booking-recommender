<?php
header('Content-Type: application/json');

$servername = "x";
$username = "x";
$password = "x";
$dbname = "x";
$port = x;

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname, $port);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if client_id is set
if (!isset($_GET['client_id'])) {
    echo json_encode(array("error" => "client_id is required"));
    exit();
}

// Get client_id from request
$client_id = $_GET['client_id'];

// SQL query to fetch recommended stores
$sql = "SELECT s.store_id, s.store_name, s.category, s.address, s.ratings, s.service, s.url 
        FROM recommended_stores rs 
        JOIN storeinfo_table s ON rs.store_id = s.store_id 
        WHERE rs.client_id = ?";

// Prepare and execute statement
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $client_id);
$stmt->execute();
$result = $stmt->get_result();

// Fetch data and store in array
$stores = array();
while ($row = $result->fetch_assoc()) {
    $stores[] = $row;
}

// Output JSON data
echo json_encode($stores, JSON_PRETTY_PRINT);

// Close statement and connection
$stmt->close();
$conn->close();
?>
