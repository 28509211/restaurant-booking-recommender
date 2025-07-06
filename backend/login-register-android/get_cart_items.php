<?php
$servername = "x";
$username = "x";
$password = "x";
$dbname = "x";
$port = x;

$conn = new mysqli($servername, $username, $password, $dbname, $port);

// 檢查連接
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$user_id = $_GET['user_id'];

// 獲取購物車中的項目
$sql = "SELECT sp.product_name, ci.quantity, sp.price FROM cartitem ci 
        JOIN store_products sp ON ci.product_id = sp.product_id 
        JOIN cart c ON ci.cart_id = c.cart_id 
        WHERE c.user_id = ? AND c.status = 'pending' AND ci.status = 'active'";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();

$cartItems = array();
while ($row = $result->fetch_assoc()) {
    $cartItems[] = $row;
}

$stmt->close();
$conn->close();

header('Content-Type: application/json');
echo json_encode($cartItems);
?>
