<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>DrumLace Tutorial</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="./style.css">
  </head>
  <body>
    <nav>
      <div class="topnav">
        <a class="active"href="./index.php">Home</a>
        <a href="./Tutorial.php" target="_blank">Tutorial</a>
        <a href="./doc.php" target="_blank">Documentation</a>
        <a href="./Feedback.php"target="_blank">Feedback</a>
      </div>
    </nav>
  <center><h1>Tutorial</h1></center>  
  <section>
  <center>
    <h2>Video Tutorial</h2>
      <video controls>
      <source src="./video/drumlace_tut.mp4" type="video/mp4">
      </video>
  </center>
  </section>
  <section aria-label="step_1">
    <h2>Step 1: Describing Drum Patterns</h2>
    To create a pattern you can either copy one from the examples section of the <a href="/doc.php" target="_blank">Documentation</a>.
    Or by describing it yourself. To do so follow the following steps:<br>
    <h3>Step 1.1: Choosing a name</h3>
    you have to name your patterns so that you can use them later, notice that the patterns can only have letters on the name. Let's name our pattern "Pattern".<br> We then start by writing: <br>
    <br>"Pattern = {}" <br>And we will descibre our rhythm within the brackets<br><br>
    <h3>Step 1.2 Choosing a Time Signature and a Tempo </h3>
    Now that we named our rhythm we need to specify the starting Time signature and the Tempo, we do this by adding them in the form "N1/N2;Tempo=N3"<br> Let's say our pattern will be played in 4/4 at 120 BPM<br>
    To continue the previous step we get:<br><br>
    "Pattern = {4/4;Tempo=120;}"<br> Notice that the ";" is needed.<br><br>
    <h3>Step 1.3 describing instrument lines</h3>
    All that's left to do is to describe what the intruments are playing.<br>
    To achieve this we write the name of the instrument and then the notes. the notes can be described by indicating the duration, such as 1/4 and then a hit "X", a pause "." or a dotted note "d".<br>
    Let's add a simple hi hat(hh) rhythm to our pattern<br><br> 
    "Pattern = {4/4;Tempo=120;<br>
    hh 1/8 |XXXX| 1/4 |X.XXX.Xdd|;}"<br><br>
    Identation, or things such as spaces, tabs and new lines are irrelevant, write the way you think is best.<br>
    Notice how you can change note duration and group notes with the same duration.<br>
    We can then add as many instrument lines as we like, let's say i want to add a bass drum(bd) and a snare drum(sn) rhythm. We can then write:<br><br>
    "Pattern = {4/4;Tempo=120;<br>
    hh 1/8 |XXXX| 1/4 |X.XXX.Xdd|;<br>
    bd 1/4 |X.X.X.X.X.X.|;<br>
    sn 1/4 |.X.X.X.X.X.X|;}"<br><br>
    The list of instruments is avaiable at the Instruments and how to call them section of the <a href="/doc.php" target="_blank">Documentation</a>
    </div>
  </section>

  <section>
    <h2>Step 2: Creating Patterns from Other Patterns</h2>
    Now that we have one or more patterns we can create new ones using the functions and algebraic expressions metioned in the Documentation.<br>
    Let's say we want to create, from the pattern described in section 1, a new pattern called inverse that's equal to Pattern but played back to front.We then add:<br><br>
    "Inverse = rev(Pattern)"<br><br>
    And if we want to create a result pattern that consists on Pattern followed by Inverse:<br><br>
    "Result = Pattern + Inverse"<br><br>
  </section>

  <section>
    <h2>Step 3: Exporting Files</h2>
    <p>All that's left to do is to say what pattern you want to export by simply writing Export(Result), since our final pattern is named Result<br><br>
    And we get the full program<br><br>
    Pattern = {4/4;Tempo=120;<br>
    hh 1/8 |XXXX| 1/4 |X.XXX.Xdd|;<br>
    bd 1/4 |X.X.X.X.X.X.|;<br>
    sn 1/4 |.X.X.X.X.X.X|;}<br><br>

    Inverse = rev(Pattern)<br><br>

    Result = Pattern + Inverse<br><br>
    And you simply press Render.<br>
    If the sound player doesn't change try refreshing the page a couple times. </p>
  </section>
  
  </body>
</html>