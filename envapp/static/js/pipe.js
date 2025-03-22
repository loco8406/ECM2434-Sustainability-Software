function Pipe() {
  if (difficultySetting == 1){
    this.speed = 6 * scaleFactor;
    this.spacing = 350 * scaleFactor;
  }
  else if (difficultySetting == 2){
    this.speed = 7 * scaleFactor;
    this.spacing = 300 * scaleFactor;
  }
  else if (difficultySetting == 3){
    this.speed = 8 * scaleFactor;
    this.spacing = 250 * scaleFactor;
  }
  else if (difficultySetting == 4){
    this.speed = 12 * scaleFactor;
    this.spacing = 100 * scaleFactor;
  }
  this.top = random(height / 6, (3 / 4) * height) * scaleFactor;
  this.bottom = height - (this.top + this.spacing);
  this.x = width;
  this.w = 80  * scaleFactor;
  this.passed = false

  this.highlight = false;

  this.hits = function(bird) {
    if (bird.y < this.top || bird.y > height - this.bottom) {
      if (bird.x + 50 > this.x && bird.x < this.x + this.w) {
        this.highlight = true;
        return true;
      }
    }
    this.highlight = false;
    return false;
  };

  this.show = function() {
    fill(255);
    if (this.highlight) {
      fill(255, 0, 0);
    }
    image(pipeImg, this.x, 0, this.w, this.top);
    image(pipeendImg, this.x, this.top - this.w * 0.47867, this.w, this.w * 0.47867)
    image(pipeImg, this.x, height - this.bottom, this.w, this.bottom);
    image(pipeendImg, this.x, height - this.bottom, this.w, this.w * 0.47867)
    
  };

  this.update = function() {
    this.x -= this.speed;
    if (bird.x > this.x && this.passed == false){
        this.passed = true
    }
    if (this.passed == true){
      score ++
      pointSound.play()
      this.passed = "n/a"
    }
  };

  this.offscreen = function() {
    if (this.x < -this.w) {
      return true;
    } else {
      return false;
    }
  };
}
