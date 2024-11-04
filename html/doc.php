<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>DrumLace Documentation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="./style.css">
    
  </head>
  <body>
    <nav>
      <div class="topnav">
        <a href="./index.php">Home</a>
        <a href="./Tutorial.php" target="_blank">Tutorial</a>
        <a href="./doc.php" target="_blank">Documentation</a>
        <a href="./Feedback.php"target="_blank">Feedback</a>
      </div>
    </nav>
  <center><h1>Documentation</h1></center> 
  <section aria-label="Music_t">
    <center><h2>A Bit of Music Theory</h2></center>
    Before we delve into the language itself it is important to refer some basic concepts,
    namely, concepts that relate to the composition of rhythms.<br>
    If you are already familiar with these concepts feel free to skip this section.<br>
    <h3>The Note</h3>
    The note is a distinct isolated sound that constitutes the basis of all music. each note has its own sound and duration.<br>
    In a drum music sheet the vertical position of a note relates to the instrument of that note, wether it is a hi hat, a snare drum or a bass drum.<br>
    Altough there are many standards the one we will consider is the Weinberg notation, indicated bellow.<br><br>
    <img src="/images/documentation/drum_notation.png" width="15%"></img><br><br>
    Notice that not all these instruments are presented in the DrumLace language only the ones described in  the table bellow (right above examples)<br><br>
    And the duration is signalled by the figure itself as presented in the image bellow.<br><br>
    <img src="/images/documentation/note-lengths-diagram.jpg" width="25%"><br><br>
    A dotted note marks one and a half of the normal duration, for example a dotted quarter note marks 3 eighth notes.

    <h3>The Meter</h3>
    A meter is a recurring pattern of beats, usually indicating an accent by the musician, and marked by a vertical line.<br>
    A simple meter is defined as N/4, where N is the number of quarter notes in a meter. For example the most common time, 4/4 or c, consists on 4 quarter notes.<br>
    It is important to mention the divisions of notes as stated in the image above, so that a meter can be constitued by notes of different lengths as long as the sum is the same. Note that all the meters in the image bellow are valid.<br><br>
    <img src="/images/documentation/divisions.png" width="25%"><br><br>
    Note that the eigths notes and the sixteenth notes when placed in a row are arranged as seen in the first four notes of the last meter.
    A compound rhythm is defined as N/8, where N is the number of eight notes. in a compound meter a beat is divided in three parts.<br><br>
    So, for example in a 6/8 meter the beat is marks 3 eighth notes and the meter contains two beats.<br><br>
    A mixed meter is defined as different meters followed by each other. 
    <h3>Tempo</h3>
    Tempo is simply the speed of the music, the number of beats per minute.
    <h3>Tupplets</h3>
    Tupplets mark an irational division of a note,for example, the tripplet marks the divion of a note into 3 instead of 2.<br><br>
    <img src="/images/documentation/tuplet.png"  height="100">
  </section>
  <center><h2>DrumLace Syntax</h2></center>
  <div class="hyperb">Note that the language itself is still being developed so it is not advisable to use too many operators in a single sentence or to parallelize patterns with different sizes.
    Any bugs or programs that don't work as intended can be reported in the <a href="./Feedback.php" target="_blank">feedback</a> page.</div>
  <section aria-label="drum_description">
    <h3>Drum Description</h3>
    A drum description consists on the following syntax<br><br>
    Name_of_the_pattern={Time_signature;Tempo=Value_of_tempo;Instrument1 Instrument1_lines;Instrument2 Instrument2_lines;...;}<br><br>
    Instrument is the name of the instrument acording to the table of instruments.<br><br>
    An Instrument line is a series of note_length |X.X.| in which "X" marks a hit, "." marks a pause and "d" marks a dotted note. You can add how many instrument lines for each instrument.<br><br>
    Keep in mind that white spaces, tabs and newlines are irrelevant so just write in whatever way you like.<br><br>
    Take the example bellow that describes the famous boots and cats rhythm.<br><br>
    BootsandCats={4/4;Tempo = 180;<br>
    hh 1/8 |xxxx| 1/4 |xx|;<br>
    sn 1/4 |.X.X|;<br>
    bd 1/4 |X.X.|;}<br><br>
    <img src="/images/documentation/BaC.png" height="100"><br>
    <div class="audiob">
    <audio controls>
      <source src="/images/documentation/BaC.wav">
    </audio>
    </div>
  </section>
  <section aria-label="Tupplet">
    <h3>Division of notes</h3>
    To divide a note the syntax "note_length {notes}" can be used, thus allowing for the description of a tupplet.
  </section>
  <section aria-label="Rhythm algebra">
    <h3>Rhythm Algebra</h3>
    After at least a pattern is defined new patterns can be defined according to some algebra rules<br><br>
    <img src="/images/documentation/operators-1.png" width="25%"><br><br>
    <h4>Concatenation/Sum</h4>
    Final_pattern=Pattern_A+Pattern_B<br>
    <h4>Looping</h4>
    Final_pattern=Pattern*number_of_iterations
    <h4>Parallelization</h4>
    Final_pattern=Pattern_A || Pattern_B<br><br>
    And you can combine all this operators to create patterns, for example<br><br>
    Final_pattern=(Pattern_A || Pattern_B)*2 + Pattern_C.<br><br>
  </section>
  <section aria-label="Functions">
    <h3>Functions</h3>
    Besides using algebraic operators there is also the option of using functions according to the syntax<br>
    Final_pattern=Function(Pattern_A,...), different functions may require differnet arguments.<br>
    The list of currently avaiable functions is presented bellow<br><br>
    <table>
      <tr>
        <th>Function and arguments</th>
        <th>Description of the function</th>
      </tr>
      <tr>
        <td>rev(Pattern)</td>
        <td>reverses the pattern, horizontal inversion</td>
      </tr>
        <td>scale(Pattern,number)</td>
        <td>multiplies the tempo of the pattern by the given number</td>
    </table>
    <br>
  </section>
  <section aria-label="Export">
    <h2>Export and DrumLace Program</h2>
      The syntax of the export is simply export(Pattern_Name)
      A DrumLace Program should at least contain a Drum Description and an Export.
  </section>
  <section aria-label="Instruments">
    <h2>Instruments and how to call them</h2>
    <table>
      <tr>
        <th>Instrument</th>
        <th>Name of intrument in DrumLace</th>
      </tr>
      <tr>
        <td>bass drum/kick drum</td>
        <td>bd</td>
      </tr>
        <td>snare drum</td>
        <td>sn</td>
      </tr>
        <td>Hi Hat</td>
        <td>hh</td>
      </tr>
        <td>Crash cymbal</td>
        <td>cymc</td>
      </tr>
        <td>Floor Tom</td>
        <td>tomfl</td>
    </table>
  </section>
  <section aria-label="Examples">
    <div class="example_prog">
    <center><h2>Examples</h2></center>
    <center><h3>Drum patterns</h3></center>
      #this is a comment<br>
      <br>
      <div class="row">
      <div class="column">
      <h4>Boots and Cats</h4>
      BootsAndCats = {4/4;Tempo=220;<br>
      hh 1/8 |XXXXXXXX|;#hi hat<br>
      bd 1/4 |X.X.|;#bass drum<br>
      sn 1/4 |.X.X|;}#snare drum<br>
      <br>
      <h4>Unnamed Rhythm</h4>
      pat={4/4;Tempo=190;<br>
      hh 1/4 |XXX.XXX.X.X.|;<br>
      bd 1/2 |XXXXXX|;<br>
      sn 1/8 |..XX..X...XX..X...XX..X.XXX.X...|;<br>
      cymc 1/1 |...|1/8|..X....|1/8|X|;}#crash cymbal<br>
      <br>
      <h4>3:4 polyrythm</h4>
      poly={4/4;Tempo = 180;<br>
      sn 1/4 |XXXX|;<br>
      tomfl 1/1 |{XXX}|;}#floor tom<br>
      </div>
      <div class="column">
      <h4>Brazillian Funk</h4>
      bfunk={4/4;Tempo=110;<br>
      bd 1/8 |d...|1/16 |.| 1/8|X..|;<br>
      sn 1/16 |...| 1/8 |dX..X|;}<br>
      <br>
      <br>
      <h4>Amen break (Drum and Bass Rhythm)</h4> 
      amen={4/4;Tempo=120;<br>
      hh 1/8 |XXXXXXXX|;<br>
      bd 1/8 |XX...X|;<br>
      sn 1/8 |..X|1/16|.X.X..X..X|;}<br>
      <br>
      <br>
      <h4>Queen's we will rock you</h4>
      Queen={4/4;Tempo = 80;<br>
      bd 1/8 |XX..XX..|;<br>
      sn 1/8 |..X...X.|;}<br>
      </div>
      </div>
      <center><h3>Full Programs</h3></center>
    <div class="row">
    <div class="column">
  <h4>Example 1</h4>
  funkintro={4/4;Tempo=110;<br>
  bd 1/8 |d...|1/16 |.| 1/8|X..|;<br>
  sn 1/16 |...| 1/8 |dX..X|; <br>
  cymc 1/1 |X|;}<br><br>
  funk={4/4;Tempo=110;<br>
  bd 1/8 |d...|1/16 |.| 1/8 |X..|;<br>
  sn 1/16 |...| 1/8 |dX..X|;}<br><br>
  funkr=funkintro+funk*3<br><br>
  hh={4/4;Tempo=110;<br>
  hh 1/8 |XXXXXXXX|;}<br>
  hha={4/4;Tempo=110;<br>
  hh 1/8 |XX|1/16|XXXX|1/8|XXXX|;}<br><br>
  cym={4/4;Tempo=110;cymc 1/1 |X|;}<br><br>
  res=funkr||(hh+hha)*2 + cym<br><br>
  export(res)<br>
  <br>
  <h4>Example 2</h4>
  funkintro={4/4;Tempo=110;<br>
  bd 1/8 |d...|1/16 |.| 1/8|X..|;<br>
  sn 1/16 |...| 1/8 |dX..X|;<br>
  cymc 1/1 |X|;}<br><br>
  
funk={4/4;Tempo=110;<br>
  bd 1/8 |d...|1/16 |.| 1/8 |X..|;<br>
  sn 1/16 |...| 1/8 |dX..X|;}<br><br>
  
funkr=funkintro+funk*3<br><br>
  
plates={4/4;Tempo=110;<br>
  hh 1/8 |XXXXXXXX|;}<br><br>

platesa={4/4;Tempo=110; #note that patterns cannot have numbers in their name<br>
  hh 1/8 |XX|1/16|XXXX|1/8|XXXX|;}<br><br>
  
cym={4/4;Tempo=110;cymc 1/1 |X|;}<br><br>
  
res=funkr||(plates+platesa)*2 + cym<br><br>
  
export(res)<br>
<br>
<br>
  </div>
  </div>
  </div>
  </section>
  </body>
</html>