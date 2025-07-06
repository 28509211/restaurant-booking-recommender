<?php
session_start(); // 開啟會話

header('Content-Type: application/json');

$response = array();

if (!empty($_POST['userId'])) {
    $userId = $_POST['userId'];

    // ex. localhost user 123 clientdatabase 3306
    $con = new mysqli("x", "x", "x", "x", "x");

    if ($con->connect_error) {
        $response['status'] = 'error';
        $response['message'] = 'Database connection failed: ' . $con->connect_error;
    } else {
        // 使用預備語句來防止SQL注入
        $stmt = $con->prepare("SELECT * FROM clientable WHERE id = ?");
        $stmt->bind_param("i", $userId);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows != 0) {
            $stmtUpdate = $con->prepare("UPDATE clientable SET apiKey = '' WHERE id = ?");
            $stmtUpdate->bind_param("i", $userId);

            if ($stmtUpdate->execute()) {
                // 銷毀會話
                session_destroy();

                $response['status'] = 'success';
                $response['message'] = 'Logout successful';
            } else {
                $response['status'] = 'error';
                $response['message'] = 'Logout failed';
            }

            $stmtUpdate->close();
        } else {
            $response['status'] = 'error';
            $response['message'] = 'Unauthorized to access';
        }

        $stmt->close();
    }

    $con->close();
} else {
    $response['status'] = 'error';
    $response['message'] = 'User ID is required';
}

echo json_encode($response);
?>
