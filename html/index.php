<?php
header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');
header('Cache-Control: no-store, no-cache, must-revalidate');
header('Cache-Control: post-check=0, pre-check=0', FALSE);
header('Pragma: no-cache');
session_start();

function create_user_directory($user_dir) {
  $session_id = session_id();
  $user_dir = "./" . sys_get_temp_dir() . "/user_" . $session_id;
  return $user_dir;
}

// Example usage
$user_dir = create_user_directory($user_dir);

$userl=explode("//", $user_dir);
$user = substr(implode('',$userl), 5);
$imgpath="/images/{$user}patternPDF.pdf";
$wavpath="/wav/{$user}patternWAV.wav";
$midipath="/midi/{$user}patternMIDI.midi";
$error="welcome to DrumLace! Press render to see the Output.";
$code = "funkintro={4/4;Tempo=110;
  bd 1/8 |d...|1/16 |.| 1/8|X..|;
  sn 1/16 |...| 1/8 |dX..X|;
  cymc 1/1 |X|;}
  
funk={4/4;Tempo=110;
  bd 1/8 |d...|1/16 |.| 1/8 |X..|;
  sn 1/16 |...| 1/8 |dX..X|;}
  
funkr=funkintro+funk*3
  
plates={4/4;Tempo=110;
  hh 1/8 |XXXXXXXX|;}

platesa={4/4;Tempo=110; #note that patterns cannot have numbers in their name
  hh 1/8 |XX|1/16|XXXX|1/8|XXXX|;}
  
cym={4/4;Tempo=110;cymc 1/1 |X|;}
  
res=funkr||(plates+platesa)*2 + cym
  
export(res)";

if (isset($_POST["Render"])){
  $code=$_POST["code"];
  $file_path="./in/input{$user}.txt";
  $fp = fopen(".{$file_path}", "w+");#nao sei pq precisa daquele ponto mas da erro sem ele
  fwrite ($fp,$code);
  fclose ($fp);
  $return = exec("cd ..;./run.sh {$file_path} {$user_dir}");
  if ($return=="0"){
    $error="compilation sucessfull!";}
  else {$error="compilation failed! Check for errors in code";}
} 
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>DrumLace</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="./style.css">
    <title>DrumLace</title>
</head>
    <nav>
      <div class="topnav">
        <a class="active"href="./index.php">Home</a>
        <a href="./Tutorial.php" target="_blank">Tutorial</a>
        <a href="./doc.php" target="_blank">Documentation</a>
        <a href="./Feedback.php"target="_blank">Feedback</a>
      </div>
    </nav>
  <center><h1>DrumLace<br><br> <img src="/images/logo/DrumLaceLogo.png" height="60"></img></h1><h6>alpha version</h6></center>
  <div class="row">
    <div class="column">
      <form action="index.php" method="post">
        <center><textarea name="code" rows="20%" cols="50%" style="font-size: 15pt" spellcheck="false"><?php echo $code;?></textarea>
        <input id="Render" type="submit" name="Render" value="Render">
      </form>
      <div class="hyperb"><a download href=<?php echo $file_path ?> target="_blank">Save Program</a></div>
    </div>
    </center>
    <div class="column">
      <center><iframe  src= <?php echo "$imgpath#toolbar=0&navpanes=0";?> title="Sheet" width="650" height="400"></iframe>
      <br>
      <form action="index.php" method="post">
        <div class="hyperb">
        <a href=<?php echo $imgpath;?> target="_blank">Open PDF</a>
        <a href=<?php echo $wavpath;?> target="_blank">Download WAV</a>
        <a href=<?php echo $midipath;?> target="_blank">Download MIDI</a>
        </div>
      </form>
      <audio controls>
        <source src=<?php echo $wavpath;?> type="audio/wav" >
        Your browser does not support the audio element.
      </audio><br>
      <?php echo $error;?>
      </center>
    </div>
  </div>
</body>
</html>