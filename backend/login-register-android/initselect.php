<?php
// 連接MYSQL
$con = mysqli_connect("x", "x", "x", "x", x);

// 檢查連接是否成功
if (!$con) {
    // 如果連接失敗，輸出錯誤消息並退出腳本
    die("資料庫連接失敗：" . mysqli_connect_error());
}

// 是否收到了來自 POST 請求的 initselect 和 client_id
if (isset($_POST['initselect']) && isset($_POST['client_id'])) {
    // 獲取來自 POST 請求的 initselect 和 client_id
    $initselect = $_POST['initselect'];
    $client_id = $_POST['client_id'];

    // 檢查該用戶是否已經存在偏好設置
    $check_sql = "SELECT * FROM preferences_table WHERE client_id = '$client_id'";
    $result = mysqli_query($con, $check_sql);

    if (mysqli_num_rows($result) > 0) {
        // 如果已經存在，則進行更新
        $update_sql = "UPDATE preferences_table SET initselect = '$initselect' WHERE client_id = '$client_id'";
        if (mysqli_query($con, $update_sql)) {
            echo "偏好設置已更新";
        } else {
            echo "更新錯誤：" . $update_sql . "<br>" . mysqli_error($con);
        }
    } else {
        // 如果不存在，則插入新的記錄
        $insert_sql = "INSERT INTO preferences_table (initselect, client_id) VALUES ('$initselect', '$client_id')";
        if (mysqli_query($con, $insert_sql)) {
            echo "偏好設置已保存";
        } else {
            echo "插入錯誤：" . $insert_sql . "<br>" . mysqli_error($con);
        }
    }
} else {
    // 如果未收到 initselect 或 client_id 參數，返回錯誤消息
    echo "未收到必需參數";
}

// 關閉資料庫
mysqli_close($con);
?>
