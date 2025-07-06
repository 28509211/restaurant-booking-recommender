<?php
$servername = "x";
$username = "x";
$password = "x";
$dbname = "x";
$port = x; // 根據您的數據庫配置設置端口

$conn = new mysqli($servername, $username, $password, $dbname, $port);

// 檢查連接
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 獲取請求中的數據
$user_id = $_POST['user_id'];
$product_id = $_POST['product_id'];
$quantity = isset($_POST['quantity']) ? $_POST['quantity'] : 1; // 默認數量為1

// 檢查是否有未提交的購物車
$sql = "SELECT cart_id FROM cart WHERE user_id = ? AND status = 'pending'";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $user_id);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows > 0) {
    // 如果有未提交的購物車，取得他的cart_id
    $stmt->bind_result($cart_id);
    $stmt->fetch();
} else {
    // 如果不存在未提交的購物車就創建一個新的購物車
    $sql = "INSERT INTO cart (user_id, status) VALUES (?, 'pending')";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $user_id);
    $stmt->execute();
    $cart_id = $stmt->insert_id;
}

// 檢查是否已經存在相同的商品在購物車中
$sql = "SELECT quantity FROM cartitem WHERE cart_id = ? AND product_id = ? AND status = 'active'";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ii", $cart_id, $product_id);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows > 0) {
    // 如果存在就更新數量
    $stmt->bind_result($existing_quantity);
    $stmt->fetch();
    $new_quantity = $existing_quantity + $quantity;

    $sql = "UPDATE cartitem SET quantity = ? WHERE cart_id = ? AND product_id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("iii", $new_quantity, $cart_id, $product_id);
} else {
    // 如果不存在，插入新的項目
    $sql = "INSERT INTO cartitem (cart_id, user_id, product_id, quantity, status) VALUES (?, ?, ?, ?, 'active')";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("iiii", $cart_id, $user_id, $product_id, $quantity);
}

if ($stmt->execute()) {
    echo json_encode(["status" => "success", "message" => "Item added to cart"]);
} else {
    echo json_encode(["status" => "error", "message" => "Failed to add item to cart"]);
}

$stmt->close();
$conn->close();
?>
