var bird;
var pipes = [];
var backgroundPos = 0
var backgroundSpeed = 1
var groundPos = 0
var groundSpeed = 6
var score = 0
var textX = 150
var textY = 350
var highScore = 0
var exponent = 2
var textDir = "ascending"
var fade = 255
var fadeAmount = 20
var currentState = "title"
var transition = false
var fadeout = true
var lockInput = false
var optionTitle = "gameplay"
var optionTextSet = false
var optionSelected = 1
var titleHeightSet = true
var difficulty = ["Easy", "Normal", "Hard", "IMPOSSIBLE!"]
var difficultySetting = 2
var style = ["Day", "Evening", "Mars"]
var styleSetting = 1
var birdColour = ["Yellow", "Blue", "Red", "Black", "Green"]
var birdColourSetting = ["1"]
var showMenu = true
var fuel = 0
var scaleFactor

// Stores High Score in a Cookie
function setHighScoreCookie(score) {
    document.cookie = `highScore=${score};path=/;max-age=30000000`;
}

// Get high score from a Cookie
function getHighScoreCookie() {
	// Search through available cookies
    var cookies = document.cookie.split('; ');
    for (let i = 0; i < cookies.length; i++) {
        var [name, value] = cookies[i].split('=');
		// select appropraite cookie and return value
        if (name === 'highScore') {
            return parseInt(value);
        }
    }
    return 0; // Default high score if no cookie exists
}


function preload() {
  soundFormats('wav')
  optionChangeSound = loadSound(staticPath + "sounds/optionChange")
  optionFailSound = loadSound(staticPath + "sounds/optionFail")
  deathSound = loadSound(staticPath + "sounds/hit")
  pointSound = loadSound(staticPath + "sounds/point")
  flapSound = loadSound(staticPath + 'sounds/flap')
  swooshSound = loadSound(staticPath + "sounds/swoosh")
  backgroundDayImg = loadImage(staticPath + "images/background.png")
  groundDayImg = loadImage(staticPath + "images/floor.png")
  pipeImg = loadImage(staticPath + "images/pipe.png")
  pipeendImg = loadImage(staticPath + "images/pipeend.png")
  bottleImg = loadImage(staticPath + "images/bottle.png")
  uiFont = loadFont(staticPath + "fonts/uifont.ttf")
}
function setup() { 
  //Create the canvas
  if(windowWidth < 600){
    createCanvas(windowWidth, windowWidth * (4/3)); 
	scaleFactor = windowWidth / 600;
  }
  else{
    createCanvas(600, 800);
	scaleFactor = 1
  }
  
  // Create 'bird' object
  bird = new Bird();
  
  // Set sprite/background
  backgroundImg = backgroundDayImg
  groundImg = groundDayImg
  birdImg = bottleImg
  
  // Get fuel value from user
  fetch('/api/points/')
    .then(response => {
      if (!response.ok) {
        throw new Error('No response!!');
      }
      return response.json();
    })
    .then(data => {
      fuel = data.fuelRemaining
    })
    .catch(error => {
      console.error('Issue getting points from user:', error);
    });
	
  // Get high score from cookie
  highScore = getHighScoreCookie();
  console.log(highScore)
}

function draw() {
  background(0);
  //Draw background and ground
  image(backgroundImg, backgroundPos * scaleFactor, 0 * scaleFactor, 2400 * scaleFactor,800 * scaleFactor);
  image(groundImg, groundPos * scaleFactor, 760 * scaleFactor, 700 * scaleFactor,200 * scaleFactor);
  
  // Scroll background and ground (Only when alive! Stop when dead)
  if(currentState != "death"){
	backgroundPos -= backgroundSpeed
	
	// Do NOT scroll during gameplay, seperate code used for this as the ground needs to be drawn OVER the pipes.
	if(currentState != "gameplay"){
		groundPos -= groundSpeed
	}
  }
  
  // Reset scroll positions when end of image reached
  if (backgroundPos <= -1200){
    backgroundPos = 0
  }
  if (groundPos <= -106){
	groundPos = 0
  }
  
  // Title screen state
  if (currentState == "title") {
	// Show bottle/bird
    bird.show();
	
	// Draw title text
    fill(255)
    textFont(uiFont)
    textSize(100 * scaleFactor)
	text("bottleBounce!", textX * scaleFactor, textY * scaleFactor)
	
	// Draw "tap to start" text
    textSize(50 * scaleFactor)
    fill(140)
    text("Tap or Click", (textX + 50) * scaleFactor, (textY + 200) * scaleFactor)
    text("to start game", (textX + 30) * scaleFactor, (textY + 250) * scaleFactor)
	
	// Bounce title screen text
    if (textDir == "ascending"){
      textY ++
    }
    else if(textDir == "descending"){
      textY --
    }
    if (textY > 360){
      textDir = "descending"
    }
    else if (textY < 340){
      textDir = "ascending"
    }
	
	// Scroll Text off the screen when game starts
    titleHeightSet = true
    if (transition == true) {
      textX += exponent
      exponent = Math.pow(exponent, 1.03)
    }
    if (textX > 650 && transition == true){
      transition = false
      currentState = optionTitle
      titleHeightSet = false
      textX = 150
      textY = 350
    }
	
	// Render fuel text
	textSize(50 * scaleFactor)
	fill(255)
	text("Fuel: " + fuel, 50 * scaleFactor, 50 * scaleFactor)
	
	// Fadeout routine
    if (fadeout == true){
      fill(0, 0, 0, fade)
      rect(0, 0, 600, 900)
      if (fade > 0){
        fade -= fadeAmount
      }
      else{
        fadeout = false
      }
    }
  }
  
  else if (currentState == "gameplay") {
	
	// Pipe logic
    for (var i = pipes.length - 1; i >= 0; i--) {
	  // Show and update pipes
      pipes[i].show();
      pipes[i].update();

	  // If bird hits pipe, change state to death
      if (pipes[i].hits(bird)) {
        deathSound.play()
        currentState = "death"
      }

	  // Remove pipe when off screen
      if (pipes[i].offscreen()) {
        pipes.splice(i, 1);
      }
    }
	
	// Draw ground over pipes
	image(groundImg, groundPos * scaleFactor, 760 * scaleFactor, 700 * scaleFactor,200 * scaleFactor);
    groundPos -= groundSpeed

	// Change state to death if ground hit
    if (bird.y > 720 * scaleFactor){
      deathSound.play()
      currentState = "death"
    }

	// Draw score text
    fill(255)
    textFont(uiFont)
    textX = 280
    textSize(100 * scaleFactor)
    if (score > 9){
      textX = 260
    }
    else{
      textX = 280
    }
    text(score, textX  * scaleFactor, 150  * scaleFactor)

	// Show and update bird position
    bird.update();
    bird.show();

	// Create new pipe at regular intervals.
    if (frameCount % 75 == 0) {
      pipes.push(new Pipe());
    }
	
	// Render fuel text
	textSize(50 * scaleFactor)
	fill(255)
	text("Fuel: " + fuel, 50 * scaleFactor, 50 * scaleFactor)
	
	// Flash screen when dieing
    if (currentState == "death"){
      background(255)
    }
  }

  else if (currentState == "death"){
	// Continue showing pipes that are still on screen
    for (var i = pipes.length - 1; i >= 0; i--) {
      pipes[i].show();
    }
	// Draw ground over pipes
    image(groundImg, groundPos * scaleFactor, 760 * scaleFactor, 700 * scaleFactor,200 * scaleFactor);
	
	// Draw score
    fill(255)
    textFont(uiFont)
    textSize(100 * scaleFactor)
    if (score > 9){
      textX = 260
    }
    else{
      textX = 280
    }
    text(score, textX * scaleFactor, 150 * scaleFactor)
	
	// Continue updating bird (let it fall)
    bird.update()
    bird.show()
	
	// Wait for bird to hit ground before showing score
    if (bird.y >= height - 79 * scaleFactor && transition == false){
      transition = true // Trigger text scrolling
      textY = 900
      swooshSound.play()
    }
	
    if (transition == true){
	  // Draw Game Over text
      textX = 120
      fill(244,226,198)
      text("GAME OVER", textX * scaleFactor, textY * scaleFactor)
	  
	  // Scroll text upward
      if (textY >= 250){
        textY -= 14
      }
	  // Draw UI for Score + Rank
      rect((textX - 50) * scaleFactor, (textY + 75) * scaleFactor, 450 * scaleFactor, 250 * scaleFactor, 20 * scaleFactor)
      textSize(50 * scaleFactor)
      fill(120)
      text("Rank  Hi Score  Score", (textX - 17.5) * scaleFactor, (textY + 150) * scaleFactor)
      textSize(30* scaleFactor)
      text("Tap or Click to return", (textX + 67.5) * scaleFactor, (textY + 300) * scaleFactor)
      textSize(100 * scaleFactor)
      fill(150)
      text(score, (textX + 287.5) * scaleFactor, (textY + 250) * scaleFactor)
	  
	  // Update highscore if score achieved is higher than current highscore.
      if (score > highScore){
          highScore = score
      }
	  
	  // Render the high score
      text(highScore, (textX + 150) * scaleFactor, (textY + 250) * scaleFactor)
	  
	  // Display appropriate rank
      if (score < 10){
        fill(255,0,0)
        text("F-", (textX - 17.5) * scaleFactor, (textY + 250) * scaleFactor)
      }
      else if (score >= 10 && score < 20){
        fill(255,69,0)
        text("D", textX * scaleFactor, (textY + 250) * scaleFactor)
      }
      else if (score >= 20 && score < 30){
        fill(255, 170, 29)
        text("C", textX * scaleFactor, (textY + 250) * scaleFactor)
      }
      else if (score >= 30 && score < 40){
        fill(173,255,47)
        text("B", textX * scaleFactor, (textY + 250) * scaleFactor)
      }
      else if (score >= 40 && score < 50){
        fill(34,139,34)
        text("A", textX * scaleFactor, (textY + 250) * scaleFactor)
      }
      else if (score >= 50){
        fill(34,139,34)
        text("A+", textX * scaleFactor, (textY + 250) * scaleFactor)
      }
    }
	
	// Render fuel text
	textSize(50 * scaleFactor)
	fill(255)
	text("Fuel: " + fuel, 50 * scaleFactor, 50 * scaleFactor)
	
	// Fade out routine
    if (fadeout == true){
      fill(0, 0, 0, fade)
      rect(0, 0, 600, 900)
      if (fade<255){
        fade += fadeAmount
      }
	  else{
		// Set high score in cookie
		setHighScoreCookie(score)
		
		// Reset game variables/state once fade ends
        currentState = "title"
        swooshSound.play()
        bird.y = 300;
        bird.x = 64;
        bird.gravity = 0.7;
        bird.lift = -12;
        bird.velocity = -12;
        transition = false
        textX = 150
        textY = 350
        exponent = 2
        pipes = []
        score = 0
		
		
		// Redirect to URL, passing the new point value after the game finished
        window.location.href = "/pointUpdate/" + fuel
      }
    }
  }
}

function mousePressed(){
	if (currentState == "gameplay"){
	  // Bird jumps when clicked if you still have droplets left
	  if(fuel > 0){
		bird.up();
		fuel --
	  }
	  // Play audio cue when trying to keep going without fuel
	  else{
		optionFailSound.play()  
	  }
    }
    if (currentState == "title" && transition == false){
	  // Click starts game
      transition = true
      optionTitle = "gameplay"
      swooshSound.play()
    }
    if (currentState == "death" && transition == true){
	  // Begin fadeout to reset
      fadeout = true
    }
}