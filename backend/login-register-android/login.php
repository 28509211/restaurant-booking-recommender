<?php
session_start();

// 驗證是否收到 email 和 password
if (empty($_POST['email']) || empty($_POST['passward'])) {
    echo json_encode([
        "status" => "failed",
        "message" => "Both email and password are required!"
    ], JSON_PRETTY_PRINT);
    exit;
}

// 獲取 POST 資料
$email = $_POST['email'];
$password = $_POST['passward'];

// 初始化回應陣列
$results = array();

// 連接到 MySQL 資料庫
$con = mysqli_connect("localhost", "tim", "11027102", "clientdatabase", 3307);

if (!$con) {
    echo json_encode([
        "status" => "failed",
        "message" => "Database connection failed!"
    ], JSON_PRETTY_PRINT);
    exit;
}

// 使用 Prepared Statements 防止 SQL 注入
$sql = "SELECT id, username, email, passward, gender FROM clientable WHERE email = ?";
$stmt = $con->prepare($sql);
$stmt->bind_param("s", $email);
$stmt->execute();
$res = $stmt->get_result();

if ($res->num_rows > 0) {
    $row = $res->fetch_assoc();

    // 驗證密碼
    if (password_verify($password, $row['passward'])) { // 修正欄位名稱為 passward
        // 生成 API Key
        try {
            $apiKey = bin2hex(random_bytes(23));
        } catch (Exception $e) {
            $apiKey = bin2hex(uniqid($email, true));
        }

        // 更新 API Key 到資料庫
        $updateSql = "UPDATE clientable SET apiKey = ? WHERE email = ?";
        $updateStmt = $con->prepare($updateSql);
        $updateStmt->bind_param("ss", $apiKey, $email);

        if ($updateStmt->execute()) {
            // 成功登入並返回用戶資料
            $results["status"] = "success";
            $results["message"] = "Login successful!";
            $results["username"] = $row["username"];
            $results["gender"] = $row["gender"];
            $results["email"] = $row["email"];
            $results["id"] = $row["id"];
            $results["apiKey"] = $apiKey;
        } else {
            $results["status"] = "failed";
            $results["message"] = "Failed to update API key, try again!";
        }
    } else {
        $results["status"] = "failed";
        $results["message"] = "Invalid email or password!";
    }
} else {
    $results["status"] = "failed";
    $results["message"] = "User not found!";
}

// 關閉連接
$stmt->close();
$con->close();

// 返回 JSON 回應
echo json_encode($results, JSON_PRETTY_PRINT);
?>
