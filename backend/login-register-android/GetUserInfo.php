<?php
header('Content-Type: application/json');
$response = array();

if (!empty($_POST['userId'])) {
    $userId = $_POST['userId'];

    $con = new mysqli("x", "x", "x", "x", x);

    if ($con->connect_error) {
        $response['status'] = 'error';
        $response['message'] = 'Database connection failed: ' . $con->connect_error;
    } else {
        // 使用 JOIN 语句来联结两个表并获取数据
        $stmt = $con->prepare("SELECT c.username, c.email, c.address, c.PhoneNumber, p.initselect AS preferences 
                               FROM clientable c 
                               LEFT JOIN preferences_table p ON c.id = p.client_id 
                               WHERE c.id = ?");
        $stmt->bind_param("i", $userId);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows != 0) {
            $userInfo = $result->fetch_assoc();
            $response = array_merge(array('status' => 'success'), $userInfo);
        } else {
            $response['status'] = 'error';
            $response['message'] = 'User not found';
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
