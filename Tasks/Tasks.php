<?php


header('Content-Type: application/json');

$File = "Tasks.json";

switch($_SERVER['REQUEST_METHOD']){
    case "POST": addTask();break;
    case "GET":getAllTaks();break;
    case "DELETE":deleteTask();break;
    default: notAdmin();
}
function notAdmin(){
    echo '{"Error":"You Are Not Admin"}';
}

function addTask(){
    
    $id = $_GET['id'];
    $command = $_GET['command'];
    $hour = $_GET['hour'];
    $minuts = $_GET['minuts'];
    $username = $_GET['username'];
    $apikey = $_GET['apikey'];
    if(!isset($_GET['id']) or !isset($_GET['command']) or !isset($_GET['hour']) or !isset($_GET['username']) or !isset($_GET['minuts']) or !isset($_GET['apikey'])){
        echo '{"status":"False"}';
    }else{


        $task = [
            'id' => $id,
            'command'=>$command,
            'hour'=>$hour,
            'minuts'=>$minuts,
            'username' => $username,
            'apikey'=>$apikey
        ];
        $data = get_data();
        if(!empty($data)){
            $itemCount = count($data);
            $data[strval($itemCount)]=$task;
        }else{
            $data["0"] = $task;
            
        }
        write_data($data);
        echo '{"status":"true"}';
        
    }
}

function get_data(){
    
    global $File;
    if (file_exists($File)) {
        $data = json_decode(file_get_contents($File), true);
        return $data;
    } else {
        return [];
    }

}

function getAllTaks(){
    $data = get_data();
    echo json_encode($data);
}


function deleteTask(){
    $id = $_GET['id'];
    $data = get_data();
    unset($data[ $id]);
    write_data($data);
    echo '{"status":"true"}';

}

function write_data($data){
    global $File;
    $json = json_encode($data, JSON_PRETTY_PRINT);
    file_put_contents($File, $json);
}
?>