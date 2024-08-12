<?php

$inputs = file_get_contents("php://input");


$VIDEO_DB = "videos.db";
$USERS = "users_db.db";
$ADMIN = "admins.db";
$CH = "channels.db";


$data = json_decode($inputs,true);

$BOT_TOKEN = "7002468912:AAGgj6eHJXQFFO-aPXx3gCJq1pZm3dYU_io"; 

$URL = "https://api.telegram.org/bot" . $BOT_TOKEN;

//webhook
//https://api.telegram.org/bot7002468912:AAGgj6eHJXQFFO-aPXx3gCJq1pZm3dYU_io/setWebhook?url=https://screamfamily.ir/PleasurePal_bot/PleasurePal_bot.php

$CHAT_ID = "983588626";
$a1 ="ارسال برای همه";
$a2 ="تعداد کاربران";
$a3 ="قفل کانال جدید";
$a4 ="حذف کانال";
$a5 ="کانال های قفل شده";

$b = "بازگشت";
$b_set = [
    [$b]
];
$bk =[
    'keyboard' => $b_set,
    'resize_keyboard' => true,
    'one_time_keyboard' => false
];

$a_kb_set = [
    [$a1],
    [$a2],
    [$a5],
    [$a3],
    [$a4],
];
$akb = [
    'keyboard' => $a_kb_set,
    'resize_keyboard' => true,
    'one_time_keyboard' => false
];
$verify = "تایید";
$v_set = [
    [$verify],
    [$b]
];
$vkb = [
    'keyboard' => $v_set,
    'resize_keyboard' => true,
    'one_time_keyboard' => false
];

if(isset($data['message'])){
    $chat_id = $data['message']['chat']['id'];
    $username = $data['message']['chat']['username'];
    $text = $data['message']['text'];
    if(is_admin($chat_id)){
        $status = status();
        if($status == ""){
            switch($text){
                case $a1: send_all("0",$text);break;
                case $a2: get_users_count($text);break;
                case $a3: add_channell("0",$text);break;
                case $a5: get_all_channels();break;
                case $a4: delete_channel("0",$text);break;
                default:admin_pannel();
            }
        }else{
            $s = explode(" ",$status);
            $status = $s[0];
            $part = $s[1];
            switch($status){
                case "send_all":send_all($part,$text);break;
                case "add_channel":add_channell($part,$text);break;
                case "delete_channel":delete_channel($part,$text);break;
                default:admin_pannel();
            }
        }
    }else{

        add_user($chat_id,$username);
        if(user_joined()){

            if($text[0] == "/" && explode(" ",$text) > 1){
                
                $vid = substr(explode(" ",$text)[1],3);
                $vid = explode("-",$vid);
                $id = $vid[1];
                $vid = get_vide($id);
                if($vid){
                    $res = send_video($vid['file_id']);
                    $res = json_decode($res,true);
                    sleep(10);
                    $res = delete_message($res['result']['message_id']);
                    send_message("😉");
            }
        }else{
            send_message("فعلا فعالیتی در دسترس نیست");
        }
    }else{

    }
    }
}else if(isset($data['channel_post'])){
    if(isset($data['channel_post']['video'])){
        
        $msg_id = $data['channel_post']['message_id'];
        $file_id = $data['channel_post']['video']['file_id'];
        $file_un_id = $data['channel_post']['video']['file_unique_id'];
        save_video($msg_id,$file_id,$file_un_id);
    }
}
else{
    sa(json_encode($data));
}
function user_joined(){
    $chs = all_channels();
    $cs = [];
    foreach($chs as $c){
        $r = user_in_channel($GLOBALS['chat_id'],"@".$c);
        if(!$r){
            array_push($cs,$c);
        }
    }
    if(count($cs)>0){

        $inlineKeyboard = [];
        
        foreach ($cs as $channel) {
                $inlineKeyboard[] = [
                [
                    'text' => "channel",
                    'url' => "https://t.me/$channel"
                ]
            ];
        }
        $set = [ 'inline_keyboard' => $inlineKeyboard];
        $text = "لطفا ابتدا وارد این کانال ها بشوید سپس مجدد اقدام کنید";
        $url = $GLOBALS['URL']."/sendMessage";
        $kb = json_encode($set);
        $parameters = ['chat_id' => $GLOBALS['chat_id'],'text' => $text,'reply_markup' => $kb];
        $r = send_request($url,$parameters);
        return false;
    }else{
        return true;
    }
}
function channel_kb(){
    $chs = all_channels();
    $set = [];
    foreach($chs as $c){
        array_push($set,[$c]);
    }
    $c_sets = [
        'keyboard' => $set,
        'resize_keyboard' => true,
        'one_time_keyboard' => false
    ];
    saw("کدام کانال حذف شود؟",$c_sets);
}
function delete_channel_1($text){
    set_data($text);
    $text .= "\n\n این کانال حذف شود؟";
    set_status("delete_channel 2");
    sv($text);

}

function delete_channel_2($text){
    if($text == $GLOBALS['verify']){
        $c = data();
        $res = del_channel($c);
        set_status("");
        if($res){
            admin_pannel("غملیات با موفقیت انجام شد");
        }else{
            admin_pannel();
        }
    }else{
        admin_pannel("عملیات لغو شد");
    }
}
function delete_channel($part,$text){
    switch($part){
        case "0":{set_status("delete_channel 1");channel_kb();};break;
        case "1": delete_channel_1($text);break;
        case "2": delete_channel_2($text);break;
    }
}
function get_all_channels(){
    $chs = all_channels();
    if(count($chs)>0){

        $t = "کانال ها :\n";
        foreach($chs as $c){
            $t.= "@".$c."\n";
        }
        set_status("");
        admin_pannel($t);
    }else{
        admin_pannel("فعلا کانالی قفل نشده است");
    }
}
function add_channell($part,$text){
    switch($part){
        case "0":{set_status("add_channel 1");sb("لطفا آیدی کانال را بفرستید ");};break;
        case "1":add_channel_1($text);break;
        case "2":add_channel_2($text);break;
    }
}
function add_channel_1($text){
    set_status("add_channel 2");
    set_data($text);
    sv($text);
}

function add_channel_2($text){
    if($text == $GLOBALS['verify']){
        $ch = data();
        lock_channel($ch);
        set_status("");
        admin_pannel("عملیات با موفقیت انجام شد");
    }else{
        admin_pannel("عملیات با موفقیت لغو شد");
    }
}
function get_users_count($text){
    $d = "تعداد کل کاربران : ";
    $d .= strval(users_count());
    set_status("");
    admin_pannel($d);
}

function send_all($part,$text){
    switch($part){
        case "0": {set_status("send_all 1");sb("چه پیامی برای همه ارسال شود؟");};break;
        case "1": send_all_1($text);break;
        case "2": send_all_2($text);break;
        default:admin_pannel();
    }
    
}

function sb($text){
    $kb = json_encode($GLOBALS['bk']);
    $url = $GLOBALS['URL']."/sendMessage";
    $parameters = ['chat_id' => $GLOBALS['chat_id'],'text' => $text,'reply_markup' => $kb];
    $res = send_request($url,$parameters);
    return $res;

}

function sv($data){
    $kb = json_encode($GLOBALS['vkb']);
    $text = $data."\n\nاین اطاعات را تایید می کنید؟";
    $url = $GLOBALS['URL']."/sendMessage";
    $parameters = ['chat_id' => $GLOBALS['chat_id'],'text' => $text,'reply_markup' => $kb];
    $res = send_request($url,$parameters);
    return $res;
}
function send_all_1($text){
    set_data($text);
    set_status("send_all 2");
    sv($text);
}
function send_all_2($text){
    if($text == $GLOBALS['verify']){
        $data = data();
        send_to_all($data);
        set_status("");
        admin_pannel("پیام با موفقیت برای همه ارسال شد");
    }else{
        admin_pannel("عملیات لغو شد");
    }
}
function admin_pannel($text = "خانه🏚"){
    set_status("");
    $url = $GLOBALS['URL']."/sendMessage";
    $kb = json_encode($GLOBALS['akb']);
    $parameters = ['chat_id' => $GLOBALS['chat_id'],'text' => $text,'reply_markup' => $kb];
    $res = send_request($url,$parameters);
    return $res;
}

function data() {
    try {
        $chatId = $GLOBALS['chat_id'];
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['ADMIN']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Prepare the query to get the status
        $stmt = $db->prepare("SELECT data FROM admins WHERE chat_id = :chat_id");
        $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
        $stmt->execute();
        
        // Fetch the status
        $status = $stmt->fetchColumn();
        
        return $status !== false ? $status : null;
        
    } catch (PDOException $e) {
        // Handle any errors
        echo "Error: " . $e->getMessage();
        return null;
    }
}
function set_data($data) {
    try {
        $chatId = $GLOBALS['chat_id'];
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['ADMIN']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Create table if it does not exist
        $db->exec("CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            chat_id TEXT NOT NULL UNIQUE, 
            status TEXT NOT NULL
        )");
        
        // Check if the record exists
        $stmt = $db->prepare("SELECT COUNT(*) FROM admins WHERE chat_id = :chat_id");
        $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
        $stmt->execute();
        $count = $stmt->fetchColumn();
        
        if ($count > 0) {
            // Update existing record
            $stmt = $db->prepare("UPDATE admins SET data = :data WHERE chat_id = :chat_id");
            $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
            $stmt->bindParam(':data', $data, PDO::PARAM_STR);
            $stmt->execute();
        } else {
            // Insert new record
            $stmt = $db->prepare("INSERT INTO admins (chat_id, data) VALUES (:chat_id, :data)");
            $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
            $stmt->bindParam(':data', $data, PDO::PARAM_STR);
            $stmt->execute();
        }
        
    } catch (PDOException $e) {
        // Handle any errors
        sa("Error: " . $e->getMessage());
    }
}
function status() {
    try {
        $chatId = $GLOBALS['chat_id'];
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['ADMIN']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Prepare the query to get the status
        $stmt = $db->prepare("SELECT status FROM admins WHERE chat_id = :chat_id");
        $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
        $stmt->execute();
        
        // Fetch the status
        $status = $stmt->fetchColumn();
        
        return $status !== false ? $status : null;
        
    } catch (PDOException $e) {
        // Handle any errors
        echo "Error: " . $e->getMessage();
        return null;
    }
}
function set_status($status) {
    try {
        $chatId = $GLOBALS['chat_id'];
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['ADMIN']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Create table if it does not exist
        $db->exec("CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            chat_id TEXT NOT NULL UNIQUE, 
            status TEXT NOT NULL
        )");
        
        // Check if the record exists
        $stmt = $db->prepare("SELECT COUNT(*) FROM admins WHERE chat_id = :chat_id");
        $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
        $stmt->execute();
        $count = $stmt->fetchColumn();
        
        if ($count > 0) {
            // Update existing record
            $stmt = $db->prepare("UPDATE admins SET status = :status WHERE chat_id = :chat_id");
            $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
            $stmt->bindParam(':status', $status, PDO::PARAM_STR);
            $stmt->execute();
            echo "Administrator status updated.";
        } else {
            // Insert new record
            $stmt = $db->prepare("INSERT INTO admins (chat_id, status) VALUES (:chat_id, :status)");
            $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
            $stmt->bindParam(':status', $status, PDO::PARAM_STR);
            $stmt->execute();
            echo "Administrator status added.";
        }
        
    } catch (PDOException $e) {
        // Handle any errors
        echo "Error: " . $e->getMessage();
    }
}
function add_admin($chatId) {
    try {
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['ADMIN']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Create table if it does not exist
        $db->exec("CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            chat_id TEXT NOT NULL UNIQUE, 
            status TEXT,
            data TEXT
        )");
        
        // Check if the record exists
        $stmt = $db->prepare("SELECT COUNT(*) FROM admins WHERE chat_id = :chat_id");
        $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
        $stmt->execute();
        $count = $stmt->fetchColumn();
        
        if($count == 0) {
            $stmt = $db->prepare("INSERT INTO admins (chat_id, status,data) VALUES (:chat_id, '','')");
            $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
            $stmt->execute();
            sa("Administrator record added.");
        }else{
            sa("Admin exist");
        }
        
    } catch (PDOException $e) {
        // Handle any errors
        sa("Error: " . $e->getMessage());
    }
}
function is_admin($chatId) {
    try {
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['ADMIN']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Prepare the query to check for existence
        $stmt = $db->prepare("SELECT COUNT(*) FROM admins WHERE chat_id = :chat_id");
        $stmt->bindParam(':chat_id', $chatId, PDO::PARAM_STR);
        $stmt->execute();
        
        // Fetch the count
        $count = $stmt->fetchColumn();

        // Return true if count is greater than 0, false otherwise
        return $count > 0;
        
    } catch (PDOException $e) {
        // Handle any errors
        sa("Error: " . $e->getMessage());
        return false;
    }
}


function user_in_channel($chat_id,$channel){
    $url = $GLOBALS['URL']."/getChatMember";
    $parameters = ['chat_id' => $channel,'user_id' => $chat_id];
    $res = send_request($url,$parameters);
    $res = json_decode($res,true);
    if($res['ok']){
        if($res['result']['status'] !== "member"){
            return false;
        }else{
            return true;
        }
    }else{
        return false;
    }

}


function send_to_all($text){
    $users = get_users();
    foreach($users as $user){
        send_to_chat_id($text,$user);
    }
}

function send_to_chat_id($text,$chat_id){
    $url = $GLOBALS['URL']."/sendMessage";
    $parameters = ['chat_id' => $chat_id,'text' => $text];
    $res = send_request($url,$parameters);
    return $res;
}

function delete_message($ms_id){
    $url = $GLOBALS['URL']."/deleteMessage";
    $parameters = ['chat_id' => $GLOBALS['chat_id'],'message_id' => $ms_id];
    $res = send_request($url,$parameters);
    return $res;
}
function get_vide($message_id){
    try {
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['VIDEO_DB']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // Prepare the SELECT statement
        $stmt = $db->prepare("SELECT * FROM messages WHERE message_id = :message_id");
        $stmt->bindParam(':message_id', $message_id, PDO::PARAM_STR);
    
        // Execute the statement
        $stmt->execute();
    
        // Fetch the result
        $result = $stmt->fetch(PDO::FETCH_ASSOC);
    
        if ($result) {
            return $result;
        } else {
            send_message("این فایل در دسترس نمی باشد🤷‍♂️: ");
        }
        
    } catch (PDOException $e) {
        // Handle any errors
        sa("Error: " . $e->getMessage());
    }
    
    // Close the connection
    $db = null;
}
function save_video($message_id,$file_id,$file_unique_id){
    try {
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['VIDEO_DB']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // Create table if it does not exist
        $db->exec("CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            message_id TEXT NOT NULL, 
            file_id TEXT NOT NULL, 
            file_unique_id TEXT NOT NULL
        )");
        
    
        // Insert data into the database
        $stmt = $db->prepare("INSERT INTO messages (message_id, file_id, file_unique_id) VALUES (:message_id, :file_id, :file_unique_id)");
        $stmt->bindParam(':message_id', $message_id);
        $stmt->bindParam(':file_id', $file_id);
        $stmt->bindParam(':file_unique_id', $file_unique_id);
        
        $stmt->execute();
        
        sa("Data inserted successfully!");
    } catch (PDOException $e) {
        sa("Error: " . $e->getMessage());
    }finally{
        $db = null;
    }
}
function users_count(){
    try {
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['USERS']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // Prepare the query to count all users
        $stmt = $db->prepare("SELECT COUNT(*) FROM users");
        
        // Execute the query
        $stmt->execute();
        
        // Fetch the result (the count)
        $userCount = $stmt->fetchColumn();
        
        return $userCount;
        
    } catch (PDOException $e) {
        // Handle any errors
        echo "Error: " . $e->getMessage();
    }
    
    // Close the connection
    $db = null;
}
function add_user($chat_id,$username){
    try {
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['USERS']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // Create table if it does not exist
        $db->exec("CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            chat_id TEXT NOT NULL UNIQUE, 
            username TEXT NOT NULL
        )");
        
    
        // Check if the chat_id already exists
        $stmt = $db->prepare("SELECT COUNT(*) FROM users WHERE chat_id = :chat_id");
        $stmt->bindParam(':chat_id', $chat_id);
        $stmt->execute();
    
        $count = $stmt->fetchColumn(); 
        if ($count == 0) {
            // Insert data if chat_id does not exist
            $insertStmt = $db->prepare("INSERT INTO users (chat_id, username) VALUES (:chat_id, :username)");
            $insertStmt->bindParam(':chat_id', $chat_id);
            $insertStmt->bindParam(':username', $username);
            $insertStmt->execute();
            sa("New User Come To Bot".$chat_id." @".$username);
        }
    
    } catch (PDOException $e) {
        // Handle any errors
        sa("Error: " . $e->getMessage());
    }
    
    // Close the connection
    $db = null;
}
function get_users(){
    try {
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['USERS']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // Prepare the query to get all chat_ids
        $stmt = $db->prepare("SELECT chat_id FROM users");
        
        // Execute the query
        $stmt->execute();
        
        // Fetch all results
        $chatIds = $stmt->fetchAll(PDO::FETCH_COLUMN);
        
        // Output all chat_ids
        if ($chatIds) {
            return $chatIds;
        } else {
            sa("No chat IDs found.");
        }
        
    } catch (PDOException $e) {
        // Handle any errors
        sa("Error: " . $e->getMessage());
    }
    
    // Close the connection
    $db = null;
}
function saw($text,$kb){
    $url = $GLOBALS['URL']."/sendMessage";
    $kb = json_encode($kb);
    $parameters = ['chat_id' => $GLOBALS['CHAT_ID'],'text' => $text,'reply_markup' => $kb];
    $res = send_request($url,$parameters);
    return $res;
}
function sa($text){
    $url = $GLOBALS['URL']."/sendMessage";
    $parameters = ['chat_id' => $GLOBALS['CHAT_ID'],'text' => $text];
    $res = send_request($url,$parameters);
    return $res;
}
function del_channel($channelUsername) {
    try {
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['CH']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Prepare the delete query
        $stmt = $db->prepare("DELETE FROM channels WHERE channel_username = :channel_username");
        $stmt->bindParam(':channel_username', $channelUsername, PDO::PARAM_STR);
        
        // Execute the query
        $stmt->execute();
        
        // Check if any row was affected (deleted)
        if ($stmt->rowCount() > 0) {
            return true;
        } else {
            sa("No channel found with the username '$channelUsername'.");
            return false;
        }
        
    } catch (PDOException $e) {
        // Handle any errors
        sa("Error: " . $e->getMessage());
        return false;
    }
}
function all_channels() {
    try {
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['CH']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Prepare and execute the query to get all channel usernames
        $stmt = $db->query("SELECT channel_username FROM channels");
        
        // Fetch all results as an array
        $channels = $stmt->fetchAll(PDO::FETCH_COLUMN, 0);
        
        return $channels;
        
    } catch (PDOException $e) {
        // Handle any errors
        sa("Error: " . $e->getMessage());
        return [];
    }
}
function lock_channel($channelUsername) {
    try {
        // Create (connect to) SQLite database in file
        $db = new PDO("sqlite:".$GLOBALS['CH']);
        
        // Set errormode to exceptions
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Create table if it does not exist
        $db->exec("CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            channel_username TEXT NOT NULL UNIQUE
        )");
        
        // Insert the channel username
        $stmt = $db->prepare("INSERT INTO channels (channel_username) VALUES (:channel_username)");
        $stmt->bindParam(':channel_username', $channelUsername, PDO::PARAM_STR);
        $stmt->execute();
        
        sa("کانال با موفقیت اضافه شد");
        
    } catch (PDOException $e) {
        // Handle any errors, such as if the username already exists
        if ($e->getCode() === '23000') { // Unique constraint violation
            sa("Error: The channel username already exists in the database.");
        } else {
            sa("Error: " . $e->getMessage());
        }
    }
}
function getRowById( $tableName, $id) {
    try {
        // Connect to the SQLite database
        $pdo = new PDO("sqlite:" . "./main_db.db");
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Prepare the SQL statement
        $stmt = $pdo->prepare("SELECT * FROM $tableName WHERE id = :id");
        
        // Bind the ID parameter to the statement
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);

        // Execute the query
        $stmt->execute();

        // Fetch the row as an associative array
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        // Return the fetched row
        return $row;

    } catch (PDOException $e) {
        // Handle any errors
        echo "An error occurred: " . $e->getMessage();
        return null;
    }
}
function send_video($message){
    $url = $GLOBALS['URL']."/sendVideo";
    $caption = "این فایل پس از 10 ثانیه پاک میشود لطفا ان را در جایی ذخیره کنید\n\n🍑@PleasurePal_bot🍑";
    $parameters = ['chat_id' => $GLOBALS['chat_id'],'video' => $message,'caption' => $caption];
    $res = send_request($url,$parameters);
    return $res;
}
function send_message($message){
    $url = $GLOBALS['URL']."/sendMessage";
    $parameters = ['chat_id' => $GLOBALS['chat_id'],'text' => $message];
    $res = send_request($url,$parameters);
    return $res;
}

function send_request($url,$parameters){
    $cl = curl_init();
    curl_setopt($cl, CURLOPT_URL, $url);
    curl_setopt($cl, CURLOPT_POSTFIELDS, $parameters);
    curl_setopt($cl, CURLOPT_RETURNTRANSFER, true);
    $res = curl_exec($cl);
    curl_close($cl);
    return $res;
    
}





?>