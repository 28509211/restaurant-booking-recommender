<?php
// 添加日志记录以调试 POST 数据
file_put_contents('php://stderr', print_r($_POST, TRUE));

// 确认所有字段是否已接收到
if (!empty($_POST['username']) && !empty($_POST['passward']) && !empty($_POST['email']) && !empty($_POST['address']) && !empty($_POST['Phonenumber']) && !empty($_POST['gender'])) {

    $con = mysqli_connect("x", "x", "x", "x", x);
    if ($con) {
        $username = $_POST['username'];
        $email = $_POST['email'];
        $address = $_POST['address'];
        $phone_number = $_POST['Phonenumber'];
        $password = password_hash($_POST['passward'], PASSWORD_DEFAULT);
        $gender = $_POST['gender'];

        // 添加调试信息
        error_log("username: " . $username);
        error_log("passward: " . $password);
        error_log("email: " . $email);
        error_log("address: " . $address);
        error_log("Phonenumber: " . $phone_number);

        // 确保字段名与数据库表结构一致
        $sql = "INSERT INTO clientable (username, passward, email, address, Phonenumber, gender) VALUES ('$username', '$password', '$email', '$address', '$phone_number', '$gender' )";
        if (mysqli_query($con, $sql)) {
            echo "success";
        } else {
            echo "Registration failed: " . mysqli_error($con);
        }
    } else {
        echo "Database connection failed: " . mysqli_connect_error();
    }
} else {
    // 添加日志记录未接收到的字段
    if (empty($_POST['username'])) error_log("Missing username");
    if (empty($_POST['passward'])) error_log("Missing passward");
    if (empty($_POST['email'])) error_log("Missing email");
    if (empty($_POST['address'])) error_log("Missing address");
    if (empty($_POST['PhoneNumber'])) error_log("Missing PhoneNumber");
    if (empty($_POST['gender'])) error_log("Missing gender");
    echo "All fields are required";
}
?>
